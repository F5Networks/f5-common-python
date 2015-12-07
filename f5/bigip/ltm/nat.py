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

from f5.bigip.rest_collection import log
from f5.bigip.rest_collection import RESTInterfaceCollection
from f5.common import constants as const
from f5.common.logger import Log

from requests.exceptions import HTTPError


class NAT(RESTInterfaceCollection):
    def __init__(self, bigip):
        super(NAT, self).__init__(bigip)
        self.base_uri = self.bigip.icr_url + 'ltm/nat/'

    @log
    def create(self, name=None, ip_address=None, orig_ip_address=None,
               traffic_group=None, vlan_name=None, folder='Common'):
        """Create NAT """
        folder = str(folder).replace('/', '')
        if not self.exists(name=name, folder=folder):
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['originatingAddress'] = orig_ip_address
            payload['translationAddress'] = ip_address
            payload['trafficGroup'] = traffic_group
            payload['vlans'] = [vlan_name]

            try:
                self.bigip.icr_session.post(
                    self.base_uri, data=payload,
                    timeout=const.CONNECTION_TIMEOUT)
            except HTTPError as exp:
                if exp.response.status_code == 409:
                    return True
                Log.error('NAT', exp.response.text)
                raise
            return True
        return False

    @log
    def get_nats(self, folder='Common'):
        """Get NATs """
        return self._get_items(folder=folder)

    @log
    def get_addrs(self, folder='Common'):
        return self._get_items(select='translationAddress', folder=folder)

    @log
    def get_addr(self, name=None, folder='Common'):
        """Get NAT addr """
        # The original was not returning anything if name was None?
        if name:
            return self._get_named_object(name, folder=folder,
                                          select='translationAddress')

    @log
    def get_original_addrs(self, folder='Common'):
        """Get NAT original addrs """
        return self._get_items(folder=folder, select='originatingAddress')

    @log
    def get_original_addr(self, name=None, folder='Common'):
        """Get NAT original addr """
        # The original was not returning anything if the name was None?
        if name:
            return self._get_named_object(name, folder=folder,
                                          select='originatingAddress')

    @log
    def get_vlan(self, name=None, folder='Common'):
        """Get NAT vlan """
        # The original was not returning anything if the name was None?
        if name:
            return self._get_named_object(name, folder=folder, select='vlans')
