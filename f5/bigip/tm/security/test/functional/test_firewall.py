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

import pytest

from distutils.version import LooseVersion
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.security.firewall import Address_List
from f5.bigip.tm.security.firewall import Policy
from f5.bigip.tm.security.firewall import Port_List
from f5.bigip.tm.security.firewall import Rule
from f5.bigip.tm.security.firewall import Rule_List
from f5.sdk_exception import ExclusiveAttributesPresent
from f5.sdk_exception import NonExtantFirewallRule
from requests.exceptions import HTTPError


DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def addrlst(mgmt_root):
    r1 = mgmt_root.tm.security.firewall.address_lists.address_list.create(
        name='fake_addr', partition='Common', addresses=[{
            'name': '10.10.10.10'}])
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def portlst(mgmt_root):
    r1 = mgmt_root.tm.security.firewall.port_lists.port_list.create(
        name='fake_port', partition='Common', ports=[{'name': '80'}])
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def rulelst(mgmt_root):
    r1 = mgmt_root.tm.security.firewall.rule_lists.rule_list.create(
        name='fake_rule_list', partition='Common')
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def policy(mgmt_root):
    p1 = mgmt_root.tm.security.firewall.policy_s.policy.create(
        name='fake_policy', partition='Common')
    yield p1
    p1.delete()


@pytest.fixture(scope='function')
def rule(policy):
    param_set = {'name': 'fake_rule', 'place-after': 'first',
                 'action': 'reject'}
    r1 = policy.rules_s.rule.create(**param_set)
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def dsnresolver(mgmt_root):
    d1 = mgmt_root.tm.net.dns_resolvers.dns_resolver.create(
        name='fake_dnsresolver', partition='Common')
    yield d1
    d1.delete()


