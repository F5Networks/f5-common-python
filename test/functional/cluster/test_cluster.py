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
from pytest import symbols


DEVICE_GROUP_NAME = 'testing_cluster'
PARTITION = 'Common'
SYNCONLYPART = 'test'


skip_cluster_tests = True
if hasattr(symbols, 'run_cluster_tests') and symbols.run_cluster_tests is True:
    skip_cluster_tests = False


class FakeDeviceInfo(object):
    def __init__(self):
        self.name = 'test'


@pytest.fixture
def BigIPSetup():
    a = ManagementRoot(
        symbols.bigip1['netloc'],
        symbols.bigip1['username'],
        symbols.bigip1['password'])
    b = ManagementRoot(
        symbols.bigip2['netloc'],
        symbols.bigip2['username'],
        symbols.bigip2['password'])
    return a, b


@pytest.fixture
def TwoBigIPTeardownSyncFailover(request, BigIPSetup):
    a, b = BigIPSetup
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
    a, b = BigIPSetup
    bigip_list = [a, b]

    def teardown_cluster():
        cm = ClusterManager(
            devices=bigip_list,
            device_group_name=DEVICE_GROUP_NAME,
            device_group_partition=PARTITION,
            device_group_type='sync-failover')
        cm.teardown()
    request.addfinalizer(teardown_cluster)


@pytest.mark.skipif(skip_cluster_tests,
                    reason="You must opt-in to run cluster tests. This "
                    "requires an additional device or possibly more. To "
                    "run them, set the symbols variable "
                    "'run_cluster_tests: True'")
class TestCluster(object):
    def test_new_failover_cluster_two_member(self, BigIPSetup):
        a, b = BigIPSetup
        bigip_list = [a, b]
        for x in range(5):
            cm = ClusterManager()

            cm.create(
                devices=bigip_list,
                device_group_name=DEVICE_GROUP_NAME,
                device_group_partition=PARTITION,
                device_group_type='sync-failover')
            cm.teardown()

    def test_existing_failover_cluster(self, BigIPSetup):
        a, b = BigIPSetup
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
