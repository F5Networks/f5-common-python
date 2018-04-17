# Copyright 2015-2106 F5 Networks Inc.
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

from f5.sdk_exception import MemberStateModifyUnsupported
from f5.sdk_exception import MissingRequiredCreationParameter

from requests.exceptions import HTTPError
from six import iterkeys

TESTDESCRIPTION = 'TESTDESCRIPTION'


def delete_pool(mgmt_root, name, partition):
    try:
        p = mgmt_root.tm.ltm.pools.pool.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_create_test(request, mgmt_root, name, partition):
    def teardown():
        delete_pool(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_pool(mgmt_root, name, partition)

    pool1 = mgmt_root.tm.ltm.pools.pool.create(name=name, partition=partition)
    request.addfinalizer(teardown)
    return pool1


def setup_member_test(request, mgmt_root, name, partition,
                      memname="192.168.15.15:80"):
    p1 = setup_basic_test(request, mgmt_root, name, partition)
    member = p1.members_s.members.create(
        name=memname, partition=partition)
    assert member.name == "192.168.15.15:80"
    return member, p1


class TestPoolMembersCollection(object):
    def test_get_collection(self, request, mgmt_root, opt_release):
        member1, pool1 = setup_member_test(request, mgmt_root, 'membertestpool1',
                                           'Common')
        pool1.members_s.members.create(
            name='192.168.16.16:8080', partition='Common')
        selfLinks = []
        for mem in pool1.members_s.get_collection():
            selfLinks.append(mem.selfLink)
            mem.delete()
            assert mem.__dict__ == {'deleted': True}
        assert selfLinks[0] == 'https://localhost/mgmt/tm/ltm/pool/' +\
            '~Common~membertestpool1/members/~Common~192.168.15.15:80' +\
            '?ver='+opt_release
        assert selfLinks[1] == 'https://localhost/mgmt/tm/ltm/pool/' +\
            '~Common~membertestpool1/members/~Common~192.168.16.16:8080' +\
            '?ver='+opt_release
        try:
            member1.refresh()
        except HTTPError as err:
            if err.response.status_code != 404:
                    raise
        pre_del = set(iterkeys(pool1.__dict__))
        pool1.refresh()
        post_del = set(iterkeys(pool1.__dict__))
        delta = pre_del - post_del
        remaining = pre_del - delta
        assert 'members_s' not in remaining

    def test_refresh_member(self, request, mgmt_root):
        member, _ = setup_member_test(request, mgmt_root, 'membertestpool1',
                                      'Common')
        member.description = TESTDESCRIPTION
        member.update(state=None)
        member.description = "NOTTESTDESCRIPTION"
        member.refresh()
        assert member.description == TESTDESCRIPTION
        member.delete()
        assert member.__dict__ == {'deleted': True}

    def test_load_member(self, request, mgmt_root):
        member1, pool1 = setup_member_test(request, mgmt_root, 'membertestpool1',
                                           'Common')
        member1.description = TESTDESCRIPTION
        member1.update(state=None)
        member2 = pool1.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert member2.description == TESTDESCRIPTION
        assert member2.selfLink == member1.selfLink
        member1.delete()
        assert member1.__dict__ == {'deleted': True}

    def test_members_exists(self, request, mgmt_root):
        member1, pool1 = setup_member_test(request, mgmt_root, 'membertestpool1',
                                           'Common')
        assert\
            member1.exists(partition="Common", name="192.168.15.15:80") is True
        assert\
            member1.exists(partition="Common", name="19.168.15.15:80") is False

    def test_state_update(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.state == 'unchecked'
        m1.state = 'user-down'
        m1.update()
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.state == 'user-down'
        assert m2.state == m1.state

    def test_state_update_with_kwargs(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.state == 'unchecked'
        m1.update(state='user-down')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.state == 'user-down'
        assert m2.state == m1.state

    def test_state_update_invalid_value_with_kwargs(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.state == 'unchecked'
        m1.update(state='down')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.state == 'unchecked'
        assert m2.state == m1.state

    def test_state_update_invalid_value(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.state == 'unchecked'
        m1.state = 'down'
        m1.update()
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.state == 'unchecked'
        assert m2.state == m1.state

    def test_session_update_with_kwargs(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.session == 'user-enabled'
        m1.update(session='user-disabled')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.session == 'user-disabled'
        assert m2.session == m1.session

    def test_session_update_invalid_value_with_kwargs(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.session == 'user-enabled'
        m1.update(session='monitor-enabled')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.session == 'user-enabled'
        assert m2.session == m1.session

    def test_session_update_invalid_value(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.session == 'user-enabled'
        m1.session = 'monitor-enabled'
        m1.update()
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.session == 'user-enabled'
        assert m2.session == m1.session

    def test_update_session_state(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.session == 'user-enabled'
        assert m1.state == 'unchecked'
        m1.session = 'user-disabled'
        m1.state = 'user-down'
        m1.update()
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        m2.session = 'user-disabled'
        m2.state = 'user-down'
        m2.session = m1.session
        m2.state = m1.state

    def test_update_session_state_kwargs(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.session == 'user-enabled'
        assert m1.state == 'unchecked'
        m1.update(session='user-disabled', state='user-down')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        m2.session = 'user-disabled'
        m2.state = 'user-down'
        m2.session = m1.session
        m2.state = m1.state

    def test_session_modify(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.session == 'user-enabled'
        m1.modify(session='user-disabled')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.session == 'user-disabled'
        assert m1.session == m2.session

    def test_state_modify(self, request, mgmt_root):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        assert m1.state == 'unchecked'
        m1.modify(state='user-down')
        m2 = pool.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert m2.state == 'user-down'
        assert m1.state == m2.state

    def test_state_modify_error(self, request, mgmt_root):
        m1, _ = setup_member_test(request, mgmt_root, 'membertestpool1', 'Common')
        with pytest.raises(MemberStateModifyUnsupported) as ex:
            m1.modify(state='down')
        assert ex.value.message == "The members resource does not support a " \
                                   "modify with the value of the 'state' " \
                                   "attribute as down. The accepted values " \
                                   "are 'user-up' or 'user-down'"

    def test_session_modify_error(self, request, mgmt_root):
        m1, _ = setup_member_test(request, mgmt_root, 'membertestpool1', 'Common')
        with pytest.raises(MemberStateModifyUnsupported) as ex:
            m1.modify(state='monitor-enabled')
        assert ex.value.message == "The members resource does not support a " \
                                   "modify with the value of the 'state' " \
                                   "attribute as monitor-enabled. " \
                                   "The accepted values are " \
                                   "'user-up' or 'user-down'"


class TestPoolsStats(object):
    def test_stats(self, request, mgmt_root, opt_release):
        m1, pool = setup_member_test(request, mgmt_root, 'membertestpool1',
                                     'Common')
        pools_stats = mgmt_root.tm.ltm.pools.stats.load()
        stats_link = 'https://localhost/mgmt/tm/ltm/pool/' +\
            '~Common~membertestpool1/stats'
        assert stats_link in pools_stats.entries
        pool_nested_stats = pools_stats.entries[stats_link]['nestedStats']
        assert pool_nested_stats['selfLink'] == stats_link+'?ver='+opt_release
        entries = pool_nested_stats['entries']
        assert entries['tmName']['description'] == '/Common/membertestpool1'
        assert entries['status.enabledState']['description'] == 'enabled'


class TestPool(object):
    def test_create_no_args(self, mgmt_root):
        pool1 = mgmt_root.tm.ltm.pools.pool
        with pytest.raises(MissingRequiredCreationParameter):
            pool1.create()

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'pool1', 'Common')
        pool1 = mgmt_root.tm.ltm.pools.pool.create(name='pool1', partition='Common')
        assert pool1.name == 'pool1'
        assert pool1.partition == 'Common'
        assert pool1.generation and isinstance(pool1.generation, int)
        assert pool1.fullPath == '/Common/pool1'
        assert pool1.kind == 'tm:ltm:pool:poolstate'
        assert pool1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/pool/~Common~pool1')

    def test_refresh(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'pool1', 'Common')
        assert pool1.allowNat == "yes"
        pool1.allowNat = "no"
        pool1.refresh()
        assert pool1.allowNat == "yes"

    def test_update(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'pool1', 'Common')
        pool1.allowNat = "no"
        pool1.update()
        assert pool1.allowNat == "no"
        pool1.allowNat = "yes"
        pool1.refresh()
        assert pool1.allowNat == "no"

    def test_create_monitor_parameter(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'pool1', 'Common')
        mon = 'min 1 of { /Common/http /Common/tcp }'
        pool1 = mgmt_root.tm.ltm.pools.pool.create(
            name='pool1', partition='Common', monitor=mon)
        assert pool1.name == 'pool1'
        assert pool1.partition == 'Common'
        assert pool1.monitor == mon
        assert pool1.generation and isinstance(pool1.generation, int)
        assert pool1.fullPath == '/Common/pool1'
        assert pool1.kind == 'tm:ltm:pool:poolstate'
        assert pool1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/pool/~Common~pool1')

    def test_update_monitor_parameter(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'pool1', 'Common')
        mon = 'min 1 of { /Common/http /Common/tcp }'
        pool1.monitor = mon
        pool1.update()
        assert pool1.monitor == mon
        # Test kwargs
        mon2 = 'min 2 of { /Common/http /Common/tcp }'
        pool1.update(monitor=mon2)
        assert pool1.monitor == mon2

    def test_modify_monitor_parameter(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'pool1', 'Common')
        mon = 'min 1 of { /Common/http /Common/tcp }'
        pool1.modify(monitor=mon)
        assert pool1.monitor == mon
