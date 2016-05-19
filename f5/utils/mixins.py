# Copyright 2016 F5 Networks Inc.
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


class DeviceMixin(object):
    '''Manage BigIP device cluster in a general way.'''

    def get_device_info(self, bigip):
        '''Get device information about a specific BigIP device.

        :param bigip: bigip object --- device to inspect
        :returns: bigip object
        '''

        coll = bigip.tm.cm.devices.get_collection()
        device = [device for device in coll if device.selfDevice == 'true']
        assert len(device) == 1
        return device[0]
