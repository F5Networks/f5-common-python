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

from f5.bigip.mixins import UnsupportedMethod
from f5.iworkflow.shared.identified_devices.config.device_info \
    import Device_Info


@pytest.fixture
def FakeDeviceInfo():
    fake_dev = mock.MagicMock()
    return Device_Info(fake_dev)


def test_create_raises(FakeDeviceInfo):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeDeviceInfo.create()
    assert str(EIO.value) == "Device_Info does not support the create method"


def test_delete_raises(FakeDeviceInfo):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeDeviceInfo.delete()
    assert str(EIO.value) == "Device_Info does not support the delete method"
