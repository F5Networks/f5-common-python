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

import mock
import pytest

from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.sys.snmp import Snmp
from f5.bigip.tm.sys.snmp import Trap
from f5.bigip.tm.sys.snmp import User
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeSnmp():
    fake_sys = mock.MagicMock()
    return Snmp(fake_sys)


@pytest.fixture
def FakeSnmpUser():
    fake_sys = mock.MagicMock()
    fake_user = User(fake_sys)
    fake_user._meta_data['bigip'].tmos_version = '12.1.0'
    return fake_user


@pytest.fixture
def FakeTrapUser():
    fake_sys = mock.MagicMock()
    fake_trap = Trap(fake_sys)
    fake_trap._meta_data['bigip'].tmos_version = '12.1.0'
    return fake_trap


def test_create_raises(FakeSnmp):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeSnmp.create()
    assert EIO.value.message == "Snmp does not support the create method"


def test_delete_raises(FakeSnmp):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeSnmp.delete()
    assert EIO.value.message == "Snmp does not support the delete method"


def test_update_user_raises(FakeSnmpUser):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeSnmpUser.update()
    assert EIO.value.message == "Update() is unsupported for User on " \
                                "version 12.1.0. " \
                                "Utilize Modify() method instead"


def test_update_trap_raises(FakeTrapUser):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeTrapUser.update()
    assert EIO.value.message == "Update() is unsupported for Trap on " \
                                "version 12.1.0. " \
                                "Utilize Modify() method instead"
