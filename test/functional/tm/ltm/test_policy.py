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
import pytest

pp('')
TESTDESCRIPTION = "TESTDESCRIPTION"


def delete_resource(resources):
    for resource in resources.get_collection():
        system_policy_obj_name = ['_sys_CEC_SSL_client_policy',
                                  '_sys_CEC_SSL_server_policy',
                                  '_sys_CEC_video_policy']
        if resource.name not in system_policy_obj_name:
            resource.delete()


@pytest.fixture
def setup(request, bigip):
    pc1 = bigip.ltm.policys
    delete_resource(pc1)


def setup_policy_test(request, bigip, partition, name, strategy="first-match"):
    def teardown():
        delete_resource(pc1)
    request.addfinalizer(teardown)
    pc1 = bigip.ltm.policys
    policy1 = pc1.policy.create(
        name=name, partition=partition, strategy=strategy)
    return policy1, pc1


class TestPolicy(object):
    def test_policy_create_refresh_update_delete_load(self, setup, request,
                                                      bigip):
        policy1, pc1 = setup_policy_test(request, bigip, 'Common', 'poltest1')
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


class TestRulesAndActions(object):
    def test_rules_refresh_update_load(self, setup, request, bigip):
        rulespc = bigip.ltm.policys
        test_pol1 = rulespc.policy.load(partition='Common',
                                        name='_sys_CEC_video_policy')
        rules_s1 = test_pol1.rules_s
        rules1 = rules_s1.rules.load(name='youporn_web_1')
        r1actions = rules1.actions_s.actions.load(name="1")
        assert r1actions.kind == r1actions._meta_data['required_json_kind']
        delete_resource(rulespc)


class TestRulesAndConditions(object):
    def test_rules_refresh_update_load(self, setup, request, bigip):
        rulespc = bigip.ltm.policys
        test_pol1 = rulespc.policy.load(partition='Common',
                                        name='_sys_CEC_video_policy')
        rules_s1 = test_pol1.rules_s
        rules1 = rules_s1.rules.load(name='youporn_web_1')
        r1conditions = rules1.conditions_s.conditions.load(name="1")
        assert r1conditions.kind ==\
            r1conditions._meta_data['required_json_kind']
        delete_resource(rulespc)
