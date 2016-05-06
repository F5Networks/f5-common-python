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


class DeviceGroupManager(DeviceMixin):
    '''Class to manage device service group.'''

    def __init__(self, dg_name, root_bigip, partition):
        '''Initialize a cluster object.'''

        self.device_group_name = dg_name
        self.partition = partition
        self.device_group = None
        self.root_bigip = root_bigip

    def create_device_group(self, bigips, cluster_type):
        '''Create the device service cluster group and add devices to it.'''

        dg = self.root_bigip.cm.device_groups.device_group
        self.device_group = dg.create(
            name=self.device_group_name,
            partition=self.partition,
            type=cluster_type
        )
        for device in bigips:
            self._add_device_to_device_group(device)

    def scale_up_device_group(self, device):
        '''Scale device group up by one device

        :param bigip: bigip object -- bigip to add to device group
        '''

        self._add_device_to_device_group(device)

    def scale_down_device_group(self, device):
        '''Scale device group down by one device

        :param bigip: bigip object -- bigip to delete from device group
        '''

        self._delete_device_from_device_group(device)

    def teardown_device_group(self, bigips):
        '''Teardown device service cluster group.

        :param bigips: list -- bigip objects
        '''

        for bigip in bigips:
            try:
                self._delete_device_from_device_group(bigip)
            except Exception as ex:
                print(ex)
                print(type(ex))
                continue
        dg = self.root_bigip.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        dg.delete()

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

        :param bigip: bigip object -- device to add to group
        '''

        device_info = self._get_device_info(device)
        dg = device.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        dg.devices_s.devices.create(
            name=device_info.name, partition=self.partition
        )
        root_dg = self.root_bigip.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        root_dg.devices_s.devices.load(
            name=device_info.name, partition=self.partition
        )
        print('added device to group ' + device_info.name)

    @pollster.poll_by_method
    def _delete_device_from_device_group(self, device):
        '''Remove device from device service cluster group.

        :param bigip: bigip object -- device to delete from group
        '''

        device_info = self._get_device_info(device)
        dg = device.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        device_device = dg.devices_s.devices.load(
            name=device_info.name, partition=self.partition
        )
        device_device.delete()
        root_dg = self.root_bigip.cm.device_groups.device_group.load(
            name=self.device_group_name, partition=self.partition
        )
        try:
            root_dg.devices_s.devices.load(
                name=device_info.name, partition=self.partition
            )
        except Exception as ex:
            print(ex)
            print(type(ex))
