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

from distutils.version import LooseVersion
import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from requests.exceptions import HTTPError


def delete_user(mgmt_root, name):
    user = mgmt_root.tm.auth.users.user
    try:
        user1 = user.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    user1.delete()


def setup_loadable_user_test(request, mgmt_root, user):
    def teardown():
        delete_user(mgmt_root, 'user1')

    request.addfinalizer(teardown)

    user1 = user.create(name='user1')
    assert user1.name == 'user1'


def setup_create_test(request, mgmt_root):
    def teardown():
        delete_user(mgmt_root, 'user1')
    request.addfinalizer(teardown)


def setup_create_two(request, mgmt_root):
    def teardown():
        for name in ['user1', 'user2']:
            delete_user(mgmt_root, name)
    request.addfinalizer(teardown)


class TestCreate(object):
    def test_create_two(self, request, mgmt_root):
        setup_create_two(request, mgmt_root)

        n1 = mgmt_root.tm.auth.users.user.create(name='user1')
        n2 = mgmt_root.tm.auth.users.user.create(name='user2')

        assert n1 is not n2
        assert n2.name != n1.name

    def test_create_no_args(self, mgmt_root):
        '''Test that user.create() with no options throws a ValueError '''
        user1 = mgmt_root.tm.auth.users.user
        with pytest.raises(MissingRequiredCreationParameter):
            user1.create()

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) < LooseVersion('11.6.0'),
        reason='Skip test if on a version below 11.6.0. The '
        'next test will implement the same logic for 11.5.4 '
        'and below.')
    def test_create_min_args_11_6_greater(self, request, mgmt_root):
        '''Test that user.create() with only required arguments work.

        This will also test that the default values are set correctly and are
        part of the user object after creating the instance on the BigIP
        '''
        setup_create_test(request, mgmt_root)

        user1 = mgmt_root.tm.auth.users.user.create(name='user1')

        assert user1.name == 'user1'
        assert user1.generation is not None \
            and isinstance(user1.generation, int)
        assert user1.fullPath == 'user1'
        assert user1.selfLink.startswith(
            'https://localhost/mgmt/tm/auth/user/user1')

        # Default Values
        assert user1.description == 'user1'
        assert user1.encryptedPassword == '!!'
        assert user1.partitionAccess[0]['role'] == 'no-access'
        assert user1.partitionAccess[0]['name'] == 'all-partitions'

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) >= LooseVersion('11.6.0'),
        reason='Skip test if on a version greater than or equal to 11.6.0')
    def test_create_min_args_11_5_4_and_lower(self, request, mgmt_root):
        '''Test that user.create() with only required arguments work.

        This will also test that the default values are set correctly and are
        part of the user object after creating the instance on the BigIP
        '''
        setup_create_test(request, mgmt_root)

        user1 = mgmt_root.tm.auth.users.user.create(name='user1')

        assert user1.name == 'user1'
        assert user1.generation is not None \
            and isinstance(user1.generation, int)
        assert user1.fullPath == 'user1'
        assert user1.selfLink.startswith(
            'https://localhost/mgmt/tm/auth/user/user1')

        # Default Values
        assert user1.description == 'user1'
        assert user1.encryptedPassword == '!!'
        assert user1.partitionAccess == 'Common'

    def test_create_description(self, request, mgmt_root, USER):
        setup_create_test(request, mgmt_root)
        USER1 = USER.create(name='user1', description='foo')
        assert USER1.description == 'foo'


class TestLoad(object):
    def test_load_no_object(self, USER):
        with pytest.raises(HTTPError) as err:
            USER.load(name='user10')
            assert err.response.status == 404

    def test_load(self, request, mgmt_root, USER):
        setup_loadable_user_test(request, mgmt_root, USER)
        n1 = mgmt_root.tm.auth.users.user.load(name='user1')
        assert n1.name == 'user1'
        assert n1.description == 'user1'
        assert isinstance(n1.generation, int)


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root, USER):
        setup_loadable_user_test(request, mgmt_root, USER)

        n1 = mgmt_root.tm.auth.users.user.load(name='user1')
        n2 = mgmt_root.tm.auth.users.user.load(name='user1')
        assert n1.description == 'user1'
        assert n2.description == 'user1'

        n2.update(description='foobaz')
        assert n2.description == 'foobaz'
        assert n1.description == 'user1'

        n1.refresh()
        assert n1.description == 'foobaz'


class TestDelete(object):
    def test_delete(self, request, mgmt_root, USER):
        setup_loadable_user_test(request, mgmt_root, USER)
        n1 = mgmt_root.tm.auth.users.user.load(name='user1')
        n1.delete()
        del(n1)
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.auth.users.user.load(name='user1')
            assert err.response.status_code == 404


class TestUpdate(object):
    def test_update_with_args(self, request, mgmt_root, USER):
        setup_loadable_user_test(request, mgmt_root, USER)
        n1 = mgmt_root.tm.auth.users.user.load(name='user1')
        assert n1.description == 'user1'
        n1.update(description='foobar')
        assert n1.description == 'foobar'

    def test_update_parameters(self, request, mgmt_root, USER):
        setup_loadable_user_test(request, mgmt_root, USER)
        n1 = mgmt_root.tm.auth.users.user.load(name='user1')
        assert n1.description == 'user1'
        n1.description = 'foobar'
        n1.update()
        assert n1.description == 'foobar'
