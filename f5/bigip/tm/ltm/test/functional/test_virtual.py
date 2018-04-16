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
from f5.bigip.tm.ltm.virtual import Policies
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import MissingRequiredReadParameter
from six import iteritems

import copy
import pytest

TESTDESCRIPTION = "TESTDESCRIPTION"


@pytest.fixture
def basic_rule(mgmt_root):
    rule1 = mgmt_root.tm.ltm.rules.rule.create(
        name='foo',
        partition='Common',
        apiAnonymous=''
    )
    yield rule1
    rule1.delete()


@pytest.fixture
def basic_vlan(mgmt_root):
    vlan1 = mgmt_root.tm.net.vlans.vlan.create(
        name='testvlan',
        partition='Common'
    )
    yield vlan1
    vlan1.delete()


@pytest.fixture
def virtual_setup(mgmt_root):
    vs_kwargs = {'name': 'vs', 'partition': 'Common'}
    vs = mgmt_root.tm.ltm.virtuals.virtual
    v1 = vs.create(profiles=['/Common/http'], **vs_kwargs)
    yield v1
    v1.delete()


@pytest.fixture
def policy_setup(request, mgmt_root):
    pol = mgmt_root.tm.ltm.policys.policy
    pol_create_kwargs = {
        'name': 'pol', 'partition': 'Common', 'legacy': True,
        'strategy': 'all-match'
    }
    pol_read_kwargs = {'name': 'pol', 'partition': 'Common'}
    vs_kwargs = {'name': 'vs', 'partition': 'Common'}

    def teardown():
        vs = mgmt_root.tm.ltm.virtuals.virtual
        if vs.exists(**vs_kwargs):
            v1 = vs.load(**vs_kwargs)
            if v1.policies_s.policies.exists(**pol_read_kwargs):
                vs_pol = v1.policies_s.policies.load(**pol_read_kwargs)
                vs_pol.delete()
        if pol.exists(**pol_read_kwargs):
            test_pol = pol.load(**pol_read_kwargs)
            test_pol.delete()
    teardown()
    p1 = pol.create(**pol_create_kwargs)
    rule = p1.rules_s.rules.create(name='test_rule', partition='Common')
    request.addfinalizer(teardown)
    return p1, rule


def setup_virtual_test(request, mgmt_root, partition, name):
    def teardown():
        def teardown():
            vs = mgmt_root.tm.ltm.virtuals.virtual
            if vs.exists(name=name, partition=partition):
                v1 = vs.load(name=name, partition=partition)
                v1.delete()

        teardown()
    request.addfinalizer(teardown)
    vc1 = mgmt_root.tm.ltm.virtuals
    virtual1 = vc1.virtual.create(name=name, partition=partition)
    return virtual1, vc1


class TestVirtual(object):
    def test_virtual_create_refresh_update_delete_load(
            self, request, mgmt_root):
        virtual1, vc1 = setup_virtual_test(
            request, mgmt_root, 'Common', 'vstest1'
        )
        assert virtual1.name == 'vstest1'
        virtual1.description = TESTDESCRIPTION
        virtual1.update()
        assert virtual1.description == TESTDESCRIPTION
        virtual1.description = ''
        virtual1.refresh()
        assert virtual1.description == TESTDESCRIPTION
        virtual2 = vc1.virtual.load(partition='Common', name='vstest1')
        assert virtual2.selfLink == virtual1.selfLink

    def test_virtual_modify(self, request, mgmt_root):
        virtual1, vc1 = setup_virtual_test(
            request, mgmt_root, 'Common', 'modtest1'
        )
        original_dict = copy.copy(virtual1.__dict__)
        desc = 'description'
        virtual1.modify(description='Cool mod test')
        for k, v in iteritems(original_dict):
            if k != desc:
                original_dict[k] = virtual1.__dict__[k]
            elif k == desc:
                assert virtual1.__dict__[k] == 'Cool mod test'

    def test_virtual_no_rules(self, virtual_setup, basic_rule):
        assert len(virtual_setup.rules) == 0

    def test_virtual_state_toggle(self, virtual_setup):
        virtual_setup.disabled = True
        virtual_setup.update()
        assert hasattr(virtual_setup, 'disabled')
        assert not hasattr(virtual_setup, 'enabled')

        virtual_setup.enabled = True
        virtual_setup.update()
        assert hasattr(virtual_setup, 'enabled')
        assert not hasattr(virtual_setup, 'disabled')

    def test_virtual_vlan_toggle(self, virtual_setup, basic_vlan):
        virtual_setup.vlansEnabled = True
        virtual_setup.update()
        assert hasattr(virtual_setup, 'vlansEnabled')
        assert not hasattr(virtual_setup, 'vlansDisabled')
        assert not hasattr(virtual_setup, 'vlans')

        virtual_setup.vlans = ['/Common/testvlan']
        virtual_setup.update()
        assert hasattr(virtual_setup, 'vlans')

        virtual_setup.vlansDisabled = True
        virtual_setup.vlans = []
        virtual_setup.update()
        assert hasattr(virtual_setup, 'vlansDisabled')
        assert not hasattr(virtual_setup, 'vlansEnabled')
        assert not hasattr(virtual_setup, 'vlans')

    def test_virtual_modify2(self, virtual_setup, basic_rule):
        virtual_setup.modify(rules=[basic_rule.name])
        virtual_setup.refresh()
        assert len(virtual_setup.rules) == 1
        virtual_setup.modify(rules=[])
        assert len(virtual_setup.rules) == 0

    def test_virtual_update(self, virtual_setup, basic_rule):
        virtual_setup.update(rules=[basic_rule.name])
        virtual_setup.refresh()
        assert len(virtual_setup.rules) == 1
        virtual_setup.update(rules=[])
        assert len(virtual_setup.rules) == 0


