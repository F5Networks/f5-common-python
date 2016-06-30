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

from pprint import pprint as pp
from requests import HTTPError

pp(__file__)
TESTDESCRIPTION = 'TESTDESCRIPTION'

# Application Service Dictionary
sections = {
    'implementation': '',
    'presentation': ''
}

definition = {'definition': sections}


def setup_application_test(request, bigip):
    return bigip.sys.application


def setup_template_collection_test(request, bigip):
    return bigip.sys.application.templates


def setup_service_collection_test(request, bigip):
    return bigip.sys.application.services


def delete_resource(resource):
    try:
        resource.delete()
    except HTTPError as ex:
        if ex.response.status_code != 404:
            raise


def setup_template_test(request, bigip, name, partition):
    template_s = setup_template_collection_test(request, bigip)

    def teardown():
        delete_resource(test_template)
    request.addfinalizer(teardown)
    test_template = template_s.template.create(
        name=name,
        partition=partition,
        actions=definition
    )
    return template_s, test_template


def setup_service_test(request, bigip, name, partition, template_name, tgroup):
    service_s = setup_service_collection_test(request, bigip)

    def teardown():
        delete_resource(test_service)
        delete_resource(test_template)

    template_factory = setup_template_collection_test(request, bigip).template
    test_template = template_factory.create(
        name=template_name,
        partition=partition,
        actions=definition
    )
    test_service = service_s.service.create(
        name=name,
        partition=partition,
        template=template_name,
        trafficGroup=tgroup
    )
    request.addfinalizer(teardown)
    return service_s, test_service


def curdle_check(collection, resource, resource_name, **kwargs):
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

    assert getattr(collection, resource_name).exists(**kwargs) is True


class TestApplication(object):
    def test_get_collection(self, request, bigip):
        app_org_s = setup_application_test(request, bigip)
        app_org_full_s = app_org_s.get_collection()
        assert len(app_org_full_s) == 4


class TestTemplateCollection(object):
    def test_get_collection(self, request, bigip):
        templ_s = setup_template_collection_test(request, bigip)
        all_templates = templ_s.get_collection()
        assert len(all_templates) == 27
        for templ in all_templates:
            assert templ.verificationStatus == 'signature-verified'
            assert templ.totalSigningStatus == 'one-cert-signed'


class TestTemplate(object):
    def test_template_CURDL(self, request, bigip):
        templ_s, test_templ = setup_template_test(
            request,
            bigip,
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


class TestServiceCollection(object):
    def test_get_collection(self, request, bigip):
        serv_s, test_service = setup_service_test(
            request,
            bigip,
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
    def test_service_CURDL(self, request, bigip):
        serv_s, test_serv = setup_service_test(
            request,
            bigip,
            'test_service',
            'Common',
            'test_template',
            '/Common/traffic-group-local-only'
        )
        # Make sure the uri is what we expect
        assert bigip._meta_data['uri'] + 'sys/application/service/~Common' \
            '~test_service.app~test_service' in test_serv._meta_data['uri']
        curdle_check(
            serv_s,
            test_serv,
            'service',
            name='test_service',
            partition='Common'
        )
