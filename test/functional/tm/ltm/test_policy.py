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

from distutils.version import LooseVersion
from pprint import pprint as pp
import pytest

pp('')
TESTDESCRIPTION = "TESTDESCRIPTION"


@pytest.fixture
def setup(request, setup_device_snapshot):
    return setup_device_snapshot


def setup_policy_test(request, mgmt_root, partition, name,
                      strategy="first-match", **kwargs):
    pc1 = mgmt_root.tm.ltm.policys
    policy1 = pc1.policy.create(
        name=name, partition=partition, strategy=strategy, **kwargs)
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
                                         'poltest1', legacy=True)
        assert policy1.name == 'poltest1'
        policy1.strategy = '/Common/all-match'
        policy1.update(legacy=True)
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