class TestProfiles(object):
    def test_profiles_CE(self, request, mgmt_root):
        v1, _ = setup_virtual_test(request, mgmt_root, 'Common', 'tv1')
        p1 = v1.profiles_s.profiles.create(name="http", partition='Common')
        test_profiles_s = v1.profiles_s
        test_profiles_s.context = 'all'
        assert '~Common~tv1/profiles/' in p1.selfLink
        assert 'http?ver=' in p1.selfLink

        p2 = v1.profiles_s.profiles
        assert p2.exists(name='http', partition='Common')

    def test_profiles_CE_check_create_params(self, request, mgmt_root):
        v1, _ = setup_virtual_test(request, mgmt_root, 'Common', 'tv2')
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            v1.profiles_s.profiles.create(name="http")
        assert "Missing required params: ['partition']" in ex.value.message

    def test_profiles_CE_check_load_params(self, request, mgmt_root):
        v1, _ = setup_virtual_test(request, mgmt_root, 'Common', 'tv3')
        p1 = v1.profiles_s.profiles.create(name="http", partition="Common")

        with pytest.raises(MissingRequiredReadParameter) as ex:
            assert v1.profiles_s.profiles.load(name='http')
        assert "Missing required params: ['partition']" in ex.value.message

        v1.profiles_s.profiles.load(name="http", partition="Common")

        # Check for existence with partition given
        p1.exists(name='http', partition='Common')

    def test_profiles_known_invalid(self, request, mgmt_root):
        v1, _ = setup_virtual_test(request, mgmt_root, 'Common', 'tv1')
        p1 = v1.profiles_s.profiles.exists(name="asdasdasd", partition='Common')
        assert p1 is False


class TestPolicies(object):
    def test_policies(self, policy_setup, virtual_setup):
        pol, pc = policy_setup
        v1 = virtual_setup
        vs_pol = v1.policies_s.policies.create(name='pol', partition='Common')
        loaded_pol = v1.policies_s.policies.load(name='pol',
                                                 partition='Common')
        assert vs_pol.name == pol.name == loaded_pol.name
        pc = list(v1.policies_s.get_collection())
        assert len(pc) == 1
        vs_pol.delete()
        v1.refresh()
        # Bump to check the below call
        assert v1.policies_s.policies.exists(name='pol',
                                             partition='Common') is False

    def test_policies_no_partition(self, virtual_setup):
        v1 = virtual_setup
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            v1.profiles_s.profiles.create(name='test_policy')
        assert "Missing required params: ['partition']" == ex.value.message

    def test_policies_missing_policy(self, virtual_setup):
        v1 = virtual_setup
        with pytest.raises(Exception) as ex:
            v1.profiles_s.profiles.create(name='bad_pol', partition='Common')
        assert 'The requested profile (/Common/bad_pol) was not found' in \
            ex.value.message

    def test_policies_load_missing_policy(self, virtual_setup):
        v1 = virtual_setup
        with pytest.raises(Exception) as ex:
            v1.policies_s.policies.load(name='bad_pol', partition='Common')
        assert 'The Policy named, bad_pol, does not exist on the device.' == \
            ex.value.message

    def test_collection(self, virtual_setup, policy_setup):
        _, _ = policy_setup
        v1 = virtual_setup
        vs_pol = v1.policies_s.policies.create(name='pol', partition='Common')
        assert vs_pol.name == 'pol'
        assert vs_pol.kind == 'tm:ltm:virtual:policies:policiesstate'
        pclst = v1.policies_s.get_collection()
        assert len(pclst) > 0
        assert isinstance(pclst[0], Policies)


class TestVirtualsStats(object):
    def test_get_virtuals_stats(self, request, mgmt_root, opt_release):
        setup_virtual_test(request, mgmt_root, 'Common', 'tv1')
        vs_stats = mgmt_root.tm.ltm.virtuals.stats.load()
        assert 'https://localhost/mgmt/tm/ltm/virtual/' +\
            '~Common~tv1/stats' in vs_stats.entries
        vs_nested_stats = vs_stats.entries['https://localhost/mgmt/tm/' +\
            'ltm/virtual/~Common~tv1/stats']['nestedStats']
        assert vs_nested_stats['selfLink'] == 'https://localhost/mgmt/tm/' +\
            'ltm/virtual/~Common~tv1/stats?ver=' + opt_release
        entries = vs_nested_stats['entries']
        assert entries['tmName']['description'] == '/Common/tv1'
        assert entries['status.enabledState']['description'] == 'enabled'
