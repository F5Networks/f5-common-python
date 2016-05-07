# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
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
"""BIG-IP® cluster module

REST URI
    ``http://localhost/mgmt/tm/cm/``

GUI Path
    ``Device Management``

REST Kind
    ``tm:cm:*``
"""


from f5.bigip.cm.device import Devices
from f5.bigip.cm.device_group import Device_Groups
from f5.bigip.cm.sync_status import Sync_Status
from f5.bigip.cm.traffic_group import Traffic_Groups
from f5.bigip.cm.trust_domain import Trust_Domains
from f5.bigip.resource import OrganizingCollection


class Cm(OrganizingCollection):
    """BIG-IP® Cluster Organizing Collection."""
    def __init__(self, bigip):
        super(Cm, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Devices, Device_Groups, Traffic_Groups, Sync_Status, Trust_Domains
        ]

    def sync_to_group(self, device_group_name):
        '''Sync the configruation of this device to the other group members.

        Execute the run command via the iControl REST session with the
        config-sync to group device-group options.  Any exceptions triggered
        by the POST to the iControl REST server are raised back to the caller.

        :param device_group_name: Name of the device group to sync.
        :type device_group_name: str
        '''
        data = {
            'command': 'run',
            'utilCmdArgs': 'run cm config-sync to-group %s' %
            device_group_name
        }
        icr_session = self._meta_data['container']._meta_data['icr_session']
        icr_session.post(self._meta_data['uri'], json=data)

    def sync_from_group(self, device_group_name):
        '''Sync the configuration of the group to this device.

        :param device_group_name: str -- name of the device group

        '''

        data = {
            'command': 'run',
            'utilCmdArgs': 'run cm config-sync from-group %s' %
            device_group_name
        }
        icr_session = self._meta_data['container']._meta_data['icr_session']
        icr_session.post(self._meta_data['uri'], json=data)
