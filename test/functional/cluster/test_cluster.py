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
from f5.multi_device.cluster.managers import DeviceGroupOperationNotSupported

import pytest


DEVICE_GROUP_NAME = 'testing_cluster'
PARTITION = 'Common'


class FakeDeviceInfo(object):
    def __init__(self):
        self.name = 'test'


@pytest.fixture
def BigIPSetup(symbols):
    a = ManagementRoot(
        symbols.bigip1['netloc'],
        symbols.bigip1['username'],
        symbols.bigip1['password'])
    b = ManagementRoot(
        symbols.bigip2['netloc'],
        symbols.bigip2['username'],
        symbols.bigip2['password'])
    c = ManagementRoot(
        symbols.bigip3['netloc'],
        symbols.bigip3['username'],
        symbols.bigip3['password'])
    return a, b, c


@pytest.fixture
def TwoBigIPTeardownSyncFailover(request, BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b]

    def teardown_cluster():
        cm = Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')
        cm.teardown_cluster()
    request.addfinalizer(teardown_cluster)


@pytest.fixture
def ThreeBigIPTeardownSyncFailover(request, BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b, c]

    def teardown_cluster():
        cm = Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')
        cm.teardown_cluster()
    request.addfinalizer(teardown_cluster)


@pytest.fixture
def TwoBigIPTeardownSyncOnly(request, BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b]

    def teardown_cluster():
        cm = Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-only')
        cm.teardown_cluster()
    request.addfinalizer(teardown_cluster)


@pytest.fixture
def ThreeBigIPTeardownSyncOnly(request, BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b, c]

    def teardown_cluster():
        cm = Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-only')
        cm.teardown_cluster()
    request.addfinalizer(teardown_cluster)


def test_failover_cluster(BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = Cluster(
        bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')

    cm.create_cluster()
    cm.scale_up_cluster(c)
    bigip_list.append(c)
    cm.scale_down_cluster(c)
    bigip_list.remove(c)
    cm.scale_up_cluster(c)
    bigip_list.append(c)
    cm.teardown_cluster()


def test_sync_only_cluster_fail_in_common(BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-only')
    assert 'Attempted to create sync-only device group in the Common ' \
        'partition. This is not supported' in ex.value.message


def test_teardown_existing_cluster(BigIPSetup):
    for x in range(5):
        a, b, c = BigIPSetup
        bigip_list = [a, b, c]
        cm = Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')
        cm.create_cluster()
        del cm
        cm = Cluster(
            bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')
        cm.teardown_cluster()


def test_scale_up_with_existing_device(
        BigIPSetup, TwoBigIPTeardownSyncFailover):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = Cluster(
        bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')
    cm.create_cluster()
    with pytest.raises(DeviceGroupOperationNotSupported) as ex:
        cm.scale_up_cluster(b)
    assert 'The following device is already a member of the device group:' in \
        ex.value.message


def test_scale_up_down_up_down(BigIPSetup, TwoBigIPTeardownSyncFailover):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = Cluster(
        bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')
    cm.create_cluster()
    for x in range(10):
        cm.scale_up_cluster(c)
        cm.scale_down_cluster(c)
