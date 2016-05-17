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

from f5.multi_device.cluster import Cluster
from f5.multi_device.cluster.managers import DeviceGroupManager
import mock
import pytest


def test___init__():
    cm = Cluster(
        [mock.MagicMock(), mock.MagicMock],
        'cluster_name',
        'test_partition',
        'sync-failover')
    assert cm.partition == 'test_partition'
    assert cm.cluster_type == 'sync-failover'
    assert isinstance(cm.dgm, DeviceGroupManager)


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
