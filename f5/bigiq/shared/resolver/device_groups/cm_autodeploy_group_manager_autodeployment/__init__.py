# coding=utf-8
#
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

"""BIG-IQ® Device Groups (shared) module for CM AutoDeployed Devices

REST URI
    ``http://localhost/mgmt/shared/resolver/device-groups/cm-autodeploy-group-manager-autodeployment``

GUI Path
    ``Device Management --> Inventory``

REST Kind
    N/A -- HTTP GET returns an error
"""
from requests.exceptions import HTTPError

from f5.bigiq.resource import Resource
from f5.bigip.resource import Collection
from f5.sdk_exception import F5SDKError


class CMAutoDeployDeviceReadOnly(F5SDKError):
    pass


class Cm_Autodeploy_Group_Manager_Autodeployment(Resource):
    """BIG-IQ® Device Group for CM AutoDeployed Devices resource"""
    def __init__(self, device_groups):
        super(Cm_Autodeploy_Group_Manager_Autodeployment,
              self).__init__(device_groups)
        self._meta_data['required_json_kind'] = \
            'shared:resolver:device-groups:devicegroupstate'
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolmembercollectionstate':
            Devices_s
        }
        self._meta_data['uri'] = "%s%s" % (
            self._meta_data['container']._meta_data['uri'],
            'cm-autodeploy-group-manager-autodeployment/')
        self._meta_data['allowed_lazy_attributes'] = [
            Devices_s
        ]

    def load(self, **kwargs):
        base_uri = "%s%s" % (self._meta_data['container']._meta_data['uri'],
                             'cm-autodeploy-group-manager-autodeployment')
        self._meta_data['uri'] = base_uri
        self._meta_data['required_load_parameters'] = {}
        refresh_session = self._meta_data['bigip']._meta_data['icr_session']
        response = refresh_session.get(base_uri, **kwargs)
        self._local_update(response.json())
        self._activate_URI(self.selfLink)
        return self

    def exists(self, **kwargs):
        return True


class Devices_s(Collection):
    """BIG-IQ® Devices sub-collection"""
    def __init__(self, cm_autodeploy_group_Manager_autodeployment):
        super(Devices_s, self).__init__(
            cm_autodeploy_group_Manager_autodeployment
        )
        self._meta_data['allowed_lazy_attributes'] = [Device]
        self._meta_data['required_json_kind'] =\
            'shared:resolver:device-groups:devicegroupdevicecollectionstate'
        self._meta_data['attribute_registry'] =\
            {'shared:resolver:device-groups:restdeviceresolverdevicestate':
             Device}


class Device(Resource):
    """BIG-IP® LTM pool members sub-collection resource"""
    def __init__(self, devices_s):
        super(Device, self).__init__(devices_s)
        self._meta_data['required_json_kind'] =\
            'shared:resolver:device-groups:restdeviceresolverdevicestate'
        self._meta_data['required_creation_parameters'] = \
            {'address', 'password', 'rootPassword'}
        self._meta_data['required_load_parameters'] = {'uuid'}

    def create(self, userName='admin', rootUser='root', **kwargs):
        self._create(userName=userName, rootUser=rootUser,
                     automaticallyUpdateFramework=True, **kwargs)
        return self

    def update(self, **kwargs):
        raise CMAutoDeployDeviceReadOnly(
            'Auto Deploy items can be created or deleted, not updated'
        )
