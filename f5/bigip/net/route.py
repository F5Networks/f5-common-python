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
from f5.common import constants as const
from f5.common.logger import Log

import json


class Route(object):
    def __init__(self, bigip):
        self.bigip = bigip
        self.domain_index = {'Common': 0}

    @icontrol_rest_folder
    @log
    def create(self, name=None, dest_ip_address=None, dest_mask=None,
               gw_ip_address=None, folder='Common'):
        """Create Route Entry """
        if dest_ip_address and dest_mask and gw_ip_address:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['gw'] = gw_ip_address
            payload['network'] = dest_ip_address + "/" + dest_mask
            request_url = self.bigip.icr_url + '/net/route/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('route', response.text)
                raise exceptions.RouteCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, folder='Common'):
        """Delete Route Entry """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/route/'
        request_url += '~' + folder + '~' + name

        response = self.bigip.icr_session.delete(
            request_url, timeout=const.CONNECTION_TIMEOUT)

        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('route', response.text)
            raise exceptions.RouteDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete Route Entries """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/route/'
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
                            Log.error('route', response.text)
                            raise exceptions.RouteDeleteException(
                                response.text)
            return True
        else:
            Log.error('route', response.text)
            raise exceptions.RouteQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_domain_by_id(self, folder='/Common', route_domain_id=0):
        """Get VLANs in Domain """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + \
            '/net/route-domain?$select=id,name,partition,vlans'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)

        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for route_domain in response_obj['items']:
                    if int(route_domain['id']) == route_domain_id:
                        return route_domain
            return None
        else:
            if response.status_code != 404:
                Log.error('route-domain', response.text)
                raise exceptions.RouteQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_vlans_in_domain_by_id(self, folder='/Common', route_domain_id=0):
        """Get VLANs in Domain """
        route_domain = self.get_domain_by_id(
            folder=folder, route_domain_id=route_domain_id)
        vlans = []
        if 'vlans' in route_domain:
            for vlan in route_domain['vlans']:
                vlans.append(vlan)
        return vlans

    @icontrol_rest_folder
    @log
    def get_vlans_in_domain(self, folder='Common'):
        """Get VLANs in Domain """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + \
            '/net/route-domain?$select=name,partition,vlans'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)

        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                vlans = []
                folder = str(folder).replace('/', '')
                for route_domain in response_obj['items']:
                    if route_domain['name'] == folder:
                        if 'vlans' in route_domain:
                            for vlan in route_domain['vlans']:
                                vlans.append(vlan)
                return vlans
            return []
        else:
            if response.status_code != 404:
                Log.error('route-domain', response.text)
                raise exceptions.RouteQueryException(response.text)
        return []

    @icontrol_rest_folder
    @log
    def add_vlan_to_domain_by_id(
            self, name=None, folder='Common', route_domain_id=0):
        """Add VLANs to Domain """
        folder = str(folder).replace('/', '')
        existing_vlans = self.get_vlans_in_domain_by_id(
            folder=folder, route_domain_id=route_domain_id)
        route_domain = self.get_domain_by_id(
            folder=folder, route_domain_id=route_domain_id)
        if not route_domain:
            raise exceptions.RouteUpdateException(
                "Cannot get route domain %s" % route_domain_id)
        if name not in existing_vlans:
            existing_vlans.append(name)
            vlans = dict()
            vlans['vlans'] = existing_vlans
            request_url = self.bigip.icr_url + '/net/route-domain/'
            request_url += '~' + folder + '~' + route_domain['name']
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(vlans),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('route-domain', response.text)
                raise exceptions.RouteUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def add_vlan_to_domain(self, name=None, folder='Common'):
        """Add VLANs to Domain """
        folder = str(folder).replace('/', '')
        existing_vlans = self.get_vlans_in_domain(folder=folder)
        if name not in existing_vlans:
            existing_vlans.append(name)
            vlans = dict()
            vlans['vlans'] = existing_vlans
            request_url = self.bigip.icr_url + '/net/route-domain/'
            request_url += '~' + folder + '~' + folder
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(vlans),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('route-domain', response.text)
                raise exceptions.RouteUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_vlan_from_domain(self, name=None, folder='Common'):
        """Remove VLANs from Domain """
        folder = str(folder).replace('/', '')
        existing_vlans = self.get_vlans_in_domain(folder)
        if name in existing_vlans:
            existing_vlans.remove(name)
            vlans = dict()
            vlans['vlans'] = existing_vlans
            request_url = self.bigip.icr_url + '/net/route-domain/'
            request_url += '~' + folder + '~' + folder
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(vlans),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('route-domain', response.text)
                raise exceptions.RouteUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def create_domain(
            self, folder='Common', strict_route_isolation=False, is_aux=False):
        """Create route domain.

        is_aux: whether it is an auxiliary route domain beyond the main
                    route domain for the folder
        """

        folder = str(folder).replace('/', '')
        if not folder == 'Common':
            payload = dict()
            payload['partition'] = '/' + folder
            payload['id'] = self._get_next_domain_id()
            payload['name'] = folder
            if is_aux:
                payload['name'] += '_aux_' + str(payload['id'])
            if strict_route_isolation:
                payload['strict'] = 'enabled'
            else:
                payload['strict'] = 'disabled'
                payload['parent'] = '/Common/0'
            request_url = self.bigip.icr_url + '/net/route-domain/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return payload['id']
            elif response.status_code == 409:
                return True
            else:
                Log.error('route-domain', response.text)
                raise exceptions.RouteCreationException(response.text)
            return False
        return False

    @icontrol_rest_folder
    @log
    def delete_domain(self, folder='Common', name=None):
        """Delete route domain """
        folder = str(folder).replace('/', '')
        if not folder == 'Common':
            request_url = self.bigip.icr_url + '/net/route-domain/'
            if name:
                request_url += '~' + folder + '~' + name
            else:
                request_url += '~' + folder + '~' + folder
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code != 404:
                Log.error('route-domain', response.text)
                raise exceptions.RouteDeleteException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def domain_exists(self, folder='Common', route_domain_id=None):
        """Does the route domain exist?  """
        folder = str(folder).replace('/', '')
        if folder == 'Common':
            return True
        request_url = self.bigip.icr_url + '/net/route-domain/'
        if route_domain_id is None:
            request_url += '~' + folder + '~' + folder
        else:
            request_url += '~' + folder + '~' + \
                folder + '_aux_' + str(route_domain_id)
        request_url += '?$select=name'

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('route', response.text)
            raise exceptions.RouteQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_domain(self, folder='Common'):
        """Get route domain """
        folder = str(folder).replace('/', '')
        if folder == 'Common':
            return 0
        if folder in self.domain_index:
            return self.domain_index[folder]
        else:
            request_url = self.bigip.icr_url + '/net/route-domain/'
            request_url += '~' + folder + '~' + folder
            request_url += '?$select=id'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'id' in response_obj:
                    self.domain_index[folder] = int(response_obj['id'])
                    return self.domain_index[folder]
            elif response.status_code != 404:
                Log.error('route-domain', response.text)
                raise exceptions.RouteQueryException(response.text)
            return 0

    @icontrol_rest_folder
    @log
    def get_domain_ids(self, folder='Common'):
        """Get route domains """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/route-domain/'
        request_url += '?$select=id,partition'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                route_domains = []
                for route_domain in response_obj['items']:
                    if not folder:
                        route_domains.append(int(route_domain['id']))
                    elif route_domain['partition'] == folder:
                        route_domains.append(int(route_domain['id']))
                return route_domains
        elif response.status_code != 404:
            Log.error('route-domain', response.text)
            raise exceptions.RouteQueryException(response.text)
        return []

    @icontrol_rest_folder
    @log
    def get_domain_names(self, folder='Common'):
        """Get route domains """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/route-domain/'
        request_url += '?$select=partition,name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                route_domains = []
                for route_domain in response_obj['items']:
                    if not folder:
                        route_domains.append(route_domain['name'])
                    elif route_domain['partition'] == folder:
                        route_domains.append(route_domain['name'])
                return route_domains
        elif response.status_code != 404:
            Log.error('route-domain', response.text)
            raise exceptions.RouteQueryException(response.text)
        return []

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common'):
        """Does route exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/route/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('route', response.text)
            raise exceptions.RouteQueryException(response.text)
        return False

    def _get_next_domain_id(self):
        """Get next route domain id """
        request_url = self.bigip.icr_url + '/net/route-domain?$select=id'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        all_identifiers = []
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for route_domain in response_obj['items']:
                    all_identifiers.append(int(route_domain['id']))
                all_identifiers = sorted(all_identifiers)
                all_identifiers.remove(0)
        else:
            raise exceptions.RouteQueryException(response.text)

        lowest_available_index = 1
        for i in range(len(all_identifiers)):
            if all_identifiers[i] < lowest_available_index:
                if len(all_identifiers) > (i + 1):
                    if all_identifiers[i + 1] > lowest_available_index:
                        return lowest_available_index
                    else:
                        lowest_available_index = lowest_available_index + 1
            elif all_identifiers[i] == lowest_available_index:
                lowest_available_index = lowest_available_index + 1
        else:
            return lowest_available_index

    @log
    def set_strict_state(self, name=None, folder='Common', state='disabled'):
        """Route domain strict attribute """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/net/route-domain/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            payload['strict'] = state
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('route', response.text)
                raise exceptions.RouteUpdateException(response.text)
        return False
