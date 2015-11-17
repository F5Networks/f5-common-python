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
from f5.common import constants as const
from f5.common.logger import Log

import json


class Interface(object):
    """Class for managing iRules on bigip """
    def __init__(self, bigip):
        self.bigip = bigip

    def get_interfaces(self):
        """Get interface names """
        request_url = self.bigip.icr_url + '/net/interface/'
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            names = []
            if 'items' in response_obj:
                for interface in response_obj['items']:
                    names.append(interface['name'])
            return names
        elif response.status_code != 404:
            Log.error('interface', response.text)
            raise exceptions.InterfaceQueryException(response.text)
        return None

    def get_mac_addresses(self):
        """Get MAC addresses for all interfaces """
        request_url = self.bigip.icr_url + '/net/interface/'
        request_url += '?$select=macAddress'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            macs = []
            if 'items' in response_obj:
                for interface in response_obj['items']:
                    macs.append(interface['macAddress'])
            return macs
        elif response.status_code != 404:
            Log.error('interface', response.text)
            raise exceptions.InterfaceQueryException(response.text)
        return None

    def get_interface_macaddresses_dict(self):
        """Get dictionary of mac addresses keyed by their interface name """
        request_url = self.bigip.icr_url + '/net/interface/'
        request_url += '?$select=name,macAddress'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return_dict = {}
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for interface in response_obj['items']:
                    return_dict[interface['name']] = interface['macAddress']
            return return_dict
        elif response.status_code != 404:
            Log.error('interface', response.text)
            raise exceptions.InterfaceQueryException(response.text)
        return None
