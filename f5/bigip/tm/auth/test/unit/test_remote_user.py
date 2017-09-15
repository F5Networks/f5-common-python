# Copyright 2017 F5 Networks Inc.
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
from f5.bigip.tm.auth.remote_user import Remote_User
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeRemoteUser():
    fake_remote_user = mock.MagicMock()
    return Remote_User(fake_remote_user)


def test_load_two(fakeicontrolsession):
    b = ManagementRoot('localhost', 'admin', 'admin')
    ru1 = b.tm.auth.remote_user.load()
    ru2 = b.tm.auth.remote_user.load()
    assert ru1 is not ru2


def test_create_raises(FakeRemoteUser):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeRemoteUser.create()
    assert str(EIO.value) == "Remote_User does not support the create method"


def test_delete_raises(FakeRemoteUser):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeRemoteUser.delete()
    assert str(EIO.value) == "Remote_User does not support the delete method"