class TestAddressList(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        ac = mgmt_root.tm.security.firewall.address_lists
        with pytest.raises(MissingRequiredCreationParameter) as err:
            ac.address_list.create(name='fail', partition='Common')

        if LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'):
            error = "This resource requires at least one of the mandatory additional parameters to be provided: addressLists, addresses, geo"
            assert str(err.value) == error
        else:
            error = "This resource requires at least one of the mandatory additional parameters to be provided: addressLists, addresses, fqdns, geo"
            assert str(err.value) == error

    def test_create_req_args(self, addrlst):
        r1 = addrlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.firewall.address_lists.address_list.create(
            name='fake_addr', partition='Common', addresses=[{
                'name': '10.10.10.10'}], description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, addrlst):
        rc = mgmt_root.tm.security.firewall.address_lists
        r1 = addrlst
        r2 = rc.address_list.load(name='fake_addr', partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.address_lists
        r1 = rc.address_list.create(name='delete_me', partition='Common',
                                    addresses=[{'name': '10.10.10.10'}])
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.address_list.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.address_lists
        with pytest.raises(HTTPError) as err:
            rc.address_list.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, addrlst):
        r1 = addrlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.firewall.address_lists
        r2 = rc.address_list.load(name='fake_addr', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_addrlst_collection(self, mgmt_root, addrlst):
        r1 = addrlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.firewall.address_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Address_List)


class TestPortList(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        ac = mgmt_root.tm.security.firewall.port_lists
        error_message = "This resource requires at least one of the mandatory additional parameters to be provided: portLists, ports"

        with pytest.raises(MissingRequiredCreationParameter) as err:
            ac.port_list.create(name='fail', partition='Common')
        assert str(err.value) == error_message

    def test_create_req_args(self, portlst):
        r1 = portlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.firewall.port_lists.port_list.create(
            name='fake_port', partition='Common', ports=[{
                'name': '80'}], description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, portlst):
        rc = mgmt_root.tm.security.firewall.port_lists
        r1 = portlst
        r2 = rc.port_list.load(name='fake_port', partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists
        r1 = rc.port_list.create(name='delete_me', partition='Common',
                                 ports=[{'name': '80'}])
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.port_list.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists
        with pytest.raises(HTTPError) as err:
            rc.port_list.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, portlst):
        r1 = portlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.firewall.port_lists
        r2 = rc.port_list.load(name='fake_port', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_portlist_collection(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Port_List)


class TestRuleList(object):
    def test_create_req_args(self, rulelst):
        r1 = rulelst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/rule-list/~Common~fake_rule_list'
        assert r1.name == 'fake_rule_list'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.firewall.rule_lists.rule_list.create(
            name='fake_rule_list', partition='Common', description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/rule-list/~Common~fake_rule_list'
        assert r1.name == 'fake_rule_list'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, rulelst):
        rc = mgmt_root.tm.security.firewall.rule_lists
        r1 = rulelst
        r2 = rc.rule_list.load(name='fake_rule_list', partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.rule_lists
        r1 = rc.rule_list.create(name='delete_me', partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.rule_list.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.rule_lists
        with pytest.raises(HTTPError) as err:
            rc.rule_list.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, rulelst):
        r1 = rulelst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/rule-list/~Common~fake_rule_list'
        assert r1.name == 'fake_rule_list'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.firewall.rule_lists
        r2 = rc.rule_list.load(name='fake_rule_list', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_portlist_collection(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.rule_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Rule_List)


class TestRules(object):
    def test_mutually_exclusive_raises(self, policy):
        param_set = {'name': 'fake_rule', 'place-after': 'first',
                     'action': 'reject', 'place-before': 'last'}
        ERR = 'Mutually exclusive arguments submitted. The following arguments cannot be set together: "place-after, place-before".'
        with pytest.raises(ExclusiveAttributesPresent) as err:
            policy.rules_s.rule.create(**param_set)
        assert str(err.value) == ERR

    def test_mandatory_attribute_missing(self, policy):
        param_set = {'name': 'fake_rule', 'action': 'reject'}
        ERR = "This resource requires at least one of the mandatory additional parameters to be provided: place-after, place-before"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            policy.rules_s.rule.create(**param_set)
        assert str(err.value) == ERR

    def test_create_req_arg(self, rule):
        r1 = rule
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_optional_args(self, policy):
        param_set = {'name': 'fake_rule', 'place-after': 'first',
                     'action': 'reject', 'description': DESC}
        r1 = policy.rules_s.rule.create(**param_set)
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC

    def test_refresh(self, policy, rule):
        r1 = rule
        r2 = policy.rules_s.rule.load(name='fake_rule')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.kind == r2.kind
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert r1.selfLink == r2.selfLink
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()
        assert r1.description == r2.description

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_delete(self, policy):
        param_set = {'name': 'delete_me', 'place-after': 'first',
                     'action': 'reject'}
        r1 = policy.rules_s.rule.create(**param_set)
        r1.delete()
        with pytest.raises(HTTPError) as err:
            policy.rules_s.rule.load(name='delete_me')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.rules_s.rule.load(name='not_exist')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_delete_11_6_0(self, policy):
        param_set = {'name': 'delete_me', 'place-after': 'first',
                     'action': 'reject'}
        r1 = policy.rules_s.rule.create(**param_set)
        r1.delete()
        try:
            policy.rules_s.rule.load(name='delete_me')

        except NonExtantFirewallRule as err:
            msg = 'The application resource named, delete_me, ' \
                  'does not exist on the device.'

            assert err.message == msg

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_load_no_object_11_6_0(self, policy):
        try:
            policy.rules_s.rule.load(name='not_exist')

        except NonExtantFirewallRule as err:
            msg = 'The application resource named, not_exist, ' \
                  'does not exist on the device.'

            assert err.message == msg

    def test_load_and_update(self, policy, rule):
        r1 = rule
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r2 = policy.rules_s.rule.load(name='fake_rule')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_rules_subcollection(self, policy, rule):
        r1 = rule
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

        rc = policy.rules_s.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Rule)


class TestPolicy(object):
    def test_create_req_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.firewall.policy_s.policy.create(
            name='fake_policy', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.delete()

    def test_refresh(self, mgmt_root, policy):
        p1 = policy
        p2 = mgmt_root.tm.security.firewall.policy_s.policy.load(
            name='fake_policy', partition='Common')
        assert p1.name == p2.name
        assert p1.kind == p2.kind
        assert p1.selfLink == p2.selfLink
        assert not hasattr(p1, 'description')
        assert not hasattr(p2, 'description')
        p2.modify(description=DESC)
        p1.modify(description=DESC)
        assert hasattr(p2, 'description')
        assert p2.description == DESC
        p1.refresh()
        assert p1.selfLink == p2.selfLink
        assert hasattr(p1, 'description')
        assert p1.description == p2.description

    def test_delete(self, mgmt_root):
        p = mgmt_root.tm.security.firewall.policy_s.policy
        p1 = p.create(name='delete_me', partition='Common')
        p1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.firewall.policy_s.policy.load(
                name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p = mgmt_root.tm.security.firewall.policy_s.policy
        with pytest.raises(HTTPError) as err:
            p.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, policy):
        p1 = policy
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.description = DESC
        p1.update()
        assert hasattr(p1, 'description')
        assert p1.description == DESC
        p = mgmt_root.tm.security.firewall.policy_s.policy
        p2 = p.load(name='fake_policy', partition='Common')
        assert p1.name == p2.name
        assert p1.partition == p2.partition
        assert p1.selfLink == p2.selfLink
        assert hasattr(p2, 'description')
        assert p1.description == p2.description

    def test_policies_collection(self, mgmt_root, policy):
        pc = mgmt_root.tm.security.firewall.policy_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Policy)


class TestGlobalRules(object):
    def test_modify_req_args(self, mgmt_root, policy):
        rules = mgmt_root.tm.security.firewall. \
            global_rules.load(partition='Common')
        assert "enforcedPolicy" not in rules.__dict__
        rules.modify(enforcedPolicy='fake_policy', partition='Common')
        assert rules.enforcedPolicy == "/Common/fake_policy"
        rules.modify(enforcedPolicy='none', partition='Common')
        assert "enforcedPolicy" not in rules.__dict__


@pytest.mark.skipif(
    pytest.config.getoption('--release') < '12.0.0',
    reason='This test will only work from version 12.0.X i.e Cascade.'
    )
class TestGlobalFqdnPolicy(object):
    def test_modify_req_args(self, mgmt_root, dsnresolver):
        policy = mgmt_root.tm.security.firewall.global_fqdn_policy.load(partition='Common')
        assert "dnsResolver" not in policy.__dict__
        policy.modify(dnsResolver='fake_dnsresolver', partition='Common')
        assert policy.dnsResolver == "/Common/fake_dnsresolver"
        policy.modify(dnsResolver='none', partition='Common')
        assert "dnsResolver" not in policy.__dict__
