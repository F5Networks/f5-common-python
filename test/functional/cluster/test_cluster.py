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
from f5.multi_device.cluster import ClusterManager

import pytest


DEVICE_GROUP_NAME = 'testing_cluster'
PARTITION = 'Common'
SYNCONLYPART = 'test'


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
        cm = ClusterManager(
            devices=bigip_list,
            device_group_name=DEVICE_GROUP_NAME,
            device_group_partition=PARTITION,
            device_group_type='sync-failover')
        cm.teardown()
    request.addfinalizer(teardown_cluster)


@pytest.fixture
def ThreeBigIPTeardownSyncFailover(request, BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b, c]

    def teardown_cluster():
        cm = ClusterManager(
            devices=bigip_list,
            device_group_name=DEVICE_GROUP_NAME,
            device_group_partition=PARTITION,
            device_group_type='sync-failover')
        cm.teardown()
    request.addfinalizer(teardown_cluster)


def test_new_failover_cluster_two_member(BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = ClusterManager()

    cm.create(
        devices=bigip_list,
        device_group_name=DEVICE_GROUP_NAME,
        device_group_partition=PARTITION,
        device_group_type='sync-failover')
    cm.teardown()


def test_new_failover_cluster_three_member(BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b, c]
    cm = ClusterManager()

    cm.create(
        devices=bigip_list,
        device_group_name=DEVICE_GROUP_NAME,
        device_group_partition=PARTITION,
        device_group_type='sync-failover')
    cm.teardown()


def test_existing_failover_cluster(BigIPSetup):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = ClusterManager()
    kwargs = {'devices': bigip_list,
              'device_group_name': DEVICE_GROUP_NAME,
              'device_group_partition': PARTITION,
              'device_group_type': 'sync-failover'}
    cm.create(**kwargs)

    del cm

    cm = ClusterManager(**kwargs)
    cm.teardown()


def test_scale_up_sync_failover(BigIPSetup, ThreeBigIPTeardownSyncFailover):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = ClusterManager()
    kwargs = {'devices': bigip_list,
              'device_group_name': DEVICE_GROUP_NAME,
              'device_group_partition': PARTITION,
              'device_group_type': 'sync-failover'}
    cm.create(**kwargs)
    cm.scale_up_by_one(c)


def test_scale_up_down_up_down_sync_failover(
        BigIPSetup, TwoBigIPTeardownSyncFailover):
    a, b, c = BigIPSetup
    bigip_list = [a, b]
    cm = ClusterManager()
    kwargs = {'devices': bigip_list,
              'device_group_name': DEVICE_GROUP_NAME,
              'device_group_partition': PARTITION,
              'device_group_type': 'sync-failover'}
    cm.create(**kwargs)
    for x in range(3):
        cm.scale_up_by_one(c)
        cm.scale_down_by_one(c)
