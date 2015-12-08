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
from f5.bigip.rest_collection import RESTInterfaceCollection
from f5.bigip.rest_collection import split_addr_port
from f5.bigip.rest_collection import strip_folder_and_prefix
from f5.common import constants as const
from f5.common.logger import Log
from requests.exceptions import HTTPError

import json
import os
import urllib


class Pool(RESTInterfaceCollection):
    def __init__(self, bigip):
        self.bigip = bigip
        self.base_uri = self.bigip.icr_uri + 'ltm/pool/'

    @log
    def create(self, name=None, lb_method=None,
               description=None, folder='Common'):
        folder = str(folder).replace('/', '')
        if not self.exists(name=name, folder=folder):
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if description:
                payload['description'] = description
            payload['loadBalancingMode'] = \
                self._get_rest_lb_method_type(lb_method)
            request_url = self.bigip.icr_url + '/ltm/pool'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolCreationException(response.text)
        return False

    def _delete(self, folder, name, timeout):
        try:
            self.bigip.icr_session.delete(self.base_uri, folder, name, timeout)
        except HTTPError as err:
            if (err.response.status_code == 400
                    and err.response.text.find('is referenced') > 0):
                Log.error('members', err.response.text)
            else:
                raise exceptions.PoolDeleteException(err.response.text)
        else:
            self._del_arp_and_fdb(name, folder)

    @log
    def delete(self, name=None, folder='Common'):
        if name:
            try:
                node_addresses =\
                    self._get_items(folder=folder, name=name,
                                    suffix='/members',
                                    timeout=const.CONNECTION_TIMEOUT)
            except HTTPError as err:
                if err.response.status_code == 404:
                    # https://github.com/F5Networks/f5-common-python/issues/25
                    return True
                else:
                    Log.error('members', err.response.text)
                    # https://github.com/F5Networks/f5-common-python/issues/25
                    return False

            for node_address in node_addresses:
                self._delete(folder, node_address, const.CONNECTION_TIMEOUT)

            try:
                self.bigip.icr_session.delete(self.base_uri, folder=folder,
                                              name=name, suffix='/members',
                                              timeout=const.CONNECTION_TIMEOUT)
            except HTTPError as err:
                if err.response.status_code == 404:
                    pass
                Log.error('members', err.response.text)
                raise
            return True
        return False

    # best effort ARP and fdb cleanup
    def _del_arp_and_fdb(self, ip_address, folder):

        if not const.FDB_POPULATE_STATIC_ARP:
            return
        arp_req = self.bigip.icr_url + '/net/arp'
        arp_req += '?$select=ipAddress,macAddress,selfLink'
        arp_req += '&$filter=partition eq ' + folder
        arp_res = self.bigip.icr_session.get(
            arp_req, timeout=const.CONNECTION_TIMEOUT)
        if not (arp_res.status_code < 400):
            return
        arp_obj = json.loads(arp_res.text)
        if 'items' not in arp_obj:
            return
        for arp in arp_obj['items']:
            if ip_address != arp['ipAddress']:
                continue
            # iControl REST ARP is broken < 11.7
            # self.bigip.arp.delete(
            #                  arp['ipAddress'],
            #                  folder)
            try:
                self.bigip.arp.delete(arp['ipAddress'], folder=folder)
            except Exception as exc:
                Log.error('ARP', exc.message)
            fdb_req = self.bigip.icr_url + '/net/fdb/tunnel'
            fdb_req += '?$select=records,selfLink'
            fdb_req += '&$filter=partition eq ' + folder
            response = self.bigip.icr_session.get(
                fdb_req, timeout=const.CONNECTION_TIMEOUT)
            if not response.status_code < 400:
                continue
            fdb_obj = json.loads(response.text)
            if 'items' not in fdb_obj:
                continue
            for tunnel in fdb_obj['items']:
                if 'records' not in tunnel:
                    continue
                records = list(tunnel['records'])
                need_to_update = False
                for record in tunnel['records']:
                    if record['name'] == arp['macAddress']:
                        records.remove(record)
                        need_to_update = True
                if need_to_update:
                    payload = dict()
                    payload['records'] = records
                    response = self.bigip.icr_session.put(
                        self.bigip.icr_link(tunnel['selfLink']),
                        data=json.dumps(payload),
                        timeout=const.CONNECTION_TIMEOUT)
                if response.status_code > 399:
                    Log.error('fdb', response.text)

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/pool/'
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
                        if not self.delete(item['name'], folder):
                            return False
                return True
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_members(self, name=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '/members?$select=name'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            members = []
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for member in return_obj['items']:
                        (addr, port) = split_addr_port(member['name'])
                        members.append(
                            {'addr': addr,
                             'port': int(port)})
            elif response.status_code != 404:
                Log.error('pool', response.text)
                raise exceptions.PoolQueryException(response.text)
            return members
        return None

    @icontrol_rest_folder
    @log
    def get_pools(self, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/pool'
        request_url += '?$select=name'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        pool_names = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for pool in return_obj['items']:
                    pool_names.append(
                        strip_folder_and_prefix(pool['name']))
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return pool_names

    @log
    def purge_orphaned_pools(self, known_pools, delete_virtual_server=True):
        request_url = self.bigip.icr_url + '/ltm/pool'
        request_url += '?$select=name,partition'

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        existing_pools = {}
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for pool in return_obj['items']:
                    existing_pools[pool['name']] = pool['partition']
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)

        Log.debug('pool', 'purging pools - existing : %s, known : %s'
                  % (existing_pools.keys(), known_pools))

        # we start with all pools and remove the ones that are
        # completely unrelated to the plugin or are OK to be there.
        cleanup_list = dict(existing_pools)

        # remove all pools which are not managed by this plugin
        for pool in existing_pools:
            if not pool.startswith(self.OBJ_PREFIX):
                del cleanup_list[pool]

        for pool in known_pools:
            decorated_pool = self.OBJ_PREFIX + pool
            Log.debug('pool', 'excluding %s from %s' %
                      (str(decorated_pool), str(cleanup_list)))
            if decorated_pool in cleanup_list:
                del cleanup_list[decorated_pool]

        # anything left should be purged
        for pool in cleanup_list:
            Log.debug('purge_orphaned_pools',
                      "Purging pool %s in folder %s" %
                      (pool, cleanup_list[pool]))
            vs_name = \
                self.bigip.virtual_server.get_virtual_servers_by_pool_name(
                    pool_name=pool, folder=cleanup_list[pool])
            if vs_name:
                try:
                    self.bigip.virtual_server.delete(
                        name=vs_name, folder=cleanup_list[pool])
                    self.bigip.virtual_server.delete_persist_profile_like(
                        match=vs_name, folder=cleanup_list[pool])
                    self.bigip.rule.delete_like(
                        match=vs_name, folder=cleanup_list[pool])
                    self.bigip.virtual_server.delete_profile_like(
                        match=vs_name, folder=cleanup_list[pool])
                except Exception as e:
                    Log.error('purge_orphaned_pools', e.message)
            try:
                Log.debug('purge_orphaned_pools',
                          "Deleting pool %s in folder %s" %
                          (pool, cleanup_list[pool]))
                self.delete(name=pool, folder=cleanup_list[pool])
            except Exception as e:
                    Log.error('purge_orphaned_pools', e.message)

    @icontrol_rest_folder
    @log
    def get_members_monitor_status(
            self, name=None, folder='Common', config_mode='object'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            if config_mode == 'iapp':
                request_url += '~' + folder + '~' + name + \
                    '.app~' + name
            else:
                request_url += '~' + folder + '~' + name
            request_url += '/members?$select=name,state'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            members = []
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for member in return_obj['items']:
                        (addr, port) = split_addr_port(member['name'])
                        member_state = 'MONITOR_STATUS_' + \
                            member['state'].upper()
                        members.append(
                            {'addr': addr,
                             'port': port,
                             'state': member_state})
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolQueryException(response.text)
            return members
        return None

    @icontrol_rest_folder
    @log
    def get_statistics(self, name=None, folder='Common', config_mode='object'):
        if not name:
            return None
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/pool/'
        if config_mode == 'iapp':
            request_url += '~' + folder + '~' + name + '.app~' + name
        else:
            request_url += '~' + folder + '~' + name
        request_url += '/stats'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_stats = {}
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'entries' in return_obj:
                stats = return_obj['entries']
                for stat in stats:
                    if 'nestedStats' in stats[stat]:
                        stats = stats[stat]['nestedStats']['entries']
                        break
                for stat in stats:
                    name = stat
                    value = None
                    if 'value' in stats[name]:
                        value = stats[name]['value']
                    if 'description' in stats[name]:
                        value = stats[name]['description']
                    if value is None:
                        Log.error('poolstats', 'bad stats:' + response.text)
                        continue
                    (st, val) = self._get_icontrol_stat(name, value)
                    if st:
                        return_stats[st] = val
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return return_stats

    @icontrol_rest_folder
    @log
    def add_member(self, name=None, ip_address=None, port=None,
                   folder='Common', no_checks=False):
        if name and ip_address and port:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '/members'
            payload = dict()
            if ':' in ip_address:
                payload['name'] = ip_address + '.' + str(port)
            else:
                payload['name'] = ip_address + ':' + str(port)
            payload['partition'] = folder
            payload['address'] = ip_address
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                Log.error('pool',
                          'tried to add member %s to non-existant pool %s.' %
                          (payload['name'], '/' + folder + '/' + name))
                return False
            elif response.status_code == 409:
                return True
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def enable_member(self, name=None, ip_address=None, port=None,
                      folder='Common', no_checks=False):
        if name and ip_address and port:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '/members/'
            request_url += '~' + folder + '~'
            if ':' in ip_address:
                request_url += urllib.quote(ip_address) + '.' + str(port)
            else:
                request_url += urllib.quote(ip_address) + ':' + str(port)

            payload = dict()
            payload['session'] = 'user-enabled'
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                Log.error('pool',
                          'tried to enable non-existant member %s on pool %s.'
                          % (ip_address + ':' + str(port),
                             '/' + folder + '/' + name))
                return False
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def disable_member(self, name=None, ip_address=None, port=None,
                       folder='Common', no_checks=False):
        if name and ip_address and port:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '/members/'
            request_url += '~' + folder + '~'
            if ':' in ip_address:
                request_url += urllib.quote(ip_address) + '.' + str(port)
            else:
                request_url += urllib.quote(ip_address) + ':' + str(port)
            payload = dict()
            payload['session'] = 'user-disabled'
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                Log.error('pool',
                          'tried to disable non-existant member %s on pool %s.'
                          % (ip_address + ':' + str(port),
                             '/' + folder + '/' + name))
                return False
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_member_ratio(self, name=None, ip_address=None, port=None,
                         ratio=1, folder='Common', no_checks=False):
        if name and ip_address and port:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '/members/'
            request_url += '~' + folder + '~'
            if ':' in ip_address:
                request_url += urllib.quote(ip_address) + '.' + str(port)
            else:
                request_url += urllib.quote(ip_address) + ':' + str(port)
            payload = dict()
            payload['ratio'] = ratio
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                Log.error(
                    'pool',
                    'tried to set ratio on non-existant member %s on pool %s.'
                    % (ip_address + ':' + str(port),
                        '/' + folder + '/' + name))
                return False
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_member(self, name=None, ip_address=None,
                      port=None, folder='Common'):
        if name and ip_address and port:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '/members/'
            request_url += '~' + folder + '~'
            if ':' in ip_address:
                request_url += urllib.quote(ip_address) + '.' + str(port)
            else:
                request_url += urllib.quote(ip_address) + ':' + str(port)
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400 or response.status_code == 404:
                # delete nodes
                node_req = self.bigip.icr_url + '/ltm/node/'
                node_req += '~' + folder + '~' + urllib.quote(ip_address)
                response = self.bigip.icr_session.delete(
                    node_req, timeout=const.CONNECTION_TIMEOUT)
                if response.status_code == 400 and \
                        response.text.find('is referenced') > 0:
                    # Node address is part of multiple pools
                    pass
                elif response.status_code > 399 and \
                        (not response.status_code == 404):
                    Log.error('node', response.text)
                    raise exceptions.PoolDeleteException(response.text)
                else:
                    self._del_arp_and_fdb(ip_address, folder)
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_all_nodes(self, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/node'
        request_url += '?$select=address,selfLink'
        request_url += '&$filter=partition eq ' + folder
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for node in return_obj['items']:
                    ip_address = node['address']
                    response = self.bigip.icr_session.delete(
                        self.bigip.icr_link(node['selfLink']),
                        timeout=const.CONNECTION_TIMEOUT)
                    if response.status_code < 400:
                        self._del_arp_and_fdb(ip_address, folder)
        elif response.status_code != 404:
            Log.error('node', response.text)
            return False
        return True

    @icontrol_rest_folder
    @log
    def get_node_addresses(self, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/node'
        request_url += '?$select=address'
        request_url += '&$filter=partition eq ' + folder
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        node_addresses = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for node in return_obj['items']:
                    node_addresses.append(node['address'])
        elif response.status_code != 404:
            Log.error('node', response.text)
            raise exceptions.PoolQueryException(response.text)
        return node_addresses

    @icontrol_rest_folder
    @log
    def get_service_down_action(self, name=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=serviceDownAction'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'serviceDownAction' not in response_obj:
                    return 'NONE'
                else:
                    if response_obj['serviceDownAction'] == 'drop':
                        return 'DROP'
                    if response_obj['serviceDownAction'] == 'reset':
                        return 'RESET'
                    if response_obj['serviceDownAction'] == 'reselect':
                        return 'RESELECT'
            elif response.status_code == 404:
                Log.error('pool', 'tied to get AOSD for non-existant pool %s'
                          % '/' + folder + '/' + name)
                raise exceptions.PoolQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_service_down_action(self, name=None,
                                service_down_action=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            if service_down_action:
                payload['serviceDownAction'] = str(service_down_action).lower()
            else:
                payload['serviceDownAction'] = 'none'
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_lb_method(self, name=None, lb_method=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            if lb_method:
                payload['loadBalancingMode'] = \
                    self._get_rest_lb_method_type(lb_method)
            else:
                payload['loadBalancingMode'] = 'least-connections-member'
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_lb_method(self, name=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=loadBalancingMode'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'loadBalancingMode' not in response_obj:
                    return 'round-robin'
                else:
                    if response_obj['loadBalancingMode'] == \
                            'least-connections-member':
                        return 'LEAST_CONNECTIONS'
                    if response_obj['loadBalancingMode'] == \
                            'ratio-least-connections-member':
                        return 'RATIO_LEAST_CONNECTIONS'
                    if response_obj['loadBalancingMode'] == \
                            'least-connections-node':
                        return 'SOURCE_IP'
                    if response_obj['loadBalancingMode'] == \
                            'observed-member':
                        return 'OBSERVED_MEMBER'
                    if response_obj['loadBalancingMode'] == \
                            'predictive-member':
                        return 'PREDICTIVE_MEMBER'
                    if response_obj['loadBalancingMode'] == \
                            'ratio-member':
                        return 'RATIO'
                    if response_obj['loadBalancingMode'] == \
                            'round-robin':
                        return 'ROUND_ROBIN'
            elif response.status_code == 404:
                Log.error(
                    'pool',
                    'tied to get lb_method for non-existant pool %s'
                    % '/' + folder + '/' + name)
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_description(self, name=None, description=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            payload = dict()
            if description:
                payload['description'] = description
            else:
                payload['description'] = ''
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_description(self, name=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=description'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'description' not in response_obj:
                    return None
                else:
                    return response_obj['description']
            elif response.status_code == 404:
                Log.error(
                    'pool',
                    'tied to get description for non-existant pool %s'
                    % '/' + folder + '/' + name)
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_monitors(self, name=None, folder='Common'):
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=monitor'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                monitors = []
                if 'monitor' in response_obj:
                    w_split = response_obj['monitor'].split()
                    for w in w_split:
                        if w.startswith('/'):
                            monitors.append(strip_folder_and_prefix(w))
                return monitors
            elif response.status_code != 404:
                Log.error('pool', response.text)
                raise exceptions.PoolQueryException(response.text)
        return []

    @icontrol_rest_folder
    @log
    def add_monitor(self, name=None, monitor_name=None, folder='Common'):
        if name and monitor_name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/pool/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=monitor'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'monitor' in response_obj:
                    w_split = response_obj['monitor'].split()
                    existing_monitors = []
                    for w in w_split:
                        if w.startswith('/'):
                            existing_monitors.append(w)
                    fp_monitor = '/' + folder + '/' + monitor_name
                    monitor_string = ''
                    if fp_monitor not in existing_monitors:
                        if response_obj['monitor'].startswith('min'):
                            min_count = w_split[1]
                            monitor_string = 'min ' + min_count + ' of { '
                            for monitor in existing_monitors:
                                monitor_string += monitor + ' '
                            monitor_string += fp_monitor + ' '
                            monitor_string += '}'
                        else:
                            for monitor in existing_monitors:
                                monitor_string += monitor + ' and '
                            monitor_string += fp_monitor
                        request_url = self.bigip.icr_url + '/ltm/pool/'
                        request_url += '~' + folder + '~' + name
                        payload = dict()
                        payload['monitor'] = monitor_string
                        response = self.bigip.icr_session.patch(
                            request_url, data=json.dumps(payload),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code < 400:
                            return True
                        else:
                            Log.error('pool', response.text)
                            raise exceptions.PoolUpdateException(response.text)
                    else:
                        return True
                else:
                    payload = dict()
                    payload['monitor'] = monitor_name
                    request_url = self.bigip.icr_url + '/ltm/pool/'
                    request_url += '~' + folder + '~' + name
                    response = self.bigip.icr_session.patch(
                        request_url, data=json.dumps(payload),
                        timeout=const.CONNECTION_TIMEOUT)
                    if response.status_code < 400:
                        return True
                    else:
                        Log.error('pool', response.text)
                        raise exceptions.PoolUpdateException(response.text)
            else:
                Log.error('pool', response.text)
                raise exceptions.PoolQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_monitor(self, name=None, monitor_name=None, folder='Common'):
        if not (name and monitor_name):
            return False
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/pool/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=monitor'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'monitor' in response_obj:
                w_split = response_obj['monitor'].split()
                existing_monitors = []
                for w in w_split:
                    if w.startswith('/'):
                        existing_monitors.append(w)
                fp_monitor = '/' + folder + '/' + monitor_name
                monitor_string = ''
                if fp_monitor in existing_monitors:
                    existing_monitors.remove(fp_monitor)
                    new_monitor_count = len(existing_monitors)
                    if new_monitor_count > 0:
                        if response_obj['monitor'].startswith('min'):
                            min_count = w_split[1]
                            if min_count > new_monitor_count:
                                min_count = new_monitor_count
                            monitor_string = 'min ' + min_count + ' of { '
                            for monitor in existing_monitors:
                                monitor_string += monitor + ' '
                            monitor_string += '}'
                        else:
                            for i in range(new_monitor_count):
                                if (i + 1) < new_monitor_count:
                                    monitor_string += \
                                        existing_monitors[i] + ' and '
                                else:
                                    monitor_string += \
                                        existing_monitors[i] + ' '
                    request_url = self.bigip.icr_url + '/ltm/pool/'
                    request_url += '~' + folder + '~' + name
                    payload = dict()
                    payload['monitor'] = monitor_string
                    response = self.bigip.icr_session.put(
                        request_url, data=json.dumps(payload),
                        timeout=const.CONNECTION_TIMEOUT)
                    if response.status_code < 400:
                        return True
                    else:
                        Log.error('pool', response.text)
                        raise exceptions.PoolUpdateException(response.text)
                else:
                    return True
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return False

    def _get_lb_method_type(self, lb_method):
        lb_method_type = self.lb_pool.typefactory.create('LocalLB.LBMethod')
        lb_method = str(lb_method).upper()

        if lb_method == 'LEAST_CONNECTIONS':
            return lb_method_type.LB_METHOD_LEAST_CONNECTION_MEMBER
        elif lb_method == 'RATIO_LEAST_CONNECTIONS':
            return lb_method_type.LB_METHOD_RATIO_LEAST_CONNECTION_MEMBER
        elif lb_method == 'SOURCE_IP':
            return lb_method_type.LB_METHOD_LEAST_CONNECTION_NODE_ADDRESS
        elif lb_method == 'OBSERVED_MEMBER':
            return lb_method_type.LB_METHOD_OBSERVED_MEMBER
        elif lb_method == 'PREDICTIVE_MEMBER':
            return lb_method_type.LB_METHOD_PREDICTIVE_MEMBER
        elif lb_method == 'RATIO':
            return lb_method_type.LB_METHOD_RATIO_MEMBER
        else:
            return lb_method_type.LB_METHOD_ROUND_ROBIN

    def _get_rest_lb_method_type(self, lb_method):
        lb_method = str(lb_method).upper()

        if lb_method == 'LEAST_CONNECTIONS':
            return 'least-connections-member'
        elif lb_method == 'RATIO_LEAST_CONNECTIONS':
            return 'ratio-least-connections-member'
        elif lb_method == 'SOURCE_IP':
            return 'least-connections-node'
        elif lb_method == 'OBSERVED_MEMBER':
            return 'observed-member'
        elif lb_method == 'PREDICTIVE_MEMBER':
            return 'predictive-member'
        elif lb_method == 'RATIO':
            return 'ratio-member'
        else:
            return 'round-robin'

    def _get_icontrol_stat(self, name, value):
        if name == "activeMemberCnt":
            return ('POOL_ACTIVE_MEMBERS', value)
        elif name == "connqAll.ageEdm":
            return ('STATISTIC_CONNQUEUE_AGGR_AGE_EXPONENTIAL_DECAY_MAX',
                    value)
        elif name == "connqAll.ageEma":
            return ('STATISTIC_CONNQUEUE_AGGR_AGE_MOVING_AVG', value)
        elif name == "connqAll.ageHead":
            return ('STATISTIC_CONNQUEUE_AGGR_AGE_OLDEST_ENTRY', value)
        elif name == "connqAll.ageMax":
            return ('STATISTIC_CONNQUEUE_AGGR_AGE_MAX', value)
        elif name == "connqAll.depth":
            return ('STATISTIC_CONNQUEUE_AGGR_CONNECTIONS', value)
        elif name == "connqAll.serviced":
            return ('STATISTIC_CONNQUEUE_AGGR_SERVICED', value)
        elif name == "connq.ageEdm":
            return ('STATISTIC_CONNQUEUE_AGE_EXPONENTIAL_DECAY_MAX', value)
        elif name == "connq.ageEma":
            return ('STATISTIC_CONNQUEUE_AGE_MOVING_AVG', value)
        elif name == "connq.ageHead":
            return ('STATISTIC_CONNQUEUE_AGE_OLDEST_ENTRY', value)
        elif name == "connq.ageMax":
            return ('STATISTIC_CONNQUEUE_AGE_MAX', value)
        elif name == "connq.depth":
            return ('STATISTIC_CONNQUEUE_CONNECTIONS', value)
        elif name == "connq.serviced":
            return ('STATISTIC_CONNQUEUE_SERVICED', value)
        elif name == "curSessions":
            return ('STATISTIC_CURRENT_SESSIONS', value)
        elif name == "minActiveMembers":
            return ('POOL_MINIMUM_ACTIVE_MEMBERS', value)
        elif name == "monitorRule":
            return ('POOL_MONITOR_RULE', value)
        elif name == "tmName":
            return ('POOL_NAME', os.path.basename(value))
        elif name == "serverside.bitsIn":
            return ('STATISTIC_SERVER_SIDE_BYTES_IN', int(value) * 8)
        elif name == "serverside.bitsOut":
            return ('STATISTIC_SERVER_SIDE_BYTES_OUT', int(value) * 8)
        elif name == "serverside.curConns":
            return ('STATISTIC_SERVER_SIDE_CURRENT_CONNECTIONS', value)
        elif name == "serverside.maxConns":
            return ('STATISTIC_SERVER_SIDE_MAXIMUM_CONNECTIONS', value)
        elif name == "serverside.pktsIn":
            return ('STATISTIC_SERVER_SIDE_PACKETS_IN', value)
        elif name == "serverside.pktsOut":
            return ('STATISTIC_SERVER_SIDE_PACKETS_OUT', value)
        elif name == "serverside.totConns":
            return ('STATISTIC_SERVER_SIDE_TOTAL_CONNECTIONS', value)
        elif name == "status.availabilityState":
            return ('AVAILABLE_STATE', value)
        elif name == "status.enabledState":
            return ('ENABLED_STATE', value)
        elif name == "status.statusReason":
            return ('STATUS_REASON', value)
        elif name == "totRequests":
            return ('STATISTIC_TOTAL_REQUESTS', value)
        else:
            return (None, None)

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common', config_mode='object'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/pool/'
        if config_mode == 'iapp':
            request_url += '~' + folder + '~' + name + '.app~' + name
        else:
            request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def member_exists(self, name=None, ip_address=None,
                      port=None, folder='Common'):
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/pool/'
        request_url += '~' + folder + '~' + name
        request_url += '/members/'
        request_url += '~' + folder + '~'
        if ':' in ip_address:
            request_url += urllib.quote(ip_address) + '.' + str(port)
        else:
            request_url += urllib.quote(ip_address) + ':' + str(port)
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'address' in response_obj:
                return True
            else:
                return False
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_all_node_count(self):
        request_url = self.bigip.icr_url + '/ltm/node'
        request_url += '?$top=1&$select=totalItems'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'totalItems' in response_obj:
                return int(response_obj['totalItems'])
        elif response.status_code != 404:
            Log.error('pool', response.text)
            raise exceptions.PoolQueryException(response.text)
        return 0
