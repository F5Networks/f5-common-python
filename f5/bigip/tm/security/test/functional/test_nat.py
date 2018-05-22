# Copyright 2015-2106 F5 Networks Inc.
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

import pytest
import time

from distutils.version import LooseVersion
from f5.bigip.tm.security.nat import Destination_Translation
from f5.bigip.tm.security.nat import Rules
from f5.bigip.tm.security.nat import Source_Translation
from f5.sdk_exception import ExclusiveAttributesPresent
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.utils.responses.handlers import Stats
from icontrol.exceptions import iControlUnexpectedHTTPError
from requests.exceptions import HTTPError

TESTDESCRIPTION = 'TESTDESCRIPTION'
not_supported_prior_12_1_0 = pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release'))
    < LooseVersion('12.1.0'),
    reason='This collection exists on 12.1.0 or greater.')


@pytest.fixture
def virtual_setup(mgmt_root):
    vs_kwargs = {'name': 'vs_fwnat', 'partition': 'Common',
                 'destination': '10.9.8.7:65432'}
    vs = mgmt_root.tm.ltm.virtuals.virtual
    v1 = vs.create(profiles=['/Common/tcp'], **vs_kwargs)
    yield v1
    v1.delete()


class PolicyHelper(object):
    @staticmethod
    def delete_policy(mgmt_root, name, partition):
        try:
            pol = mgmt_root.tm.security.nat.policys.policy.load(
                name=name, partition=partition)
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            return
        pol.delete()

    @staticmethod
    def setup_basic_test(request, mgmt_root, name, partition):
        def teardown():
            PolicyHelper.delete_policy(mgmt_root, name, partition)

        pol = mgmt_root.tm.security.nat.policys.policy.create(
            name=name, partition=partition)
        request.addfinalizer(teardown)
        return pol


class SrcXlatHelper(object):
    @staticmethod
    def delete_src_xlat(mgmt_root, name, partition):
        try:
            src_xlat = mgmt_root.tm.security.nat.source_translations.\
                source_translation.load(name=name, partition=partition)
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            return
        src_xlat.delete()

    @staticmethod
    def setup_basic_test(request, mgmt_root, **kwargs):
        name = kwargs.get('name')
        partition = kwargs.get('partition')
        type_ = kwargs.get('type')
        addresses = kwargs.get('addresses', [])
        ports = kwargs.get('ports', [])

        def teardown():
            SrcXlatHelper.delete_src_xlat(mgmt_root, name, partition)

        xlat = mgmt_root.tm.security.nat.source_translations.\
            source_translation.create(name=name, partition=partition,
                                      type=type_, addresses=addresses,
                                      ports=ports)
        request.addfinalizer(teardown)
        return xlat


class DstXlatHelper(object):
    @staticmethod
    def delete_dst_xlat(mgmt_root, name, partition):
        try:
            dst_xlat = mgmt_root.tm.security.nat.destination_translations.\
                destination_translation.load(name=name, partition=partition)
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            return
        dst_xlat.delete()

    @staticmethod
    def setup_basic_test(request, mgmt_root, **kwargs):
        name = kwargs.get('name')
        partition = kwargs.get('partition')
        type_ = kwargs.get('type')
        addresses = kwargs.get('addresses', [])
        ports = kwargs.get('ports', [])

        def teardown():
            DstXlatHelper.delete_dst_xlat(mgmt_root, name, partition)

        xlat = mgmt_root.tm.security.nat.destination_translations.\
            destination_translation.create(name=name, partition=partition,
                                           type=type_, addresses=addresses,
                                           ports=ports)
        request.addfinalizer(teardown)
        return xlat


