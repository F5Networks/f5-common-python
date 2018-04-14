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

from distutils.version import LooseVersion
from f5.sdk_exception import MissingRequiredCreationParameter
from requests.exceptions import HTTPError


pytestmark = pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release'))
    < LooseVersion('12.0.0'),
    reason='Needs v12 TMOS or greater to pass.'
)


@pytest.fixture(scope='function')
def users_link(mgmt_root):
    collection = mgmt_root.cm.system.authn.providers.tmos_s.get_collection()
    resource = collection[0]
    result = resource.attrs['usersReference']
    return result


@pytest.fixture(scope='function')
def token(mgmt_root, users_link):
    collection = mgmt_root.shared.authz.tokens_s
    resource = collection.token.create(
        token='T1234512345123451234512345',
        user=users_link
    )
    yield resource
    resource.delete()


@pytest.fixture(scope='function')
def user(mgmt_root):
    collection = mgmt_root.shared.authz.users_s
    resource = collection.user.create(name='user12345', password='f5pass12345')
    yield resource
    resource.delete()


class TestAuthz(object):
    def test_create(self, token):
        assert token.kind == 'shared:authz:tokens:authtokenitemstate'

    def test_load_no_token(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            collection = mgmt_root.shared.authz.tokens_s
            collection.token.load(
                name='asdasdasd'
            )
        assert err.value.response.status_code == 404

    def test_load(self, mgmt_root, token):
        collection = mgmt_root.shared.authz.tokens_s
        resource = collection.token.load(name=token.name)
        assert token.name == resource.name
        assert token.selfLink == resource.selfLink

    def test_exists(self, mgmt_root, token):
        name = str(token.name)
        collection = mgmt_root.shared.authz.tokens_s
        exists = collection.token.exists(name=name)
        assert exists is True

    def test_package_mgmt_tasks_collection(self, mgmt_root, token):
        col = mgmt_root.shared.authz.tokens_s.get_collection()
        assert isinstance(col, list)
        assert len(col) > 0

    def test_user_create(self, user):
        assert user.kind == 'shared:authz:users:usersworkerstate'

    def test_user_modify_password(self, mgmt_root, user):
        collection = mgmt_root.shared.authz.users_s
        resource = collection.user.load(name='user12345')
        if LooseVersion(pytest.config.getoption('--release')) > LooseVersion('12.1.0'):
            # In 12.x.x there were no 'encryptedPassword' parameter
            # on the response to shared/authz/users/user
            oldPasswd = resource.encryptedPassword
            resource.modify(name='user12345', password='f5site02')
            newPasswd = resource.encryptedPassword
            assert oldPasswd != newPasswd
        else:
            # In case of 12.x.x versions just make sure modify is not raising
            # any exceptions and the user still exists after modification
            resource.modify(name='user12345', password='f5site02')
            exists = collection.user.exists(name='user12345')
            assert exists is True

    def test_user_create_no_password(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            collection = mgmt_root.shared.authz.users_s
            collection.user.create(name='user12345')
