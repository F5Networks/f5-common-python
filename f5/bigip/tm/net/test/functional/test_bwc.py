# Copyright 2020 F5 Networks Inc.
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

from requests.exceptions import HTTPError


TEST_DESCR = "TEST DESCRIPTION"


def delete_resource(resource):
    try:
        resource.delete()
    except HTTPError as err:
        if err.response.status_code != 404:
            raise


def setup_policy_test(request, mgmt_root, name, partition, maxRate):
    def teardown():
        delete_resource(policy)
    request.addfinalizer(teardown)

    policy = mgmt_root.tm.net.bwc.policys.policy.create(
        name=name, partition=partition, maxRate=maxRate)
    return policy


class TestPolicys(object):
    def test_policy_list(self, mgmt_root):
        policies = mgmt_root.tm.net.bwc.policys.get_collection()
        assert len(policies)
        for policy in policies:
            assert policy.generation


class TestPolicy(object):
    def test_policy_CURDL(self, request, mgmt_root):
        # Create and Delete are tested by the setup/teardown
        p1 = setup_policy_test(
            request, mgmt_root, 'bwc-policy-test', 'Common', 1000000
        )

        # Load
        p2 = mgmt_root.tm.net.bwc.policys.policy.load(
            name='bwc-policy-test', partition='Common')
        assert p1.name == 'bwc-policy-test'
        assert p1.name == p2.name
        assert p1.generation == p2.generation

        # Update
        p1.description = TEST_DESCR
        p1.update()
        assert p1.description == TEST_DESCR
        assert p1.generation > p2.generation

        # Refresh
        p2.refresh()
        assert p2.description == TEST_DESCR
        assert p1.generation == p2.generation
