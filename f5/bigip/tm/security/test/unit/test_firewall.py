# Copyright 2017 F5 Networks Inc.
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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.security.firewall import Address_List
from f5.bigip.tm.security.firewall import Policy
from f5.bigip.tm.security.firewall import Port_List
from f5.bigip.tm.security.firewall import Rule
from f5.bigip.tm.security.firewall import Rule_List
from f5.bigip.tm.security.firewall import Rules_s
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeAddrLst():
    fake_col = mock.MagicMock()
    fake_col._meta_data['bigip'].tmos_version = '11.6.0'
    fake_addrlst = Address_List(fake_col)
    return fake_addrlst


@pytest.fixture
def FakePortLst():
    fake_col = mock.MagicMock()
    fake_portlst = Port_List(fake_col)
    return fake_portlst


@pytest.fixture
def FakeRuleLst():
    fake_col = mock.MagicMock()
    fake_rulelst = Rule_List(fake_col)
    return fake_rulelst


@pytest.fixture
def FakePolicy():
    fake_col = mock.MagicMock()
    fake_policy = Policy(fake_col)
    return fake_policy


def Makerulelist(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.firewall.rule_lists.rule_list
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/firewall/rule-list/~Common' \
        '~testrulelst/'
    return p


def MakePolicyRules(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.firewall.policy_s.policy
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/firewall/policy/' \
        '~Common~fakepolicy/'
    return p


def MakeGlobalRules(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.firewall.global_rules
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/firewall/global_rules/'
    return p


def MakeGlobalFqdnPolicy(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.firewall.global_fqdn_policy
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/firewall/global-fqdn-policy/'
    return p


class TestAddressList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.address_lists.address_list
        r2 = b.tm.security.firewall.address_lists.address_list
        assert r1 is not r2

    def test_create_no_args(self, FakeAddrLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeAddrLst.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.firewall.address_lists.address_list.create(
                name='destined_to_fail', partition='Fake')


class TestPortList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.port_lists.port_list
        r2 = b.tm.security.firewall.port_lists.port_list
        assert r1 is not r2

    def test_create_no_args(self, FakePortLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePortLst.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.firewall.port_lists.port_list.create(
                name='destined_to_fail', partition='Fake')


class TestRuleList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.rule_lists.rule_list
        r2 = b.tm.security.firewall.rule_lists.rule_list
        assert r1 is not r2

    def test_create_no_args(self, FakeRuleLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRuleLst.create()


class TestRulesSubcollection(object):
    def test_rule_subcollection(self, fakeicontrolsession):
        pc = Rules_s(Makerulelist(fakeicontrolsession))
        kind = 'tm:security:firewall:policy:rules:rulesstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Rules_s)
        assert kind in list(iterkeys(test_meta))
        assert Rule in test_meta2

    def test_app_create(self, fakeicontrolsession):
        pc = Rules_s(Makerulelist(fakeicontrolsession))
        pc2 = Rules_s(Makerulelist(fakeicontrolsession))
        r1 = pc.rule
        r2 = pc2.rule
        assert r1 is not r2

    def test_app_create_no_args_v11(self, fakeicontrolsession):
        pc = Rules_s(Makerulelist(fakeicontrolsession))
        with pytest.raises(MissingRequiredCreationParameter):
            pc.rule.create()


class TestPolicy(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.policy_s.policy
        r2 = b.tm.security.firewall.policy_s.policy
        assert r1 is not r2

    def test_create_no_args(self, FakePolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePolicy.create()


class TestPolicyRuleSubCollection(object):
    def test_policy_rule_subcollection(self, fakeicontrolsession):
        pc = Rules_s(MakePolicyRules(fakeicontrolsession))
        kind = 'tm:security:firewall:policy:rules:rulesstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Rules_s)
        assert kind in list(iterkeys(test_meta))
        assert Rule in test_meta2


class TestGlobalRules(object):
    def test_global_rules(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        kind = "tm:security:firewall:global-rules:global-rulesstate"
        rules = b.tm.security.firewall.global_rules
        rules_kind = rules._meta_data["required_json_kind"]
        assert rules_kind == kind


class TestGlobalFqdnPolicy(object):
    def test_global_fqdn_policy(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '12.0.0'
        kind = "tm:security:firewall:global-fqdn-policy:global-fqdn-policystate"
        policy = b.tm.security.firewall.global_fqdn_policy
        policy_kind = policy._meta_data["required_json_kind"]
        assert policy_kind == kind
