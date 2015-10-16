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

from f5.common.logger import Log
from f5.common import constants as const
from f5.bigip.interfaces import icontrol_rest_folder
from f5.bigip.interfaces import strip_folder_and_prefix
from f5.bigip import exceptions
from f5.bigip.interfaces import log

import json


class NAT(object):
    def __init__(self, bigip):
        self.bigip = bigip

    @icontrol_rest_folder
    @log
    def create(self, name=None, ip_address=None, orig_ip_address=None,
               traffic_group=None, vlan_name=None, folder='Common'):
        """ Create NAT """
        folder = str(folder).replace('/', '')
        if not self.exists(name=name, folder=folder):
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['originatingAddress'] = orig_ip_address
            payload['translationAddress'] = ip_address
            payload['trafficGroup'] = traffic_group
            payload['vlans'] = [vlan_name]
            request_url = self.bigip.icr_url + '/ltm/nat'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('NAT', response.text)
                raise exceptions.NATCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, folder='Common'):
        """ Delete NAT """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/nat/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('NAT', response.text)
                raise exceptions.NATDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """ Delete all NATs """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/nat/'
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
                            Log.error('nat', response.text)
                            raise exceptions.NATDeleteException(response.text)
            return True
        else:
            Log.error('nat', response.text)
            raise exceptions.NATQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_nats(self, folder='Common'):
        """ Get NATs """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/nat'
        request_url += '?$select=name'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        nat_names = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for nat in return_obj['items']:
                    nat_names.append(strip_folder_and_prefix(nat['name']))
        elif response.status_code != 404:
            Log.error('nat', response.text)
            raise exceptions.NATQueryException(response.text)
        return nat_names

    @icontrol_rest_folder
    @log
    def get_addrs(self, folder='Common'):
        """ Get NAT addrs """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/nat'
        request_url += '?$select=translationAddress'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        trans_addresses = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for nat in return_obj['items']:
                    nat_trans = nat['translationAddress']
                    trans_addresses.append(nat_trans)
        else:
            Log.error('nat', response.text)
            raise exceptions.NATQueryException(response)
        return trans_addresses

    @icontrol_rest_folder
    @log
    def get_addr(self, name=None, folder='Common'):
        """ Get NAT addr """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/nat/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=translationAddress'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'translationAddress' in return_obj:
                    return return_obj['translationAddress']
            else:
                Log.error('nat', response.text)
                raise exceptions.NATQueryException(response.text)
            return None

    @icontrol_rest_folder
    @log
    def get_original_addrs(self, folder='Common'):
        """ Get NAT original addrs """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/nat'
        request_url += '?$select=originatingAddress'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        orig_addresses = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for nat in return_obj['items']:
                    orig_addresses.append(nat['originatingAddress'])
        else:
            Log.error('nat', response.text)
            raise exceptions.NATQueryException(response.text)
        return orig_addresses

    @icontrol_rest_folder
    @log
    def get_original_addr(self, name=None, folder='Common'):
        """ Get NAT original addr """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/nat/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=originatingAddress'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'originatingAddress' in return_obj:
                    return return_obj['originatingAddress']
            else:
                Log.error('nat', response.text)
                raise exceptions.NATQueryException(response.text)
            return None

    @icontrol_rest_folder
    @log
    def get_vlan(self, name=None, folder='Common'):
        """ Get NAT vlan """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/nat/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=vlans'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            return_vlans = []
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'vlans' in return_obj:
                    for vlan in return_obj['vlans']:
                        return_vlans.append(strip_folder_and_prefix(vlan))
            elif response.status_code != 404:
                Log.error('nat', response.text)
                raise exceptions.NATQueryException(response.text)
            if len(return_vlans) == 1:
                return_vlans = return_vlans[0]
            return return_vlans
        return None

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common'):
        """ Does NAT exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/nat/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('nat', response.text)
        return False
