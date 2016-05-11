# Copyright 2015-2016 F5 Networks Inc.
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

from f5.multi_device.cluster import DeviceGroup
from f5.multi_device.cluster import DeviceGroupNotSupported
from f5.multi_device.cluster import DeviceGroupOperationNotSupported
from f5.multi_device.cluster import MissingRequiredDeviceGroupParameter
from f5.multi_device.cluster import UnexpectedDeviceGroupState
from f5.multi_device.cluster import UnexpectedDeviceGroupType

import mock
import pytest


class MockDeviceInfo(object):
    def __init__(self, name):
        self.name = name
        self.selfDevice = 'true'


class FakeActDevice(object):
    def __init__(self, state):
        self.failoverState = state


@pytest.fixture
def BigIPs():
    mock_bigips = []
    for bigip in range(4):
        mock_bigip = mock.MagicMock()
        mock_bigip.__name = 'me'
        mock_bigip.tm.cm.devices.get_collection.return_value = \
            [MockDeviceInfo('test')]
        mock_bigip.tm.cm.devices.get_collection.__name__ = 'test'
        mock_bigips.append(mock_bigip)
    return mock_bigips


@pytest.fixture
@mock.patch('f5.multi_device.cluster.DeviceGroup._check_all_devices_in_sync')
@mock.patch('f5.multi_device.cluster.pollster')
@mock.patch('f5.multi_device.cluster.DeviceGroup._add_device_to_device_group')
def DeviceGroupCreateNew(mock_sync, mock_poll, mock_add, BigIPs):
    mock_bigips = BigIPs
    dg = DeviceGroup()
    dg.create(
        devices=mock_bigips, device_group_name='test',
        device_group_partition='Common', device_group_type='sync-failover')
    return dg, mock_bigips


def test_missing_required_parameter(BigIPs):
    with pytest.raises(MissingRequiredDeviceGroupParameter) as ex:
        DeviceGroup(devices=BigIPs)
    assert 'device_group_name' in ex.value.message
    with pytest.raises(MissingRequiredDeviceGroupParameter) as ex:
        DeviceGroup(
            devices=BigIPs, device_group_name='test', device_group_type='test')
    assert 'device_group_partition' in ex.value.message


def test_validate_unsupported_type(BigIPs):
    with pytest.raises(DeviceGroupNotSupported) as ex:
        DeviceGroup(
            devices=BigIPs, device_group_name='test',
            device_group_type='wrong', device_group_partition='Common')
    assert 'Unsupported cluster type was given: wrong' == ex.value.message


def test_validate_type_mismatch(BigIPs):
    with pytest.raises(UnexpectedDeviceGroupType) as ex:
        with mock.patch(
                'f5.multi_device.cluster.DeviceGroup._get_device_group'
        ) as mock_dg_res:
            mock_dg_res().type = 'sync-only'
            DeviceGroup(
                devices=BigIPs, device_group_name='test',
                device_group_type='sync-failover',
                device_group_partition='part')
    assert "Device group type found: 'sync-only' does not match expected " \
        "device group type: 'sync-failover'" == ex.value.message


def test_scale_up_device_already_in_group(DeviceGroupCreateNew, BigIPs):
    dg, mock_bigips = DeviceGroupCreateNew
    mock_bigip = mock.MagicMock()
    mock_bigip.tm.cm.devices.get_collection.return_value = \
        [MockDeviceInfo('test')]
    mock_bigip.tm.cm.devices.get_collection.__name__ = 'test'
    dg.check_device_group_status = mock.MagicMock()
    mock_names_in_group = mock.MagicMock()
    mock_names_in_group.return_value = ['test']
    dg._get_device_names_in_group = mock_names_in_group
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        dg.scale_up(mock_bigip)
    assert "Device: 'test' is already in device group" == ex.value.message


def test_scale_down_device_not_in_group(DeviceGroupCreateNew, BigIPs):
    dg, mock_bigips = DeviceGroupCreateNew
    mock_bigip = mock.MagicMock()
    mock_bigip.tm.cm.devices.get_collection.return_value = \
        [MockDeviceInfo('test')]
    mock_bigip.tm.cm.devices.get_collection.__name__ = 'test'
    dg.check_device_group_status = mock.MagicMock()
    mock_names_in_group = mock.MagicMock()
    mock_names_in_group.return_value = ['no_match']
    dg._get_device_names_in_group = mock_names_in_group
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        dg.scale_down(mock_bigip)
    assert "Device: 'test' is not in device group" == ex.value.message


def test_check_devices_active_licensed_unexpected(DeviceGroupCreateNew):
    dg, mock_bigips = DeviceGroupCreateNew
    dg._get_devices_by_activation_state = mock.MagicMock(return_value=['one'])
    with pytest.raises(UnexpectedDeviceGroupState) as ex:
        dg._check_devices_active_licensed()
    assert ex.value.message == \
        "One or more devices not in 'Active' and licensed state."


def test__ensure_device_active_unexpected(DeviceGroupCreateNew):
    dg, mock_bigips = DeviceGroupCreateNew
    mock_bigips[0].tm.cm.devices.device.load.return_value = FakeActDevice('no')
    dg.get_device_info = mock.MagicMock()
    with pytest.raises(UnexpectedDeviceGroupState) as ex:
        dg._ensure_device_active(mock_bigips[0])
    assert ex.value.message == \
        "A device in the cluster was not in the 'Active' state."


def test__check_all_devices_in_sync_unexpected(DeviceGroupCreateNew):
    dg, mock_bigips = DeviceGroupCreateNew
    dg._get_devices_by_failover_status = mock.MagicMock(
        return_value=['one', 'two'])
    with pytest.raises(UnexpectedDeviceGroupState) as ex:
        dg._check_all_devices_in_sync()
    assert "Expected all devices in group to have 'In Sync' status." == \
        ex.value.message
