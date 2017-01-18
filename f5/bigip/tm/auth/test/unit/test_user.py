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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.auth.user import User
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeUser():
    fake_user_s = mock.MagicMock()
    fake_user = User(fake_user_s)
    return fake_user


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('localhost', 'admin', 'admin')
        n1 = b.tm.auth.users.user
        n2 = b.tm.auth.users.user
        assert n1 is not n2

    def test_create_no_args(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create()

    def test_create_descriptiom(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create(description='description')

    def test_create_encrypted_password(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create(encryptedPassword='JGE#)$GJ#$G#')

    def test_create_partition_access(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create(partitionAccess='description')

    def test_create_prompt_for_password(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create(promptForPassword='bash')

    def test_create_shell(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create(shell='bash')
