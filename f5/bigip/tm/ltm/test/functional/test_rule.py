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

import pytest

from f5.bigip.tm.ltm.rule import Rule
from f5.sdk_exception import MissingRequiredCreationParameter
from requests.exceptions import HTTPError


RULE = '''when CLIENT_ACCEPTED {
if { [IP::addr [IP::client_addr] equals 10.10.10.10] } {
pool my_pool
}
}
'''


def delete_rule(mgmt_root, name, partition):
    try:
        r = mgmt_root.tm.ltm.rules.rule.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    r.delete()


def setup_create_test(request, mgmt_root, name, partition):
    def teardown():
        delete_rule(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_rule(mgmt_root, name, partition)

    rule1 = mgmt_root.tm.ltm.rules.rule.create(
        name=name, partition=partition, apiAnonymous=RULE)
    request.addfinalizer(teardown)
    return rule1


class TestCreate(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.rules.rule.create()

    def test_create_no_apianonymous(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.rules.rule.create(name='rule1', partition='Common')

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.ltm.rules.rule.create(
            name='rule1', partition='Common', apiAnonymous=RULE)
        assert rule1.name == 'rule1'
        assert rule1.partition == 'Common'
        assert rule1.generation and isinstance(rule1.generation, int)
        assert 'my_pool' in rule1.apiAnonymous
        assert rule1.fullPath == '/Common/rule1'
        assert rule1.kind == 'tm:ltm:rule:rulestate'
        assert rule1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/rule/~Common~rule1')

        # These are test cases that fail due to BigIP REST API problems
        # assert rule1.ignoreVerification is False

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.ltm.rules.rule.create(
            name='rule1', partition='Common',
            apiAnonymous=RULE,
            ignoreVerification=True)
        assert rule1.ignoreVerification == 'true'

        # These are assertions that fail due to BigIP REST API problems
        # assert rule1.ignoreVerifcation is True

    def test_create_duplicate(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        mgmt_root.tm.ltm.rules.rule.create(
            name='rule1',
            partition='Common',
            apiAnonymous=RULE,
            ignoreVerification=True)
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.ltm.rules.rule.create(
                name='rule1',
                partition='Common',
                apiAnonymous=RULE,
                ignoreVerification=True)
            assert err.response.status_code == 400


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        r1 = mgmt_root.tm.ltm.rules.rule.load(
            name='rule1', partition='Common')
        r2 = mgmt_root.tm.ltm.rules.rule.load(
            name='rule1', partition='Common')
        assert not hasattr(r1, 'ignoreVerification')
        assert not hasattr(r2, 'ignoreVerification')

        r2.update(ignoreVerification=True)
        assert r2.ignoreVerification == 'true'
        assert not hasattr(r1, 'ignoreVerification')

        r1.refresh()
        assert r1.ignoreVerification == 'true'


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.ltm.rules.rule.load(
                name='rule1', partition='Common')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.ltm.rules.rule.load(
            name='rule1', partition='Common')
        assert not hasattr(rule1, 'ignoreVerification')
        rule1.update(ignoreVerification=True)
        rule2 = mgmt_root.tm.ltm.rules.rule.load(
            name='rule1', partition='Common')
        assert rule1.ignoreVerification == 'true'
        assert rule2.ignoreVerification == 'true'


class TestUpdate(object):
    def test_update(self, request, mgmt_root):
        rule1 = setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rule1.update(ignoreVerification=True)
        assert rule1.ignoreVerification == 'true'

    def test_update_samevalue(self, request, mgmt_root):
        rule1 = setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rule1.update(ignoreVerification=False)
        assert not hasattr(rule1, 'ignoreVerfication')

        # These are assertsion that fail due to BigIP REST API problems
        # assert rule1.ignoreVerification == 'false'


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.ltm.rules.rule.load(
                name='rule1', partition='Common')
            assert err.response.status_code == 404


class TestRuleCollection(object):
    def test_rule_collection(self, request, mgmt_root):
        rc = mgmt_root.tm.ltm.rules.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Rule)


class TestRulesStats(object):
    def test_stats(self, request, mgmt_root, opt_release):
        setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rules_stats = mgmt_root.tm.ltm.rules.stats.load()
        stats_link = 'https://localhost/mgmt/tm/ltm/rule/' +\
            '~Common~rule1:CLIENT_ACCEPTED/stats'
        assert stats_link in rules_stats.entries
        rule_nested_stats = rules_stats.entries[stats_link]['nestedStats']
        assert rule_nested_stats['selfLink'] == stats_link+'?ver='+opt_release
        entries = rule_nested_stats['entries']
        assert entries['tmName']['description'] == '/Common/rule1'
        assert entries['totalExecutions']['value'] == 0
