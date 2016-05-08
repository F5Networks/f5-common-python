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

from f5.bigip.mixins import DeviceMixin
from f5.managers.device_group_manager import DeviceGroupManager as dgm
from f5.managers.trusted_peer_manager import TrustedPeerManager as peer_mgr


class ClusterNotSupported(Exception):
    pass


class ClusterManager(DeviceMixin):
    '''Manage a cluster of BigIPs.

    This is accomplished with REST URI calls only, but some operations are
    only permitted via tmsh commands (such as adding cm/trust-domain peers).
    We get around this issue by deploying iApps (sys/application).
    '''

    def __init__(self, bigips, cluster_name, partition, cluster_type):
        if len(bigips) > 8:
            raise ClusterNotSupported(
                'The number of devices to cluster is not supported.'
            )
        self.bigips = bigips
        self.root_bigip = self.bigips[0]
        self.peers = self.bigips[1:]
        self.cluster_name = cluster_name
        self.partition = partition
        self.cluster_type = cluster_type
        self.dgm = dgm(
            cluster_name, self.root_bigip, bigips, partition, cluster_type
        )
        self.peer_mgr = peer_mgr('Root', partition)

    def create_cluster(self):
        print('Checking state of devices to be clustered...')
        self.dgm.ensure_devices_active_licensed()
        print('Adding trusted peers to root BigIP...')
        self.peer_mgr.add_trusted_peers(self.root_bigip, self.peers)
        print('Creating device group...')
        self.dgm.create_device_group()

    def teardown_cluster(self):
        self.dgm.teardown_device_group()
        for bigip in self.bigips:
            self.peer_mgr.remove_trusted_peers(bigip)

    def scale_cluster_up(self, bigip):
        '''Scale cluster up by one device.

        :param bigip: bigip object -- bigip to add
        '''

        if len(self.bigips) == 8:
            raise ClusterNotSupported(
                'The number of devices to cluster is not supported.'
            )
        print('Scaling cluster up by one device...')
        self.peer_mgr.add_trusted_peers(self.bigip_root, bigip)
        self.dgm.scale_up_device_group(bigip)
        self.bigips.append(bigip)
        self._sync_and_check_cluster_status()

    def scale_cluster_down(self, bigip):
        '''Scale cluster down by one device.

        :param bigip: bigip object -- bigip to delete
        '''

        # if scaling down the root, assign new root
        self.dgm.scale_down_device_group(bigip)
        self._modify_trusted_peer(
            bigip, self._get_delete_peer_command, self.root_bigip
        )
        self.bigips.remove(bigip)
        self.dgm._all_devices_in_sync()
        self.dgm.check_device_group_status()