@not_supported_prior_12_1_0
class XlatTemplate(object):
    """Base class for common Translation resource code.

    Contains tests common to both SourceTranslation and
    DestinationTranslation resources.
    """
    def test_create_no_args(self, mgmt_root):
        xlat = self.xlat_obj(mgmt_root)
        with pytest.raises(MissingRequiredCreationParameter):
            xlat.create()

    def test_create_missing_type(self, mgmt_root):
        xlat = self.xlat_obj(mgmt_root)
        with pytest.raises(MissingRequiredCreationParameter):
            xlat.create(name='xlat_notype', partition='Common')

    def test_create_snat_missing_addrs(self, mgmt_root):
        xlat = self.xlat_obj(mgmt_root)
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            xlat.create(name='xlat_snat', partition='Common',
                        type='static-nat')
        expected_msg = ('Security NAT translation object (/Common/'
                        'xlat_snat) is static NAT and requires '
                        'at least one address before it can be used.')
        assert expected_msg in str(excinfo.value)

    def test_create_spat_missing_ports(self, mgmt_root):
        xlat = self.xlat_obj(mgmt_root)
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            xlat.create(name='xlat_spat', partition='Common',
                        type='static-pat')
        expected_msg = ('Security NAT translation object (/Common/'
                        'xlat_spat) is static PAT and requires '
                        'at least one port before it can be used.')
        assert expected_msg in str(excinfo.value)

    def test_create_static_nat(self, request, mgmt_root):
        xlat = self.xlat_helper.setup_basic_test(
            request, mgmt_root, name='xlat_static_nat', partition='Common',
            type='static-nat', addresses=['1.1.1.1'])
        assert xlat.name == 'xlat_static_nat'
        assert xlat.type == 'static-nat'
        assert xlat.addresses == [{'name': '1.1.1.1'}]

    def test_create_static_pat(self, request, mgmt_root):
        xlat = self.xlat_helper.setup_basic_test(
            request, mgmt_root, name='xlat_static_pat', partition='Common',
            type='static-pat', ports=['1025-65535'])
        assert xlat.name == 'xlat_static_pat'
        assert xlat.type == 'static-pat'
        assert xlat.ports == [{'name': '1025-65535'}]

    def test_load(self, request, mgmt_root):
        name = 'xlat_load'
        partition = 'Common'
        self.xlat_helper.setup_basic_test(
            request, mgmt_root, name=name, partition=partition,
            type='static-nat', addresses=['1.1.1.2'])

        xlat_obj = self.xlat_obj(mgmt_root)
        xlat = xlat_obj.load(name=name, partition=partition)
        assert xlat.name == name
        assert xlat.type == 'static-nat'
        assert xlat.addresses == [{'name': '1.1.1.2'}]

    def test_delete(self, request, mgmt_root):
        name = 'xlat_del'
        partition = 'Common'
        self.xlat_helper.setup_basic_test(
            request, mgmt_root, name=name, partition=partition,
            type='static-pat', ports=['1025-65535'])
        xlat_obj = self.xlat_obj(mgmt_root)
        xlat = xlat_obj.load(name=name, partition=partition)
        resource_type = 'source' if 'source' in xlat.kind else 'destination'
        xlat.delete()
        del(xlat)
        with pytest.raises(HTTPError) as excinfo:
            xlat_obj = self.xlat_obj(mgmt_root)
            xlat_obj.load(name=name, partition=partition)

        expected_msg = 'The requested security nat {} translation (/{}/{}) ' \
                       'was not found'.format(resource_type, partition, name)
        assert expected_msg in str(excinfo.value)

    def test_stats(self, request, mgmt_root):
        xlat = self.xlat_helper.setup_basic_test(
            request, mgmt_root, name='xlat_stats', partition='Common',
            type='static-pat', addresses=['1.1.1.3'], ports=['1025-65535'])

        nops = 0
        time.sleep(0.1)
        while True:
            try:
                stats = Stats(xlat.stats.load())
                pool_nm = '/Common/xlat_stats'
                assert stats.stat['tmName']['description'] == pool_nm
                assert stats.stat['common_translationRequests']['value'] == 0
                break
            except Exception as e:
                # This can be caused by restjavad restarting.
                if nops == 3:
                    raise e
                else:
                    nops += 1
            time.sleep(1)


class TestDestinationTranslationCommon(XlatTemplate):
    def xlat_obj(self, mgmt_root):
        return mgmt_root.tm.security.nat.destination_translations.\
            destination_translation

    @property
    def xlat_helper(self):
        return DstXlatHelper


class TestSourceTranslationCommon(XlatTemplate):
    def xlat_obj(self, mgmt_root):
        return mgmt_root.tm.security.nat.source_translations.source_translation

    @property
    def xlat_helper(self):
        return SrcXlatHelper


@not_supported_prior_12_1_0
class TestDestinationTranslation(object):
    def test_collection(self, request, mgmt_root):
        DstXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat_dpat', partition='Common',
            type='static-pat', addresses=['3.1.1.0/24'], ports=['1025-65535'])
        xlat_col = mgmt_root.tm.security.nat. \
            destination_translations.get_collection()
        assert isinstance(xlat_col, list)
        assert len(xlat_col)
        assert isinstance(xlat_col[0], Destination_Translation)


