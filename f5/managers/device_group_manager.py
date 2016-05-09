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


class ClusterGroupNotSynced(Exception):
    pass


class UnexpectedClusterState(Exception):
    pass


class DeviceGroupManager(DeviceMixin):
    '''Class to manage device service group.'''

    sync_status_entry = 'https://localhost/mgmt/tm/cm/sync-status/0'

    def __init__(self, dg_name, root_device, devices, partition, dg_type):
        '''Initialize a cluster object.'''

        self.device_group_name = dg_name
        self.partition = partition
        self.root_device = root_device
        self.devices = devices[:]
        self.device_group_type = dg_type

    def create_device_group(self):
        '''Create the device service cluster group and add devices to it.'''

        self._all_devices_in_sync()
        dg = self.root_device.cm.device_groups.device_group
        dg.create(
            name=self.device_group_name,
            partition=self.partition,
            type=self.device_group_type
        )
        for device in self.devices:
            self._add_device_to_device_group(device)
            device.sys.config.save()
        self.check_device_group_status()

    def check_device_group_status(self):
        if self.device_group_type == 'sync-failover':
            self._ensure_active_standby()
        elif self.device_group_type == 'sync-only':
            self.ensure_devices_active_licensed()
        self._ensure_all_devices_in_sync()

    def scale_up_device_group(self, device):
        '''Scale device group up by one device

        :param bigip: bigip object -- bigip to add to device group
        '''

        self._add_device_to_device_group(device)
        device.sys.config.save()
        self.devices.append(device)
        self.check_device_group_status()

    def scale_down_device_group(self, device):
        '''Scale device group down by one device

        :param bigip: bigip object -- bigip to delete from device group
        '''

        self._delete_device_from_device_group(device)
        device.sys.config.save()
        self.devices.remove(device)
        self.check_device_group_status()

    def teardown_device_group(self):
        '''Teardown device service cluster group.

        :param bigips: list -- bigip objects
        '''

        self.check_device_group_status()
        for device in self.devices:
            self._delete_device_from_device_group(device)
            self._ensure_device_active(device)
        dg = self.root_device.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        dg.delete()
        self.ensure_devices_active_licensed()
        self._all_devices_in_sync()

        for device in self.devices:
            try:
                dg = self._get_device_group(device)
            except Exception:
                continue
            else:
                dg.delete()
        self.ensure_devices_active_licensed()
        self._all_devices_in_sync()

    def _get_device_group(self, device):
        '''Get the device group through a device.

        :param device: bigip object -- device
        '''

        device_group = device.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        return device_group

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

    def _delete_device_from_device_group(self, device):
        '''Remove device from device service cluster group.

        :param bigip: bigip object -- device to delete from group
        '''

        device_info = self.get_device_info(device)
        dg = device.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        device_device = dg.devices_s.devices.load(
            name=device_info.name, partition=self.partition
        )
        device_device.delete()

    @pollster.poll_by_method
    def _ensure_device_active(self, device):
        device.cm.sync_to_group(self.device_group_name)
        act = device.cm.devices.device.load(
            name=self.get_device_info(device).name,
            partition=self.partition
        )
        if act.failoverState != 'active':
            raise UnexpectedClusterState(
                'A device in the cluster was not in the Active state.'
            )

    def _ensure_active_standby(self):
        self.root_device.cm.sync_to_group(self.device_group_name)
        self._devices_in_standby()
        if not self._get_devices_by_activation_state('active'):
            raise UnexpectedClusterState(
                'Expected one device to be active in this cluster.'
            )
        self._all_devices_in_sync()

    def _ensure_all_devices_in_sync(self):
        self.root_device.cm.sync_to_group(self.device_group_name)
        self._all_devices_in_sync()

    @pollster.poll_by_method
    def ensure_devices_active_licensed(self):
        '''All devices should be in an active/licensed state.'''

        if len(self._get_devices_by_activation_state('active')) != \
                len(self.devices):
            raise UnexpectedClusterState(
                'One or more BigIP devices was not in a active/licensed state.'
            )

    @pollster.poll_by_method
    def _all_devices_in_sync(self):
        '''Wait until all devices have failover status of 'In Sync'.'''

        if len(self._get_devices_by_failover_status('In Sync')) != \
                len(self.devices):
            raise UnexpectedClusterState(
                "Expected all devices in cluster to have 'In Sync' status."
            )

    @pollster.poll_by_method
    def _devices_in_standby(self):
        '''Wait until n-1 devices in 'standby' activation state.'''

        standby_bigips = \
            self._get_devices_by_activation_state('standby')
        if len(standby_bigips) != (len(self.devices)-1):
            raise UnexpectedClusterState(
                'Expected n-1 devices to be in standby state'
            )
        return standby_bigips

    def _get_devices_by_failover_status(self, status):
        '''Get a list of bigips by failover status.'''

        bigips = []
        for bigip in self.devices:
            sync_status = bigip.cm.sync_status
            sync_status.refresh()
            current_status = (sync_status.entries[self.sync_status_entry]
                              ['nestedStats']['entries']['status']
                              ['description'])
            if status == current_status:
                bigips.append(bigip)
        return bigips

    def _get_devices_by_activation_state(self, state):
        '''Get a list of bigips by activation statue.'''

        bigips = []
        for bigip in self.devices:
            act = bigip.cm.devices.device.load(
                name=self.get_device_info(bigip).name,
                partition=self.partition
            )
            if act.failoverState == state:
                bigips.append(bigip)
        return bigips
