# Copyright 2016 F5 Networks Inc.
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
from requests.exceptions import HTTPError


def delete_user(bigip, name):
    user = bigip.auth.users.user
    try:
        user1 = user.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    user1.delete()


def setup_loadable_user_test(request, bigip, user):
    def teardown():
        delete_user(bigip, 'user1')

    request.addfinalizer(teardown)

    user1 = user.create(name='user1')
    assert user1.name == 'user1'


def setup_create_test(request, bigip):
    def teardown():
        delete_user(bigip, 'user1')
    request.addfinalizer(teardown)


def setup_create_two(request, bigip):
    def teardown():
        for name in ['user1', 'user2']:
            delete_user(bigip, name)
    request.addfinalizer(teardown)


class TestCreate(object):
    def test_create_two(self, request, bigip):
        setup_create_two(request, bigip)

        n1 = bigip.auth.users.user.create(name='user1')
        n2 = bigip.auth.users.user.create(name='user2')

        assert n1 is not n2
        assert n2.name != n1.name

    def test_create_no_args(self, bigip):
        '''Test that user.create() with no options throws a ValueError '''
        user1 = bigip.auth.users.user
        with pytest.raises(MissingRequiredCreationParameter):
            user1.create()

    def test_create_min_args(self, request, bigip):
        '''Test that user.create() with only required arguments work.

        This will also test that the default values are set correctly and are
        part of the user object after creating the instance on the BigIP
        '''
        setup_create_test(request, bigip)

        user1 = bigip.auth.users.user.create(name='user1')

        assert user1.name == 'user1'
        assert user1.generation is not None \
            and isinstance(user1.generation, int)
        assert user1.fullPath == 'user1'
        assert user1.selfLink.startswith(
            'https://localhost/mgmt/tm/auth/user/user1')

        # Default Values
        assert user1.description == 'user1'
        assert user1.encryptedPassword == '!!'
        assert user1.partitionAccess == [dict(
            name='all-partitions',
            role='no-access'
        )]

    def test_create_description(self, request, bigip, USER):
        setup_create_test(request, bigip)
        USER1 = USER.create(name='user1', description='foo')
        assert USER1.description == 'foo'


class TestLoad(object):
    def test_load_no_object(self, USER):
        with pytest.raises(HTTPError) as err:
            USER.load(name='user10')
            assert err.response.status == 404

    def test_load(self, request, bigip, USER):
        setup_loadable_user_test(request, bigip, USER)
        n1 = bigip.auth.users.user.load(name='user1')
        assert n1.name == 'user1'
        assert n1.description == 'user1'
        assert isinstance(n1.generation, int)


class TestRefresh(object):
    def test_refresh(self, request, bigip, USER):
        setup_loadable_user_test(request, bigip, USER)

        n1 = bigip.auth.users.user.load(name='user1')
        n2 = bigip.auth.users.user.load(name='user1')
        assert n1.description == 'user1'
        assert n2.description == 'user1'

        n2.update(description='foobaz')
        assert n2.description == 'foobaz'
        assert n1.description == 'user1'

        n1.refresh()
        assert n1.description == 'foobaz'


class TestDelete(object):
    def test_delete(self, request, bigip, USER):
        setup_loadable_user_test(request, bigip, USER)
        n1 = bigip.auth.users.user.load(name='user1')
        n1.delete()
        del(n1)
        with pytest.raises(HTTPError) as err:
            bigip.auth.users.user.load(name='user1')
            assert err.response.status_code == 404


class TestUpdate(object):
    def test_update_with_args(self, request, bigip, USER):
        setup_loadable_user_test(request, bigip, USER)
        n1 = bigip.auth.users.user.load(name='user1')
        assert n1.description == 'user1'
        n1.update(description='foobar')
        assert n1.description == 'foobar'

    def test_update_parameters(self, request, bigip, USER):
        setup_loadable_user_test(request, bigip, USER)
        n1 = bigip.auth.users.user.load(name='user1')
        assert n1.description == 'user1'
        n1.description = 'foobar'
        n1.update()
        assert n1.description == 'foobar'
