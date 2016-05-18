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
from f5.multi_device.cluster import Cluster
from f5.multi_device.cluster import ClusterNotSupported
from f5.multi_device.cluster.managers import DeviceGroupManager
from f5.multi_device.cluster import RootRemovalNotSupported

import mock
import pytest


class MockDeviceInfo(object):
    def __init__(self, name):
        self.name = name


@pytest.fixture
def FailoverCluster():
    mock_bigips = []
    for bigip in range(4):
        mock_bigips.append(ManagementRoot('test', 'un', 'pw'))
    cluster = Cluster(
        mock_bigips, 'cluster_name', 'part', 'sync-failover')
    return cluster, mock_bigips


@pytest.fixture
def FailoverClusterTwoBigIPs():
    mock_bigips = []
    for bigip in range(2):
        mock_bigips.append(ManagementRoot('test', 'un', 'pw'))
    cluster = Cluster(
        mock_bigips, 'cluster_name', 'part', 'sync-failover')
    return cluster, mock_bigips


@pytest.fixture
def SyncOnlyCluster():
    mock_bigips = []
    for bigip in range(8):
        mock_bigips.append(ManagementRoot('test', 'un', 'pw'))
    cluster = Cluster(
        mock_bigips, 'cluster_name', 'part', 'sync-only')
    return cluster, mock_bigips


def test___init__():
    with mock.patch('f5.multi_device.cluster.dgm.__init__', return_value=None):
        mock_bigips = [mock.MagicMock(), mock.MagicMock()]
        cluster = Cluster(mock_bigips, 'name', 'part', 'sync-failover')
        assert cluster.dgm.__init__.call_args == mock.call(
            'name', mock_bigips[0], mock_bigips, 'part', 'sync-failover'
        )
    assert cluster.partition == 'part'
    assert cluster.cluster_type == 'sync-failover'
    assert isinstance(cluster.dgm, DeviceGroupManager)


def test__init__bad_cluster_type():
    with pytest.raises(Exception) as ex:
        Cluster(
            [mock.MagicMock(), mock.MagicMock],
            'cluster_name',
            'test_partition',
            'sync-bad-over')
    assert 'Unsupported cluster type was given: sync-bad-over' \
        in ex.value.message


def test__init__bad_cluster_number():
    with pytest.raises(Exception) as ex:
        Cluster(
            [mock.MagicMock()],
            'cluster_name',
            'test_partition',
            'sync-only')
    assert 'The number of devices to cluster is not supported.' \
        in ex.value.message


def test_create_cluster_failover(FailoverCluster):
    cluster, mock_bigips = FailoverCluster
    cluster.dgm = mock.MagicMock()
    cluster.peer_mgr = mock.MagicMock()
    cluster.create_cluster()
    assert cluster.dgm.check_devices_active_licensed.call_args == mock.call()
    assert cluster.peer_mgr.add_trusted_peers.call_args == \
        mock.call(cluster.root_bigip, cluster.peers)


def test_teardown_cluster_synconly(SyncOnlyCluster):
    cluster, mock_bigips = SyncOnlyCluster
    cluster.dgm = mock.MagicMock()
    cluster.peer_mgr = mock.MagicMock()
    cluster.create_cluster()
    cluster.teardown_cluster()
    assert cluster.dgm.teardown_device_group.call_args == mock.call()
    expected_call_list = []
    for bigip in mock_bigips:
        expected_call_list.append(mock.call(bigip))
    assert cluster.peer_mgr.remove_trusted_peers.call_args_list == \
        expected_call_list


def test_scale_up_cluster(FailoverCluster):
    cluster, mock_bigips = FailoverCluster
    cluster.dgm = mock.MagicMock()
    cluster.peer_mgr = mock.MagicMock()
    cluster.create_cluster()
    new_bigip = ManagementRoot('test', 'un', 'pw')
    cluster.scale_up_cluster(new_bigip)
    assert len(cluster.bigips) == len(mock_bigips) + 1
    assert cluster.peer_mgr.add_trusted_peers.call_args == \
        mock.call(cluster.root_bigip, [new_bigip])
    assert cluster.dgm.scale_up_device_group.call_args == mock.call(new_bigip)
    assert cluster.dgm.check_device_group_status.call_args == mock.call()


def test_scale_down_cluster(SyncOnlyCluster):
    cluster, mock_bigips = SyncOnlyCluster
    cluster.dgm = mock.MagicMock()
    cluster.peer_mgr = mock.MagicMock()
    cluster.create_cluster()
    scale_down_bigip = mock_bigips[3]
    with mock.patch('f5.multi_device.cluster.Cluster.get_device_info') as \
            mock_device_info:
        mock_device_info.side_effect = [
            MockDeviceInfo('root'), MockDeviceInfo('test')]
        cluster.scale_down_cluster(scale_down_bigip)
        assert cluster.get_device_info.call_args_list == \
            [mock.call(scale_down_bigip), mock.call(cluster.root_bigip)]
        assert cluster.dgm.scale_down_device_group.call_args == \
            mock.call(scale_down_bigip)
        assert cluster.peer_mgr.remove_trusted_peers.call_args_list == \
            [mock.call(cluster.root_bigip, scale_down_bigip),
             mock.call(scale_down_bigip)]
        assert cluster.dgm.cleanup_scaled_down_device.call_args == \
            mock.call(scale_down_bigip)
        assert cluster.dgm.check_device_group_status.call_args == mock.call()
        assert len(cluster.bigips) == len(mock_bigips) - 1


def test_scale_down_cluster_not_supported(FailoverClusterTwoBigIPs):
    cluster, mock_bigips = FailoverClusterTwoBigIPs
    cluster.dgm = mock.MagicMock()
    cluster.peer_mgr = mock.MagicMock()
    cluster.create_cluster()
    with pytest.raises(ClusterNotSupported) as ex:
        cluster.scale_down_cluster(mock_bigips[1])
    assert ex.value.message == \
        'The number of devices to cluster is not supported.'


def test_scale_down_cluster_root_removal_not_supported(SyncOnlyCluster):
    cluster, mock_bigips = SyncOnlyCluster
    cluster.dgm = mock.MagicMock()
    cluster.peer_mgr = mock.MagicMock()
    cluster.create_cluster()
    with mock.patch('f5.multi_device.cluster.Cluster.get_device_info'):
        with pytest.raises(RootRemovalNotSupported) as ex:
            cluster.scale_down_cluster(mock_bigips[0])
        assert ex.value.message == \
            'Removing trusted root device is not currently supported.'
