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
from f5.common import pollster
from f5.managers.device_group_manager import DeviceGroupManager


class BigIPDeviceNotInExpectedState(Exception):
    pass


class ClusterNotSupported(Exception):
    pass


class UnexpectedBigIPState(Exception):
    pass


class ClusterManager(DeviceMixin):
    '''Manage a cluster of BigIPs.

    This is accomplished with REST URI calls only, but some operations are
    only permitted via tmsh commands (such as adding cm/trust-domain peers).
    We get around this issue by deploying iApps (sys/application).
    '''

    iapp_actions = {'definition': {'implementation': None, 'presentation': ''}}
    sync_status_entry = 'https://localhost/mgmt/tm/cm/sync-status/0'

    def __init__(self, bigips, cluster_name, partition, cluster_type):
        if len(bigips) > 8:
            raise ClusterNotSupported(
                'The number of devices to cluster is not supported.'
            )
        self.bigips = bigips
        self.root_bigip = self.bigips[0]
        self.peers = self.bigips[1:]
        self.cluster_name = cluster_name
        self.peer_iapp_prefix = 'cluster_iapp'
        self.partition = partition
        self.cluster_type = cluster_type
        self.device_group = DeviceGroupManager(
            cluster_name, self.root_bigip, partition
        )

    def create_bigip_cluster(self):
        '''Cluster the BigIP devices given.'''
        self._ensure_bigips_active_licensed()
        print('Creating cluster group...')
        self._create_device_cluster()
        if self.cluster_type == 'sync-failover':
            print('Ensure cluster has settled into active/standby...')
            self._devices_in_standby()
        elif self.cluster_type == 'sync-only':
            print('Ensure devices are all in sync and active...')
        self.root_bigip.cm.sync(self.cluster_name)
        self._all_devices_in_sync()

    def teardown_bigip_cluster(self):
        '''Teardown cluster of BigIP devices.'''

        if self.cluster_type == 'sync-failover':
            self._devices_in_standby()
        self.root_bigip.cm.sync(self.cluster_name)
        self.device_group.teardown_device_group(self.bigips)
        # remove other devices from each device
        for peer in self.peers:
            self._modify_trusted_peer(
                peer, self._get_delete_peer_command, peer
            )

    def _ensure_bigips_active_licensed(self):
        '''All devices should be in an active/licensed state.'''
        if len(self._get_bigips_by_activation_state('active')) != \
                len(self.bigips):
            raise BigIPDeviceNotInExpectedState(
                'One or more BigIP devices was not in a active/licensed state.'
            )

    def scale_cluster_up(self, bigip):
        '''Scale cluster up by one device.

        :param bigip: bigip object -- bigip to add
        '''

        if len(self.bigips) == 8:
            raise ClusterNotSupported(
                'The number of devices to cluster is not supported.'
            )
        self._modify_trusted_peer(
            bigip, self._get_add_peer_command, self.root_bigip
        )
        self.device_group.scale_up_device_group(bigip)
        self.bigips.append(bigip)

    def scale_cluster_down(self, bigip):
        '''Scale cluster down by one device.

        :param bigip: bigip object -- bigip to delete
        '''

        self.device_group.scale_down_device_group(bigip)
        self._modify_trusted_peer(
            bigip, self._get_delete_peer_command, self.root_bigip
        )
        self.bigips.remove(bigip)

    def _create_device_cluster(self):
        '''Deploy an iapp to add trusted peers, then create device group.'''

        for peer in self.peers:
            self._modify_trusted_peer(
                peer, self._get_add_peer_command, self.root_bigip
            )
        self._all_devices_in_sync()
        self.device_group.create_device_group(self.bigips, self.cluster_type)

    def _modify_trusted_peer(
            self, peer, mod_peer_func, deploy_bigip
    ):
        '''Modify a trusted peer device.

        :param peer: bigip object -- peer to modify
        :param mod_peer_func: function -- function to call to modify peer
        '''

        peer_info = self._get_device_info(peer)
        iapp_name = '%s_%s' % (self.peer_iapp_prefix, peer_info.name)
        mod_peer_cmd = mod_peer_func(peer)
        iapp_actions = self.iapp_actions.copy()
        iapp_actions['definition']['implementation'] = mod_peer_cmd
        self._deploy_iapp(iapp_name, iapp_actions, deploy_bigip)
        # Once the command has been run via the iapp, delete the iapp
        self._delete_iapp(iapp_name, deploy_bigip)

    @pollster.poll_by_method
    def _all_devices_in_sync(self):
        '''Wait until all devices have failover status of 'In Sync'.'''
        assert len(self._get_bigips_by_failover_status('In Sync')) == \
            len(self.bigips)

    @pollster.poll_by_method
    def _devices_in_standby(self):
        '''Wait until n-1 devices in 'standby' activation state.'''
        standby_bigips = \
            self._get_bigips_by_activation_state('standby')
        assert len(standby_bigips) == (len(self.bigips)-1)
        return standby_bigips

    def _get_bigips_by_failover_status(self, status):
        '''Get a list of bigips by failover status.'''
        bigips = []
        for bigip in self.bigips:
            sync_status = bigip.cm.sync_status
            sync_status.refresh()
            current_status = (sync_status.entries[self.sync_status_entry]
                              ['nestedStats']['entries']['status']
                              ['description'])
            if status == current_status:
                bigips.append(bigip)
        return bigips

    def _get_bigips_by_activation_state(self, state):
        '''Get a list of bigips by activation statue.'''
        bigips = []
        for bigip in self.bigips:
            act = bigip.cm.devices.device.load(
                name=self._get_device_info(bigip).name,
                partition=self.partition
            )
            if act.failoverState == state:
                bigips.append(bigip)
        return bigips

    def _delete_iapp(self, iapp_name, deploy_bigip):
        '''Delete an iapp service and template on the root device.

        :param iapp_name: str -- name of iapp
        '''

        iapp = deploy_bigip.sys.applications
        iapp_service = iapp.services.service.load(
            name=iapp_name, partition=self.partition
        )
        iapp_service.delete()
        iapp_template = iapp.templates.template.load(
            name=iapp_name, partition=self.partition
        )
        iapp_template.delete()

    def _deploy_iapp(self, iapp_name, actions, deploy_bigip):
        '''Deploy iapp on the root device.

        :param iapp_name: str -- name of iapp
        :param actions: dict -- actions definition of iapp sections
        '''

        tmpl = deploy_bigip.sys.applications.templates.template
        serv = deploy_bigip.sys.applications.services.service
        tmpl.create(name=iapp_name, partition=self.partition, actions=actions)
        serv.create(
            name=iapp_name, partition=self.partition, template=iapp_name
        )

    def _get_add_peer_command(self, peer):
        '''Get tmsh command to add a trusted peer.

        :param peer: bigip object -- peer device
        :returns: str -- tmsh command to add trusted peer
        '''

        peer_device = self._get_device_info(peer)
        add_peer_cmd = 'tmsh::modify cm trust-domain Root ca-devices add ' \
            '\\{{ {0} \\}} name {1} username admin password admin'.format(
                peer_device.managementIp, peer_device.name
            )
        return add_peer_cmd

    def _get_delete_peer_command(self, peer):
        '''Get tmsh command to delete a trusted peer.

        :param peer: bigip object -- peer device
        :returns: str -- tmsh command to delete trusted peer
        '''

        peer_device = self._get_device_info(peer)
        del_peer_cmd = 'tmsh::modify cm trust-domain Root ca-devices delete ' \
            '\\{ %s \\}' % peer_device.name
        return del_peer_cmd
