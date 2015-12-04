""" Classes and functions for configuring ARP on bigip """
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
# pylint: disable=broad-except,no-self-use

from f5.bigip import exceptions
from f5.bigip.interfaces import icontrol_folder
from f5.bigip.interfaces import icontrol_rest_folder
from f5.bigip.interfaces import log
from f5.common import constants as const
from f5.common.logger import Log

import json
import netaddr
import urllib


class ARP(object):
    """Class for configuring ARP on bigip """

    def __init__(self, bigip):
        self.bigip = bigip
        # add iControl interfaces if they don't exist yet
        self.bigip.icontrol.add_interfaces(['Networking.ARP'])

        # iControl helper objects
        self.net_arp = self.bigip.icontrol.Networking.ARP

    # pylint: disable=pointless-string-statement
    '''
    @icontrol_rest_folder
    @log
    def create(self, ip_address=None, mac_address=None, folder='Common'):
        payload = dict()
        payload['name'] = ip_address
        payload['partition'] = folder
        payload['ipAddress'] = ip_address
        payload['macAddress'] = mac_address
        request_url = self.icr_url + '/net/arp/'
        response = self.icr_session.post(request_url,
                              data=json.dumps(payload),
                              timeout=)
        Log.debug('ARP::create response',
                  '%s' % response.json())
        if response.status_code < 400:
            return True
        elif response.status_code == 409:
            return True
        else:
            raise exceptions.StaticARPCreationException(response.text)
    '''
    # pylint: enable=pointless-string-statement

    @icontrol_folder
    @log
    def create(self, ip_address=None, mac_address=None, folder='Common'):
        """Create an ARP static entry """
        if not self.exists(ip_address=ip_address, folder=folder):
            # ARP entries can't handle %0 on them like other
            # TMOS objects.
            ip_address = self._remove_route_domain_zero(ip_address)
            try:
                create_arp = self.net_arp.typefactory.create
                entry = create_arp('Networking.ARP.StaticEntry')
                entry.address = ip_address
                entry.mac_address = mac_address
                self.net_arp.add_static_entry([entry])
                return True
            except Exception as exc:
                Log.error('ARP', 'create exception: ' + exc.message)
                raise exceptions.StaticARPCreationException(exc.message)
        return False

    # pylint: disable=pointless-string-statement
    '''
    @icontrol_rest_folder
    def delete(self, ip_address=None, folder='Common'):
        if ip_address:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/arp/'
            request_url += '~' + folder + '~' + urllib.quote(
                                  self._remove_route_domain_zero(ip_address))
            response = self.bigip.icr_session.delete(request_url,
                                            timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                raise exceptions.StaticARPDeleteException(response.text)
                Log.error('ARP', response.text)
        return False
    '''
    # pylint: enable=pointless-string-statement

    @icontrol_folder
    @log
    def delete(self, ip_address=None, folder='Common'):
        """Delete an ARP static entry """
        if self.exists(ip_address=ip_address, folder=folder):
            # ARP entries can't handle %0 on them like other
            # TMOS objects.
            ip_address = self._remove_route_domain_zero(ip_address)
            try:
                self.net_arp.delete_static_entry_v2(
                    ['/' + folder + '/' + ip_address])
                return True
            except Exception as exc:
                Log.error('ARP', 'delete exception: ' + exc.message)
                raise exceptions.StaticARPDeleteException(exc.message)
        return False

    @icontrol_folder
    @log
    def delete_by_mac(self, mac_address=None, folder='Common'):
        """Delete an ARP static entry by MAC address """
        if mac_address:
            arps = self.get_arps(None, folder)
            for arp in arps:
                for ip_address in arp:
                    if arp[ip_address] == mac_address:
                        self.delete(ip_address=ip_address, folder=folder)

    @icontrol_folder
    @log
    def delete_by_subnet(self, subnet=None, mask=None, folder='Common'):
        """Delete ARP static entries on subnet """
        if subnet:
            mask_div = subnet.find('/')
            if mask_div > 0:
                try:
                    rd_div = subnet.find('%')
                    if rd_div > -1:
                        network = netaddr.IPNetwork(
                            subnet[0:mask_div][0:rd_div] + subnet[mask_div:])
                    else:
                        network = netaddr.IPNetwork(subnet)
                except Exception as exc:
                    Log.error('ARP', exc.message)
                    return []
            elif not mask:
                return []
            else:
                try:
                    rd_div = subnet.find('%')
                    if rd_div > -1:
                        network = netaddr.IPNetwork(
                            subnet[0:rd_div] + '/' + mask)
                    else:
                        network = netaddr.IPNetwork(subnet + '/' + mask)
                except Exception as exc:
                    Log.error('ARP', exc.message)
                    return []

            return self._delete_by_network(folder, network)

    def _delete_by_network(self, folder, network):
        """Delete for network """
        if not network:
            return []
        mac_addresses = []
        request_url = self.bigip.icr_url + '/net/arp'
        request_filter = 'partition eq ' + folder
        request_url += '?$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for arp in response_obj['items']:
                    ad_rd_div = arp['ipAddress'].find('%')
                    if ad_rd_div > -1:
                        address = netaddr.IPAddress(
                            arp['ipAddress'][0:ad_rd_div])
                    else:
                        address = netaddr.IPAddress(arp['ipAddress'])

                    if address in network:
                        mac_addresses.append(arp['macAddress'])
                        self.delete(arp['ipAddress'],
                                    folder=arp['partition'])
        return mac_addresses

    @icontrol_rest_folder
    @log
    def get_arps(self, ip_address=None, folder='Common'):
        """Get ARP static entry """
        folder = str(folder).replace('/', '')
        if ip_address:
            request_url = self.bigip.icr_url + '/net/arp/'
            request_url += '~' + folder + '~' + urllib.quote(
                self._remove_route_domain_zero(ip_address))
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            Log.debug('ARP::get response',
                      '%s' % response.json())
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                return [
                    {response_obj['name']:
                     response_obj['macAddress']}
                ]
            else:
                Log.error('ARP', response.text)
                raise exceptions.StaticARPQueryException(response.text)
        else:
            request_url = self.bigip.icr_url + '/net/arp'
            request_filter = 'partition eq ' + folder
            request_url += '?$filter=' + request_filter
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            Log.debug('ARP::get response',
                      '%s' % response.json())
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'items' in response_obj:
                    arps = []
                    for arp in response_obj['items']:
                        arps.append(
                            {arp['name']:
                             arp['macAddress']}
                        )
                    return arps
            else:
                Log.error('ARP', response.text)
                raise exceptions.StaticARPQueryException(response.text)
        return []

    # pylint: disable=pointless-string-statement
    '''
    @icontrol_rest_folder
    def delete_all(self, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/arp/'
        request_url += '?$select=name,selfLink'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(request_url,
                                             timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            deletions = []
            if 'items' in response_obj:
                for item in response_obj['items']:
                    if item['name'].startswith(self.OBJ_PREFIX):
                        deletions.append(self.bigip.icr_link(item['selfLink']))
            for delete in deletions:
                response = self.bigip.icr_session.delete(delete,
                                              timeout=const.CONNECTION_TIMEOUT)
                if response.status_code > 400 and \
                  (not response.status_code == 404):
                    Log.error('ARP', response.text)
                    return False
        elif response.status_code == 404:
            return True
        else:
            Log.error('ARP', response.text)
            exceptions.StaticARPDeleteException(response.text)
     '''
    # pylint: enable=pointless-string-statement

    @icontrol_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete all ARP entries """
        try:
            self.net_arp.delete_all_static_entries()
        except Exception as exc:
            Log.error('ARP', 'delete exception: ' + exc.message)
            raise exceptions.StaticARPDeleteException(exc.message)

    # pylint: disable=pointless-string-statement
    '''
    @icontrol_rest_folder
    def exists(self, ip_address=None, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/arp/'
        request_url += '~' + folder + '~' + urllib.quote(
                        self._remove_route_domain_zero(ip_address))
        response = self.bigip.icr_session.get(request_url,
                                  timeout=const.CONNECTION_TIMEOUT)
        Log.debug('ARP::exists response',
                      '%s' % response.text)
        if response.status_code < 400:
            return True
        return False
    '''
    # pylint: enable=pointless-string-statement

    @icontrol_folder
    @log
    def exists(self, ip_address=None, folder='Common'):
        """Does ARP entry exist? """
        # ARP entries can't handle %0 on them like other
        # TMOS objects.
        ip_address = self._remove_route_domain_zero(ip_address)
        try:
            arp_list = self.net_arp.get_static_entry_list()
        except Exception as exc:
            Log.error('ARP', 'query exception: %s on %s' %
                      (exc.message, self.bigip.device_name))
            raise exceptions.StaticARPQueryException(exc.message)

        if '/' + folder + '/' + ip_address in arp_list:
            return True
        else:
            return False

    def _remove_route_domain_zero(self, ip_address):
        """Remove route domain zero from ip_address """
        decorator_index = ip_address.find('%0')
        if decorator_index > 0:
            ip_address = ip_address[:decorator_index]
        return ip_address
