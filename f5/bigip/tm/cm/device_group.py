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

"""BIG-IP® cluster device-group submodule

REST URI
    ``http://localhost/mgmt/tm/cm/device-group``

GUI Path
    ``Device Management --> Device Groups``

REST Kind
    ``tm:cm:device-group:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Device_Groups(Collection):
    """BIG-IP® cluster device-groups collection."""
    def __init__(self, cm):
        super(Device_Groups, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [Device_Group]
        self._meta_data['attribute_registry'] =\
            {'tm:cm:device-group:device-groupstate': Device_Group}


class Device_Group(Resource):
    """BIG-IP® cluster device-group resource"""
    def __init__(self, device_groups):
        super(Device_Group, self).__init__(device_groups)
        self._meta_data['read_only_attributes'].append('type')
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:cm:device-group:device-groupstate'
        self._meta_data['attribute_registry'] = {
            'tm:cm:device-group:devices:devicescollectionstate': Devices_s
        }

    def sync_to(self):
        """Wrapper method that synchronizes configuration to DG.


        Executes the containing object's cm :meth:`~f5.bigip.cm.Cm.exec_cmd`
        method to sync the configuration TO the device-group.

        :note:: Both sync_to, and sync_from methods are convenience
                methods which usually are not what this SDK offers.
                It is best to execute config-sync with the use of
                exec_cmd() method on the cm endpoint.
        """
        device_group_collection = self._meta_data['container']
        cm = device_group_collection._meta_data['container']
        sync_cmd = 'config-sync to-group %s' % self.name
        cm.exec_cmd('run', utilCmdArgs=sync_cmd)

    def sync_from(self):
        """Wrapper method that synchronizes configuration from DG.


        Executes the containing object's cm :meth:`~f5.bigip.cm.Cm.exec_cmd`
        method to sync the configuration FROM the device-group.

        :note:: Both sync_to, and sync_from methods are convenience
                methods which usually are not what this SDK offers.
                It is best to execute config-sync with the use of
                exec_cmd() method on the cm endpoint.
        """
        device_group_collection = self._meta_data['container']
        cm = device_group_collection._meta_data['container']
        sync_cmd = 'config-sync from-group %s' % self.name
        cm.exec_cmd('run', utilCmdArgs=sync_cmd)


class Devices_s(Collection):
    """BIG-IP® cluster devices-group devices subcollection."""
    def __init__(self, device_group):
        super(Devices_s, self).__init__(device_group)
        self._meta_data['allowed_lazy_attributes'] = [Devices]
        self._meta_data['required_json_kind'] =\
            'tm:cm:device-group:devices:devicescollectionstate'
        self._meta_data['attribute_registry'] =\
            {'tm:cm:device-group:devices:devicesstate': Devices}


class Devices(Resource):
    """BIG-IP® cluster devices-group devices subcollection resource."""
    def __init__(self, devices_s):
        super(Devices, self).__init__(devices_s)
        self._meta_data['required_json_kind'] =\
            'tm:cm:device-group:devices:devicesstate'
        self._meta_data['required_creation_parameters'].update(('partition',))
