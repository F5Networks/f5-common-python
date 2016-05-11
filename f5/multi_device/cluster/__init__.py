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
from f5.multi_device.cluster.managers import DeviceGroupManager as dgm
from f5.multi_device.cluster.managers import TrustedPeerManager as peer_mgr


class ClusterNotSupported(Exception):
    pass


class RootRemovalNotSupported(Exception):
    pass


class Cluster(DeviceMixin):
    '''Manage a cluster of BigIPs.

    This is accomplished with REST URI calls only, but some operations are
    only permitted via tmsh commands (such as adding cm/trust-domain peers).
    We get around this issue by deploying iApps (sys/application).
    '''

    available_cluster_types = ['sync-only', 'sync-failover']

    def __init__(self, bigips, cluster_name, partition, cluster_type):
        '''Initialize a cluster manager object.

        :param bigips: list -- list of bigip ojects to cluster
        :param cluster_name: str -- name of device service group
        :param partition: str -- partition to deploy cluster to
        :param cluster_type: str -- type of cluster configuration
        '''

        if len(bigips) < 2 or len(bigips) > 8:
            msg = 'The number of devices to cluster is not supported.'
            raise ClusterNotSupported(msg)
        elif cluster_type not in self.available_cluster_types:
            msg = 'Unsupported cluster type was given: %s' % cluster_type
            raise ClusterNotSupported(msg)

        self.bigips = bigips[:]
        self.root_bigip = bigips[0]
        self.peers = bigips[1:]
        self.cluster_name = cluster_name
        self.partition = partition
        self.cluster_type = cluster_type
        self.dgm = dgm(
            cluster_name, self.root_bigip, bigips[:], partition, cluster_type
        )
        self.peer_mgr = peer_mgr('Root', partition)

    def create_cluster(self):
        '''Create a cluster of BigIP devices.'''

        print('Checking state of devices to be clustered...')
        self.dgm.check_devices_active_licensed()
        print('Adding trusted peers to root BigIP...')
        self.peer_mgr.add_trusted_peers(self.root_bigip, self.peers)
        print('Creating device group...')
        self.dgm.create_device_group()

    def teardown_cluster(self):
        '''Teardown the cluster of BigIP devices.'''

        print('Tearing down the cluster...')
        self.dgm.teardown_device_group()
        for bigip in self.bigips:
            self.peer_mgr.remove_trusted_peers(bigip)

    def scale_up_cluster(self, bigip):
        '''Scale cluster up by one device.

        :param bigip: bigip object -- bigip to add
        :raises: ClusterNotSupported
        '''

        if len(self.bigips) == 8:
            msg = 'The number of devices to cluster is not supported.'
            raise ClusterNotSupported(msg)
        print('Scaling cluster up by one device...')
        self.peer_mgr.add_trusted_peers(self.root_bigip, [bigip])
        self.dgm.scale_up_device_group(bigip)
        self.bigips.append(bigip)
        self.dgm.check_device_group_status()

    def scale_down_cluster(self, bigip):
        '''Scale cluster down by one device.

        :param bigip: bigip object -- bigip to delete
        :raises: ClusterNotSupported
        '''

        if len(self.bigips) < 3:
            msg = 'The number of devices to cluster is not supported.'
            raise ClusterNotSupported(msg)
        bigip_name = self.get_device_info(bigip).name
        root_name = self.get_device_info(self.root_bigip).name
        if bigip_name == root_name:
            msg = 'Removing trusted root device is not currently supported.'
            raise RootRemovalNotSupported(msg)
        print('Scaling cluster down by one device...')
        self.dgm.scale_down_device_group(bigip)
        self.peer_mgr.remove_trusted_peers(self.root_bigip, bigip)
        self.dgm.cleanup_scaled_down_device(bigip)
        self.peer_mgr.remove_trusted_peers(bigip)
        self.bigips.remove(bigip)
        self.dgm.check_device_group_status()