@not_supported_prior_12_1_0
class TestSourceTranslation(object):
    """Tests unique to SourceTranslation resource

    e.g. only SourceTranslation resources support type 'dynamic-pat'.
    """
    def src_xlat_obj(self, mgmt_root):
        return mgmt_root.tm.security.nat.source_translations.source_translation

    def test_create_dpat_nat_missing_addrs(self, mgmt_root):
        src_xlat = self.src_xlat_obj(mgmt_root)
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            src_xlat.create(name='srcxlat_dpat', partition='Common',
                            type='dynamic-pat', ports=['1025-1234'])
        expected_msg = ('Security NAT translation object (/Common/'
                        'srcxlat_dpat) is dynamic PAT and requires '
                        'at least one address and port before it '
                        'can be used.')
        assert expected_msg in str(excinfo.value)

    def test_create_dpat_nat_missing_ports(self, mgmt_root):
        src_xlat = self.src_xlat_obj(mgmt_root)
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            src_xlat.create(name='srcxlat_dpat', partition='Common',
                            type='dynamic-pat', addresses=['2.1.1.1'])
        expected_msg = ('Security NAT translation object (/Common/'
                        'srcxlat_dpat) is dynamic PAT and requires '
                        'at least one address and port before it '
                        'can be used.')
        assert expected_msg in str(excinfo.value)

    def test_create_with_invalid_pat_mode(self, mgmt_root):
        src_xlat = self.src_xlat_obj(mgmt_root)
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            src_xlat.create(name='srcxlat_dpat', partition='Common',
                            type='dynamic-pat', addresses=['2.1.1.2'],
                            ports=['1025-1234'], patMode='invalidMode')

        expected_msg = ('invalid property value \\\\"pat-mode\\\\":\\\\"'
                        'invalidMode\\\\')
        assert expected_msg in str(excinfo.value)

    def test_create_pat_mode_requires_dpat(self, mgmt_root):
        src_xlat = self.src_xlat_obj(mgmt_root)
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            src_xlat.create(name='srcxlat_patmode', partition='Common',
                            type='static-nat', addresses=['2.1.1.3'],
                            ports=['1025-65535'], patMode='pba')
        expected_msg = ("Attribute \\\'pat_mode\\\' is not allowed "
                        "to be set on source translation object if "
                        "\\\'nat-type\\\' is other than \\\'dynamic-pat\\\'")
        assert expected_msg in str(excinfo.value)

    def test_create_dynamic_pat(self, request, mgmt_root):
        src_xlat = SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat_dpat', partition='Common',
            type='dynamic-pat', addresses=['2.2.1.0/24'], ports=['1025-65535'])
        assert src_xlat.name == 'srcxlat_dpat'
        assert src_xlat.type == 'dynamic-pat'
        assert src_xlat.patMode == 'napt'
        assert src_xlat.addresses == [{'name': '2.2.1.0/24'}]
        assert src_xlat.ports == [{'name': '1025-65535'}]

    def test_update_pat_mode(self, request, mgmt_root):
        src_xlat = SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat_update', partition='Common',
            type='dynamic-pat', addresses=['2.2.2.0/24', '2.2.3.0/24'],
            ports=['1025-65535'])
        assert src_xlat.name == 'srcxlat_update'
        assert src_xlat.type == 'dynamic-pat'
        assert src_xlat.patMode == 'napt'
        assert src_xlat.addresses == [{'name': '2.2.2.0/24'},
                                      {'name': '2.2.3.0/24'}]
        src_xlat.patMode = 'pba'
        src_xlat.update()
        assert src_xlat.patMode == "pba"
        src_xlat.patMode = "napt"
        src_xlat.refresh()
        assert src_xlat.patMode == "pba"

    def test_collection(self, request, mgmt_root):
        SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat_dpat', partition='Common',
            type='dynamic-pat', addresses=['2.2.4.0/24'], ports=['1025-65535'])
        xlat_col = mgmt_root.tm.security.nat.\
            source_translations.get_collection()
        assert isinstance(xlat_col, list)
        assert len(xlat_col)
        assert isinstance(xlat_col[0], Source_Translation)


