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

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.gtm.rule import Rule
from requests.exceptions import HTTPError

pytestmark = pytest.mark.skipif(
    True, reason='these tests require the optional gtm module')


RULE = '''when LB_SELECTED {
   set wipHost [LB::server addr]
}
'''


def delete_rule(mgmt_root, name, partition):
    r = mgmt_root.tm.gtm.rules.rule
    try:
        r.load(name=name, partition=partition)
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

    rule1 = mgmt_root.tm.gtm.rules.rule
    rule1.create(name=name, partition=partition, apiAnonymous=RULE)
    request.addfinalizer(teardown)
    return rule1


class TestCreate(object):
    def test_create_no_args(self, mgmt_root):
        rule1 = mgmt_root.tm.gtm.rules.rule
        with pytest.raises(MissingRequiredCreationParameter):
            rule1.create()

    def test_create_no_apianonymous(self, mgmt_root):
        rule1 = mgmt_root.tm.gtm.rules.rule
        with pytest.raises(MissingRequiredCreationParameter):
            rule1.create(name='rule1', partition='Common')

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.gtm.rules.rule
        rule1.create(name='rule1', partition='Common', apiAnonymous=RULE)
        assert rule1.name == 'rule1'
        assert rule1.partition == 'Common'
        assert rule1.generation and isinstance(rule1.generation, int)
        assert 'LB_SELECTED' in rule1.apiAnonymous
        assert rule1.fullPath == '/Common/rule1'
        assert rule1.kind == 'tm:gtm:rule:rulestate'
        assert rule1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/rule/~Common~rule1')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.gtm.rules.rule
        rule1.create(name='rule1', partition='Common',
                     apiAnonymous=RULE,
                     check='syntax')
        assert 'check syntax' in rule1.apiAnonymous

    def test_create_duplicate(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.gtm.rules.rule
        rule1.create(name='rule1', partition='Common',
                     apiAnonymous=RULE,
                     check='syntax')
        rule2 = mgmt_root.tm.gtm.rules.rule
        with pytest.raises(HTTPError) as err:
            rule2.create(name='rule1', partition='Common',
                         apiAnonymous=RULE,
                         check='syntax')
            assert err.response.status_code == 400


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        r1 = mgmt_root.tm.gtm.rules.rule.load(
            name='rule1', partition='Common')
        r2 = mgmt_root.tm.gtm.rules.rule.load(
            name='rule1', partition='Common')
        assert 'check syntax' not in r1.apiAnonymous
        assert 'check syntax' not in r2.apiAnonymous

        r2.update(apiAnonymous='check syntax\n' + RULE)
        assert 'check syntax' in r2.apiAnonymous
        assert 'check syntax' not in r1.apiAnonymous

        r1.refresh()
        assert 'check syntax' in r1.apiAnonymous


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.rules.rule.load(
                name='rule1', partition='Common')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.gtm.rules.rule.load(
            name='rule1', partition='Common')
        assert 'check syntax' not in rule1.apiAnonymous
        rule1.update(apiAnonymous='check syntax\n' + RULE)
        rule2 = mgmt_root.tm.gtm.rules.rule.load(
            name='rule1', partition='Common')
        assert 'check syntax' in rule1.apiAnonymous
        assert 'check syntax' in rule2.apiAnonymous


class TestUpdate(object):
    def test_update(self, request, mgmt_root):
        rule1 = setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rule1.update(apiAnonymous='check syntax\n' + RULE)
        assert 'check syntax' in rule1.apiAnonymous

    def test_update_samevalue(self, request, mgmt_root):
        rule1 = setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        rule1.update(apiAnonymous='check none\n' + RULE)
        assert 'check syntax' not in rule1.apiAnonymous


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'rule1', 'Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.rules.rule.load(
                name='rule1', partition='Common')
            assert err.response.status_code == 404


class TestRuleCollection(object):
    def test_rule_collection(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'rule1', 'Common')
        rule1 = mgmt_root.tm.gtm.rules.rule
        rule1.create(name='rule1', partition='Common', apiAnonymous=RULE)
        assert rule1.name == 'rule1'
        assert rule1.partition == 'Common'
        assert rule1.generation and isinstance(rule1.generation, int)
        assert 'LB_SELECTED' in rule1.apiAnonymous
        assert rule1.fullPath == '/Common/rule1'
        assert rule1.kind == 'tm:gtm:rule:rulestate'
        assert rule1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/rule/~Common~rule1')

        rc = mgmt_root.tm.gtm.rules.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Rule)
