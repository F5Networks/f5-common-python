# Copyright 2021 F5 Networks Inc.
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


def setup_cipher_rule_test(request, mgmt_root, name, partition, maxRate):
    def teardown():
        delete_resource(rule)
    request.addfinalizer(teardown)

    rule = mgmt_root.tm.ltm.cipher.rules.rule.create(
        name=name, partition=partition, maxRate=maxRate)
    return rule


def setup_cipher_group_test(request, mgmt_root, name, partition, maxRate):
    def teardown():
        delete_resource(group)
    request.addfinalizer(teardown)

    group = mgmt_root.tm.ltm.cipher.groups.group.create(
        name=name, partition=partition, maxRate=maxRate)
    return group


class TestCipherRules(object):
    def test_cipher_rule_list(self, mgmt_root):
        rules = mgmt_root.tm.ltm.cipher.rules.get_collection()
        assert len(rules)
        for rule in rules:
            assert rule.generation


class TestCipherRule(object):
    def test_cipher_rule_CURDL(self, request, mgmt_root):
        # Create and Delete are tested by the setup/teardown
        r1 = setup_cipher_rule_test(
            request, mgmt_root, 'cipher-rule-test', 'Common', 1000000
        )

        # Load
        r2 = mgmt_root.tm.ltm.cipher.rules.rule.load(
            name='cipher-rule-test', partition='Common')
        assert r1.name == 'cipher-rule-test'
        assert r1.name == r2.name
        assert r1.generation == r2.generation

        # Update
        r1.description = TEST_DESCR
        r1.update()
        assert r1.description == TEST_DESCR
        assert r1.generation > r2.generation

        # Refresh
        r2.refresh()
        assert r2.description == TEST_DESCR
        assert r1.generation == r2.generation


class TestCipherGroups(object):
    def test_cipher_group_list(self, mgmt_root):
        groups = mgmt_root.tm.ltm.cipher.groups.get_collection()
        assert len(groups)
        for group in groups:
            assert group.generation


class TestCipherGroup(object):
    def test_cipher_group_CURDL(self, request, mgmt_root):
        # Create and Delete are tested by the setup/teardown
        g1 = setup_cipher_group_test(
            request, mgmt_root, 'cipher-group-test', 'Common', 1000000
        )

        # Load
        g2 = mgmt_root.tm.ltm.cipher.groups.group.load(
            name='cipher-group-test', partition='Common')
        assert g1.name == 'cipher-group-test'
        assert g1.name == g2.name
        assert g1.generation == g2.generation

        # Update
        g1.description = TEST_DESCR
        g1.update()
        assert g1.description == TEST_DESCR
        assert g1.generation > g2.generation

        # Refresh
        g2.refresh()
        assert g2.description == TEST_DESCR
        assert g1.generation == g2.generation
