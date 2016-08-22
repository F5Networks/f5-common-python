# coding=utf-8
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

'''Class for managing a DeviceGroup for a set of BIG-IP® devices

Managing a device group for clustering is an event-driven process. Please
use the methods here to control that process. The fundamental idea is that
any action should have an observable outcome. Adding a device to the device
group should have a consequence for each member of the device group,
including the newly added member.

Examples:

There are two major use-cases here:

    * Manage an existing device group:

        list_of_bigips = [ManagementRoot(...), ManagementRoot(...)]
        device_group = DeviceGroup(
                            devices=list_of_bigips,
                            device_group_name='my_cluster',
                            device_group_type='sync-failover',
                            device_group_partition='Common'
                        )
        device_group.ensure_all_devices_in_sync()

    * Create a new device group and manage it:

        list_of_bigips = [ManagementRoot(...), ManagementRoot(...)]
        device_group = DeviceGroup()
        device_group.create(
                        devices=list_of_bigips,
                        device_group_name='my_cluster',
                        device_group_type='sync-failover',
                        device_group_partition='Common'
                    )
        device_group.ensure_all_devices_in_sync()

Methods:

    * create -- create a device group from a list of devices
    * teardown -- teardown a device group, but leave the trust domain intact
    * validate -- ensure a device group is in the proper state based on inputs
    * manage_extant -- manage an existing device group

'''
from __future__ import print_function

from f5.multi_device.exceptions import DeviceGroupNotSupported
from f5.multi_device.exceptions import MissingRequiredDeviceGroupParameter
from f5.multi_device.exceptions import UnexpectedDeviceGroupDevices
from f5.multi_device.exceptions import UnexpectedDeviceGroupState
from f5.multi_device.exceptions import UnexpectedDeviceGroupType

from f5.multi_device.utils import get_device_info
from f5.multi_device.utils import pollster


