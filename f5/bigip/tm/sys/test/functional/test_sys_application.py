# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from requests import HTTPError

from f5.bigip.contexts import TransactionContextManager
from f5.bigip.contexts import TransactionSubmitException
from f5.bigip.tm.sys.application import Service
from f5.bigip.tm.sys.application import Template

import pytest

TESTDESCRIPTION = 'TESTDESCRIPTION'

# Application service dictionary, which matches JSON structure
sections = {
    'implementation': '',
    'presentation': ''
}

definition = {'definition': sections}


def setup_application_test(request, mgmt_root):
    return mgmt_root.tm.sys.application


def setup_template_collection_test(request, mgmt_root):
    return mgmt_root.tm.sys.application.templates


def setup_service_collection_test(request, mgmt_root):
    return mgmt_root.tm.sys.application.services


def delete_resource(resource):
    try:
        resource.delete()
    except HTTPError as ex:
        if ex.response.status_code != 404:
            raise


def setup_template_test(request, mgmt_root, name, partition):
    template_s = setup_template_collection_test(request, mgmt_root)

    def teardown():
        delete_resource(test_template)

    request.addfinalizer(teardown)
    test_template = template_s.template.create(
        name=name,
        partition=partition,
        actions=definition
    )
    assert isinstance(test_template, Template)
    assert id(test_template) != id(template_s.template)
    return template_s, test_template


def setup_service_test(request, mgmt_root, name, partition,
                       template_name, tgroup):
    service_s = setup_service_collection_test(request, mgmt_root)

    def teardown():
        # Delete the service first, then the template
        delete_resource(test_service)
        delete_resource(test_template)

    template_factory = setup_template_collection_test(
        request, mgmt_root
    ).template
    test_template = template_factory.create(
        name=template_name,
        partition=partition,
        actions=definition
    )
    assert isinstance(test_template, Template)
    assert id(test_template) != id(template_factory)
    test_service = service_s.service.create(
        name=name,
        partition=partition,
        template=template_name,
        trafficGroup=tgroup
    )
    assert isinstance(test_service, Service)
    assert id(test_service) != id(service_s.service)
    request.addfinalizer(teardown)
    return service_s, test_service


def curdle_check2(collection, resource, resource_name, **kwargs):
    name = kwargs['name']
    assert resource.name == name
    second_resource = getattr(collection, resource_name).load(**kwargs)

    assert second_resource.name == resource.name
    assert second_resource.generation == resource.generation

    resource.description = TESTDESCRIPTION
    resource.update()
    assert resource.description == TESTDESCRIPTION
    assert resource.generation > second_resource.generation

    second_resource.refresh()
    assert second_resource.generation == resource.generation


def curdle_check(collection, resource, resource_name, **kwargs):
    curdle_check2(collection, resource, resource_name, **kwargs)

    assert getattr(collection, resource_name).exists(**kwargs) is True


class TestApplication(object):
    def test_get_collection(self, request, mgmt_root):
        app_org_s = setup_application_test(request, mgmt_root)
        app_org_full_s = app_org_s.get_collection()
        assert len(app_org_full_s) == 4

    def test_disallowed_params(self, request, mgmt_root):
        """Tests that a disallowed parameter is removed

        This check does not test for failure. Instead, the code in the
        associated class will pop the disallowed parameter off of the
        kwargs.

        Then, the kwargs will be sent through the check_load_parameters,
        which checks for "name" and "partition".

        Finally, the code will issue a GET request to BIG-IP. If this
        method fails, then our disallowed parameter was not removed
        properly.

        :param mgmt_root:
        :return:
        """
        serv_s, test_serv = setup_service_test(
            request,
            mgmt_root,
            'test_service2',
            'Common',
            'test_template2',
            '/Common/traffic-group-local-only'
        )
        # Make sure the uri is what we expect
        uri = ''.join([
            mgmt_root._meta_data['uri'],
            'tm/sys/application/service/~Common',
            '~test_service2.app~test_service2'])
        assert uri in test_serv._meta_data['uri']

        curdle_check2(
            serv_s,
            test_serv,
            'service',
            name='test_service2',
            partition='Common',
            template="bar",
            trafficGroup="foo"
        )


class TestTemplateCollection(object):
    def test_get_collection(self, request, mgmt_root):
        templ_s = setup_template_collection_test(request, mgmt_root)
        all_templates = templ_s.get_collection()
        assert len(all_templates) == 27
        for templ in all_templates:
            assert templ.verificationStatus == 'signature-verified'
            assert templ.totalSigningStatus == 'one-cert-signed'


class TestTemplate(object):
    def test_template_CURDL(self, request, mgmt_root):
        templ_s, test_templ = setup_template_test(
            request,
            mgmt_root,
            'test_template',
            'Common'
        )
        curdle_check(
            templ_s,
            test_templ,
            'template',
            name='test_template',
            partition='Common'
        )


class TestTemplateTransaction(object):
    def test_template_transaction_CURDL(self, request, mgmt_root):
        with pytest.raises(TransactionSubmitException) as ex:
            tx = mgmt_root.tm.transactions.transaction
            with TransactionContextManager(tx) as api:
                api.tm.sys.application.templates.template.create(
                    name="template_transaction",
                    partition="Common",
                    actions=dict(
                        definition=dict(
                            implementation='',
                            presentation=''
                        )
                    )
                )
        assert 'may' in str(ex.value.message)


class TestServiceCollection(object):
    def test_get_collection(self, request, mgmt_root):
        serv_s, test_service = setup_service_test(
            request,
            mgmt_root,
            'test_service',
            'Common',
            'test_template',
            '/Common/traffic-group-local-only'
        )

        all_services = serv_s.get_collection()
        assert len(all_services) is 1
        # Description field does not exist until assigned
        # The creation of this field is tested in check_curdl
        assert hasattr(all_services[0], 'description') is False
        assert all_services[0].name == 'test_service'


class TestService(object):
    def test_service_CURDL(self, request, mgmt_root):
        serv_s, test_serv = setup_service_test(
            request,
            mgmt_root,
            'test_service',
            'Common',
            'test_template',
            '/Common/traffic-group-local-only'
        )
        # Make sure the uri is what we expect
        uri = ''.join([
            mgmt_root._meta_data['uri'],
            'tm/sys/application/service/~Common',
            '~test_service.app~test_service'
        ])

        assert uri in test_serv._meta_data['uri']
        curdle_check(
            serv_s,
            test_serv,
            'service',
            name='test_service',
            partition='Common'
        )
