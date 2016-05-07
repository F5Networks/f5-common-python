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


class DeviceGroupOperationNotSupported(Exception):
    pass


class UnexpectedClusterState(Exception):
    pass


class DeviceGroupManager(DeviceMixin):
    '''Class to manage device service group.'''

    sync_status_entry = 'https://localhost/mgmt/tm/cm/sync-status/0'

    def __init__(self, dg_name, root_device, devices, partition, dg_type):
        '''Initialize a device group manager.

        :param dg_name:
        :param root_device:
        :param devices:
        :param partition:
        :param dg_type:
        '''

        self.device_group_name = dg_name
        self.partition = partition
        self.root_device = root_device
        self.devices = devices[:]
        self.device_group_type = dg_type
        if dg_type == 'sync-only' and partition == 'Common':
            msg = 'Attempted to create sync-only device group in the Common ' \
                'partition. This is not supported.'
            raise DeviceGroupOperationNotSupported(msg)

    def create_device_group(self):
        '''Create the device service cluster group and add devices to it.'''

        self._check_all_devices_in_sync()
        dg = self.root_device.tm.cm.device_groups.device_group
        dg.create(
            name=self.device_group_name,
            partition=self.partition,
            type=self.device_group_type
        )
        for device in self.devices:
            self._add_device_to_device_group(device)
            device.tm.sys.config.save()
        self.check_device_group_status()

    def check_device_group_status(self):
        '''Check if the device group status based on the cluster type'''
        if self.device_group_type == 'sync-failover':
            self._ensure_active_standby()
        elif self.device_group_type == 'sync-only':
            self.check_devices_active_licensed()
        self._ensure_all_devices_in_sync()

    def scale_up_device_group(self, device):
        '''Scale device group up by one device

        :param device: bigip object -- device to add to device group
        '''

        device_info = self.get_device_info(device)
        if device_info.name in self._get_device_names_in_group():
            msg = 'The following device is already a member of the device ' \
                'group: %s' % device_info.name
            raise DeviceGroupOperationNotSupported(msg)
        self._check_device_failover_status(device, 'In Sync')
        self._add_device_to_device_group(device)
        device.tm.sys.config.save()
        self.devices.append(device)
        self.check_device_group_status()

    def scale_down_device_group(self, device):
        '''Scale device group down by one device

        :param device: bigip object -- device to delete from device group
        '''

        device_info = self.get_device_info(device)
        if device_info.name not in self._get_device_names_in_group():
            msg = 'The following device is not a member of the device ' \
                'group: %s' % device_info.name
            raise DeviceGroupOperationNotSupported(msg)
        self._delete_device_from_device_group(device)
        device.tm.sys.config.save()
        self.devices.remove(device)
        self.check_device_group_status()

    def cleanup_scaled_down_device(self, device):
        '''Remove all devices from device group on orphaned device.

        :param device: bigip object -- device to cleanup
        '''

        dg = self._delete_all_devices_from_device_group(device)
        dg.delete()
        self.check_device_group_status()

    def teardown_device_group(self):
        '''Teardown device service cluster group.'''

        self.check_device_group_status()
        for device in self.devices:
            self._delete_device_from_device_group(device)
            self._ensure_device_active(device)
            self._ensure_all_devices_in_sync()
        dg = self._get_device_group(self.root_device)
        dg.delete()
        self.check_devices_active_licensed()
        self._check_all_devices_in_sync()
        self.check_devices_active_licensed()
        self._check_all_devices_in_sync()

    def _get_device_names_in_group(self):
        """_get_device_names_in_group

        :returns: list -- list of device names in group
        """

        device_names = []
        dg = self._get_device_group(self.root_device)
        members = dg.devices_s.get_collection()
        for member in members:
            device_names.append(member.name)
        return device_names

    def _get_device_group(self, device):
        '''Get the device group through a device.

        :param device: bigip object -- device
        :returns: tm.cm.device_groups.device_group object
        '''

        return device.tm.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )

    @pollster.poll_by_method
    def check_devices_active_licensed(self):
        '''All devices should be in an active/licensed state.

        :raises: UnexpectedClusterState
        '''

        if len(self._get_devices_by_activation_state('active')) != \
                len(self.devices):
            msg = "One or more devices was not in a 'Active' and licensed " \
                "state."
            raise UnexpectedClusterState(msg)

    @pollster.poll_by_method
    def _add_device_to_device_group(self, device):
        '''Add device to device service cluster group.

        :param device: bigip object -- device to add to group
        '''

        device_info = self.get_device_info(device)
        dg = self._get_device_group(device)
        dg.devices_s.devices.create(
            name=device_info.name, partition=self.partition
        )
        root_dg = self._get_device_group(self.root_device)
        root_dg.devices_s.devices.load(
            name=device_info.name, partition=self.partition
        )
        print('added following device to group: ' + device_info.name)

    def _delete_all_devices_from_device_group(self, device):
        '''Remove all devices from device service cluster group.

        :param device: bigip object -- device to clean
        '''

        dg = self._get_device_group(device)
        dg_devices = dg.devices_s.get_collection()
        for device in dg_devices:
            device.delete()
        return dg

    def _delete_device_from_device_group(self, device):
        '''Remove device from device service cluster group.

        :param device: bigip object -- device to delete from group
        '''

        device_info = self.get_device_info(device)
        dg = self._get_device_group(device)
        device_device = dg.devices_s.devices.load(
            name=device_info.name, partition=self.partition
        )
        device_device.delete()

    @pollster.poll_by_method
    def _ensure_device_active(self, device):
        '''Ensure a single device is in an active state

        :param device: bigip object -- device to inspect
        :raises: UnexpectedClusterState
        '''

        self._sync_to_group(device)
        act = device.tm.cm.devices.device.load(
            name=self.get_device_info(device).name,
            partition=self.partition
        )
        if act.failoverState != 'active':
            msg = "A device in the cluster was not in the 'Active' state."
            raise UnexpectedClusterState(msg)

    def _sync_to_group(self, device):
        '''Sync the device to the cluster group

        :param device: bigip object -- device to sync to group
        '''

        config_sync_cmd = 'config-sync to-group %s' % self.device_group_name
        device.tm.cm.exec_cmd('run', utilCmdArgs=config_sync_cmd)

    def _ensure_active_standby(self):
        """Ensure cluster is in active standby configuration."""

        self._sync_to_group(self.root_device)
        self._check_devices_in_standby()
        if not self._get_devices_by_activation_state('active'):
            msg = "Expected one device to be in 'Active' state."
            raise UnexpectedClusterState(msg)
        self._check_all_devices_in_sync()

    def _ensure_all_devices_in_sync(self):
        """Ensure all devices have 'In Sync' status are sync is done."""

        self._sync_to_group(self.root_device)
        self._check_all_devices_in_sync()

    @pollster.poll_by_method
    def _check_all_devices_in_sync(self):
        '''Wait until all devices have failover status of 'In Sync'.

        :raises: UnexpectedClusterState
        '''

        if len(self._get_devices_by_failover_status('In Sync')) != \
                len(self.devices):
            msg = "Expected all devices in group to have 'In Sync' status."
            raise UnexpectedClusterState(msg)

    @pollster.poll_by_method
    def _check_devices_in_standby(self):
        '''Wait until n-1 devices in 'standby' activation state.

        :raises: UnexpectedClusterState
        :returns: list -- devices in standby
        '''

        standbys = self._get_devices_by_activation_state('standby')
        if len(standbys) != (len(self.devices)-1):
            msg = "Expected n-1 devices to be in 'Standby' state."
            raise UnexpectedClusterState(msg)
        return standbys

    def _get_devices_by_failover_status(self, status):
        '''Get a list of devices by failover status.

        :param status: str -- status to filter the returned list of devices
        :returns: list -- list of devices that have the given status
        '''

        devices = []
        for device in self.devices:
            if (self._check_device_failover_status(device, status)):
                devices.append(device)
        return devices

    def _check_device_failover_status(self, device, status):
        '''Determine if a device has a specific failover status.

        :param status: str -- status to check against
        :returns: bool -- True is it has status, False otherwise
        '''

        sync_status = device.tm.cm.sync_status
        sync_status.refresh()
        current_status = (sync_status.entries[self.sync_status_entry]
                          ['nestedStats']['entries']['status']
                          ['description'])
        if status == current_status:
            return True
        return False

    def _get_devices_by_activation_state(self, state):
        '''Get a list of devices by activation statue.

        :param state: str -- state to filter the returned list of devices
        :returns: list -- list of devices that are in the given state
        '''

        bigips = []
        for bigip in self.devices:
            act = bigip.tm.cm.devices.device.load(
                name=self.get_device_info(bigip).name,
                partition=self.partition
            )
            if act.failoverState == state:
                bigips.append(bigip)
        return bigips


