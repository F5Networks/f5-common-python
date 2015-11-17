"""vxlan.py """
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
# pylint: disable=broad-except

from eventlet import greenthread
from f5.bigip import exceptions
from f5.bigip.interfaces import icontrol_rest_folder
from f5.bigip.interfaces import log
from f5.bigip.interfaces import prefixed
from f5.bigip.interfaces import strip_folder_and_prefix
from f5.common import constants as const
from f5.common.logger import Log

import json
import os


class VXLAN(object):
    """Interface for vxlan related REST methods """

    OBJ_PREFIX = 'uuid_'

    def __init__(self, bigip):
        self.bigip = bigip

    @icontrol_rest_folder
    @log
    def create_multipoint_profile(self, name=None, folder='Common'):
        """Create vxlan multipoint tunnel profile """
        if not self.profile_exists(name=name, folder=folder):
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['defaultsFrom'] = 'vxlan'
            payload['floodingType'] = 'multipoint'
            payload['port'] = const.VXLAN_UDP_PORT
            request_url = self.bigip.icr_url + '/net/tunnels/vxlan/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.staus_code == 409:
                return True
            else:
                Log.error('VXLAN', response.text)
                raise exceptions.VXLANCreationException(response.text)
        else:
            return False

    @icontrol_rest_folder
    @log
    def delete_profile(self, name=None, folder='Common'):
        """Delete vxlan multipoint tunnel profile """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/vxlan/'
        request_url += '~' + folder + '~' + name

        response = self.bigip.icr_session.delete(
            request_url, timeout=const.CONNECTION_TIMEOUT)

        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def create_multipoint_tunnel(self, name=None,
                                 profile_name=None,
                                 self_ip_address=None,
                                 vxlanid=0,
                                 description=None,
                                 folder='Common',
                                 route_domain_id=0):
        """Create vxlan multipoint tunnel """
        if not self.tunnel_exists(name=name, folder=folder):
            folder = str(folder).replace('/', '')
            # check partition is okay to create in
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            payload['profile'] = profile_name
            payload['key'] = vxlanid
            payload['localAddress'] = self_ip_address
            payload['remoteAddress'] = '0.0.0.0'
            if description:
                payload['description'] = description
            request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                if not folder == 'Common':
                    self.bigip.route.add_vlan_to_domain_by_id(
                        name=name, folder=folder,
                        route_domain_id=route_domain_id)
                return True
            else:
                Log.error('VXLAN', response.text)
                raise exceptions.VXLANCreationException(response.text)
        else:
            return False

    @icontrol_rest_folder
    @log
    def delete_tunnel(self, name=None, folder='Common'):
        """Delete vxlan multipoint tunnel """
        folder = str(folder).replace('/', '')
        # delete arp and fdb records for this tunnel first
        request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
        request_url += '~' + folder + '~' + name + '?ver=11.5.0'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if const.FDB_POPULATE_STATIC_ARP:
                if 'records' in response_obj:
                    for record in response_obj['records']:
                        self.bigip.arp.delete_by_mac(
                            mac_address=record['name'], folder=folder)
            payload = dict()
            payload['records'] = []
            tunnel_link = self.bigip.icr_link(response_obj['selfLink'])
            response = self.bigip.icr_session.patch(
                tunnel_link, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code > 399:
                Log.error('fdb', response.text)
                raise exceptions.VXLANDeleteException(response.text)
        elif response.status_code != 404:
            Log.error('fdb', response.text)
            raise exceptions.VXLANQueryException(response.text)
        request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.delete(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANDeleteException(response.text)

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete vxlan multipoint tunnels """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
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
                        self.delete_all_fdb_entries(item['name'], folder)
                        response = self.bigip.icr_session.delete(
                            self.bigip.icr_link(item['selfLink']),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code > 400 and \
                           response.status_code != 404:
                            Log.error('VXLAN', response.text)
                            raise exceptions.VXLANDeleteException(
                                response.text)
        elif response.status_code != 404:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANQueryException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def get_fdb_entry(self,
                      tunnel_name=None,
                      mac=None,
                      folder='Common'):
        """Get vxlan fdb entry """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
        request_url += '~' + folder + '~' + tunnel_name + '?ver=11.5.0'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'records' in response_obj:
                if not mac:
                    return response_obj['records']
                else:
                    for record in response_obj['records']:
                        if record['name'] == mac:
                            return record
        elif response.status_code != 404:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANQueryException(response.text)
        return []

    @icontrol_rest_folder
    @log
    def add_fdb_entry(self,
                      tunnel_name=None,
                      mac_address=None,
                      vtep_ip_address=None,
                      arp_ip_address=None,
                      folder=None):
        """Add vxlan fdb entry """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
        request_url += '~' + folder + '~' + tunnel_name + '?ver=11.5.0'
        records = self.get_fdb_entry(tunnel_name=tunnel_name,
                                     mac=None,
                                     folder=folder)
        fdb_entry = dict()
        fdb_entry['name'] = mac_address
        fdb_entry['endpoint'] = vtep_ip_address

        for i in range(len(records)):
            if records[i]['name'] == mac_address:
                records[i] = fdb_entry
                break
        else:
            records.append(fdb_entry)

        payload = dict()
        payload['records'] = records
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            if const.FDB_POPULATE_STATIC_ARP:
                if arp_ip_address:
                    try:
                        if self.bigip.arp.create(ip_address=arp_ip_address,
                                                 mac_address=mac_address,
                                                 folder=folder):
                            return True
                        else:
                            return False
                    except Exception as exc:
                        Log.error('VXLAN',
                                  'could not create static arp: %s on %s'
                                  % (exc.message, self.bigip.device_name))
                        return False
            return True
        else:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def add_fdb_entries(self, fdb_entries=None):
        """Add vxlan fdb entries """
        for tunnel_name in fdb_entries:
            folder = fdb_entries[tunnel_name]['folder']
            if folder != 'Common':
                folder = prefixed(folder)
            request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
            request_url += '~' + folder + '~' + self.OBJ_PREFIX + \
                tunnel_name + '?ver=11.5.0'
            existing_records = self.get_fdb_entry(tunnel_name=tunnel_name,
                                                  mac=None,
                                                  folder=folder)
            new_records = []
            new_mac_addresses = []
            new_arp_addresses = {}

            tunnel_records = fdb_entries[tunnel_name]['records']
            for mac in tunnel_records:
                fdb_entry = dict()
                fdb_entry['name'] = mac
                fdb_entry['endpoint'] = tunnel_records[mac]['endpoint']
                new_records.append(fdb_entry)
                new_mac_addresses.append(mac)
                if tunnel_records[mac]['ip_address']:
                    new_arp_addresses[mac] = tunnel_records[mac]['ip_address']

            for record in existing_records:
                if not record['name'] in new_mac_addresses:
                    new_records.append(record)
                else:
                    # This fdb entry exists and is not being updated.
                    # So, do not update the ARP record either.
                    if record['name'] in new_arp_addresses:
                        del new_arp_addresses[record['name']]

            payload = dict()
            payload['records'] = new_records
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                if const.FDB_POPULATE_STATIC_ARP:
                    for mac in new_arp_addresses:
                        try:
                            self.bigip.arp.create(
                                ip_address=new_arp_addresses[mac],
                                mac_address=mac,
                                folder=folder)
                        except Exception as exc:
                            Log.error('VXLAN',
                                      'could not create static arp: %s'
                                      % exc.message)
            return True
        return False

    @icontrol_rest_folder
    @log
    def delete_fdb_entry(self,
                         tunnel_name=None,
                         mac_address=None,
                         arp_ip_address=None,
                         folder='Common'):
        """Delete vxlan fdb entry """
        folder = str(folder).replace('/', '')
        if const.FDB_POPULATE_STATIC_ARP:
            if arp_ip_address:
                self.bigip.arp.delete(ip_address=arp_ip_address,
                                      folder=folder)
        request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
        request_url += '~' + folder + '~' + tunnel_name + '?ver=11.5.0'
        records = self.get_fdb_entry(tunnel_name=tunnel_name,
                                     mac=None,
                                     folder=folder)
        if not records:
            return False
        original_len = len(records)
        records = [record for record in records
                   if record.get('name') != mac_address]
        if original_len != len(records):
            if len(records) == 0:
                records = None
            payload = dict()
            payload['records'] = records
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('VXLAN', response.text)
                raise exceptions.VXLANUpdateException(response.text)
            return False
        return False

    @icontrol_rest_folder
    @log
    def delete_fdb_entries(self,
                           tunnel_name=None,
                           fdb_entries=None):
        """Delete vxlan fdb entries """
        for tunnel_name in fdb_entries:
            folder = fdb_entries[tunnel_name]['folder']
            if folder != 'Common':
                folder = prefixed(folder)
            request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
            request_url += '~' + folder + '~' + tunnel_name + '?ver=11.5.0'
            existing_records = self.get_fdb_entry(tunnel_name=tunnel_name,
                                                  mac=None,
                                                  folder=folder)
            arps_to_delete = {}
            new_records = []

            for record in existing_records:
                for mac in fdb_entries[tunnel_name]['records']:
                    if record['name'] == mac and mac['ip_address']:
                        arps_to_delete[mac] = mac['ip_address']
                        break
                else:
                    new_records.append(record)

            if len(new_records) == 0:
                new_records = None
            payload = dict()
            payload['records'] = new_records
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                if const.FDB_POPULATE_STATIC_ARP:
                    for mac in arps_to_delete:
                        self.bigip.arp.delete(ip_address=arps_to_delete[mac],
                                              folder='Common')
            return True
        return False

    @icontrol_rest_folder
    @log
    def delete_all_fdb_entries(self, tunnel_name=None, folder='Common'):
        """Delete fdb entries """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/fdb/tunnel/'
        request_url += '~' + folder + '~' + tunnel_name + '?ver=11.5.0'
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps({'records': None}),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400 or response.status_code == 404:
            return True
        else:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_profiles(self, folder='Common'):
        """Get tunnel profiles """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/vxlan'
        request_filter = 'partition eq ' + folder
        request_url += '?$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            profile_list = []
            if 'items' in return_obj:
                for profile in return_obj['items']:
                    profile_list.append(
                        strip_folder_and_prefix(profile['name']))
                return profile_list
            else:
                return None
        elif response.status_code != 404:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def profile_exists(self, name=None, folder='Common'):
        """Does vxlan tunnel exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/vxlan/'
        request_url += '~' + folder + '~' + name

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code != 404:
            Log.error('VXLAN', response.text)
            raise exceptions.VXLANQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_tunnels(self, folder='Common'):
        """Get tunnels """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/tunnel'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '?$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            tunnel_list = []
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for tunnel in return_obj['items']:
                    if tunnel['profile'].find('vxlan') > 0:
                        tunnel_list.append(
                            strip_folder_and_prefix(tunnel['name']))
                return tunnel_list
            else:
                return None
        elif response.status_code != 404:
            Log.error('VXLAN', response.text)
            exceptions.VXLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_tunnel_key(self, name=None, folder='Common'):
        """Get tunnel key """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            Log.debug('VXLAN', 'get_tunnel_key got %s' + str(return_obj))
            return return_obj['key']
        elif response.status_code != 404:
            Log.error('VXLAN', response.text)
            exceptions.VXLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_tunnel_by_description(self, description=None, folder='Common'):
        """Get tunnel by description """
        folder = str(folder).replace('/', '')
        if description:
            request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
            if folder:
                request_filter = 'partition eq ' + folder
                request_url += '?$filter=' + request_filter
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for tunnel in return_obj['items']:
                        if tunnel['description'] == description:
                            return strip_folder_and_prefix(tunnel['name'])
                return None
            elif response.status_code != 404:
                Log.error('VXLAN', response.text)
                raise exceptions.VXLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_tunnel_folder(self, tunnel_name=None):
        """Get tunnel folder """
        if tunnel_name:
            request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'items' in return_obj:
                    for tunnel in return_obj['items']:
                        if tunnel['name'] == tunnel_name:
                            return tunnel['partition']
                return None
            elif response.status_code != 404:
                Log.error('VXLAN', response.text)
                raise exceptions.VXLANQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def tunnel_exists(self, name=None, folder='Common'):
        """Does tunnel exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/net/tunnels/tunnel/'
        request_url += '~' + folder + '~' + name

        for retry in range(2):
            if retry > 0:
                Log.error('VXLAN', 'Attempting REST retry after 401 error')
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 401:
                if retry < 1:
                    greenthread.sleep(1)
                    continue
                else:
                    Log.error('VXLAN', response.text)
                    raise exceptions.VXLANQueryException(response.text)
            elif response.status_code != 404:
                Log.error('VXLAN', response.text)
                raise exceptions.VXLANQueryException(response.text)
            else:
                return False
        return False

    @icontrol_rest_folder
    def _in_use(self, name=None, folder=None):
        """Is tunnel used by selfip? """
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
                Log.error('self', response.text)
                raise exceptions.VXLANQueryException(response.text)
        return False