@not_supported_prior_12_1_0
class TestPolicy(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.security.nat.policys.policy.create()

    def test_create_req_args(self, request, mgmt_root):
        name = 'pol_req_args'
        partition = 'Common'
        pol = PolicyHelper.setup_basic_test(
            request, mgmt_root, name, partition)

        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~{}~{}'.format(partition, name)
        assert pol.name == name
        assert pol.partition == partition
        assert pol.selfLink.startswith(URI)
        assert not hasattr(pol, 'description')
        assert pol.rules_s.get_collection() == []

    def test_add_rules_subcollection(self, request, mgmt_root):
        pol = PolicyHelper.setup_basic_test(request, mgmt_root,
                                            'natpolicy', 'Common')
        assert pol.rules_s.get_collection() == []
        params = {'name': 'natrule', 'place-before': 'first'}
        pol.rules_s.rules.create(**params)

        assert pol.rules_s.rules.exists(name='natrule')

        rule_col = pol.rules_s.get_collection()

        assert isinstance(rule_col, list)
        assert len(rule_col) == 1
        assert isinstance(rule_col[0], Rules)
        assert rule_col[0].name == 'natrule'

    def test_policy_rules_load(self, request, mgmt_root):
        pol = PolicyHelper.setup_basic_test(request, mgmt_root,
                                            'natpolicy', 'Common')

        params = {'name': 'natrule', 'place-before': 'first'}
        pol.rules_s.rules.create(**params)

        rule = pol.rules_s.rules.load(name='natrule')
        rule_col = pol.rules_s.get_collection()
        assert rule_col[0].name == rule.name

    def test_add_rules_subcollection_order(self, request, mgmt_root):
        pol = PolicyHelper.setup_basic_test(request, mgmt_root,
                                            'natpolicy', 'Common')
        assert pol.rules_s.get_collection() == []
        param_list = [{'name': 'rule_first', 'place-before': 'first'},
                      {'name': 'rule_mid', 'place-after': 'first'},
                      {'name': 'rule_last', 'place-after': 'last'}]
        for params in param_list:
            pol.rules_s.rules.create(**params)

        rule_col = pol.rules_s.get_collection()

        assert isinstance(rule_col, list)
        assert len(rule_col) == len(param_list)
        assert isinstance(rule_col[0], Rules)
        assert rule_col[0].name == 'rule_first'
        assert rule_col[-1].name == 'rule_last'

    def test_policy_create_invalid_args(self, request, mgmt_root):
        pol = PolicyHelper.setup_basic_test(request, mgmt_root,
                                            'natpolicy', 'Common')
        assert pol.rules_s.get_collection() == []
        params = {'name': 'invalid',
                  'place-before': 'first',
                  'place-after': 'last'}
        with pytest.raises(ExclusiveAttributesPresent):
            pol.rules_s.rules.create(**params)

    def test_policy_update_invalid_args(self, request, mgmt_root):
        pol = PolicyHelper.setup_basic_test(request, mgmt_root,
                                            'natpolicy', 'Common')
        assert pol.rules_s.get_collection() == []
        params = {'name': 'invalid',
                  'place-before': 'first'}
        pol.rules_s.rules.create(**params)
        params.update({'place-after': 'last'})
        with pytest.raises(ExclusiveAttributesPresent):
            pol.rules_s.rules.update(**params)

    def test_policy_modify_invalid_args(self, request, mgmt_root):
        pol = PolicyHelper.setup_basic_test(request, mgmt_root,
                                            'natpolicy', 'Common')
        assert pol.rules_s.get_collection() == []
        params = {'name': 'invalid',
                  'place-before': 'first'}
        pol.rules_s.rules.create(**params)
        params.update({'place-after': 'last'})
        with pytest.raises(ExclusiveAttributesPresent):
            pol.rules_s.rules.modify(**params)

    def test_create_policy_add_xlats(self, request, mgmt_root):
        partition = 'Common'
        src_xlat = SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat', partition=partition,
            type='static-pat', addresses=['4.1.1.0/24'], ports=['1025-65535'])

        dst_xlat = DstXlatHelper.setup_basic_test(
            request, mgmt_root, name='dstxlat', partition=partition,
            type='static-pat', addresses=['4.2.1.0/24'], ports=['1025-65535'])

        pol = PolicyHelper.setup_basic_test(
            request, mgmt_root, 'natpolicy', partition)

        params = {'name': 'natrule', 'place-before': 'first',
                  'source': {'addresses': ['4.3.1.0/24']},
                  'translation': {'source': src_xlat.name,
                                  'destination': dst_xlat.name}}
        pol.rules_s.rules.create(**params)

        rule_col = pol.rules_s.get_collection()
        src_xlat_full_name = "/{}/{}".format(partition, src_xlat.name)
        dst_xlat_full_name = "/{}/{}".format(partition, dst_xlat.name)
        assert rule_col[0].translation['source'] == src_xlat_full_name
        assert rule_col[0].translation['destination'] == dst_xlat_full_name
        assert rule_col[0].source['addresses'] == [{'name': '4.3.1.0/24'}]

    def test_update_policy_add_xlats(self, request, mgmt_root):
        partition = 'Common'
        src_xlat = SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat', partition=partition,
            type='static-pat', addresses=['5.1.1.0/24'], ports=['1025-65535'])

        pol = PolicyHelper.setup_basic_test(
            request, mgmt_root, 'natpolicy', partition)

        params = {'name': 'natrule', 'place-before': 'first',
                  'source': {'addresses': ['5.2.1.0/24']}}
        pol.rules_s.rules.create(**params)

        rule = pol.rules_s.rules.load(name='natrule')
        rule.update(source={'addresses': ['5.3.1.0/24']},
                    translation={'source': src_xlat.name})

        rule_col = pol.rules_s.get_collection()
        src_xlat_full_name = "/{}/{}".format(partition, src_xlat.name)
        assert rule_col[0].translation['source'] == src_xlat_full_name
        assert rule_col[0].source['addresses'] == [{'name': '5.3.1.0/24'}]

    def test_modify_policy_add_xlats(self, request, mgmt_root):
        partition = 'Common'
        src_xlat = SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat', partition=partition,
            type='static-pat', addresses=['6.1.1.0/24'], ports=['1025-65535'])

        pol = PolicyHelper.setup_basic_test(
            request, mgmt_root, 'natpolicy', partition)

        params = {'name': 'natrule', 'place-before': 'first',
                  'source': {'addresses': ['6.2.1.0/24']}}
        pol.rules_s.rules.create(**params)

        rule = pol.rules_s.rules.load(name='natrule')
        rule.modify(source={'addresses': ['6.3.1.0/24']},
                    translation={'source': src_xlat.name})

        rule_col = pol.rules_s.get_collection()
        src_xlat_full_name = "/{}/{}".format(partition, src_xlat.name)
        assert rule_col[0].translation['source'] == src_xlat_full_name
        assert rule_col[0].source['addresses'] == [{'name': '6.3.1.0/24'}]

    def test_load(self, request, mgmt_root):
        name = 'pol_load'
        partition = 'Common'
        PolicyHelper.setup_basic_test(request, mgmt_root, name, partition)
        pol = mgmt_root.tm.security.nat.policys.policy.load(
            name=name, partition=partition)
        params = {'name': 'natrule', 'place-before': 'first'}
        pol.rules_s.rules.create(**params)
        pol = mgmt_root.tm.security.nat.policys.policy.load(
            name=name, partition=partition)
        assert pol.name == name
        rule_col = pol.rules_s.get_collection()

        assert isinstance(rule_col, list)
        assert len(rule_col) == 1
        assert isinstance(rule_col[0], Rules)
        assert rule_col[0].name == 'natrule'

    def test_delete(self, request, mgmt_root):
        name = 'pol_del'
        partition = 'Common'
        PolicyHelper.setup_basic_test(request, mgmt_root, name, partition)
        pol = mgmt_root.tm.security.nat.policys.policy.load(
            name=name, partition=partition)

        pol.delete()
        del(pol)
        with pytest.raises(HTTPError) as excinfo:
            mgmt_root.tm.security.nat.policys.policy.load(
                name=name, partition=partition)

        expected_msg = 'The requested security nat policy ' \
                       '(/{}/{}) was not found'.format(partition, name)
        assert expected_msg in str(excinfo.value)

    def test_add_policy_to_virtual(self, request, mgmt_root, virtual_setup):
        src_xlat = SrcXlatHelper.setup_basic_test(
            request, mgmt_root, name='srcxlat', partition='Common',
            type='dynamic-pat', addresses=['7.1.1.0/24'], ports=['1025-65535'],
            patMode='pba')

        pol = PolicyHelper.setup_basic_test(
            request, mgmt_root, 'natpolicy', 'Common')

        params = {'name': 'natrule', 'place-before': 'first',
                  'source': {'addresses': ['7.2.1.0/24']},
                  'translation': {'source': src_xlat.name}}
        pol.rules_s.rules.create(**params)

        try:
            virtual_setup.modify(securityNatPolicy={"policy": pol.name})
            assert virtual_setup.securityNatPolicy["policy"].endswith(pol.name)

        finally:
            virtual_setup.modify(securityNatPolicy={"policy": None})
