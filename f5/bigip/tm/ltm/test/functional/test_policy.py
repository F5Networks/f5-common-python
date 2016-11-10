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

import copy
from distutils.version import LooseVersion
import json
import os
from pprint import pprint as pp
import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.ltm.policy import NonExtantPolicyRule
from f5.bigip.tm.ltm.policy import OperationNotSupportedOnPublishedPolicy

pp('')
TESTDESCRIPTION = "TESTDESCRIPTION"
CURDIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def setup(request, setup_device_snapshot):
    return setup_device_snapshot


def setup_policy_test(request, mgmt_root, partition, name,
                      strategy="first-match", **kwargs):
    def teardown_policy():
        kw = copy.deepcopy(kwargs)
        kw.pop('legacy', None)
        kw.pop('publish', None)
        if mgmt_root.tm.ltm.policys.policy.exists(
                name=name, partition=partition, **kw):
            pol = mgmt_root.tm.ltm.policys.policy.load(
                name=name, partition=partition, **kw)
            pol.delete()
        # Try to delete published draft if exists as well
        kw.pop('subPath', None)
        if mgmt_root.tm.ltm.policys.policy.exists(
                name=name, partition=partition, **kw):
            pol = mgmt_root.tm.ltm.policys.policy.load(
                name=name, partition=partition, **kw)
            pol.delete()

    pc1 = mgmt_root.tm.ltm.policys
    policy1 = pc1.policy.create(
        name=name, partition=partition, strategy=strategy, **kwargs)
    request.addfinalizer(teardown_policy)
    return policy1, pc1


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) > LooseVersion('12.0.0'),
    reason='Policies Changed in 12.1 to require workflows.'
)
class TestPolicy_legacy(object):
    def test_policy_create_refresh_update_delete_load(self, setup, request,
                                                      mgmt_root):
        policy1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                         'poltest1')
        assert policy1.name == 'poltest1'
        policy1.strategy = '/Common/all-match'
        policy1.update()
        assert policy1.strategy == '/Common/all-match'
        policy1.strategy = '/Common/first-match'
        policy1.refresh()
        assert policy1.strategy == '/Common/all-match'
        policy2 = pc1.policy.load(partition='Common', name='poltest1')
        assert policy2.selfLink == policy1.selfLink
        p2rc = policy2.rules_s
        p2rc.refresh()
        assert p2rc._meta_data['required_json_kind'] == p2rc.kind
        assert p2rc.get_collection() == []
        policy1.modify(strategy='/Common/first-match')
        assert policy2.strategy == '/Common/all-match'
        assert policy1.strategy != policy2.strategy
        policy2.refresh()
        assert policy1.strategy == policy2.strategy

    def test_rules_actions_refresh_update_load(self,
                                               setup, request, mgmt_root):
        rulespc = mgmt_root.tm.ltm.policys
        test_pol1 = rulespc.policy.load(partition='Common',
                                        name='_sys_CEC_video_policy')
        rules_s1 = test_pol1.rules_s
        rules1 = rules_s1.rules.load(name='cnn_web_1')
        r1actions = rules1.actions_s.actions.load(name="1")
        assert r1actions.kind == r1actions._meta_data['required_json_kind']

    def test_rules_conditions_refresh_update_load(self,
                                                  setup, request, mgmt_root):
        rulespc = mgmt_root.tm.ltm.policys
        test_pol1 = rulespc.policy.load(partition='Common',
                                        name='_sys_CEC_video_policy')
        rules_s1 = test_pol1.rules_s
        rules1 = rules_s1.rules.load(name='cnn_web_1')
        r1conditions = rules1.conditions_s.conditions.load(name="1")
        assert r1conditions.kind == r1conditions._meta_data[
            'required_json_kind']

    def test_rules_nonextant_on_load(self, setup, request, mgmt_root):
        rulespc = mgmt_root.tm.ltm.policys
        test_pol1 = rulespc.policy.load(partition='Common',
                                        name='_sys_CEC_video_policy')
        rules_s1 = test_pol1.rules_s
        with pytest.raises(NonExtantPolicyRule) as ex:
            rules_s1.rules.load(name='bad_rule')
        assert 'The rule named, bad_rule, does not exist on the device.' in \
            ex.value.message

    def test_rules_nonextant_on_exists(self, setup, request, mgmt_root):
        rulespc = mgmt_root.tm.ltm.policys
        test_pol1 = rulespc.policy.load(partition='Common',
                                        name='_sys_CEC_video_policy')
        rules_s1 = test_pol1.rules_s
        assert rules_s1.rules.exists(name='bad_rule') is False

    def test_create_policy_legacy_false(self, setup, request, mgmt_root):
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', legacy=False)
        assert pol1.name == 'poltest1'

    def test_policy_update_race(self, setup, request, mgmt_root):
        full_pol_dict = json.load(
            open(os.path.join(CURDIR, 'full_policy.json')))
        empty_pol_dict = copy.deepcopy(full_pol_dict)
        empty_pol_dict['rules'] = []
        pol, pc = setup_policy_test(request, mgmt_root, 'Common', 'racetest')
        for i in range(30):
            # Start out with an empty policy (no rules)
            pol.refresh()
            assert pol.rules_s.rules.exists(name='test_rule') is False
            assert list(pol.rules_s.get_collection()) == []
            # Update policy to have rules, which have conditions and actions
            pol.update(**full_pol_dict)
            # Ensure rules, actions, and conditions are present
            assert pol.rules_s.rules.exists(name='test_rule') is True
            rule = pol.rules_s.rules.load(name='test_rule')
            assert rule.actions_s.actions.exists(name='0')
            assert rule.actions_s.actions.exists(name='1')
            assert rule.conditions_s.conditions.exists(name='0')
            assert rule.conditions_s.conditions.exists(name='1')
            assert rule.conditions_s.conditions.exists(name='2')
            assert rule.conditions_s.conditions.exists(name='3')
            assert rule.conditions_s.conditions.exists(name='4')
            # Wipe the rule with an update
            pol.update(**empty_pol_dict)
            assert pol.rules_s.rules.exists(name='test_rule') is False


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.1.0'),
    reason='Policies Changed in 12.1 to require workflows.'
)
class TestPolicy(object):
    def test_policy_create_refresh_update_delete_load(self, setup, request,
                                                      mgmt_root):
        policy1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                         'poltest1', subPath='Drafts',
                                         legacy=False)
        assert policy1.name == 'poltest1'
        policy1.strategy = '/Common/all-match'
        policy1.update()
        assert policy1.strategy == '/Common/all-match'
        policy1.strategy = '/Common/first-match'
        policy1.refresh()
        assert policy1.strategy == '/Common/all-match'
        policy2 = pc1.policy.load(
            partition='Common', name='poltest1', subPath='Drafts')
        assert policy2.selfLink == policy1.selfLink
        p2rc = policy2.rules_s
        p2rc.refresh()
        assert p2rc._meta_data['required_json_kind'] == p2rc.kind
        assert p2rc.get_collection() == []
        policy1.modify(strategy='/Common/first-match')
        assert policy2.strategy == '/Common/all-match'
        assert policy1.strategy != policy2.strategy
        policy2.refresh()
        assert policy1.strategy == policy2.strategy

    def test_policy_create_no_subpath(self, setup, mgmt_root, request):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            pol, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                         'poltest1', legacy=False)
        msg = "The keyword 'subPath' must be specified when creating " \
            "draft policy in TMOS versions >= 12.1.0. Try and specify " \
            "subPath as 'Drafts'."
        assert msg == ex.value.message

    def test_policy_create_legacy_and_publish(
            self, setup, mgmt_root, request):
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', legacy=True, publish=True)
        assert 'Drafts' not in pol1._meta_data['uri']
        assert pol1.status == 'legacy'

    def test_policy_create_draft(self, setup, mgmt_root, request):
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', legacy=False,
                                      subPath='Drafts')
        assert pol1.fullPath == '/Common/Drafts/poltest1'
        pol1.strategy = '/Common/all-match'
        pol1.update()
        assert pol1.strategy == '/Common/all-match'
        pol1a = pc1.policy.load(
            name='poltest1', partition='Common', subPath='Drafts')
        assert pol1a.strategy == pol1.strategy

    def test_policy_publish_draft_on_create(self, setup, mgmt_root, request):
        # Can publish a draft two ways, by providing publish=True to create
        # for a policy, or call .publish() on an existing policy object
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', subPath='Drafts',
                                      legacy=False, publish=True)
        assert pol1.fullPath == '/Common/poltest1'
        assert pol1.status == 'published'
        pol2 = pc1.policy.load(name='poltest1', partition='Common')
        assert pol1.status == 'published'
        assert pol1.strategy == '/Common/first-match'
        assert pol1.strategy == pol2.strategy
        pol2.delete()

    def test_policy_publish_draft(self, setup, mgmt_root, request):
        # Can publish a draft two ways, by providing publish=True to create
        # for a policy, or call .publish() on an existing policy object
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', subPath='Drafts',
                                      legacy=False)
        assert pol1.fullPath == '/Common/Drafts/poltest1'
        assert pol1.status == 'draft'
        pol1.publish()
        assert pol1.fullPath == '/Common/poltest1'
        assert pol1.status == 'published'
        pol2 = pc1.policy.load(name='poltest1', partition='Common')
        assert pol1.status == 'published'
        pol2.delete()

    def test_policy_publish_draft_update_exception(
            self, setup, mgmt_root, request):
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', subPath='Drafts',
                                      legacy=False)
        # Cannot update a published policy
        assert pol1.fullPath == '/Common/Drafts/poltest1'
        assert pol1.status == 'draft'
        pol1.publish()
        assert pol1.fullPath == '/Common/poltest1'
        assert pol1.status == 'published'
        pol2 = pc1.policy.load(name='poltest1', partition='Common')
        assert pol1.status == 'published'
        pol2.strategy = '/Common/all-match'
        with pytest.raises(OperationNotSupportedOnPublishedPolicy) as ex:
            pol2.update()
        assert 'Update operation not allowed on a published policy.' == \
            ex.value.message
        pol1.delete()

    def test_policy_publish_draft_modify_exception(
            self, mgmt_root, request):
        pol1, pc1 = setup_policy_test(request, mgmt_root, 'Common',
                                      'poltest1', subPath='Drafts',
                                      legacy=False)
        assert pol1.fullPath == '/Common/Drafts/poltest1'
        assert pol1.status == 'draft'
        pol1.publish()
        with pytest.raises(OperationNotSupportedOnPublishedPolicy) as ex:
            pol1.modify(strategy='/Common/all-match')
        assert 'Modify operation not allowed on a published policy.' == \
            ex.value.message
        pol1.delete()

    def test_policy_update_race(self, setup, request, mgmt_root):
        full_pol_dict = json.load(
            open(os.path.join(CURDIR, 'full_policy.json')))
        empty_pol_dict = copy.deepcopy(full_pol_dict)
        empty_pol_dict['rules'] = []
        pol, pc = setup_policy_test(request, mgmt_root, 'Common', 'racetest',
                                    subPath='Drafts')
        for i in range(30):
            # Start out with an empty policy (no rules)
            assert pol.rules_s.rules.exists(name='test_rule') is False
            assert list(pol.rules_s.get_collection()) == []
            # Update policy to have rules, which have conditions and actions
            pol.update(**full_pol_dict)
            # Ensure rules, actions, and conditions are present
            assert pol.rules_s.rules.exists(name='test_rule') is True
            rule = pol.rules_s.rules.load(name='test_rule')
            assert rule.actions_s.actions.exists(name='0')
            assert rule.actions_s.actions.exists(name='1')
            assert rule.conditions_s.conditions.exists(name='0')
            assert rule.conditions_s.conditions.exists(name='1')
            assert rule.conditions_s.conditions.exists(name='2')
            assert rule.conditions_s.conditions.exists(name='3')
            assert rule.conditions_s.conditions.exists(name='4')
            # Wipe the rule with an update
            pol.update(**empty_pol_dict)
            assert pol.rules_s.rules.exists(name='test_rule') is False

    def test_rules_nonextant_on_load(self, setup, request, mgmt_root):
        pol, pc = setup_policy_test(request, mgmt_root, 'Common', 'racetest',
                                    subPath='Drafts')
        with pytest.raises(NonExtantPolicyRule) as ex:
            pol.rules_s.rules.load(name='bad_rule')
        assert 'The rule named, bad_rule, does not exist on the device.' in \
            ex.value.message

    def test_rules_nonextant_on_exists(self, setup, request, mgmt_root):
        pol, pc = setup_policy_test(request, mgmt_root, 'Common', 'racetest',
                                    subPath='Drafts')
        assert pol.rules_s.rules.exists(name='bad_rule') is False
