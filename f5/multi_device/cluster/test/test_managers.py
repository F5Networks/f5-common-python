# Copyright 2016 F5 Networks Inc.

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
#

from f5.multi_device.cluster.managers import DeviceGroupManager
from f5.multi_device.cluster.managers import DeviceGroupOperationNotSupported
from f5.multi_device.cluster.managers import UnexpectedClusterState

import mock
import pytest


CLASS_LOC = 'f5.multi_device.cluster.managers.DeviceGroupManager'


class FakeActDevice(object):
    def __init__(self, state):
        self.failoverState = state


class FakeDeviceInfo(object):
    def __init__(self, name='test'):
        self.name = name


@pytest.fixture
def SetupThreeDevices():
    root_device = mock.MagicMock()
    devices = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]
    return root_device, devices


@pytest.fixture
def SetupSyncFailover(SetupThreeDevices):
    root_device, devices = SetupThreeDevices
    dgm = DeviceGroupManager(
        'dg_name', root_device, devices, 'part', 'sync-failover')
    return root_device, devices, dgm


@pytest.fixture
def DGMSyncFailover(SetupSyncFailover):
    root_device, devices, dgm = SetupSyncFailover
    dgm.get_device_info = mock.MagicMock(return_value=FakeDeviceInfo())
    dgm._get_devices_by_activation_state = mock.MagicMock(
        return_value=['one', 'two'])
    dgm._get_devices_by_failover_status = mock.MagicMock(
        return_value=['one', 'two', 'three'])
    return dgm, root_device, devices


@pytest.fixture
def DGMSyncOnly(SetupThreeDevices):
    root_device, devices = SetupThreeDevices
    dgm = DeviceGroupManager(
        'dg_name', root_device, devices, 'part', 'sync-only')
    device_info_mock = mock.MagicMock(return_value=FakeDeviceInfo())
    dgm.get_device_info = device_info_mock
    return dgm, root_device, devices


@pytest.fixture
def SyncFailoverScaleUp(DGMSyncFailover):
    dgm, root_device, devices = DGMSyncFailover
    # After cluster has been scaled up, ensure one more device in in
    # standby state
    dgm._get_devices_by_activation_state = mock.MagicMock(
        return_value=['one', 'two', 'three'])
    # And ensure all new devices in sync
    dgm._get_devices_by_failover_status = mock.MagicMock(
        return_value=['one', 'two', 'three', 'four'])
    return dgm, root_device, devices


def test___init__(DGMSyncOnly):
    dgm, root_device, devices = DGMSyncOnly
    assert dgm.device_group_name == 'dg_name'
    assert dgm.partition == 'part'
    assert dgm.root_device == root_device
    assert dgm.devices == devices
    assert dgm.device_group_type == 'sync-only'


def test_create_device_group(DGMSyncFailover):
    dgm, root_device, devices = DGMSyncFailover
    with mock.patch(CLASS_LOC + '._check_all_devices_in_sync'):
        dgm.create_device_group()
        assert dgm.root_device.tm.cm.device_groups.device_group.create.\
            call_args == mock.call(
                name='dg_name', partition='part', type='sync-failover')


def test_create_device_group_sync_only_in_common(DGMSyncOnly):
    root_device = mock.MagicMock()
    devices = [mock.MagicMock(), mock.MagicMock(), mock.MagicMock()]
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        DeviceGroupManager(
            'dg_name', root_device, devices, 'Common', 'sync-only')
    assert 'Attempted to create sync-only device group in the Common ' \
        'partition. This is not supported.' == ex.value.message


def test_scale_up_device_group_already_member(DGMSyncOnly):
    new_device = mock.MagicMock()
    dgm, root_device, devices = DGMSyncOnly
    dgm.get_device_info.return_value = FakeDeviceInfo()
    dgm._get_device_names_in_group = mock.MagicMock(
        return_value=['test1', 'test2', 'test'])
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        dgm.scale_up_device_group(new_device)
    assert 'The following device is already a member of the device ' \
        'group: test' == ex.value.message


def test_scale_down_device_group_not_member(DGMSyncFailover):
    new_device = mock.MagicMock()
    dgm, root_device, devices = DGMSyncFailover
    dgm._get_device_names_in_group = mock.MagicMock(
        return_value=['test1', 'test2', 'test3'])
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        dgm.scale_down_device_group(new_device)
    assert 'The following device is not a member of the device group:' in \
        ex.value.message


def test_check_devices_active_licensed_unexpected(SetupSyncFailover):
    root_device, devices, dgm = SetupSyncFailover
    dgm._get_devices_by_activation_state = mock.MagicMock(return_value=['one'])
    with pytest.raises(UnexpectedClusterState) as ex:
        dgm.check_devices_active_licensed()
    assert ex.value.message == \
        "One or more devices was not in a 'Active' and licensed state."


def test__ensure_device_active_unexpected(SetupSyncFailover):
    root_device, devices, dgm = SetupSyncFailover
    root_device.tm.cm.devices.device.load.return_value = FakeActDevice('no')
    dgm.get_device_info = mock.MagicMock()
    with pytest.raises(UnexpectedClusterState) as ex:
        dgm._ensure_device_active(root_device)
    assert ex.value.message == \
        "A device in the cluster was not in the 'Active' state."


def test__check_devices_in_standby_unexpected(SetupSyncFailover):
    root_device, devices, dgm = SetupSyncFailover
    dgm._get_devices_by_activation_state = mock.MagicMock(
        return_value=['one'])
    with pytest.raises(UnexpectedClusterState) as ex:
        dgm._check_devices_in_standby()
    assert "Expected n-1 devices to be in 'Standby' state." == \
        ex.value.message


def test__ensure_active_standby_unexpected(SetupSyncFailover):
    root_device, devices, dgm = SetupSyncFailover
    # The side effect here creates a list of return values. The first call
    # call for standby devices returns n-1 devices in standby.
    # The second call for active devices returns no active devices, thus
    # exciting the exception we expect.
    dgm._get_devices_by_activation_state = mock.MagicMock(
        side_effect=[['one', 'two'], []])
    with pytest.raises(UnexpectedClusterState) as ex:
        dgm._ensure_active_standby()
    assert ex.value.message == \
        "Expected one device to be in 'Active' state."


def test__check_all_devices_in_sync_unexpected(SetupSyncFailover):
    root_device, devices, dgm = SetupSyncFailover
    dgm._get_devices_by_failover_status = mock.MagicMock(
        return_value=['one', 'two'])
    with pytest.raises(UnexpectedClusterState) as ex:
        dgm._check_all_devices_in_sync()
    assert "Expected all devices in group to have 'In Sync' status." == \
        ex.value.message
