# Copyright 2015 F5 Networks Inc.
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

import copy
from distutils.version import LooseVersion
from f5.bigip.tm.asm.policies import Blocking_Settings
from f5.bigip.tm.asm.policies import Cookie
from f5.bigip.tm.asm.policies import Cookies_s
from f5.bigip.tm.asm.policies import Evasion
from f5.bigip.tm.asm.policies import Evasions_s
from f5.bigip.tm.asm.policies import Filetype
from f5.bigip.tm.asm.policies import Filetypes_s
from f5.bigip.tm.asm.policies import Gwt_Profile
from f5.bigip.tm.asm.policies import Gwt_Profiles_s
from f5.bigip.tm.asm.policies import Header
from f5.bigip.tm.asm.policies import Headers_s
from f5.bigip.tm.asm.policies import History_Revision
from f5.bigip.tm.asm.policies import History_Revisions_s
from f5.bigip.tm.asm.policies import Host_Name
from f5.bigip.tm.asm.policies import Host_Names_s
from f5.bigip.tm.asm.policies import Http_Protocol
from f5.bigip.tm.asm.policies import Http_Protocols_s
from f5.bigip.tm.asm.policies import Json_Profile
from f5.bigip.tm.asm.policies import Json_Profiles_s
from f5.bigip.tm.asm.policies import Method
from f5.bigip.tm.asm.policies import Methods_s
from f5.bigip.tm.asm.policies import Parameter
from f5.bigip.tm.asm.policies import Parameters_s
from f5.bigip.tm.asm.policies import ParametersCollection
from f5.bigip.tm.asm.policies import ParametersResource
from f5.bigip.tm.asm.policies import Policy
from f5.bigip.tm.asm.policies import Policy_Builder
from f5.bigip.tm.asm.policies import Response_Page
from f5.bigip.tm.asm.policies import Response_Pages_s
from f5.bigip.tm.asm.policies import Signature
from f5.bigip.tm.asm.policies import Signature_Set
from f5.bigip.tm.asm.policies import Signature_Sets_s
from f5.bigip.tm.asm.policies import Signatures_s
from f5.bigip.tm.asm.policies import Url
from f5.bigip.tm.asm.policies import UrlParametersCollection
from f5.bigip.tm.asm.policies import UrlParametersResource
from f5.bigip.tm.asm.policies import Urls_s
from f5.bigip.tm.asm.policies import Violation
from f5.bigip.tm.asm.policies import Violations_s
from f5.bigip.tm.asm.policies import Web_Services_Securities_s
from f5.bigip.tm.asm.policies import Web_Services_Security
from f5.bigip.tm.asm.policies import Whitelist_Ip
from f5.bigip.tm.asm.policies import Whitelist_Ips_s
from f5.bigip.tm.asm.policies import Xml_Profile
from f5.bigip.tm.asm.policies import Xml_Profiles_s
from f5.sdk_exception import AttemptedMutationOfReadOnly
from f5.sdk_exception import UnsupportedMethod
from f5.sdk_exception import UnsupportedOperation

import pytest
from requests.exceptions import HTTPError
from six import iteritems
from six import iterkeys
import time


def delete_policy_item(mgmt_root, name):
    col = mgmt_root.tm.asm.policies_s.get_collection()
    if len(col) > 0:
        for i in col:
            if i.name == name:
                i.delete()


def delete_apply_policy_task(mgmt_root):
    col = mgmt_root.tm.asm.tasks.apply_policy_s.get_collection()
    if len(col) > 0:
        for i in col:
            i.delete()


@pytest.fixture(scope='session')
def policy(mgmt_root):
    pol1 = mgmt_root.tm.asm.policies_s.policy.create(name='fake_policy')
    yield pol1
    delete_policy_item(mgmt_root, 'fake_policy')


@pytest.fixture(scope='session')
def signature(mgmt_root):
    coll = mgmt_root.tm.asm.signature_sets_s.get_collection(
        requests_params={'params': '$top=2'})
    lnk = str(coll[1].selfLink)
    yield lnk


@pytest.fixture(scope='class')
def resp_page(policy):
    rescol = policy.response_pages_s.get_collection()
    for item in rescol:
        if item.responsePageType == 'default':
            yield item.id


@pytest.fixture(scope='class')
def set_history(mgmt_root, policy):
    reference = {'link': policy.selfLink}
    mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.create(
        policyReference=reference)
    # We need to pause here as the history revisions take time to update
    time.sleep(3)
    col = policy.history_revisions_s.get_collection()
    hashid = str(col[0].id)
    yield hashid
    delete_apply_policy_task(mgmt_root)


class TestPolicy(object):
    def test_create_req_arg(self, policy):
        pol1 = policy
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri+endpoint
        assert pol1.name == 'fake_policy'
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.subPath == '/Common'
        assert pol1.kind == 'tm:asm:policies:policystate'

    def test_create_optional_args(self, mgmt_root):
        codes = [400, 401, 403]
        pol1 = mgmt_root.tm.asm.policies_s.policy.create(
            name='fake_policy_opt', allowedResponseCodes=codes)
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri+endpoint
        assert pol1.name == 'fake_policy_opt'
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.kind == 'tm:asm:policies:policystate'
        assert pol1.allowedResponseCodes == codes
        delete_policy_item(mgmt_root, 'fake_policy_opt')

    def test_refresh(self, policy, mgmt_root):
        pol1 = policy
        pol2 = mgmt_root.tm.asm.policies_s.policy.load(id=pol1.id)
        assert pol1.name == pol2.name
        assert pol1.selfLink == pol2.selfLink
        assert pol1.kind == pol2.kind
        assert pol1.allowedResponseCodes == pol2.allowedResponseCodes
        pol1.modify(allowedResponseCodes=[400, 503])
        assert pol1.selfLink == pol2.selfLink
        assert pol1.allowedResponseCodes != pol2.allowedResponseCodes
        pol2.refresh()
        assert pol1.allowedResponseCodes == pol2.allowedResponseCodes

    def test_modify(self, policy):
        original_dict = copy.copy(policy.__dict__)
        itm = 'allowedResponseCodes'
        policy.modify(allowedResponseCodes=[400])
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = policy.__dict__[k]
            elif k == itm:
                assert policy.__dict__[k] == [400]

    def test_delete(self, mgmt_root):
        pol1 = mgmt_root.tm.asm.policies_s.policy.create(name='delete_me')
        idhash = str(pol1.id)
        pol1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.policies_s.policy.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.policies_s.policy.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, mgmt_root):
        pol1 = policy
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri+endpoint
        assert pol1.name == 'fake_policy'
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.subPath == '/Common'
        assert pol1.kind == 'tm:asm:policies:policystate'
        pol1.modify(allowedResponseCodes=[400, 503])
        assert pol1.allowedResponseCodes == [400, 503]
        pol2 = mgmt_root.tm.asm.policies_s.policy.load(id=pol1.id)
        assert pol1.name == pol2.name
        assert pol1.selfLink == pol2.selfLink
        assert pol1.kind == pol2.kind
        assert pol1.allowedResponseCodes == pol2.allowedResponseCodes

    def test_policy_collection(self, mgmt_root):
        pc = mgmt_root.tm.asm.policies_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Policy)

    def test_policies_attr_reg(self, policy):
        obj_class = [Blocking_Settings, Cookies_s, Filetypes_s,
                     Gwt_Profiles_s, Headers_s, Host_Names_s, Json_Profiles_s,
                     Methods_s, Parameters_s, Signatures_s, Signature_Sets_s,
                     Urls_s, Whitelist_Ips_s, Xml_Profiles_s,
                     Response_Pages_s, Policy_Builder, History_Revisions_s]
        attributes = policy._meta_data['attribute_registry']
        assert set(obj_class) == set(attributes.values())


