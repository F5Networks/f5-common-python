# Copyright 2018 F5 Networks Inc.
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
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.sys.disk import Logical_Disk
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def fake_disk():
    fake_oc = mock.MagicMock()
    return Logical_Disk(fake_oc)


class TestDiskOC(object):
    def test_oc(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        d1 = b.tm.sys.disk
        assert isinstance(d1, OrganizingCollection)
        assert hasattr(d1, 'logical_disks')


class TestLogicalDisk(object):
    def test_logical_disk_update_raises(self, fake_disk):
        with pytest.raises(UnsupportedMethod) as EIO:
            fake_disk.update()
        assert str(EIO.value) == "Logical_Disk does not support the update method, only load and refresh"

    def test_logical_disk_create_raises(self, fake_disk):
        with pytest.raises(UnsupportedMethod) as EIO:
            fake_disk.create()
        assert str(EIO.value) == "Logical_Disk does not support the create method, only load and refresh"

    def test_logical_disk_modify_raises(self, fake_disk):
        with pytest.raises(UnsupportedMethod) as EIO:
            fake_disk.modify()
        assert str(EIO.value) == "Logical_Disk does not support the modify method, only load and refresh"

    def test_logical_disk_delete_raises(self, fake_disk):
        with pytest.raises(UnsupportedMethod) as EIO:
            fake_disk.delete()
        assert str(EIO.value) == "Logical_Disk does not support the delete method, only load and refresh"
