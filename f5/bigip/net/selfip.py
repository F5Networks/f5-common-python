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
from f5.bigip.rest_collection import strip_domain_address
from f5.bigip.rest_collection import strip_folder_and_prefix
from f5.common import constants as const
from f5.common.logger import Log

import json
import netaddr
import os


class SelfIP(object):
    """Class for managing bigip selfips """
    def __init__(self, bigip):
        self.bigip = bigip

    @icontrol_rest_folder
    @log
    def create(self, name=None, ip_address=None, netmask=None,
               vlan_name=None, floating=False, traffic_group=None,
               folder='Common', preserve_vlan_name=False):
        """Create selfip """
        if name:
            folder = str(folder).replace('/', '')
            if not traffic_group:
                if floating:
                    traffic_group = \
                        const.SHARED_CONFIG_DEFAULT_FLOATING_TRAFFIC_GROUP
                else:
                    traffic_group = const.SHARED_CONFIG_DEFAULT_TRAFFIC_GROUP
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if not netmask:
                netmask = '32'
                payload['address'] = ip_address + '/' + str(netmask)
            else:
                if ':' in str(netmask):
                    net = netaddr.IPNetwork('::/' + str(netmask))
                else:
                    net = netaddr.IPNetwork('1.1.1.1/' + str(netmask))
                payload['address'] = ip_address + '/' + str(net.prefixlen)
            if floating:
                payload['floating'] = 'enabled'
            else:
                payload['floating'] = 'disabled'
            payload['trafficGroup'] = traffic_group
            if not vlan_name.startswith('/Common'):
                payload['vlan'] = '/' + folder + '/' + vlan_name
            else:
                payload['vlan'] = vlan_name

            request_url = self.bigip.icr_url + '/net/self/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            elif response.status_code == 400 and \
                response.text.find("must be one of the vlans "
                                   "in the associated route domain") > 0:
                self.bigip.route.add_vlan_to_domain(
                    name=vlan_name, folder=folder)
                Log.error('self', 'bridge creation was halted before '
                                  'it was added to route domain.'
                                  'attempting to add to route domain '
                                  'and retrying SelfIP creation.')
                response = self.bigip.icr_session.post(
                    request_url, data=json.dumps(payload),
                    timeout=const.CONNECTION_TIMEOUT)
                if response.status_code < 400:
                    return True
                elif response.status_code == 409:
                    return True
                else:
                    Log.error('self', response.text)
                    raise exceptions.SelfIPCreationException(response.text)
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, folder='Common', preserve_vlan_name=False):
        """Delete selfip """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                Log.error('self', response.text)
                raise exceptions.SelfIPDeleteException(response.text)
            else:
                return True
        return False

    @icontrol_rest_folder
    @log
    def delete_by_vlan_name(self, vlan_name=None, folder='Common'):
        """Delete selfip by vlan name """
        if vlan_name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self'
            request_url += '?$select=vlan,selfLink,floating'
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
                    float_to_delete = []
                    nonfloat_to_delete = []
                    for selfip in return_obj['items']:
                        name = os.path.basename(selfip['vlan'])
                        if vlan_name == name or \
                           vlan_name == strip_folder_and_prefix(name):
                            if selfip['floating'] == 'enabled':
                                float_to_delete.append(
                                    self.bigip.icr_link(selfip['selfLink']))
                            else:
                                nonfloat_to_delete.append(
                                    self.bigip.icr_link(selfip['selfLink']))
                    for selfip in float_to_delete:
                        del_res = self.bigip.icr_session.delete(
                            selfip, timeout=const.CONNECTION_TIMEOUT)
                        if del_res.status_code > 399 and\
                           del_res.status_code != 404:
                            Log.error('self', del_res.text)
                            raise exceptions.SelfIPDeleteException(
                                del_res.text)
                    for selfip in nonfloat_to_delete:
                        del_res = self.bigip.icr_session.delete(
                            selfip, timeout=const.CONNECTION_TIMEOUT)
                        if del_res.status_code > 399 and\
                           del_res.status_code != 404:
                            Log.error('self', del_res.text)
                            raise exceptions.SelfIPDeleteException(
                                del_res.text)
                return True
            else:
                Log.error('selfip', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete selfips """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/self/'
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
                            Log.error('self', response.text)
                            raise exceptions.SelfIPDeleteException(
                                response.text)
            return True
        else:
            Log.error('self', response.text)
            raise exceptions.SelfIPQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_selfips(self, folder='Common', vlan=None):
        """Get selfips """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/self/'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '?$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for selfip in return_obj['items']:
                    if vlan and selfip['vlan'] != vlan:
                        continue
                    selfip['name'] = strip_folder_and_prefix(selfip['name'])
                    return_list.append(selfip)
        elif response.status_code != 404:
            Log.error('self', response.text)
            raise exceptions.SelfIPQueryException(response.text)
        return return_list

    @icontrol_rest_folder
    @log
    def get_selfip_list(self, folder='Common'):
        """Get selfips """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/self/'
        request_url += '?$select=name'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for selfip in return_obj['items']:
                    return_list.append(strip_folder_and_prefix(selfip['name']))
        elif response.status_code != 404:
            Log.error('self', response.text)
            raise exceptions.SelfIPQueryException(response.text)
        return return_list

    @icontrol_rest_folder
    @log
    def get_addrs(self, folder='Common'):
        """Get selfip addrs """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/self/'
        request_url += '?$select=address'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_list = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for selfip in return_obj['items']:
                    return_list.append(
                        self._strip_mask(selfip['address']))
        elif response.status_code != 404:
            Log.error('self', response.text)
            raise exceptions.SelfIPQueryException(response.text)
        return return_list

    @icontrol_rest_folder
    @log
    def get_addr(self, name=None, folder='Common'):
        """Get selfip addr """
        folder = str(folder).replace('/', '')
        if name:
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=address'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return self._strip_mask(return_obj['address'])
            elif response.status_code != 404:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_mask(self, name=None, folder='Common'):
        """Get selfip netmask """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=address'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                try:
                    net = netaddr.IPNetwork(
                        strip_domain_address(return_obj['address']))
                    return str(net.netmask)
                except Exception as e:
                    Log.error('self', 'get_mask exception:' + e.message)
            elif response.status_code != 404:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_mask(self, name=None, netmask=None, folder='Common'):
        """Set selfip netmask """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=address'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                try:
                    address = self._strip_mask(return_obj['address'])
                    net = netaddr.IPNetwork(
                        strip_domain_address(address) + '/' + netmask)
                    payload = dict()
                    payload['address'] = address + '/' + str(net.prefixlen)
                    request_url = self.bigip.icr_url + '/net/self/'
                    request_url += '~' + folder + '~' + name
                    response = self.bigip.icr_session.put(
                        request_url, data=json.dumps(payload),
                        timeout=const.CONNECTION_TIMEOUT)
                    if response.status_code < 400:
                        return True
                    else:
                        Log.error('self', response.text)
                        raise exceptions.SelfIPUpdateException(response.text)
                except Exception as e:
                    Log.error('self', 'set_mask exception:' + e.message)
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_vlan(self, name=None, folder='Common'):
        """Get selfip vlan """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=vlan'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'vlan' in return_obj:
                    return strip_folder_and_prefix(return_obj['vlan'])
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_vlan(self, name=None, vlan_name=None, folder='Common'):
        """Set selfip vlan """
        if name and vlan_name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['vlan'] = vlan_name
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_description(self, name=None, description=None, folder='Common'):
        """Set selfip description """
        if name and description:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['description'] = description
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_description(self, name=None, folder='Common'):
        """Get selfip description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=description'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return return_obj['description']
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_traffic_group(self, name=None, traffic_group=None,
                          folder='Common'):
        """Set selfip traffic group """
        if name and traffic_group:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['trafficGroup'] = traffic_group
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_traffic_group(self, name=None, folder='Common'):
        """Get selfip traffic group """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=trafficGroup'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                return return_obj['trafficGroup']
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_port_lockdown_allow_all(self, name=None, folder='Commmon'):
        """Set selfip port lockdown allow all """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['allowService'] = 'all'
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_port_lockdown_allow_default(self, name=None, folder='Common'):
        """Set selfip port lockdown allow default """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['allowService'] = 'default'
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_port_lockdown_allow_none(self, name=None, folder='Common'):
        """Set selfip port lockdown allow none """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['allowService'] = 'none'
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('self', response.text)
                raise exceptions.SelfIPUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_floating_addrs(self, prefix=None, folder='Common'):
        """Set selfip floating addresses """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/self/'
        request_url += '?$select=trafficGroup,floating,address'
        request_filter = 'partition eq ' + folder
        request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        floats = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for selfip in return_obj['items']:
                    if selfip['floating'] == 'enabled':
                        floats.append(
                            self._strip_mask(selfip['address']))
        else:
            Log.error('self', response.text)
            raise exceptions.SelfIPQueryException(response.text)
        return floats

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common'):
        """Does selfip exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/self/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            request_url = self.bigip.icr_url + '/net/self/'
            request_url += '~' + folder + '~' + strip_folder_and_prefix(name)
            request_url += '?$select=name'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                Log.error('self', response.text)
                raise exceptions.SelfIPQueryException(response.text)
        else:
            Log.error('self', response.text)
            raise exceptions.SelfIPQueryException(response.text)
        return False

    def _strip_mask(self, ip_address):
        """strip mask """
        mask_index = ip_address.find('/')
        if mask_index > 0:
            ip_address = ip_address[:mask_index]
        return ip_address

    def _get_traffic_group_full_path(self, traffic_group, folder=None):
        """get traffic group full path """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/cm/traffic-group'
        request_url += '?$select=name,fullPath'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for tg in response_obj['items']:
                    if tg['name'] == traffic_group:
                        return tg['fullPath']
                    else:
                        Log.error('traffic-group',
                                  'traffic-group %s not found.'
                                  % traffic_group)
                        return None
