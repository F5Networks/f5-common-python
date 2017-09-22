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

from f5.bigip import ManagementRoot
from f5.bigip.tm.auth.remote_role import Remote_Role
from f5.bigip.tm.auth.remote_role import Role_Infos
from f5.sdk_exception import UnsupportedMethod

import mock
import pytest


@pytest.fixture
def FakeRemoteRole():
    fake_remote_role = mock.MagicMock()
    return Remote_Role(fake_remote_role)


def MakeRemoteRole(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    r = b.tm.auth.remote_role.load()
    return r


def test_load_two(fakeicontrolsession):
    b = ManagementRoot('localhost', 'admin', 'admin')
    s1 = b.tm.auth.remote_role.load()
    s2 = b.tm.auth.remote_role.load()
    assert s1 is not s2


def test_create_raises(FakeRemoteRole):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeRemoteRole.create()
    assert str(EIO.value) == "Remote_Role does not support the create method"


def test_delete_raises(FakeRemoteRole):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeRemoteRole.delete()
    assert str(EIO.value) == "Remote_Role does not support the delete method"


def test_role_info(fakeicontrolsession):
    ri = Role_Infos(MakeRemoteRole(fakeicontrolsession))
    assert ri.__class__.__name__ == 'Role_Infos'