class TrustedPeerManager(DeviceMixin):
    '''Manages the trusted peers of a BigIP device.'''

    iapp_actions = {'definition': {'implementation': None, 'presentation': ''}}

    def __init__(self, trust_name, partition):
        '''Initialize a trusted peer manager object.

        :param trust_name: str -- name of trust to use
        :param partition: str -- partition to place trusted peers in
        '''

        self.trust_name = trust_name
        self.partition = partition
        self.peer_iapp_prefix = 'cluster_iapp'

    def reset_trust(self, bigip):
        '''Reset trust on all domains on the device.

        :param bigip: bigip object -- bigip on which to reset trust
        '''

        reset_trust_cmd = self._get_reset_trust_cmd()
        iapp_actions = self.iapp_actions.copy()
        iapp_actions['definition']['implementation'] = reset_trust_cmd
        self._deploy_iapp('reset_trust', iapp_actions, bigip)
        self._delete_iapp('reset_trust', bigip)

    def add_trusted_peers(self, root_bigip, peers):
        '''Add trusted peers to the root bigip device.

        :param root_bigip: bigip object -- device to add trusted peers to
        :param peers: list -- bigip objects to add to root device
        '''

        for peer in peers:
            self._modify_trusted_peer(peer, self._get_add_peer_cmd, root_bigip)

    def remove_trusted_peers(self, bigip, peer_to_remove=None):
        '''Remove all trusted peers, unless one is given explicitly.

        :param bigip: bigip object -- bigip to remove peers from
        :param peer_to_remove: bigip object -- single peer to remove
        '''

        tds = bigip.tm.cm.trust_domains.trust_domain.load(name=self.trust_name)
        bigip_info = self.get_device_info(bigip)
        peer_list = [dv for dv in tds.caDevices if bigip_info.name not in dv]
        if peer_to_remove:
            peer_name = self.get_device_info(peer_to_remove)
            peer_list = [peer for peer in peer_list if peer_name.name in peer]
        for peer in peer_list:
            peer_hostname = peer.replace('/%s/' % self.partition, '')
            self._modify_trusted_peer(
                peer_hostname, self._get_delete_peer_cmd, bigip
            )

    def _modify_trusted_peer(
            self, peer, mod_peer_func, deploy_bigip
    ):
        '''Modify a trusted peer device by deploying an iapp.


        :param peer: bigip object -- peer to modify
        :param mod_peer_func: function -- function to call to modify peer
        :param deploy_bigip: bigip object -- bigip on which to deploy the iapp
        '''

        iapp_name = '%s_peer' % (self.peer_iapp_prefix)
        mod_peer_cmd = mod_peer_func(peer)
        iapp_actions = self.iapp_actions.copy()
        iapp_actions['definition']['implementation'] = mod_peer_cmd
        self._deploy_iapp(iapp_name, iapp_actions, deploy_bigip)
        self._delete_iapp(iapp_name, deploy_bigip)

    def _delete_iapp(self, iapp_name, deploy_bigip):
        '''Delete an iapp service and template on the root device.

        :param iapp_name: str -- name of iapp
        :param deploy_bigip: bigip object -- where the iapp will be deleted
        '''

        iapp = deploy_bigip.tm.sys.applications
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
        :param deploy_bigip: bigip object -- bigip object where iapp will be
            created
        '''

        tmpl = deploy_bigip.tm.sys.applications.templates.template
        serv = deploy_bigip.tm.sys.applications.services.service
        tmpl.create(name=iapp_name, partition=self.partition, actions=actions)
        serv.create(
            name=iapp_name, partition=self.partition, template=iapp_name
        )

    def _get_add_peer_cmd(self, peer):
        '''Get tmsh command to add a trusted peer.

        :param peer: bigip object -- peer device
        :returns: str -- tmsh command to add trusted peer
        '''

        peer_device = self.get_device_info(peer)
        print('Adding following peer to root: %s' % peer_device.name)
        username = peer._meta_data['username']
        password = peer._meta_data['password']
        return 'tmsh::modify cm trust-domain Root ca-devices add ' \
            '\\{ %s \\} name %s username %s password %s' % (
                peer_device.managementIp, peer_device.name, username, password
            )

    def _get_delete_peer_cmd(self, peer_name):
        '''Get tmsh command to delete a trusted peer.

        :param peer: bigip object -- peer device
        :returns: str -- tmsh command to delete trusted peer
        '''

        return 'tmsh::modify cm trust-domain Root ca-devices delete ' \
            '\\{ %s \\}' % peer_name

    def _get_reset_trust_cmd(self):
        '''Get tmsh command to reset trust on all domains.

        :returns: str -- tmsh command to reset trust
        '''

        return 'tmsh::delete cm trust-domain all ' \
            'keep-current-certificate-authority'
