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

from requests.exceptions import HTTPError
from six import iterkeys

from f5.sdk_exception import MissingRequiredCreationParameter

TESTDESCRIPTION = 'TESTDESCRIPTION'


def delete_pool(bigip, name, partition):
    try:
        p = bigip.ltm.pools.pool.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_create_test(request, bigip, name, partition):
    def teardown():
        delete_pool(bigip, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, bigip, name, partition):
    def teardown():
        delete_pool(bigip, name, partition)

    pool1 = bigip.ltm.pools.pool.create(name=name, partition=partition)
    request.addfinalizer(teardown)
    return pool1


def setup_member_test(request, bigip, name, partition,
                      memname="192.168.15.15:80"):
    p1 = setup_basic_test(request, bigip, name, partition)
    member = p1.members_s.members.create(
        name=memname, partition=partition)
    assert member.name == "192.168.15.15:80"
    return member, p1


class TestPoolMembersCollection(object):
    def test_get_collection(self, request, bigip, opt_release):
        member1, pool1 = setup_member_test(request, bigip, 'membertestpool1',
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


class TestPoolMembers(object):
    def test_create_member(self, request, bigip):
        member, _ = setup_member_test(request, bigip, 'membertestpool1',
                                      'Common')

    def test_update_member(self, request, bigip):
        member, _ = setup_member_test(request, bigip, 'membertestpool1',
                                      'Common')
        member.update(description=TESTDESCRIPTION, state=None)
        assert member.__dict__.pop('description') == TESTDESCRIPTION
        member.delete()
        assert member.__dict__ == {'deleted': True}

    def test_refresh_member(self, request, bigip):
        member, _ = setup_member_test(request, bigip, 'membertestpool1',
                                      'Common')
        member.description = TESTDESCRIPTION
        member.update(state=None)
        member.description = "NOTTESTDESCRIPTION"
        member.refresh()
        assert member.description == TESTDESCRIPTION
        member.delete()
        assert member.__dict__ == {'deleted': True}

    def test_load_member(self, request, bigip):
        member1, pool1 = setup_member_test(request, bigip, 'membertestpool1',
                                           'Common')
        member1.description = TESTDESCRIPTION
        member1.update(state=None)
        member2 = pool1.members_s.members.load(
            name='192.168.15.15:80', partition='Common')
        assert member2.description == TESTDESCRIPTION
        assert member2.selfLink == member1.selfLink
        member1.delete()
        assert member1.__dict__ == {'deleted': True}

    def test_members_exists(self, request, bigip):
        member1, pool1 = setup_member_test(request, bigip, 'membertestpool1',
                                           'Common')
        assert\
            member1.exists(partition="Common", name="192.168.15.15:80") is True
        assert\
            member1.exists(partition="Common", name="19.168.15.15:80") is False


class TestPool(object):
    def test_create_no_args(self, bigip):
        pool1 = bigip.ltm.pools.pool
        with pytest.raises(MissingRequiredCreationParameter):
            pool1.create()

    def test_create(self, request, bigip):
        setup_create_test(request, bigip, 'pool1', 'Common')
        pool1 = bigip.ltm.pools.pool.create(name='pool1', partition='Common')
        assert pool1.name == 'pool1'
        assert pool1.partition == 'Common'
        assert pool1.generation and isinstance(pool1.generation, int)
        assert pool1.fullPath == '/Common/pool1'
        assert pool1.kind == 'tm:ltm:pool:poolstate'
        assert pool1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/pool/~Common~pool1')

    def test_refresh(self, request, bigip):
        pool1 = setup_basic_test(request, bigip, 'pool1', 'Common')
        assert pool1.allowNat == "yes"
        pool1.allowNat = "no"
        pool1.refresh()
        assert pool1.allowNat == "yes"

    def test_update(self, request, bigip):
        pool1 = setup_basic_test(request, bigip, 'pool1', 'Common')
        pool1.allowNat = "no"
        pool1.update()
        assert pool1.allowNat == "no"
        pool1.allowNat = "yes"
        pool1.refresh()
        assert pool1.allowNat == "no"
