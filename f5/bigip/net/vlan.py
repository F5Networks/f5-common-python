"""Classes and functions for configuring vlans on BIG-IP """
# Copyright 2014 F5 Networks Inc.
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

from f5.bigip import exceptions
from f5.bigip.rest_collection import icontrol_rest_folder
from f5.bigip.rest_collection import log
from f5.bigip.rest_collection import strip_folder_and_prefix
from f5.common import constants as const
from f5.common.logger import Log

import json
import os


class Vlan(object):
    """Class for configuring vlans on bigip """
    def __init__(self, bigip):
        self.bigip = bigip

    @icontrol_rest_folder
    @log
    def create(self, name=None, vlanid=None, interface=None,
               folder='Common', description=None, route_domain_id=0):
        """Create vlan.

        route_domain_id is an int

        """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if vlanid:
                payload['tag'] = vlanid
                if interface:
                    payload['interfaces'] = [{'name': interface,
                                              'tagged': True}]
            else:
                payload['tag'] = 0
                if interface:
                    payload['interfaces'] = [{'name': interface,
                                              'untagged': True}]
            if description:
                payload['description'] = description
            request_url = self.bigip.icr_url + '/net/vlan/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                if not folder == 'Common':
                    self.bigip.route.add_vlan_to_domain_by_id(
                        name=name, folder=folder,
                        route_domain_id=route_domain_id)
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('VLAN', response.text)
                raise exceptions.VLANCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, folder='Common'):
        """Delete vlan """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                Log.error('VLAN', response.text)
                raise exceptions.VLANDeleteException(response.text)
            else:
                return True
        return False

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete vlans """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/vlan/'
        request_url += '?$select=name,selfLink'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for item in response_obj['items']:
                    if item['name'].startswith(self.OBJ_PREFIX):
                        response = self.bigip.icr_session.delete(
                            self.bigip.icr_link(item['selfLink']),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code > 400 and \
                           response.status_code != 404:
                            Log.error('vlan', response.text)
                            raise exceptions.VLANDeleteException(response.text)
        elif response.status_code == 404:
            return True
        else:
            Log.error('VLAN', response.text)
            raise exceptions.VLANQueryException(response.text)

    @icontrol_rest_folder
    @log
    def get_vlans(self, folder='Common'):
        """Get vlans """
        request_url = self.bigip.icr_url + '/net/vlan/'
        request_url += '?$select=name'
        if folder:
            folder = str(folder).replace('/', '')
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for vlan in return_obj['items']:
                    return_list.append(strip_folder_and_prefix(vlan['name']))
        elif response.status_code != 404:
            Log.error('VLAN', response.text)
            raise exceptions.VLANQueryException(response.text)
        return return_list

    @icontrol_rest_folder
    @log
    def get_id(self, name=None, folder='Common'):
        """Get vlan id """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=tag'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return return_obj['tag']
            elif response.status_code != 404:
                Log.error('VLAN', response.text)
                raise exceptions.VLANQueryException(response.text)
        return 0

    @icontrol_rest_folder
    @log
    def set_id(self, name=None, vlanid=0, folder='Common'):
        """Set vlan id """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['tag'] = vlanid
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('VLAN', response.text)
                raise exceptions.VLANUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_interface(self, name=None, folder='Common'):
        """Get vlan interface by name """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            request_url += '/interfaces?$select=name'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '&$filter=' + request_filter
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for interface in return_obj['items']:
                        return interface['name']
            elif response.status_code == 404:
                return None
            else:
                Log.error('VLAN', response.text)
                raise exceptions.VLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_interface(self, name=None, interface='1.1', folder='Common'):
        """Set vlan interface """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            if self.bigip.system.get_platform().startswith(
                    const.BIGIP_VE_PLATFORM_ID):
                payload['interfaces'] = [{'name': interface, 'untagged': True}]
            else:
                payload['interfaces'] = [{'name': interface, 'untagged': True}]
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('VLAN', response.text)
                raise exceptions.VLANUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_vlan_name_by_description(self, description=None, folder='Common'):
        """Get vlan by description """
        if description:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + \
                '/net/vlan?$select=name,description'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '&$filter=' + request_filter
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for vlan in return_obj['items']:
                        if vlan['description'] == description:
                            return vlan['name']
            elif response.status_code == 404:
                return None
            else:
                Log.error('VLAN', response.text)
                raise exceptions.VLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_description(self, name=None, description=None, folder='Common'):
        """Set vlan description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['description'] = description
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('VLAN', response.text)
                raise exceptions.VLANUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_description(self, name=None, folder='Common'):
        """Get vlan description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + \
                '/net/vlan?$select=name,description'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '&$filter=' + request_filter
            else:
                folder = 'Common'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for vlan in return_obj['items']:
                        vlan_name = os.path.basename(vlan['name'])
                        if vlan_name == name:
                            if 'description' in vlan:
                                return vlan['description']
                        if vlan_name == \
                           strip_folder_and_prefix(name):
                            if 'description' in vlan:
                                return vlan['description']
            elif response.status_code != 404:
                Log.error('VLAN', response.text)
                raise exceptions.VLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common'):
        """Does vlan exist? """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/vlan/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=name'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                Log.error('VLAN', response.text)
                raise exceptions.VLANQueryException(response.text)
        return False

    @icontrol_rest_folder
    def _in_use(self, name=None, folder=None):
        """Does selfip use vlan? """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self?$select=vlan'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '&$filter=' + request_filter
            else:
                folder = 'Common'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for selfip in return_obj['items']:
                        vlan_name = os.path.basename(selfip['vlan'])
                        if vlan_name == name:
                            return True
                        if vlan_name == \
                           strip_folder_and_prefix(name):
                            return True
            elif response.status_code != 404:
                Log.error('VLAN', response.text)
                raise exceptions.VLANQueryException(response.text)
        return False
