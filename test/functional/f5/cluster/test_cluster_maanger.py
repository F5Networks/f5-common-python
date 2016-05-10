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

from f5.bigip import BigIP
from f5.cluster.cluster_manager import ClusterManager
from f5.cluster.device_group_maanger import DeviceGroupManager as dgm


DEVICE_GROUP_NAME = 'testing_cluster'
PARTITION = 'Common'


def test_failover_cluster_management(symbols):
    a = BigIP(
        symbols.bigip[0].netloc,
        symbols.bigip[0].username,
        symbols.bigip[0].password)
    b = BigIP(
        symbols.bigip[1].netloc,
        symbols.bigip[1].username,
        symbols.bigip[1].password)
    c = BigIP(
        symbols.bigip[2].netloc,
        symbols.bigip[2].username,
        symbols.bigip[2].password)

    bigip_list = [a, b]
    dg = dgm(DEVICE_GROUP_NAME, PARTITION, a, bigip_list, 'sync-failover')
    cm = ClusterManager(
        bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-failover')

    cm.create_cluster()
    dg.check_device_group_status()

    cm.scale_cluster_up(c)
    bigip_list.append(c)
    dg.check_device_group_status()

    cm.scale_cluster_down(b)
    bigip_list.remove(b)
    dg.check_device_group_status()

    cm.teardown_cluster()


def test_sync_only_cluster_management(symbols):
    a = BigIP(
        symbols.bigip[0].netloc,
        symbols.bigip[0].username,
        symbols.bigip[0].password)
    b = BigIP(
        symbols.bigip[1].netloc,
        symbols.bigip[1].username,
        symbols.bigip[1].password)
    c = BigIP(
        symbols.bigip[2].netloc,
        symbols.bigip[2].username,
        symbols.bigip[2].password)

    bigip_list = [a, b]
    dg = dgm(DEVICE_GROUP_NAME, PARTITION, a, bigip_list, 'sync-only')
    cm = ClusterManager(
        bigip_list, DEVICE_GROUP_NAME, PARTITION, 'sync-only')

    cm.create_cluster()
    dg.check_device_group_status()

    cm.scale_cluster_up(c)
    bigip_list.append(c)

    dg.check_device_group_status()
    cm.scale_cluster_down(b)
    bigip_list.remove(b)
    dg.check_device_group_status()

    cm.teardown_cluster()
