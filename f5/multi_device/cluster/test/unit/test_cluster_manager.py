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

from f5.bigip import ManagementRoot
from f5.multi_device.cluster import AlreadyManagingCluster
from f5.multi_device.cluster import ClusterManager
from f5.multi_device.cluster import ClusterNotSupported
from f5.multi_device.cluster import DeviceGroup
from f5.multi_device.cluster import NoClusterToManage

import mock
import pytest


class MockDeviceInfo(object):
    def __init__(self, name):
        self.name = name


@pytest.fixture
def BigIPs(fakeicontrolsession):
    mock_bigips = []
    for bigip in range(4):
        mock_bigips.append(ManagementRoot('test', 'un', 'pw'))
    return mock_bigips


@pytest.fixture
@mock.patch('f5.multi_device.cluster.DeviceGroup')
@mock.patch('f5.multi_device.cluster.TrustDomain')
def ClusterManagerCreateNew(mock_dg, mock_td):
    cm = ClusterManager()
    return cm


@pytest.fixture
@mock.patch('f5.multi_device.cluster.DeviceGroup.__init__', return_value=None)
@mock.patch('f5.multi_device.cluster.TrustDomain.__init__', return_value=None)
def ClusterManagerExisting(mock_dg, mock_td, BigIPs):
    mock_bigips = BigIPs
    cm = ClusterManager(
        devices=mock_bigips, device_group_name='name',
        device_group_partition='part',
        device_group_type='sync-failover')
    return cm, mock_bigips


@pytest.fixture
def FailoverClusterTwoBigIPs():
    mock_bigips = []
    for bigip in range(2):
        mock_bigips.append(ManagementRoot('test', 'un', 'pw'))
    cm = ClusterManager()
    cm.create(mock_bigips, 'cluster_name', 'part', 'sync-failover')
    return cm, mock_bigips


@pytest.fixture
def SyncOnlyCluster():
    mock_bigips = []
    for bigip in range(8):
        mock_bigips.append(ManagementRoot('test', 'un', 'pw'))
    cm = ClusterManager(
        mock_bigips, 'cluster_name', 'part', 'sync-only')
    return cm, mock_bigips


def test___init__existing_cluster(ClusterManagerExisting):
    cm, mock_bigips = ClusterManagerExisting
    assert cm.cluster.device_group_partition == 'part'
    assert cm.cluster.device_group_type == 'sync-failover'
    assert cm.cluster.device_group_name == 'name'
    assert cm.cluster.devices == mock_bigips
    assert isinstance(cm.device_group, DeviceGroup)


def test_no_cluster_to_manage():
    with pytest.raises(NoClusterToManage) as ex:
        cm = ClusterManager()
        cm.cluster
    assert 'The ClusterManager is not managing a cluster.' == ex.value.message


def test_already_managing_cluster(ClusterManagerExisting):
    cm, mock_bigips = ClusterManagerExisting
    with pytest.raises(AlreadyManagingCluster) as ex:
        cm.create(test='test')
    assert 'The ClusterManager is already managing a cluster.' == \
        ex.value.message


def test__init__bad_cluster_number():
    with pytest.raises(ClusterNotSupported) as ex:
        ClusterManager(
            devices=[mock.MagicMock()],
            device_group_name='cluster_name',
            device_group_partition='test_partition',
            device_group_type='sync-only')
    assert 'The number of devices to cluster is not supported.' \
        in ex.value.message


def test_create_cluster(ClusterManagerCreateNew, BigIPs):
    cm = ClusterManagerCreateNew
    mock_bigips = BigIPs
    cm.create(
        devices=mock_bigips,
        device_group_name='cluster_name',
        device_group_partition='test_partition',
        device_group_type='sync-failover')
    assert cm.trust_domain.create.call_args == \
        mock.call(devices=mock_bigips, partition='test_partition')
    assert cm.device_group.create.call_args == \
        mock.call(devices=mock_bigips,
                  device_group_name='cluster_name',
                  device_group_partition='test_partition',
                  device_group_type='sync-failover')
    assert cm.cluster.devices == mock_bigips
    assert cm.cluster.device_group_partition == 'test_partition'
    assert cm.cluster.device_group_name == 'cluster_name'
    assert cm.cluster.device_group_type == 'sync-failover'


def test_teardown_cluster(ClusterManagerCreateNew, BigIPs):
    cm = ClusterManagerCreateNew
    mock_bigips = BigIPs
    cm.create(
        devices=mock_bigips,
        device_group_name='cluster_name',
        device_group_partition='test_partition',
        device_group_type='sync-failover')
    cm.teardown()
    assert cm.device_group.teardown.call_args == mock.call()
    assert cm.trust_domain.teardown.call_args == mock.call()
    assert cm.cluster is None


def itest_scale_up_too_many_devices(ClusterManagerCreateNew, BigIPs):
    cm = ClusterManagerCreateNew
    mock_bigips = BigIPs
    cm.create(
        devices=mock_bigips, device_group_name='name',
        device_group_partition='part', device_group_type='sync-failover')
    mock_bigip1 = mock.MagicMock()
    cm.scale_up_by_one(mock_bigip1)
    mock_bigip2 = mock.MagicMock()
    cm.scale_up_by_one(mock_bigip2)
    mock_bigip3 = mock.MagicMock()
    cm.scale_up_by_one(mock_bigip3)
    mock_bigip4 = mock.MagicMock()
    cm.scale_up_by_one(mock_bigip4)
    with pytest.raises(ClusterNotSupported) as ex:
        cm.scale_up_by_one(mock.MagicMock())
    assert sorted(cm.cluster.devices) == sorted(mock_bigips)
    assert 'The number of devices to cluster is not supported.' == \
        ex.value.message


def itest_scale_down_cluster_not_supported(ClusterManagerCreateNew, BigIPs):
    cm = ClusterManagerCreateNew
    mock_bigips = BigIPs
    cm.create(
        devices=mock_bigips, device_group_name='name',
        device_group_partition='part', device_group_type='sync-failover')
    cm.scale_down_by_one(mock_bigips[0])
    assert cm.cluster.devices == mock_bigips
    cm.scale_down_by_one(mock_bigips[0])
    with pytest.raises(ClusterNotSupported) as ex:
        cm.scale_down_by_one(mock_bigips[0])
    assert 'The number of devices to cluster is not supported.' == \
        ex.value.message