class TestMethods(object):
    def test_create_req_arg(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        assert met1.kind == 'tm:asm:policies:methods:methodstate'
        assert met1.name == 'DELETE'
        assert met1.actAsMethod == 'GET'
        met1.delete()

    def test_create_optional_args(self, policy):
        met1 = policy.methods_s.method.create(name='Foo', actAsMethod='POST')
        assert met1.kind == 'tm:asm:policies:methods:methodstate'
        assert met1.name == 'Foo'
        assert met1.actAsMethod == 'POST'
        met1.delete()

    def test_refresh(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        met2 = policy.methods_s.method.load(id=met1.id)
        assert met1.kind == met2.kind
        assert met1.name == met2.name
        assert met1.actAsMethod == met2.actAsMethod
        met2.modify(actAsMethod='POST')
        assert met1.actAsMethod == 'GET'
        assert met2.actAsMethod == 'POST'
        met1.refresh()
        assert met1.actAsMethod == 'POST'
        met1.delete()

    def test_modify(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        original_dict = copy.copy(met1.__dict__)
        itm = 'actAsMethod'
        met1.modify(actAsMethod='POST')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = met1.__dict__[k]
            elif k == itm:
                assert met1.__dict__[k] == 'POST'
        met1.delete()

    def test_delete(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        idhash = str(met1.id)
        met1.delete()
        with pytest.raises(HTTPError) as err:
            policy.methods_s.method.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.methods_s.method.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        assert met1.kind == 'tm:asm:policies:methods:methodstate'
        assert met1.name == 'DELETE'
        assert met1.actAsMethod == 'GET'
        met1.modify(actAsMethod='POST')
        assert met1.actAsMethod == 'POST'
        met2 = policy.methods_s.method.load(id=met1.id)
        assert met1.name == met2.name
        assert met1.selfLink == met2.selfLink
        assert met1.kind == met2.kind
        assert met1.actAsMethod == met2.actAsMethod

    def test_method_subcollection(self, policy):
        mc = policy.methods_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Method)


class TestFiletypes(object):
    def test_create_req_arg(self, policy):
        ft1 = policy.filetypes_s.filetype.create(name='fake_type')
        assert ft1.kind == 'tm:asm:policies:filetypes:filetypestate'
        assert ft1.name == 'fake_type'
        assert ft1.responseCheck is False
        ft1.delete()

    def test_create_optional_args(self, policy):
        ft1 = policy.filetypes_s.filetype.create(name='fake_type',
                                                 responseCheck=True)
        assert ft1.kind == 'tm:asm:policies:filetypes:filetypestate'
        assert ft1.name == 'fake_type'
        assert ft1.responseCheck is True
        ft1.delete()

    def test_refresh(self, policy):
        ft1 = policy.filetypes_s.filetype.create(name='fake_type')
        ft2 = policy.filetypes_s.filetype.load(id=ft1.id)
        assert ft1.kind == ft2.kind
        assert ft1.name == ft2.name
        assert ft1.responseCheck == ft2.responseCheck
        ft2.modify(responseCheck=True)
        assert ft1.responseCheck is False
        assert ft2.responseCheck is True
        ft1.refresh()
        assert ft1.responseCheck is True
        ft1.delete()

    def test_modify(self, policy):
        ft1 = policy.filetypes_s.filetype.create(name='fake_type')
        original_dict = copy.copy(ft1.__dict__)
        itm = 'responseCheck'
        ft1.modify(responseCheck=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = ft1.__dict__[k]
            elif k == itm:
                assert ft1.__dict__[k] is True

        ft1.delete()

    def test_delete(self, policy):
        ft1 = policy.filetypes_s.filetype.create(name='fake_type')
        idhash = str(ft1.id)
        ft1.delete()
        with pytest.raises(HTTPError) as err:
            policy.filetypes_s.filetype.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.filetypes_s.filetype.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        ft1 = policy.filetypes_s.filetype.create(name='fake_type')
        assert ft1.kind == 'tm:asm:policies:filetypes:filetypestate'
        assert ft1.name == 'fake_type'
        assert ft1.responseCheck is False
        ft1.modify(responseCheck=True)
        assert ft1.responseCheck is True
        ft2 = policy.filetypes_s.filetype.load(id=ft1.id)
        assert ft1.name == ft2.name
        assert ft1.selfLink == ft2.selfLink
        assert ft1.kind == ft2.kind
        assert ft1.responseCheck == ft2.responseCheck
        ft1.delete()

    def test_filetypes_subcollection(self, policy):
        ftc = policy.filetypes_s.get_collection()
        assert isinstance(ftc, list)
        assert len(ftc)
        assert isinstance(ftc[0], Filetype)


class TestCookies(object):
    def test_create_req_arg(self, policy):
        cook1 = policy.cookies_s.cookie.create(name='fake_type')
        assert cook1.kind == 'tm:asm:policies:cookies:cookiestate'
        assert cook1.name == 'fake_type'
        assert cook1.enforcementType == 'allow'
        cook1.delete()

    def test_create_optional_args(self, policy):
        cook1 = policy.cookies_s.cookie.create(name='fake_type',
                                               enforcementType='enforce')
        assert cook1.kind == 'tm:asm:policies:cookies:cookiestate'
        assert cook1.name == 'fake_type'
        assert cook1.enforcementType == 'enforce'
        cook1.delete()

    def test_refresh(self, policy):
        cook1 = policy.cookies_s.cookie.create(name='fake_type')
        cook2 = policy.cookies_s.cookie.load(id=cook1.id)
        assert cook1.kind == cook2.kind
        assert cook1.name == cook2.name
        assert cook1.enforcementType == cook2.enforcementType
        cook2.modify(enforcementType='enforce')
        assert cook1.enforcementType == 'allow'
        assert cook2.enforcementType == 'enforce'
        cook1.refresh()
        assert cook1.enforcementType == 'enforce'
        cook1.delete()

    def test_modify(self, policy):
        cook1 = policy.cookies_s.cookie.create(name='fake_type')
        original_dict = copy.copy(cook1.__dict__)
        itm = 'isBase64'
        cook1.modify(isBase64=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = cook1.__dict__[k]
            elif k == itm:
                assert cook1.__dict__[k] is True
        cook1.delete()

    def test_delete(self, policy):
        cook1 = policy.cookies_s.cookie.create(name='fake_type')
        idhash = str(cook1.id)
        cook1.delete()
        with pytest.raises(HTTPError) as err:
            policy.cookies_s.cookie.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.cookies_s.cookie.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        cook1 = policy.cookies_s.cookie.create(name='fake_type')
        assert cook1.kind == 'tm:asm:policies:cookies:cookiestate'
        assert cook1.name == 'fake_type'
        assert cook1.enforcementType == 'allow'
        cook1.modify(enforcementType='enforce')
        assert cook1.enforcementType == 'enforce'
        cook2 = policy.cookies_s.cookie.load(id=cook1.id)
        assert cook1.name == cook2.name
        assert cook1.selfLink == cook2.selfLink
        assert cook1.kind == cook2.kind
        assert cook1.enforcementType == cook2.enforcementType
        cook1.delete()

    def test_cookies_subcollection(self, policy):
        cc = policy.cookies_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Cookie)


class TestHostNames(object):
    def test_create_req_arg(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com')
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == 'fake-domain.com'
        assert host1.includeSubdomains is False
        host1.delete()

    def test_create_optional_args(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com',
                                                     includeSubdomains=True)
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == 'fake-domain.com'
        assert host1.includeSubdomains is True
        host1.delete()

    def test_refresh(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com')
        host2 = policy.host_names_s.host_name.load(id=host1.id)
        assert host1.kind == host2.kind
        assert host1.name == host2.name
        assert host1.includeSubdomains == host2.includeSubdomains
        host2.modify(includeSubdomains=True)
        assert host1.includeSubdomains is False
        assert host2.includeSubdomains is True
        host1.refresh()
        assert host1.includeSubdomains is True
        host1.delete()

    def test_modify(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com')
        original_dict = copy.copy(host1.__dict__)
        itm = 'includeSubdomains'
        host1.modify(includeSubdomains=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = host1.__dict__[k]
            elif k == itm:
                assert host1.__dict__[k] is True
        host1.delete()

    def test_delete(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com')
        idhash = str(host1.id)
        host1.delete()
        with pytest.raises(HTTPError) as err:
            policy.host_names_s.host_name.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.host_names_s.host_name.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com')
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == 'fake-domain.com'
        assert host1.includeSubdomains is False
        host1.modify(includeSubdomains=True)
        assert host1.includeSubdomains is True
        host2 = policy.host_names_s.host_name.load(id=host1.id)
        assert host1.name == host2.name
        assert host1.selfLink == host2.selfLink
        assert host1.kind == host2.kind
        assert host1.includeSubdomains == host2.includeSubdomains
        host1.delete()

    def test_cookies_subcollection(self, policy):
        host1 = policy.host_names_s.host_name.create(name='fake-domain.com')
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == 'fake-domain.com'
        cc = policy.host_names_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Host_Name)
        host1.delete()


class TestBlockingSettings(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedMethod):
            policy.blocking_settings.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedMethod):
            policy.blocking_settings.delete()

    def test_load(self, policy):
        block = policy.blocking_settings.load()
        attributes = block._meta_data['attribute_registry']
        obj_class = [Evasions_s, Http_Protocols_s, Violations_s,
                     Web_Services_Securities_s]
        v12kind = 'tm:asm:policies:blocking-settings:blocking-' \
                  'settingcollectionstate'
        v11kind = 'tm:asm:policies:blocking-settings'
        if LooseVersion(pytest.config.getoption('--release')) < \
                LooseVersion('12.0.0'):
            assert block.kind == v11kind
        else:
            assert block.kind == v12kind
        assert hasattr(block, 'httpProtocolReference')
        assert hasattr(block, 'webServicesSecurityReference')
        assert hasattr(block, 'evasionReference')
        assert hasattr(block, 'violationReference')
        assert set(obj_class) == set(attributes.values())


class TestEvasions(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.evasions_s.evasion.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.evasions_s.evasion.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        eva2 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        assert eva1.kind == eva2.kind
        assert eva1.description == eva2.description
        assert eva1.enabled == eva2.enabled
        eva2.modify(enabled=False)
        assert eva1.enabled is True
        assert eva2.enabled is False
        eva1.refresh()
        assert eva1.enabled is False

    def test_modify(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        original_dict = copy.copy(eva1.__dict__)
        itm = 'enabled'
        eva1.modify(enabled=False)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = eva1.__dict__[k]
            elif k == itm:
                assert eva1.__dict__[k] is False

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.evasions_s.evasion.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        hashid = str(coll[0].id)
        eva1 = policy.blocking_settings.evasions_s.evasion.load(id=hashid)
        assert eva1.kind == 'tm:asm:policies:blocking-' \
                            'settings:evasions:evasionstate'
        assert eva1.enabled is False
        eva1.modify(enabled=True)
        assert eva1.enabled is True
        eva2 = policy.blocking_settings.evasions_s.evasion.load(id=eva1.id)
        assert eva1.selfLink == eva2.selfLink
        assert eva1.kind == eva2.kind
        assert eva1.enabled == eva2.enabled

    def test_evasions_subcollection(self, policy):
        coll = policy.blocking_settings.evasions_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Evasion)


class TestViolations(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.violations_s.violation.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.violations_s.violation.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        vio2 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        assert vio1.kind == vio2.kind
        assert vio1.description == vio2.description
        assert vio1.learn == vio2.learn
        vio2.modify(learn=False)
        assert vio1.learn is True
        assert vio2.learn is False
        vio1.refresh()
        assert vio1.learn is False

    def test_modify(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        original_dict = copy.copy(vio1.__dict__)
        itm = 'learn'
        vio1.modify(learn=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = vio1.__dict__[k]
            elif k == itm:
                assert vio1.__dict__[k] is True

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.violations_s.violation.load(
                id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        hashid = str(coll[0].id)
        vio1 = policy.blocking_settings.violations_s.violation.load(id=hashid)
        assert vio1.kind == 'tm:asm:policies:blocking-settings' \
                            ':violations:violationstate'
        assert vio1.learn is True
        vio1.modify(learn=False)
        assert vio1.learn is False
        vio2 = policy.blocking_settings.violations_s.violation.load(id=vio1.id)
        assert vio1.selfLink == vio2.selfLink
        assert vio1.kind == vio2.kind
        assert vio1.learn == vio2.learn

    def test_violations_subcollection(self, policy):
        coll = policy.blocking_settings.violations_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Violation)


class TestHTTPProtoccols(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.http_protocols_s.http_protocol.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.blocking_settings.http_protocols_s.http_protocol.delete()

    def test_refresh(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(
            id=hashid)
        http2 = policy.blocking_settings.http_protocols_s.http_protocol.load(
            id=hashid)
        assert http1.kind == http2.kind
        assert http1.description == http2.description
        assert http1.enabled == http2.enabled
        http2.modify(enabled=False)
        assert http1.enabled is True
        assert http2.enabled is False
        http1.refresh()
        assert http1.enabled is False

    def test_modify(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(
            id=hashid)
        original_dict = copy.copy(http1.__dict__)
        itm = 'enabled'
        http1.modify(enabled=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = http1.__dict__[k]
            elif k == itm:
                assert http1.__dict__[k] is True

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.blocking_settings.http_protocols_s.\
                http_protocol.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        hashid = str(coll[1].id)
        http1 = policy.blocking_settings.http_protocols_s.http_protocol.load(
            id=hashid)
        assert http1.kind == 'tm:asm:policies:blocking-settings:' \
                             'http-protocols:http-protocolstate'
        assert http1.enabled is True
        http1.modify(enabled=False)
        assert http1.enabled is False
        http2 = policy.blocking_settings.http_protocols_s.\
            http_protocol.load(id=http1.id)
        assert http1.selfLink == http2.selfLink
        assert http1.kind == http2.kind
        assert http1.enabled == http2.enabled

    def test_httpprotocols_subcollection(self, policy):
        coll = policy.blocking_settings.http_protocols_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Http_Protocol)


class TestWebServicesSecurities(object):
    def test_create_raises(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(UnsupportedOperation):
            wsc.web_services_security.create()

    def test_delete_raises(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(UnsupportedOperation):
            wsc.web_services_security.delete()

    def test_refresh(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hashid = str(coll[1].id)
        ws1 = wsc.web_services_security.load(id=hashid)
        ws2 = wsc.web_services_security.load(id=hashid)
        assert ws1.kind == ws2.kind
        assert ws1.description == ws2.description
        assert ws1.enabled == ws2.enabled
        ws2.modify(enabled=False)
        assert ws1.enabled is True
        assert ws2.enabled is False
        ws1.refresh()
        assert ws1.enabled is False

    def test_modify(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hashid = str(coll[1].id)
        ws1 = wsc.web_services_security.load(id=hashid)
        original_dict = copy.copy(ws1.__dict__)
        itm = 'enabled'
        ws1.modify(enabled=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = ws1.__dict__[k]
            elif k == itm:
                assert ws1.__dict__[k] is True

    def test_load_no_object(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        with pytest.raises(HTTPError) as err:
            wsc.web_services_security.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        hashid = str(coll[1].id)
        ws1 = wsc.web_services_security.load(id=hashid)
        assert ws1.kind == 'tm:asm:policies:blocking-settings:' \
                           'web-services-securities:web-services-securitystate'
        assert ws1.enabled is True
        ws1.modify(enabled=False)
        assert ws1.enabled is False
        ws2 = wsc.web_services_security.load(id=ws1.id)
        assert ws1.selfLink == ws2.selfLink
        assert ws1.kind == ws2.kind
        assert ws1.enabled == ws2.enabled

    def test_webservicessecurities_subcollection(self, policy):
        wsc = policy.blocking_settings.web_services_securities_s
        coll = wsc.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Web_Services_Security)


class TestUrls(object):
    def test_create_req_arg(self, policy):
        url1 = policy.urls_s.url.create(name='testing')
        assert url1.kind == 'tm:asm:policies:urls:urlstate'
        assert url1.name == '/testing'
        assert url1.type == 'explicit'
        assert url1.clickjackingProtection is False
        url1.delete()

    def test_create_optional_args(self, policy):
        url1 = policy.urls_s.url.create(name='testing',
                                        clickjackingProtection=True)
        assert url1.kind == 'tm:asm:policies:urls:urlstate'
        assert url1.name == '/testing'
        assert url1.type == 'explicit'
        assert url1.clickjackingProtection is True
        url1.delete()

    def test_refresh(self, policy):
        url1 = policy.urls_s.url.create(name='testing')
        url2 = policy.urls_s.url.load(id=url1.id)
        assert url1.kind == url2.kind
        assert url1.name == url2.name
        assert url1.clickjackingProtection == url2.clickjackingProtection
        url2.modify(clickjackingProtection=True)
        assert url1.clickjackingProtection is False
        assert url2.clickjackingProtection is True
        url1.refresh()
        assert url1.clickjackingProtection is True
        url1.delete()

    def test_modify(self, policy):
        url1 = policy.urls_s.url.create(name='testing')
        original_dict = copy.copy(url1.__dict__)
        itm = 'clickjackingProtection'
        url1.modify(clickjackingProtection=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = url1.__dict__[k]
            elif k == itm:
                assert url1.__dict__[k] is True
        url1.delete()

    def test_delete(self, policy):
        url1 = policy.urls_s.url.create(name='testing')
        idhash = str(url1.id)
        url1.delete()
        with pytest.raises(HTTPError) as err:
            policy.urls_s.url.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.urls_s.url.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        url1 = policy.urls_s.url.create(name='testing')
        assert url1.kind == 'tm:asm:policies:urls:urlstate'
        assert url1.name == '/testing'
        assert url1.type == 'explicit'
        assert url1.clickjackingProtection is False
        url1.modify(clickjackingProtection=True)
        assert url1.clickjackingProtection is True
        url2 = policy.urls_s.url.load(id=url1.id)
        assert url1.name == url2.name
        assert url1.selfLink == url2.selfLink
        assert url1.kind == url2.kind
        assert url1.clickjackingProtection == url2.clickjackingProtection
        url1.delete()

    def test_urls_subcollection(self, policy):
        cc = policy.urls_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Url)


class TestParametersCol(object):
    def test_new_method(self, policy):
        url_res = policy.urls_s.url.create(name='testing')
        kind_pol = 'tm:asm:policies:parameters:parameterstate'
        kind_url = 'tm:asm:policies:urls:parameters:parameterstate'

        policyparam = Parameters_s(policy)
        test_meta_pol = policyparam._meta_data['attribute_registry']
        test_meta_pol2 = policyparam._meta_data['allowed_lazy_attributes']
        assert isinstance(policyparam, ParametersCollection)
        assert hasattr(policyparam, 'parameter')
        assert policyparam.__class__.__name__ == 'Parameters_s'
        assert kind_pol in list(iterkeys(test_meta_pol))
        assert Parameter in test_meta_pol2

        urlparam = Parameters_s(url_res)
        test_meta_url = urlparam._meta_data['attribute_registry']
        test_meta_url2 = urlparam._meta_data['allowed_lazy_attributes']
        assert isinstance(urlparam, UrlParametersCollection)
        assert hasattr(urlparam, 'parameter')
        assert urlparam.__class__.__name__ == 'Parameters_s'
        assert kind_url in list(iterkeys(test_meta_url))
        assert Parameter in test_meta_url2
        url_res.delete()


class TestParametersRes(object):
    def test_new_method(self, policy):
        url_res = policy.urls_s.url.create(name='testing')
        kind_pol = 'tm:asm:policies:parameters:parameterstate'
        kind_url = 'tm:asm:policies:urls:parameters:parameterstate'

        policyparam = Parameter((Parameters_s(policy)))
        test_meta_pol = policyparam._meta_data['required_json_kind']
        assert isinstance(policyparam, ParametersResource)
        assert policyparam.__class__.__name__ == 'Parameter'
        assert kind_pol in test_meta_pol

        urlparam = Parameter((Parameters_s(url_res)))
        test_meta_url = urlparam._meta_data['required_json_kind']
        assert isinstance(urlparam, UrlParametersResource)
        assert urlparam.__class__.__name__ == 'Parameter'
        assert kind_url in test_meta_url
        url_res.delete()


class TestUrlParameters(object):
    def test_create_req_arg(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter')
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is False
        param1.delete()
        url.delete()

    def test_create_optional_args(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter',
                                                   sensitiveParameter=True)
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is True
        param1.delete()
        url.delete()

    def test_refresh(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter')
        param2 = url.parameters_s.parameter.load(id=param1.id)
        assert param1.kind == param2.kind
        assert param1.name == param2.name
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param2.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is False
        assert param2.sensitiveParameter is True
        param1.refresh()
        assert param1.sensitiveParameter is True
        param1.delete()
        url.delete()

    def test_modify(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter')
        original_dict = copy.copy(param1.__dict__)
        itm = 'sensitiveParameter'
        param1.modify(sensitiveParameter=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = param1.__dict__[k]
            elif k == itm:
                assert param1.__dict__[k] is True
        param1.delete()
        url.delete()

    def test_delete(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter')
        idhash = str(param1.id)
        param1.delete()
        with pytest.raises(HTTPError) as err:
            url.parameters_s.parameter.load(id=idhash)
        assert err.value.response.status_code == 404
        url.delete()

    def test_load_no_object(self, policy):
        url = policy.urls_s.url.create(name='testing')
        with pytest.raises(HTTPError) as err:
            url.parameters_s.parameter.load(id='Lx3553-321')
        assert err.value.response.status_code == 404
        url.delete()

    def test_load(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter')
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is False
        param1.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is True
        param2 = url.parameters_s.parameter.load(id=param1.id)
        assert param1.name == param2.name
        assert param1.selfLink == param2.selfLink
        assert param1.kind == param2.kind
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param1.delete()
        url.delete()

    def test_urls_subcollection(self, policy):
        url = policy.urls_s.url.create(name='testing')
        param1 = url.parameters_s.parameter.create(name='testing_parameter')
        assert param1.kind == 'tm:asm:policies:urls:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.sensitiveParameter is False

        cc = url.parameters_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], UrlParametersResource)
        param1.delete()
        url.delete()


class TestPolicyParameters(object):
    def test_create_req_arg(self, policy):
        param1 = policy.parameters_s.parameter.create(name='testing_parameter')
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is False
        param1.delete()

    def test_create_optional_args(self, policy):
        param1 = policy.parameters_s.parameter.create(
            name='testing_parameter', sensitiveParameter=True)
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is True
        param1.delete()

    def test_refresh(self, policy):
        param1 = policy.parameters_s.parameter.create(name='testing_parameter')
        param2 = policy.parameters_s.parameter.load(id=param1.id)
        assert param1.kind == param2.kind
        assert param1.name == param2.name
        assert param1.level == param2.level
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param2.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is False
        assert param2.sensitiveParameter is True
        param1.refresh()
        assert param1.sensitiveParameter is True
        param1.delete()

    def test_modify(self, policy):
        param1 = policy.parameters_s.parameter.create(name='testing_parameter')
        original_dict = copy.copy(param1.__dict__)
        itm = 'sensitiveParameter'
        param1.modify(sensitiveParameter=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = param1.__dict__[k]
            elif k == itm:
                assert param1.__dict__[k] is True
        param1.delete()

    def test_delete(self, policy):
        param1 = policy.parameters_s.parameter.create(name='testing_parameter')
        idhash = str(param1.id)
        param1.delete()
        with pytest.raises(HTTPError) as err:
            policy.parameters_s.parameter.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.parameters_s.parameter.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        param1 = policy.parameters_s.parameter.create(name='testing_parameter')
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is False
        param1.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is True
        param2 = policy.parameters_s.parameter.load(id=param1.id)
        assert param1.name == param2.name
        assert param1.selfLink == param2.selfLink
        assert param1.kind == param2.kind
        assert param1.level == param2.level
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param1.delete()

    def test_parameters_subcollection(self, policy):
        param1 = policy.parameters_s.parameter.create(name='testing_parameter')
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == 'testing_parameter'
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is False

        cc = policy.parameters_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], ParametersResource)
        param1.delete()


class TestWhitelistIps(object):
    def test_create_req_arg(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.1')
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == '11.11.11.1'
        assert ip1.ipMask == '255.255.255.255'
        ip1.delete()

    def test_create_optional_args(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.0', ipMask='255.255.255.224')
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == '11.11.11.0'
        assert ip1.ipMask == '255.255.255.224'
        ip1.delete()

    def test_refresh(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.1')
        ip2 = policy.whitelist_ips_s.whitelist_ip.load(id=ip1.id)
        assert ip1.kind == ip2.kind
        assert ip1.ipAddress == ip2.ipAddress
        assert ip1.description == ip2.description
        ip2.modify(description='TESTFAKE')
        assert ip1.description == ''
        assert ip2.description == 'TESTFAKE'
        ip1.refresh()
        assert ip1.description == 'TESTFAKE'
        ip1.delete()

    def test_modify_read_only_raises(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.0', ipMask='255.255.255.0')
        with pytest.raises(AttemptedMutationOfReadOnly):
            ip1.modify(ipMask='255.255.255.224')

    def test_modify(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.1')
        original_dict = copy.copy(ip1.__dict__)
        itm = 'description'
        ip1.modify(description='TESTFAKE')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = ip1.__dict__[k]
            elif k == itm:
                assert ip1.__dict__[k] == 'TESTFAKE'
        ip1.delete()

    def test_delete(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.1')
        idhash = str(ip1.id)
        ip1.delete()
        with pytest.raises(HTTPError) as err:
            policy.whitelist_ips_s.whitelist_ip.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.whitelist_ips_s.whitelist_ip.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.1')
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == '11.11.11.1'
        assert ip1.ipMask == '255.255.255.255'
        assert ip1.description == ''
        ip1.modify(description='TESTFAKE')
        assert ip1.description == 'TESTFAKE'
        ip2 = policy.whitelist_ips_s.whitelist_ip.load(id=ip1.id)
        assert ip1.kind == ip2.kind
        assert ip1.ipAddress == ip2.ipAddress
        assert ip1.selfLink == ip2.selfLink
        assert ip1.description == ip2.description
        ip1.delete()

    def test_whitelistips_subcollection(self, policy):
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress='11.11.11.1')
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == '11.11.11.1'
        assert ip1.ipMask == '255.255.255.255'
        cc = policy.whitelist_ips_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Whitelist_Ip)
        ip1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestGwtProfiles(object):
    def test_create_req_arg(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt')
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == 'fake_gwt'
        assert gwt1.description == ''
        gwt1.delete()

    def test_create_optional_args(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt',
                                                        description='FAKEDESC')
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == 'fake_gwt'
        assert gwt1.description == 'FAKEDESC'
        gwt1.delete()

    def test_refresh(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt')
        gwt2 = policy.gwt_profiles_s.gwt_profile.load(id=gwt1.id)
        assert gwt1.kind == gwt2.kind
        assert gwt1.name == gwt2.name
        assert gwt1.description == gwt2.description
        gwt2.modify(description='FAKEDESC')
        assert gwt1.description == ''
        assert gwt2.description == 'FAKEDESC'
        gwt1.refresh()
        assert gwt1.description == 'FAKEDESC'
        gwt1.delete()

    def test_modify(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt')
        original_dict = copy.copy(gwt1.__dict__)
        itm = 'description'
        gwt1.modify(description='FAKEDESC')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = gwt1.__dict__[k]
            elif k == itm:
                assert gwt1.__dict__[k] == 'FAKEDESC'
        gwt1.delete()

    def test_delete(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt')
        idhash = str(gwt1.id)
        gwt1.delete()
        with pytest.raises(HTTPError) as err:
            policy.gwt_profiles_s.gwt_profile.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.gwt_profiles_s.gwt_profile.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt')
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == 'fake_gwt'
        assert gwt1.description == ''
        gwt1.modify(description='FAKEDESC')
        assert gwt1.description == 'FAKEDESC'
        gwt2 = policy.gwt_profiles_s.gwt_profile.load(id=gwt1.id)
        assert gwt1.name == gwt2.name
        assert gwt1.selfLink == gwt2.selfLink
        assert gwt1.kind == gwt2.kind
        assert gwt1.description == gwt2.description
        gwt1.delete()

    def test_gwtprofile_subcollection(self, policy):
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name='fake_gwt')
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == 'fake_gwt'
        assert gwt1.description == ''
        cc = policy.gwt_profiles_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Gwt_Profile)
        gwt1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestJsonProfile(object):
    def test_create_req_arg(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(name='fake_json')
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == 'fake_json'
        assert json1.description == ''
        json1.delete()

    def test_create_optional_args(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(
            name='fake_json', description='FAKEDESC')
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == 'fake_json'
        assert json1.description == 'FAKEDESC'
        json1.delete()

    def test_refresh(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(name='fake_json')
        json2 = policy.json_profiles_s.json_profile.load(id=json1.id)
        assert json1.kind == json2.kind
        assert json1.name == json2.name
        assert json1.description == json2.description
        json2.modify(description='FAKEDESC')
        assert json1.description == ''
        assert json2.description == 'FAKEDESC'
        json1.refresh()
        assert json1.description == 'FAKEDESC'
        json1.delete()

    def test_modify(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(name='fake_json')
        original_dict = copy.copy(json1.__dict__)
        itm = 'description'
        json1.modify(description='FAKEDESC')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = json1.__dict__[k]
            elif k == itm:
                assert json1.__dict__[k] == 'FAKEDESC'
        json1.delete()

    def test_delete(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(name='fake_json')
        idhash = str(json1.id)
        json1.delete()
        with pytest.raises(HTTPError) as err:
            policy.json_profiles_s.json_profile.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.json_profiles_s.json_profile.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(name='fake_json')
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == 'fake_json'
        assert json1.description == ''
        json1.modify(description='FAKEDESC')
        assert json1.description == 'FAKEDESC'
        json2 = policy.json_profiles_s.json_profile.load(id=json1.id)
        assert json1.name == json2.name
        assert json1.selfLink == json2.selfLink
        assert json1.kind == json2.kind
        assert json1.description == json2.description
        json1.delete()

    def test_jsonprofile_subcollection(self, policy):
        json1 = policy.json_profiles_s.json_profile.create(name='fake_json')
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == 'fake_json'
        assert json1.description == ''
        cc = policy.json_profiles_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Json_Profile)
        json1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestXmlProfile(object):
    def test_create_req_arg(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(name='fake_xml')
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == 'fake_xml'
        assert xml1.description == ''
        xml1.delete()

    def test_create_optional_args(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(
            name='fake_xml', description='FAKEDESC')
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == 'fake_xml'
        assert xml1.description == 'FAKEDESC'
        xml1.delete()

    def test_refresh(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(name='fake_xml')
        xml2 = policy.xml_profiles_s.xml_profile.load(id=xml1.id)
        assert xml1.kind == xml2.kind
        assert xml1.name == xml2.name
        assert xml1.description == xml2.description
        xml2.modify(description='FAKEDESC')
        assert xml1.description == ''
        assert xml2.description == 'FAKEDESC'
        xml1.refresh()
        assert xml1.description == 'FAKEDESC'
        xml1.delete()

    def test_modify(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(name='fake_xml')
        original_dict = copy.copy(xml1.__dict__)
        itm = 'description'
        xml1.modify(description='FAKEDESC')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = xml1.__dict__[k]
            elif k == itm:
                assert xml1.__dict__[k] == 'FAKEDESC'
        xml1.delete()

    def test_delete(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(name='fake_xml')
        idhash = str(xml1.id)
        xml1.delete()
        with pytest.raises(HTTPError) as err:
            policy.xml_profiles_s.xml_profile.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.xml_profiles_s.xml_profile.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(name='fake_xml')
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == 'fake_xml'
        assert xml1.description == ''
        xml1.modify(description='FAKEDESC')
        assert xml1.description == 'FAKEDESC'
        xml2 = policy.xml_profiles_s.xml_profile.load(id=xml1.id)
        assert xml1.name == xml2.name
        assert xml1.selfLink == xml2.selfLink
        assert xml1.kind == xml2.kind
        assert xml1.description == xml2.description
        xml1.delete()

    def test_xmlprofile_subcollection(self, policy):
        xml1 = policy.xml_profiles_s.xml_profile.create(name='fake_xml')
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == 'fake_xml'
        assert xml1.description == ''
        cc = policy.xml_profiles_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Xml_Profile)
        xml1.delete()


class TestSignature(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.signatures_s.signature.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.signatures_s.signature.delete()

    def test_refresh(self, policy):
        coll = policy.signatures_s.get_collection()
        hashid = str(coll[1].id)
        ws1 = policy.signatures_s.signature.load(id=hashid)
        ws2 = policy.signatures_s.signature.load(id=hashid)
        assert ws1.kind == ws2.kind
        assert ws1.performStaging == ws2.performStaging
        ws2.modify(performStaging=False)
        assert ws1.performStaging is True
        assert ws2.performStaging is False
        ws1.refresh()
        assert ws1.performStaging is False

    def test_modify(self, policy):
        coll = policy.signatures_s.get_collection()
        hashid = str(coll[1].id)
        ws1 = policy.signatures_s.signature.load(id=hashid)
        original_dict = copy.copy(ws1.__dict__)
        itm = 'performStaging'
        ws1.modify(performStaging=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = ws1.__dict__[k]
            elif k == itm:
                assert ws1.__dict__[k] is True

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.signatures_s.signature.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.signatures_s.get_collection()
        hashid = str(coll[1].id)
        ws1 = policy.signatures_s.signature.load(id=hashid)
        assert ws1.kind == 'tm:asm:policies:signatures:signaturestate'
        assert ws1.performStaging is True
        ws1.modify(performStaging=False)
        assert ws1.performStaging is False
        ws2 = policy.signatures_s.signature.load(id=ws1.id)
        assert ws1.selfLink == ws2.selfLink
        assert ws1.kind == ws2.kind
        assert ws1.performStaging == ws2.performStaging

    def test_signatures_subcollection(self, policy):
        coll = policy.signatures_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Signature)


class TestSignatureSets(object):
    def test_create_req_arg(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature})
        assert ss1.kind == 'tm:asm:policies:signature-sets:signature-setstate'
        assert ss1.alarm is True
        assert ss1.learn is True
        ss1.delete()

    def test_create_optional_args(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature}, alarm=False,
            learn=False)
        assert ss1.kind == 'tm:asm:policies:signature-sets:signature-setstate'
        assert ss1.alarm is False
        assert ss1.learn is False
        ss1.delete()

    def test_refresh(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature})
        ss2 = policy.signature_sets_s.signature_set.load(id=ss1.id)
        assert ss1.kind == ss2.kind
        assert ss1.alarm == ss2.alarm
        assert ss1.learn == ss2.learn
        ss2.modify(alarm=False)
        assert ss1.alarm is True
        assert ss2.alarm is False
        ss1.refresh()
        assert ss1.alarm is False
        ss1.delete()

    def test_modify(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature})
        original_dict = copy.copy(ss1.__dict__)
        itm = 'alarm'
        ss1.modify(alarm=False)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = ss1.__dict__[k]
            elif k == itm:
                assert ss1.__dict__[k] is False
        ss1.delete()

    def test_delete(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature})
        idhash = str(ss1.id)
        ss1.delete()
        with pytest.raises(HTTPError) as err:
            policy.signature_sets_s.signature_set.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.signature_sets_s.signature_set.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature})
        assert ss1.kind == 'tm:asm:policies:signature-sets:signature-setstate'
        assert ss1.alarm is True
        assert ss1.learn is True
        ss1.modify(alarm=False)
        assert ss1.alarm is False
        ss2 = policy.signature_sets_s.signature_set.load(id=ss1.id)
        assert ss1.selfLink == ss2.selfLink
        assert ss1.kind == ss2.kind
        assert ss1.alarm == ss2.alarm
        assert ss1.learn == ss2.learn
        ss1.delete()

    def test_signatureset_subcollection(self, policy):
        cc = policy.signature_sets_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Signature_Set)


class TestHeaders(object):
    def test_create_req_arg(self, policy):
        h1 = policy.headers_s.header.create(name='Fake')
        assert h1.kind == 'tm:asm:policies:headers:headerstate'
        assert h1.name == 'fake'
        assert h1.type == 'explicit'
        assert h1.base64Decoding is False
        h1.delete()

    def test_create_optional_args(self, policy):
        h1 = policy.headers_s.header.create(name='Fake', base64Decoding=True)
        assert h1.kind == 'tm:asm:policies:headers:headerstate'
        assert h1.name == 'fake'
        assert h1.type == 'explicit'
        assert h1.base64Decoding is True
        h1.delete()

    def test_refresh(self, policy):
        h1 = policy.headers_s.header.create(name='Fake')
        h2 = policy.headers_s.header.load(id=h1.id)
        assert h1.kind == h2.kind
        assert h1.name == h2.name
        assert h1.base64Decoding == h2.base64Decoding
        h2.modify(base64Decoding=True)
        assert h1.base64Decoding is False
        assert h2.base64Decoding is True
        h1.refresh()
        assert h1.base64Decoding is True
        h1.delete()

    def test_modify(self, policy):
        h1 = policy.headers_s.header.create(name='Fake')
        original_dict = copy.copy(h1.__dict__)
        itm = 'base64Decoding'
        h1.modify(base64Decoding=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = h1.__dict__[k]
            elif k == itm:
                assert h1.__dict__[k] is True
        h1.delete()

    def test_delete(self, policy):
        h1 = policy.headers_s.header.create(name='Fake')
        idhash = str(h1.id)
        h1.delete()
        with pytest.raises(HTTPError) as err:
            policy.headers_s.header.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.headers_s.header.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        h1 = policy.headers_s.header.create(name='Fake')
        assert h1.kind == 'tm:asm:policies:headers:headerstate'
        assert h1.name == 'fake'
        assert h1.base64Decoding is False
        h1.modify(base64Decoding=True)
        assert h1.base64Decoding is True
        h2 = policy.headers_s.header.load(id=h1.id)
        assert h1.name == h2.name
        assert h1.selfLink == h2.selfLink
        assert h1.kind == h2.kind
        assert h1.base64Decoding == h2.base64Decoding
        h1.delete()

    def test_method_subcollection(self, policy):
        mc = policy.headers_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Header)


class TestPolicyBuilder(object):
    def test_update_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.policy_builder.update()

    def test_modify(self, policy):
        r1 = policy.policy_builder.load()
        original_dict = copy.copy(r1.__dict__)
        itm = 'enablePolicyBuilder'
        r1.modify(enablePolicyBuilder=True)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] is True

    def test_load(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:pbconfigstate'
        assert r1.enablePolicyBuilder is True
        assert hasattr(r1, 'responseStatusCodes')
        assert hasattr(r1, 'learnFromResponses')
        r1.modify(enablePolicyBuilder=False)
        assert r1.enablePolicyBuilder is False
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
        assert not hasattr(r2, 'responseStatusCodes')
        assert not hasattr(r2, 'learnFromResponses')

    def test_refresh(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:pbconfigstate'
        assert r1.enablePolicyBuilder is False
        assert not hasattr(r1, 'responseStatusCodes')
        assert not hasattr(r1, 'learnFromResponses')
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
        assert r2.enablePolicyBuilder is False
        assert not hasattr(r2, 'responseStatusCodes')
        assert not hasattr(r2, 'learnFromResponses')
        r2.modify(enablePolicyBuilder=True)
        assert r2.enablePolicyBuilder is True
        assert hasattr(r2, 'responseStatusCodes')
        assert hasattr(r2, 'learnFromResponses')
        r1.refresh()
        assert hasattr(r1, 'responseStatusCodes')
        assert hasattr(r1, 'learnFromResponses')
        assert r1.enablePolicyBuilder == r2.enablePolicyBuilder


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestResponsePages(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.response_pages_s.response_page.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.response_pages_s.response_page.delete()

    def test_refresh(self, policy, resp_page):
        hashid = resp_page
        r1 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:response-pages:response-pagestate'
        assert r1.responseActionType == 'default'
        assert r1.responsePageType == 'default'
        r2 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.responseActionType == r2.responseActionType
        assert r1.responsePageType == r2.responsePageType
        r2.responseActionType = 'redirect'
        r2.responseRedirectUrl = 'http://fake-site.com'
        r2.modify(responseActionType='redirect',
                  responseRedirectUrl='http://fake-site.com')
        assert r1.responseActionType == 'default'
        assert r2.responseActionType == 'redirect'
        assert not hasattr(r1, 'responseRedirectUrl')
        assert hasattr(r2, 'responseRedirectUrl')
        r1.refresh()
        assert hasattr(r1, 'responseRedirectUrl')
        assert r1.responseActionType == r2.responseActionType
        assert r1.responseRedirectUrl == 'http://fake-site.com'

    def test_modify(self, policy, resp_page):
        hashid = resp_page
        r1 = policy.response_pages_s.response_page.load(id=hashid)
        original_dict = copy.copy(r1.__dict__)
        itm = 'responseRedirectUrl'
        r1.modify(responseRedirectUrl='http://modified-fake.com')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 'http://modified-fake.com'

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.response_pages_s.response_page.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, resp_page):
        hashid = resp_page
        r1 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:response-pages:response-pagestate'
        assert r1.responsePageType == 'default'
        assert r1.responseActionType == 'redirect'
        assert r1.responseRedirectUrl == 'http://modified-fake.com'
        r1.modify(responseRedirectUrl='http://loaded-fake.com')
        assert r1.responseRedirectUrl == 'http://loaded-fake.com'
        r2 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.responseActionType == r2.responseActionType
        assert r1.responsePageType == r2.responsePageType
        assert r1.responseRedirectUrl == r2.responseRedirectUrl

    def test_method_subcollection(self, policy):
        mc = policy.response_pages_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Response_Page)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestHistoryRevisions(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.history_revisions_s.history_revision.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.history_revisions_s.history_revision.delete()

    def test_modify_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.history_revisions_s.history_revision.create()

    def test_refresh(self, policy, set_history):
        hashid = set_history
        r1 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:history-revisions:' \
                          'history-revisionstate'
        link = str(policy.selfLink) + '/' + 'history-revisions' + '/' + hashid
        assert r1.selfLink == link
        r2 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.history_revisions_s.history_revision.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, set_history):
        hashid = set_history
        r1 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:history-revisions:' \
                          'history-revisionstate'
        link = str(policy.selfLink) + '/'+'history-revisions' + '/' + hashid
        assert r1.selfLink == link
        r2 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_method_subcollection(self, policy):
        mc = policy.history_revisions_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], History_Revision)