class DeviceGroup(object):
    '''Class to manage device service group

    For the non-public methods, there are a few flavors of behavior:
    get, check, and ensure. A 'get' retrieves some info from the device
    without any assumptions about that info. A 'check' will assert a device's
    info is as expected. An 'ensure' method often does one or more of the
    above and also may take some other action to enforce the expected state,
    such as syncing config.

    The pollster is used heavliy here for 'check' and 'get' methods, since we
    are often waiting for the device or devices to respond to some action.

    Example:

        * dg = self._get_device_group()
        * self._check_all_devices_in_sync()
        * self.ensure_all_devices_in_sync()

    '''

    available_types = ['sync-failover', 'sync-only']
    sync_status_entry = 'https://localhost/mgmt/tm/cm/sync-status/0'

    def __init__(self, **kwargs):
        '''Initialize a device group manager.

        '''

        if kwargs:
            self.manage_extant(**kwargs)

    def _set_attributes(self, **kwargs):
        '''Set instance attributes based on kwargs

        :param kwargs: dict -- kwargs to set as attributes
        '''

        try:
            self.devices = kwargs['devices'][:]
            self.name = kwargs['device_group_name']
            self.type = kwargs['device_group_type']
            self.partition = kwargs['device_group_partition']
        except KeyError as ex:
            raise MissingRequiredDeviceGroupParameter(ex)

    def validate(self, **kwargs):
        '''Validate device group state among given devices.

        :param kwargs: dict -- keyword args of device group information
        :raises: UnexpectedDeviceGroupType, UnexpectedDeviceGroupDevices
        '''

        self._set_attributes(**kwargs)
        self._check_type()
        self.dev_group_uri_res = self._get_device_group(self.devices[0])
        if self.dev_group_uri_res.type != self.type:
            msg = 'Device group type found: %r does not match expected ' \
                'device group type: %r' % (
                    self.dev_group_uri_res.type, self.type
                )
            raise UnexpectedDeviceGroupType(msg)
        queried_device_names = self._get_device_names_in_group()
        given_device_names = []
        for device in self.devices:
            device_name = get_device_info(device).name
            given_device_names.append(device_name)
        if sorted(queried_device_names) != sorted(given_device_names):
            msg = 'Given devices does not match queried devices.'
            raise UnexpectedDeviceGroupDevices(msg)
        self.ensure_all_devices_in_sync()

    def _check_type(self):
        '''Check that the device group type is correct.

        :raises: DeviceGroupOperationNotSupported, DeviceGroupNotSupported
        '''

        if self.type not in self.available_types:
            msg = 'Unsupported cluster type was given: %s' % self.type
            raise DeviceGroupNotSupported(msg)
        elif self.type == 'sync-only' and self.name != 'device_trust_group':
            msg = "Management of sync-only device groups only supported for " \
                "built-in device group named 'device_trust_group'"
            raise DeviceGroupNotSupported(msg)

    def manage_extant(self, **kwargs):
        self.validate(**kwargs)

    def create(self, **kwargs):
        '''Create the device service cluster group and add devices to it.'''

        self._set_attributes(**kwargs)
        self._check_type()
        pollster(self._check_all_devices_in_sync)()
        dg = self.devices[0].tm.cm.device_groups.device_group
        dg.create(name=self.name, partition=self.partition, type=self.type)
        for device in self.devices:
            self._add_device_to_device_group(device)
            device.tm.sys.config.exec_cmd('save')
        self.ensure_all_devices_in_sync()

    def teardown(self):
        '''Teardown device service cluster group.'''

        self.ensure_all_devices_in_sync()
        for device in self.devices:
            self._delete_device_from_device_group(device)
            self._sync_to_group(device)
            pollster(self._ensure_device_active)(device)
            self.ensure_all_devices_in_sync()
        dg = pollster(self._get_device_group)(self.devices[0])
        dg.delete()
        pollster(self._check_devices_active_licensed)()
        pollster(self._check_all_devices_in_sync)()

    def _get_device_names_in_group(self):
        '''_get_device_names_in_group

        :returns: list -- list of device names in group
        '''

        device_names = []
        dg = pollster(self._get_device_group)(self.devices[0])
        members = dg.devices_s.get_collection()
        for member in members:
            member_name = member.name.replace('/%s/' % self.partition, '')
            device_names.append(member_name)
        return device_names

    def _get_device_group(self, device):
        '''Get the device group through a device.

        :param device: bigip object -- device
        :returns: tm.cm.device_groups.device_group object
        '''

        return device.tm.cm.device_groups.device_group.load(
            name=self.name, partition=self.partition
        )

    def _check_devices_active_licensed(self):
        '''All devices should be in an active/licensed state.

        :raises: UnexpectedClusterState
        '''

        if len(self._get_devices_by_activation_state('active')) != \
                len(self.devices):
            msg = "One or more devices not in 'Active' and licensed state."
            raise UnexpectedDeviceGroupState(msg)

    def _add_device_to_device_group(self, device):
        '''Add device to device service cluster group.

        :param device: bigip object -- device to add to group
        '''

        device_name = get_device_info(device).name
        dg = pollster(self._get_device_group)(device)
        print('Adding following device to group: ' + device_name)
        dg.devices_s.devices.create(name=device_name, partition=self.partition)
        pollster(self._check_device_exists_in_device_group)(device_name)

    def _check_device_exists_in_device_group(self, device_name):
        '''Check whether a device exists in the device group

        :param device: ManagementRoot object -- device to look for
        '''

        dg = self._get_device_group(self.devices[0])
        dg.devices_s.devices.load(name=device_name, partition=self.partition)

    def _delete_device_from_device_group(self, device):
        '''Remove device from device service cluster group.

        :param device: ManagementRoot object -- device to delete from group
        '''

        device_name = get_device_info(device).name
        print('Deleting following device from group: %s ' % device_name)
        dg = pollster(self._get_device_group)(device)
        device_to_remove = dg.devices_s.devices.load(
            name=device_name, partition=self.partition
        )
        device_to_remove.delete()

    def _ensure_device_active(self, device):
        '''Ensure a single device is in an active state

        :param device: ManagementRoot object -- device to inspect
        :raises: UnexpectedClusterState
        '''

        act = device.tm.cm.devices.device.load(
            name=get_device_info(device).name,
            partition=self.partition
        )
        if act.failoverState != 'active':
            msg = "A device in the cluster was not in the 'Active' state."
            raise UnexpectedDeviceGroupState(msg)

    def _sync_to_group(self, device):
        '''Sync the device to the cluster group

        :param device: bigip object -- device to sync to group
        '''

        config_sync_cmd = 'config-sync to-group %s' % self.name
        device.tm.cm.exec_cmd('run', utilCmdArgs=config_sync_cmd)

    def ensure_all_devices_in_sync(self):
        """Ensure all devices have 'In Sync' status are sync is done."""

        self._sync_to_group(self.devices[0])
        pollster(self._check_all_devices_in_sync)()

    def _check_all_devices_in_sync(self):
        '''Wait until all devices have failover status of 'In Sync'.

        :raises: UnexpectedClusterState
        '''

        if len(self._get_devices_by_failover_status('In Sync')) != \
                len(self.devices):
            msg = "Expected all devices in group to have 'In Sync' status."
            raise UnexpectedDeviceGroupState(msg)

    def _get_devices_by_failover_status(self, status):
        '''Get a list of bigips by failover status.

        :param status: str -- status to filter the returned list of devices
        :returns: list -- list of devices that have the given status
        '''

        devices_with_status = []
        for device in self.devices:
            if (self._check_device_failover_status(device, status)):
                devices_with_status.append(device)
        return devices_with_status

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
        '''Get a list of bigips by activation statue.

        :param state: str -- state to filter the returned list of devices
        :returns: list -- list of devices that are in the given state
        '''

        devices_with_state = []
        for device in self.devices:
            act = device.tm.cm.devices.device.load(
                name=get_device_info(device).name,
                partition=self.partition
            )
            if act.failoverState == state:
                devices_with_state.append(device)
        return devices_with_state
