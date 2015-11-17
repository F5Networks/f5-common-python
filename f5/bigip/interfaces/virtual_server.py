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
from f5.bigip.interfaces import icontrol_rest_folder
from f5.bigip.interfaces import log
from f5.bigip.interfaces import split_addr_port
from f5.bigip.interfaces import strip_folder_and_prefix
from f5.common import constants as const
from f5.common.logger import Log

import json
import os
import urllib


class VirtualServer(object):

    def __init__(self, bigip):
        self.bigip = bigip
        self.common_persistence_profiles = {}
        self.folder_persistence_profiles = {}
        self.common_profiles = {}
        self.folder_profiles = {}

    @icontrol_rest_folder
    @log
    def create(self, name=None, ip_address=None, mask=None,
               port=None, protocol=None, vlan_name=None,
               traffic_group=None, use_snat=True,
               snat_pool=None, folder='Common', preserve_vlan_name=False):
        """Create vip """

        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if str(ip_address).endswith('%0'):
                ip_address = ip_address[:-2]
            if not port:
                port = 0
            if ':' in ip_address:
                payload['destination'] = ip_address + '.' + str(port)
            else:
                payload['destination'] = ip_address + ':' + str(port)
            if mask:
                payload['mask'] = mask
            if not protocol:
                protocol = 'tcp'
            else:
                protocol = self._get_rest_protocol(protocol)
            payload['ipProtocol'] = protocol
            if vlan_name:
                payload['vlansEnabled'] = True
                payload['vlans'] = [vlan_name]
            else:
                payload['vlansDisabled'] = True
            if use_snat:
                payload['sourceAddressTranslation'] = dict()
                if snat_pool:
                    payload['sourceAddressTranslation']['type'] = 'snat'
                    payload['sourceAddressTranslation']['pool'] = snat_pool
                else:
                    payload['sourceAddressTranslation']['type'] = 'automap'
            if not traffic_group:
                traffic_group = \
                    const.SHARED_CONFIG_DEFAULT_FLOATING_TRAFFIC_GROUP

            request_url = self.bigip.icr_url + '/ltm/virtual/'
            Log.debug('virtual', 'adding virtual: ' + str(payload))
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400 or response.status_code == 409:
                request_url = self.bigip.icr_url + '/ltm/virtual-address/'
                request_url += '~' + folder + '~' + urllib.quote(ip_address)
                payload = dict()
                payload['trafficGroup'] = traffic_group
                response = self.bigip.icr_session.put(
                    request_url, data=json.dumps(payload),
                    timeout=const.CONNECTION_TIMEOUT)
                if response.status_code < 400:
                    return True
                else:
                    Log.error('virtual-address', response.text)
                    raise exceptions.VirtualServerUpdateException(
                        response.text)
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def create_ip_forwarder(self, name=None, ip_address=None,
                            mask=None, vlan_name=None,
                            traffic_group=None, use_snat=True,
                            snat_pool=None, folder='Common',
                            preserve_vlan_name=False):
        """Create ip forwarding vip """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if str(ip_address).endswith('%0'):
                ip_address = ip_address[:-2]
            if ':' in ip_address:
                payload['destination'] = ip_address + '.0'
            else:
                payload['destination'] = ip_address + ':0'
            payload['mask'] = mask
            payload['ipProtocol'] = 'any'
            if vlan_name:
                payload['vlansEnabled'] = True
                payload['vlans'] = [vlan_name]
            else:
                payload['vlansDisabled'] = True
            if vlan_name:
                payload['vlans'] = [vlan_name]
            if use_snat:
                payload['sourceAddressTranslation'] = dict()
                if snat_pool:
                    payload['sourceAddressTranslation']['type'] = 'snat'
                    payload['sourceAddressTranslation']['pool'] = snat_pool
                else:
                    payload['sourceAddressTranslation']['type'] = 'automap'
            if not traffic_group:
                traffic_group = \
                    const.SHARED_CONFIG_DEFAULT_FLOATING_TRAFFIC_GROUP
            payload['ipForward'] = True

            request_url = self.bigip.icr_url + '/ltm/virtual/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400 or response.status_code == 409:
                request_url = self.bigip.icr_url + '/ltm/virtual-address/'
                request_url += '~' + folder + '~' + urllib.quote(ip_address)
                payload = dict()
                payload['trafficGroup'] = traffic_group
                response = self.bigip.icr_session.put(
                    request_url, data=json.dumps(payload),
                    timeout=const.CONNECTION_TIMEOUT)
                if response.status_code < 400:
                    return True
                else:
                    Log.error('virtual-address', response.text)
                    raise exceptions.VirtualServerUpdateException(
                        response.text)
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def create_fastl4(self, name=None, ip_address=None, mask=None,
                      port=None, protocol=None, vlan_name=None,
                      traffic_group=None, use_snat=True,
                      snat_pool=None, folder='Common',
                      preserve_vlan_name=False):
        """Create fast L4 vip """

        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if str(ip_address).endswith('%0'):
                ip_address = ip_address[:-2]
            if not port:
                port = 0
            if ':' in ip_address:
                payload['destination'] = ip_address + '.' + str(port)
            else:
                payload['destination'] = ip_address + ':' + str(port)
            payload['mask'] = mask
            if not protocol:
                protocol = 'tcp'
            else:
                protocol = self._get_rest_protocol(protocol)
            payload['ipProtocol'] = protocol
            if vlan_name:
                payload['vlansEnabled'] = True
                payload['vlans'] = [vlan_name]
            else:
                payload['vlansDisabled'] = True
            if use_snat:
                payload['sourceAddressTranslation'] = dict()
                if snat_pool:
                    payload['sourceAddressTranslation']['type'] = 'snat'
                    payload['sourceAddressTranslation']['pool'] = snat_pool
                else:
                    payload['sourceAddressTranslation']['type'] = 'automap'
            if not traffic_group:
                traffic_group = \
                    const.SHARED_CONFIG_DEFAULT_FLOATING_TRAFFIC_GROUP
            payload['profiles'] = ['fastL4']

            request_url = self.bigip.icr_url + '/ltm/virtual/'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400 or response.status_code == 409:
                request_url = self.bigip.icr_url + '/ltm/virtual-address/'
                request_url += '~' + folder + '~' + urllib.quote(ip_address)
                payload = dict()
                payload['trafficGroup'] = traffic_group
                response = self.bigip.icr_session.put(
                    request_url, data=json.dumps(payload),
                    timeout=const.CONNECTION_TIMEOUT)
                if response.status_code < 400:
                    return True
                else:
                    Log.error('virtual-address', response.text)
                    raise exceptions.VirtualServerUpdateException(
                        response.text)
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def add_profile(self, name=None, profile_name=None,
                    client_context=True, server_context=True,
                    folder='Common'):
        """Add vip profile """
        if name and profile_name:
            folder = str(folder).replace('/', '')
            found_profile = self._which_profile(profile_name, folder)
            if found_profile:
                profile_name = found_profile
            if not self.virtual_server_has_profile(name,
                                                   profile_name,
                                                   client_context,
                                                   server_context,
                                                   folder):
                payload = dict()
                payload['name'] = profile_name
                if client_context and not server_context:
                    payload['context'] = 'clientside'
                elif not client_context and server_context:
                    payload['context'] = 'serverside'
                else:
                    payload['context'] = 'all'
                request_url = self.bigip.icr_url + '/ltm/virtual/'
                request_url += '~' + folder + '~' + name
                request_url += '/profiles'
                response = self.bigip.icr_session.post(
                    request_url, data=json.dumps(payload),
                    timeout=const.CONNECTION_TIMEOUT)
                if response.status_code < 400:
                    return True
                elif response.status_code == 409:
                    return True
                else:
                    Log.error('profile', response.text)
                    raise exceptions.VirtualServerCreationException(
                        response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_profile(self, name=None, profile_name=None,
                       client_context=True, server_context=True,
                       folder='Common'):
        """Remove vip profile """
        if name and profile_name:
            folder = str(folder).replace('/', '')
            found_profile = self._which_profile(profile_name, folder)
            if found_profile:
                profile_name = found_profile
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '/profiles?$select=name,selfLink,context'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'items' in response_obj:
                    for profile in response_obj['items']:
                        if profile_name == profile['name'] or \
                                profile_name == strip_folder_and_prefix(
                                profile['name']):
                            if (profile['context'] == 'clientside' and
                                    client_context) or \
                                    (profile['context'] == 'serverside' and
                                     server_context) or \
                                    (profile['context'] == 'all' and
                                     client_context and server_context):
                                profile['selfLink'] = \
                                    profile['selfLink'].split('?')[0]
                                del_req = self.bigip.icr_link(
                                    profile['selfLink'])
                                del_res = self.bigip.icr_session.delete(
                                    del_req, timeout=const.CONNECTION_TIMEOUT)
                                if del_res.status_code < 400:
                                    return True
                                else:
                                    Log.error('profile', del_res.text)
                                    exps = exceptions
                                    exp = exps.VirtualServerDeleteException
                                    raise exp(del_res.text)

                elif response.status_code == 404:
                    return True
                else:
                    Log.error('virtual', response.text)
                    raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def virtual_server_has_profile(self, name=None, profile_name=None,
                                   client_context=True, server_context=True,
                                   folder='Common'):
        """Does vip have profile? """
        if name and profile_name:
            folder = str(folder).replace('/', '')
            found_profile = self._which_profile(profile_name, folder)
            if found_profile:
                profile_name = found_profile
            profiles = self.get_profiles(name, folder)
            common_name = strip_folder_and_prefix(profile_name)
            for profile in profiles:
                if profile_name in profile:
                    if client_context and \
                            profile.get(profile_name)['client_context']:
                        return True
                    if server_context and \
                            profile.get(profile_name)['server_context']:
                        return True
                if common_name in profile:
                    if client_context and \
                            profile.get(common_name)['client_context']:
                        return True
                    if server_context and \
                            profile.get(common_name)['server_context']:
                        return True
        return False

    @icontrol_rest_folder
    @log
    def http_profile_exists(self, name=None, folder='Common'):
        """Does http profile exist? """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/profile/http/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=name'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return False
            else:
                Log.error('http-profile', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_profiles(self, name=None, folder='Common'):
        """Get profiles """
        return_profiles = []
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '/profiles'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'items' in response_obj:
                    for profile in response_obj['items']:
                        p = dict()
                        profile_name = strip_folder_and_prefix(
                            profile['name'])
                        p[profile_name] = dict()
                        if profile['context'] == 'all':
                            p[profile_name]['client_context'] = True
                            p[profile_name]['server_context'] = True
                        elif profile['context'] == 'clientside':
                            p[profile_name]['client_context'] = True
                            p[profile_name]['server_context'] = False
                        elif profile['context'] == 'serverside':
                            p[profile_name]['client_context'] = False
                            p[profile_name]['server_context'] = True
                        return_profiles.append(p)
            elif response.status_code != 404:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return return_profiles

    @icontrol_rest_folder
    @log
    def get_all_profiles(self, folder='Common'):
        """Get profiles """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_profiles = []
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for p in response_obj['items']:
                    type_link = self.bigip.icr_link(
                        p['reference']['link']
                        ) + '&$select=name,partition&$filter=partition eq ' \
                          + folder
                    pr_res = self.bigip.icr_session.get(
                        type_link, timeout=const.CONNECTION_TIMEOUT)
                    if pr_res.status_code < 400:
                        pr_res_obj = json.loads(pr_res.text)
                        if 'items' in pr_res_obj:
                            for profile in pr_res_obj['items']:
                                if profile['partition'] == 'Common':
                                    self.common_profiles[profile['name']] = 1
                                else:
                                    self.folder_profiles[profile['name']] = \
                                        profile['partition']
                                return_profiles.append(profile['name'])
                    else:
                        Log.error('profile', pr_res.text)
                        raise exceptions.VirtualServerQueryException(
                            pr_res.text)
        elif response.status_code == 404:
            return []
        else:
            raise exceptions.VirtualServerQueryException(response.text)

        self.folder_profiles[folder] = folder

        return return_profiles

    @icontrol_rest_folder
    @log
    def delete_all_profiles(self, folder='Common'):
        """Delete profiles """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for p in response_obj['items']:
                    type_link = self.bigip.icr_link(
                        p['reference']['link']
                        ) + '&$select=name,selfLink&$filter=partition eq ' + \
                            folder
                    pr_res = self.bigip.icr_session.get(
                        type_link, timeout=const.CONNECTION_TIMEOUT)
                    if pr_res.status_code < 400:
                        pr_res_obj = json.loads(pr_res.text)
                        if 'items' in pr_res_obj:
                            for profile in pr_res_obj['items']:
                                if profile['name'].startswith(self.OBJ_PREFIX):
                                    profile['selfLink'] = \
                                        profile['selfLink'].spit('?')[0]
                                    del_resp = self.bigip.icr_session.delete(
                                        self.bigip.icr_link(
                                            profile['selfLink']),
                                        timeout=const.CONNECTION_TIMEOUT)
                                    if del_resp.status_code > 399 and \
                                            del_resp.status_code != 404:
                                        Log.error('profile', del_resp.text)
                                        exps = exceptions
                                        exp = exps.VirtualServerDeleteException
                                        raise exp(del_resp.text)
                                    else:
                                        self.folder_profiles = {}
                                        self.common_profiles = {}
                    else:
                        Log.error('profile', pr_res.text)
                        raise exceptions.VirtualServerQueryException(
                            pr_res.text)
        elif response.status_code == 404:
            True
        else:
            raise exceptions.VirtualServerQueryException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def delete_all_profiles_like(self, match=None, folder='Common'):
        """Delete profiles that match by name """
        if not match:
            return False
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for p in response_obj['items']:
                    type_link = self.bigip.icr_link(
                        p['reference']['link']
                        ) + '&$select=name,selfLink&$filter=partition eq ' + \
                            folder
                    pr_res = self.bigip.icr_session.get(
                        type_link, timeout=const.CONNECTION_TIMEOUT)
                    if pr_res.status_code < 400:
                        pr_res_obj = json.loads(pr_res.text)
                        if 'items' in pr_res_obj:
                            for profile in pr_res_obj['items']:
                                if profile['name'].find(match) > -1:
                                    profile['selfLink'] = \
                                        profile['selfLink'].spit('?')[0]
                                    del_resp = self.bigip.icr_session.delete(
                                        self.bigip.icr_link(
                                            profile['selfLink']),
                                        timeout=const.CONNECTION_TIMEOUT)
                                    if del_resp.status_code > 399 and \
                                       del_resp.status_code != 404:
                                        Log.error('profile', del_resp.text)
                                        exps = exceptions
                                        exp = exps.VirtualServerDeleteException
                                        raise exp(del_resp.text)
                                    else:
                                        self.folder_profiles = {}
                                        self.common_profiles = {}
                    else:
                        Log.error('profile', pr_res.text)
                        raise exceptions.VirtualServerQueryException(
                            pr_res.text)
        elif response.status_code == 404:
            True
        else:
            raise exceptions.VirtualServerQueryException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def create_http_profile(self, name=None, xff=True, pipelining=False,
                            unknown_verbs=False, server_agent=None,
                            folder='Common'):
        """Create http profile """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['partition'] = folder
            if xff:
                payload['insertXforwardedFor'] = 'enabled'
            if server_agent:
                payload['serverAgentName'] = server_agent
            enforcement = dict()
            if pipelining:
                enforcement['pipeline'] = 'allow'
            else:
                enforcement['pipeline'] = 'reject'
            if unknown_verbs:
                enforcement['unknownMethod'] = 'allow'
            else:
                enforcement['unknownMethod'] = 'reject'
            request_url = self.bigip.icr_url + '/ltm/profile/http'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                self.folder_profiles[name] = folder
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('http-profile', response.text)
                raise exceptions.VirtualServerCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_all_http_profiles(self, folder='Common'):
        """Get all http profiles """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile/http'
        request_url += '?$select=name'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_profiles = []
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for profile in response_obj['items']:
                    return_profiles.append(
                        strip_folder_and_prefix(profile['name']))
        elif response.status_code == 404:
            return []
        else:
            raise exceptions.VirtualServerQueryException(response.text)
        return return_profiles

    @icontrol_rest_folder
    @log
    def delete_all_http_profiles(self, folder='Common'):
        """Delete all http profiles """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile/http'
        request_url += '?$select=name,selfLink'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for profile in response_obj['items']:
                    if profile['name'].startswith(self.OBJ_PREFIX):
                        profile['selfLink'] = profile['selfLink'].split('?')[0]
                        response = self.bigip.icr_session.delete(
                            self.bigip.icr_link(profile['selfLink']),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code > 399 and \
                           response.status_code != 404:
                            Log.error('persistence', response.text)
                            raise exceptions.VirtualServerDeleteException(
                                response.text)
                        else:
                            self.common_profiles = {}
                            self.folder_profiles = {}
        elif response.status_code != 404:
            Log.error('persistence', response.text)
            raise exceptions.VirtualServerQueryException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def create_cookie_profile(self, name=None,
                              cookie_name=None, folder='Common'):
        """Create cookie profile """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            if cookie_name:
                payload['cookieName'] = cookie_name
            payload['partition'] = folder
            request_url = self.bigip.icr_url + '/ltm/persistence/cookie'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                self.folder_persistence_profiles[name] = folder
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('cookie-persist', response.text)
                raise exceptions.VirtualServerCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_all_persistence_profiles(self, folder='Common'):
        """Get all persistence profiles """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_profiles = []
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for p in response_obj['items']:
                    type_link = self.bigip.icr_link(
                        p['reference']['link']
                        ) + '&$select=name,partition&$filter=partition eq ' \
                          + folder
                    pr_res = self.bigip.icr_session.get(
                        type_link, timeout=const.CONNECTION_TIMEOUT)
                    if pr_res.status_code < 400:
                        pr_res_obj = json.loads(pr_res.text)
                        if 'items' in pr_res_obj:
                            for profile in pr_res_obj['items']:
                                if profile['partition'] == 'Common':
                                    self.common_persistence_profiles[
                                        profile['name']] = 1
                                else:
                                    self.folder_persistence_profiles[
                                        profile['name']] = \
                                        profile['partition']
                                return_profiles.append(profile['name'])
                    else:
                        Log.error('persistence', pr_res.text)
                        raise exceptions.VirtualServerQueryException(
                            pr_res.text)
        elif response.status_code == 404:
            return []
        else:
            raise exceptions.VirtualServerQueryException(response.text)

        self.folder_persistence_profiles[folder] = folder

        return return_profiles

    @icontrol_rest_folder
    @log
    def delete_all_persistence_profiles(self, folder='Common'):
        """Delete all persistence profiles """
        timeout = const.CONNECTION_TIMEOUT
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence'
        response = self.bigip.icr_session.get(
            request_url, timeout=timeout)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for p in response_obj['items']:
                    type_link = self.bigip.icr_link(
                        p['reference']['link']
                        ) + '&$select=name,selfLink&$filter=partition eq ' + \
                            folder
                    pr_res = self.bigip.icr_session.get(
                        type_link, timeout=timeout)
                    if pr_res.status_code < 400:
                        pr_res_obj = json.loads(pr_res.text)
                        if 'items' in pr_res_obj:
                            for profile in pr_res_obj['items']:
                                if profile['name'].startswith(self.OBJ_PREFIX):
                                    profile['selfLink'] = \
                                        profile['selfLink'].split('?')[0]
                                    del_resp = self.bigip.icr_session.delete(
                                        self.bigip.icr_link(
                                            profile['selfLink']),
                                        timeout=timeout)
                                    if del_resp.status_code > 399 and \
                                       del_resp.status_code != 404:
                                        Log.error('persistence', del_resp.text)
                                        exps = exceptions
                                        exp = exps.VirtualServerDeleteException
                                        raise exp(del_resp.text)
                                    else:
                                        self.folder_persistence_profiles = {}
                                        self.common_persistence_profiles = {}
                    else:
                        Log.error('persistence', pr_res.text)
                        raise exceptions.VirtualServerQueryException(
                            pr_res.text)
        elif response.status_code == 404:
            True
        else:
            raise exceptions.VirtualServerQueryException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def cookie_persist_profile_exists(self, name=None, folder='Common'):
        """Does cookie persistence profile exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence/cookie/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return False
        else:
            Log.error('cookie-persist', response.text)
            raise exceptions.VirtualServerQueryException(response.text)

    @icontrol_rest_folder
    @log
    def delete_cookie_persist_profile(self, name=None, folder='Common'):
        """Delete cookie persistence profile """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence/cookie/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name,selfLink'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if response_obj['name'] == name:
                response_obj['selfLink'] = \
                    response_obj['selfLink'].split('?')[0]
                del_req = self.bigip.icr_link(response_obj['selfLink'])
                del_res = self.bigip.icr_session.delete(
                    del_req, timeout=const.CONNECTION_TIMEOUT)
                if del_res.status_code < 400:
                    if name in self.folder_persistence_profiles:
                        del self.folder_persistence_profiles[name]
                    if name in self.common_persistence_profiles:
                        del self.common_profiles[name]
                    return True
                else:
                    Log.error('persistence', del_res.text)
        elif response.status_code == 404:
            return True
        else:
            Log.error('cookie-persist', response.text)
            raise exceptions.VirtualServerDeleteException(response.text)

    @icontrol_rest_folder
    @log
    def create_uie_profile(self, name=None, rule_name=None, folder='Common'):
        """Create uie profile """
        if name and rule_name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['name'] = name
            payload['rule'] = rule_name
            payload['partition'] = folder
            request_url = self.bigip.icr_url + '/ltm/persistence/universal'
            response = self.bigip.icr_session.post(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                self.folder_persistence_profiles[name] = folder
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('persistence', response.text)
                raise exceptions.VirtualServerCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def uie_persist_profile_exists(self, name=None, folder='Common'):
        """Does uie profile exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence/universal/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return False
        else:
            Log.error('uie-persist', response.text)
            raise exceptions.VirtualServerQueryException(response.text)

    @icontrol_rest_folder
    @log
    def delete_uie_persist_profile(self, name=None, folder='Common'):
        """Delete uie profile """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence/universal/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name,selfLink'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if response_obj['name'] == name:
                response_obj['selfLink'] = \
                    response_obj['selfLink'].split('?')[0]
                del_req = self.bigip.icr_link(response_obj['selfLink'])
                del_res = self.bigip.icr_session.delete(
                    del_req, timeout=const.CONNECTION_TIMEOUT)
                if del_res.status_code < 400:
                    if name in self.folder_persistence_profiles:
                        del self.folder_persistence_profiles[name]
                    if name in self.common_persistence_profiles:
                        del self.common_persistence_profiles[name]
                    return True
                else:
                    Log.error('persistence', del_res.text)
        elif response.status_code == 404:
            return True
        else:
            Log.error('uie-persist', response.text)
            raise exceptions.VirtualServerDeleteException(response.text)

    @icontrol_rest_folder
    @log
    def delete_persist_profile(self, name=None, folder='Common'):
        """Delete persist profile """
        folder = str(folder).replace('/', '')
        link = self.get_persistence_link(name, folder)
        if link:
            link = link.split('?')[0]
            response = self.bigip.icr_session.delete(
                link, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                if name in self.folder_persistence_profiles:
                    del self.folder_persistence_profiles[name]
                if name in self.common_persistence_profiles:
                    del self.common_persistence_profiles[name]
                return True
            elif response.status_code == 404:
                return True
            else:
                raise exceptions.VirtualServerDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_persist_profile_like(self, match=None, folder='Common'):
        """Delete persist profile """
        if not match:
            return False
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/persistence'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for p in response_obj['items']:
                    type_link = self.bigip.icr_link(
                        p['reference']['link']
                        ) + '&$select=name,selfLink&$filter=partition eq ' + \
                            folder
                    pr_res = self.bigip.icr_session.get(
                        type_link, timeout=const.CONNECTION_TIMEOUT)
                    if pr_res.status_code < 400:
                        pr_res_obj = json.loads(pr_res.text)
                        if 'items' in pr_res_obj:
                            for profile in pr_res_obj['items']:
                                if profile['name'].find(match) > -1:
                                    profile['selfLink'] = \
                                        profile['selfLink'].split('?')[0]
                                    del_resp = self.bigip.icr_session.delete(
                                        self.bigip.icr_link(
                                            profile['selfLink']),
                                        timeout=const.CONNECTION_TIMEOUT)
                                    if del_resp.status_code > 399 and \
                                            del_resp.status_code != 404:
                                        Log.error('persistence', del_resp.text)
                                        exps = exceptions
                                        exp = exps.VirtualServerDeleteException
                                        raise exp(del_resp.text)
                                    else:
                                        self.folder_persistence_profiles = {}
                                        self.common_persistence_profiles = {}
                    else:
                        Log.error('persistence', pr_res.text)
                        raise exceptions.VirtualServerQueryException(
                            pr_res.text)
        elif response.status_code == 404:
            True
        else:
            raise exceptions.VirtualServerQueryException(response.text)
        return True

    @icontrol_rest_folder
    @log
    def get_profile_link(self, name=None, folder='Common'):
        """Get profile link """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/profile/'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            for refs in response_obj['items']:
                link = self.bigip.icr_link(refs['reference']['link'])
                link += '&$select=name,fullPath,selfLink'
                profile_resp = self.bigip.icr_session.get(
                    link, timeout=const.CONNECTION_TIMEOUT)
                if profile_resp.status_code < 400:
                    profile_obj = json.loads(profile_resp.text)
                    if 'items' in profile_obj:
                        for profile in profile_obj['items']:
                            if profile['name'] == name:
                                return self.bigip.icr_link(
                                    profile['selfLink'])
        elif response.status_code == 404:
            return None
        else:
            raise exceptions.VirtualServerQueryException(response.text)

    @icontrol_rest_folder
    @log
    def get_persistence_link(self, name=None):
        """Get persistence link """
        if name:
            request_url = self.bigip.icr_url + '/ltm/persistence/'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                for refs in response_obj['items']:
                    link = self.bigip.icr_link(refs['reference']['link'])
                    link += '&$select=name,partition,fullPath,selfLink'
                    profile_resp = self.bigip.icr_session.get(
                        link, timeout=const.CONNECTION_TIMEOUT)
                    if profile_resp.status_code < 400:
                        profile_obj = json.loads(profile_resp.text)
                        if 'items' in profile_obj:
                            for profile in profile_obj['items']:
                                if profile['name'] == name:
                                    return self.bigip.icr_link(
                                        profile['selfLink'])
        elif response.status_code == 404:
            return None
        else:
            raise exceptions.VirtualServerQueryException(response.text)

    @icontrol_rest_folder
    @log
    def virtual_server_has_rule(self, name=None,
                                rule_name=None, folder='Common'):
        """Does vip have rule? """
        if name and rule_name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=rules'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'rules' in response_obj:
                    rule = '/' + folder + '/' + rule_name
                    if rule in response_obj['rules']:
                        return True
                    else:
                        return False
            elif response.status_code == 404:
                return False
            else:
                raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def add_rule(self, name=None, rule_name=None,
                 priority=500, folder='Common'):
        """Add rule to vip """
        if name and rule_name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=rules'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'rules' in response_obj:
                    rule = '/' + folder + '/' + rule_name
                    if rule not in response_obj['rules']:
                        rules_list = response_obj['rules']
                        rules_list.append(rule)
                        rules = {'rules': rules_list}
                        request_url = self.bigip.icr_url + '/ltm/virtual/'
                        request_url += '~' + folder + '~' + name

                        Log.debug('virtual-server', 'add rule body: %s'
                                  % response_obj)

                        response = self.bigip.icr_session.patch(
                            request_url, data=json.dumps(rules),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code < 400:
                            return True
                        else:
                            Log.error('virtual', response.text)
                            raise exceptions.VirtualServerUpdateException(
                                response.text)
                    else:
                        # rule was already assigned to this virtual server
                        return True
                else:
                    # no rules.. add this one
                    rules = {'rules': ['/' + folder + '/' + rule_name]}
                    request_url = self.bigip.icr_url + '/ltm/virtual/'
                    request_url += '~' + folder + '~' + name
                    response = self.bigip.icr_session.patch(
                        request_url, data=json.dumps(rules),
                        timeout=const.CONNECTION_TIMEOUT)
                    if response.status_code < 400:
                        return True
                    else:
                        Log.error('virtual', response.text)
                        raise exceptions.VirtualServerUpdateException(
                            response.text)

            elif response.status_code == 404:
                return False
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_rule(self, name=None, rule_name=None,
                    priority=500, folder='Common'):
        """Remove rule from vip """
        if name and rule_name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=rules'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'rules' in response_obj:
                    rule = '/' + folder + '/' + rule_name
                    if rule in response_obj['rules']:
                        rules_list = response_obj['rules']
                        rules_list.remove(rule)
                        rules = {'rules': rules_list}
                        request_url = self.bigip.icr_url + '/ltm/virtual/'
                        request_url += '~' + folder + '~' + name
                        response = self.bigip.icr_session.put(
                            request_url, data=json.dumps(rules),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code < 400:
                            return True
                        else:
                            Log.error('virtual', response.text)
                            raise exceptions.VirtualServerUpdateException(
                                response.text)
                    else:
                        # rule not assigned
                        return True
                else:
                    # no assigned rules
                    return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_persist_profile(self, name=None, profile_name=None,
                            folder='Common'):
        """Set persist profile on vip """
        if name and profile_name:
            folder = str(folder).replace('/', '')
            found_profile = self._which_persistence_profile(profile_name,
                                                            folder)
            if found_profile:
                profile_name = found_profile
            payload = dict()
            payload['persist'] = [{'name': profile_name}]
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_fallback_persist_profile(self, name=None, profile_name=None,
                                     folder='Common'):
        """Set fallback persist profile on vip """
        if name and profile_name:
            folder = str(folder).replace('/', '')
            found_profile = self._which_persistence_profile(profile_name,
                                                            folder)
            if found_profile:
                profile_name = found_profile
            payload = dict()
            payload['fallbackPersistence'] = \
                strip_folder_and_prefix(profile_name)
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_all_persist_profiles(self, name=None, folder='Common'):
        """Remove persist profiles from vip """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['fallbackPersistence'] = ''
            payload['persist'] = []
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_and_delete_persist_profile(self, name=None,
                                          profile_name=None, folder='Common'):
        """Remove and delete persist profiles """
        if name and profile_name:
            folder = str(folder).replace('/', '')
            self.remove_all_persist_profiles(name, folder)
            return self.delete_persist_profile(profile_name, folder)
        return False

    @icontrol_rest_folder
    @log
    def enable_virtual_server(self, name=None, folder='Common'):
        """Enable vip """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['enabled'] = True
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def disable_virtual_server(self, name=None, folder='Common'):
        """Disable vip """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['disabled'] = True
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, folder='Common'):
        """Delete vip """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_virtual_servers(self, folder='Common'):
        """Get vips """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/virtual'
        request_url += '?$select=name'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        vs_names = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for vs in return_obj['items']:
                    vs_names.append(strip_folder_and_prefix(vs['name']))
        elif response.status_code != 404:
            Log.error('virtual', response.text)
            raise exceptions.VirtualServerQueryException(response.text)
        return vs_names

    @icontrol_rest_folder
    @log
    def get_virtual_servers_by_pool_name(self,
                                         pool_name=None,
                                         folder='Common'):
        """Get vips by pool name """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/virtual'
        request_url += '?$select=name,pool'
        request_url += '&$filter=partition eq ' + folder

        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        vs_names = []
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            if 'items' in return_obj:
                for vs in return_obj['items']:
                    if 'pool' in vs and \
                            os.path.basename(vs['pool']) == pool_name:
                        vs_names.append(strip_folder_and_prefix(vs['name']))
        elif response.status_code != 404:
            Log.error('virtual', response.text)
            raise exceptions.VirtualServerQueryException(response.text)
        return vs_names

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Delete vips """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/virtual/'
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
                        item['selfLink'] = item['selfLink'].split('?')[0]
                        response = self.bigip.icr_session.delete(
                            self.bigip.icr_link(item['selfLink']),
                            timeout=const.CONNECTION_TIMEOUT)
                        if response.status_code > 400 and \
                           response.status_code != 404:
                            Log.error('virtual', response.text)
                            raise exceptions.VirtualServerDeleteException(
                                response.text)
            return True
        elif response.status_code != 404:
            Log.error('rule', response.text)
            raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_pool(self, name=None, folder='Common'):
        """Get pool """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=pool'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'pool' in response_obj:
                    return strip_folder_and_prefix(response_obj['pool'])
                else:
                    return None
            elif response.status_code == 404:
                return None
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_pool(self, name=None, pool_name=None, folder='Common'):
        """Set pool on vip """
        if name and pool_name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['pool'] = pool_name
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_addr_port(self, name=None, ip_address=None,
                      port=None, folder='Common'):
        """Set vip addr and port """
        if name and ip_address:
            if not port:
                port = 0
            else:
                try:
                    port = int(port)
                except Exception as e:
                    Log.error('virtual', e.message)
                    return False
            folder = str(folder).replace('/', '')
            payload = dict()
            if ':' in ip_address:
                payload['destination'] = ip_address + "." + str(port)
            else:
                payload['destination'] = ip_address + ":" + str(port)
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_addr(self, name=None, folder='Common'):
        """Get vip addr """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=destination'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'destination' in response_obj:
                    dest = os.path.basename(
                        response_obj['destination'])
                    (ip_addr, port) = split_addr_port(dest)  # @UnusedVariable
                    return ip_addr
                else:
                    return None
            elif response.status_code == 404:
                return None
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_port(self, name=None, folder='Common'):
        """Get vip port """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=destination'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'destination' in response_obj:
                    dest = os.path.basename(
                        response_obj['destination'])
                    (ip_addr, port) = split_addr_port(dest)  # @UnusedVariable
                    return port
                else:
                    return -1
            elif response.status_code == 404:
                return -1
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return -1

    @icontrol_rest_folder
    @log
    def set_mask(self, name=None, netmask=None, folder='Common'):
        """Set vip mask """
        if name and netmask:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['mask'] = netmask
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_mask(self, name=None, folder='Common'):
        """Get vip mask """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=mask'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'mask' in response_obj:
                    return response_obj['mask']
                else:
                    return None
            elif response.status_code == 404:
                return None
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_protocol(self, name=None, protocol=None, folder='Common'):
        """Set vip protocol """
        if name and protocol:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['ipProtocol'] = protocol.lower()
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_protocol(self, name=None, folder='Common'):
        """Get vip protocol """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=ipProtocol'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'ipProtocol' in response_obj:
                    return response_obj['ipProtocol'].upper()
                else:
                    return ''
            elif response.status_code == 404:
                return ''
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return ''

    @icontrol_rest_folder
    @log
    def set_description(self, name=None, description=None, folder='Common'):
        """Set vip description """
        if name and description:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['description'] = description
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_description(self, name=None, folder='Common'):
        """Get vip description """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=description'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'description' in response_obj:
                    return response_obj['description']
                else:
                    return ''
            elif response.status_code == 404:
                return None
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return ''

    @icontrol_rest_folder
    @log
    def set_traffic_group(self, name=None, traffic_group=None,
                          folder='Common'):
        """Set vip traffic group """
        if name and traffic_group:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=destination'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'destination' in response_obj:
                    dest = response_obj['destination']
                    (address, port) = split_addr_port(dest)  # @UnusedVariable
                    va_req = self.bigip.icr_url + '/ltm/virtual-address/'
                    va_req += urllib.quote(address).replace('/', '~')
                    payload = dict()
                    payload['trafficGroup'] = traffic_group
                    va_response = self.bigip.icr_session.patch(
                        va_req, data=json.dumps(payload),
                        timeout=const.CONNECTION_TIMEOUT)
                    if va_response.status_code < 400:
                        return True
                    else:
                        Log.error('virtual-address', va_response.text)
                        raise exceptions.VirtualServerUpdateException(
                            va_response.text)
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_traffic_group(self, name=None, folder='Common'):
        """Get vip traffic group """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=destination'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'destination' in response_obj:
                    dest = response_obj['destination']
                    (address, port) = split_addr_port(dest)  # @UnusedVariable
                    va_req = self.bigip.icr_url + '/ltm/virtual-address/'
                    va_req += urllib.quote(address).replace('/', '~')
                    va_req += '?$select=trafficGroup'
                    va_response = self.bigip.icr_session.get(
                        va_req, timeout=const.CONNECTION_TIMEOUT)
                    if va_response.status_code < 400:
                        va_response_obj = json.loads(va_response.text)
                        return os.path.basename(
                            va_response_obj['trafficGroup'])
                    else:
                        Log.error('virtual-address', va_response.text)
                        raise exceptions.VirtualServerQueryException(
                            va_response.text)
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_connection_limit(self, name=None, connection_limit=0,
                             folder='Common'):
        """Set vip connection limit """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['connectionLimit'] = connection_limit
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_connection_limit(self, name=None,
                             folder='Common'):
        """Get vip connection limit """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '?$select=connectionLimit'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'connectionLimit' in response_obj:
                    return int(response_obj['ConnectionLimit'])
                else:
                    return 0
            elif response.status_code == 404:
                return 0
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return 0

    @icontrol_rest_folder
    @log
    def set_snat_automap(self, name=None, folder='Common'):
        """Set vip snat automap """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['sourceAddressTranslation'] = {"type": "automap"}
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def set_snat_pool(self, name=None, pool_name=None, folder='Common'):
        """Set vip snat pool """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['sourceAddressTranslation'] = {"type": "snat",
                                                   "pool": pool_name}
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def remove_snat(self, name=None, folder='Common'):
        """Set vip snat """
        if name:
            folder = str(folder).replace('/', '')
            payload = dict()
            payload['sourceAddressTranslation'] = {"type": "none"}
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('virtual', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_statistics(self, name=None, folder='Common'):
        """Get vip statistics """
        if name:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual/'
            request_url += '~' + folder + '~' + name
            request_url += '/stats'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            return_stats = {}
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'entries' in return_obj:
                    for stat in return_obj['entries']:
                        name = stat
                        if 'value' in return_obj['entries'][name]:
                            value = return_obj['entries'][name]['value']
                        if 'description' in return_obj['entries'][name]:
                            value = return_obj['entries'][name]['description']
                        (st, val) = self._get_icontrol_stat(name, value)
                        if st:
                            return_stats[st] = val
            elif response.status_code != 404:
                Log.error('pool', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
            return return_stats
        return None

    def _get_rest_protocol(self, protocol):
        """Get vip protocol """
        if str(protocol).lower() == 'tcp':
            return 'tcp'
        elif str(protocol).lower() == 'udp':
            return 'udp'
        elif str(protocol).lower() == 'http':
            return 'tcp'
        elif str(protocol).lower() == 'https':
            return 'tcp'
        elif str(protocol).lower() == 'dns':
            return 'udp'
        elif str(protocol).lower() == 'dnstcp':
            return 'tcp'
        elif str(protocol).lower() == 'sctp':
            return 'sctp'
        else:
            return 'tcp'

    def _get_icontrol_stat(self, name, value):
        """Get vip stats """
        if name == "clientside.bitsIn":
            return ('STATISTIC_CLIENT_SIDE_BYTES_IN', (value * 8))
        elif name == "clientside.bitsOut":
            return ('STATISTIC_CLIENT_SIDE_BYTES_OUT', (value * 8))
        elif name == "clientside.curConns":
            return ('STATISTIC_CLIENT_SIDE_CURRENT_CONNECTIONS', value)
        elif name == "clientside.maxConns":
            return ('STATISTIC_CLIENT_SIDE_MAXIMUM_CONNECTIONS', value)
        elif name == "clientside.pktsIn":
            return ('STATISTIC_CLIENT_SIDE_PACKETS_IN', value)
        elif name == "clientside.pktsOut":
            return ('STATISTIC_CLIENT_SIDE_PACKETS_OUT', value)
        elif name == "clientside.totConns":
            return ('STATISTIC_CLIENT_SIDE_TOTAL_CONNECTIONS', value)
        elif name == "csMaxConnDur":
            return ('STATISTIC_MAXIMUM_CONNECTION_DURATION', value)
        elif name == "csMeanConnDur":
            return ('STATISTIC_MEAN_CONNECTION_DURATION', value)
        elif name == "csMinConnDur":
            return ('STATISTIC_MINIMUM_CONNECTION_DURATION', value)
        elif name == "ephemeral.bitsIn":
            return ('STATISTIC_EPHEMERAL_BYTES_IN', (value * 8))
        elif name == "ephemeral.bitsOut":
            return ('STATISTIC_EPHEMERAL_BYTES_OUT', (value * 8))
        elif name == "ephemeral.curConns":
            return ('STATISTIC_EPHEMERAL_CURRENT_CONNECTIONS', value)
        elif name == "ephemeral.maxConns":
            return ('STATISTIC_EPHEMERAL_MAXIMUM_CONNECTIONS', value)
        elif name == "ephemeral.pktsIn":
            return ('STATISTIC_EPHEMERAL_PACKETS_IN', value)
        elif name == "ephemeral.pktsOut":
            return ('STATISTIC_EPHEMERAL_PACKETS_OUT', value)
        elif name == "ephemeral.totConns":
            return ('STATISTIC_EPHEMERAL_TOTAL_CONNECTIONS', value)
        elif name == "fiveMinAvgUsageRatio":
            return ('STATISTIC_VIRTUAL_SERVER_FIVE_MIN_AVG_CPU_USAGE', value)
        elif name == "fiveSecAvgUsageRatio":
            return ('STATISTIC_VIRTUAL_SERVER_FIVE_SEC_AVG_CPU_USAGE', value)
        elif name == "oneMinAvgUsageRatio":
            return ('STATISTIC_VIRTUAL_SERVER_ONE_MIN_AVG_CPU_USAGE', value)
        elif name == "syncookie.accepts":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_SW_ACCEPTS', value)
        elif name == "syncookie.hwAccepts":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_HW_ACCEPTS', value)
        elif name == "syncookie.hwSyncookies":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_HW_TOTAL', value)
        elif name == "syncookie.hwsyncookieInstance":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_HW_INSTANCES', value)
        elif name == "syncookie.rejects":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_SW_REJECTS', value)
        elif name == "syncookie.swsyncookieInstance":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_SW_INSTANCES', value)
        elif name == "syncookie.syncacheCurr":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_CACHE_USAGE', value)
        elif name == "syncookie.syncacheOver":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_CACHE_OVERFLOWS',
                    value)
        elif name == "syncookie.syncookies":
            return ('STATISTIC_VIRTUAL_SERVER_SYNCOOKIE_SW_TOTAL', value)
        elif name == "totRequests":
            return ('STATISTIC_TOTAL_REQUESTS', value)
        else:
            return (None, None)

    @icontrol_rest_folder
    @log
    def get_virtual_service_insertion(self, folder='Common'):
        """Get vips """
        folder = str(folder).replace('/', '')
        virtual_services = []
        request_url = self.bigip.icr_url + '/ltm/virtual'
        request_url += '?$select=name,destination,mask,ipProtocol'
        if folder:
            request_filter = 'partition eq ' + folder
            request_url += '&$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for v in response_obj['items']:
                    dest = \
                        os.path.basename(
                            v['destination'])
                    (vip_addr, vip_port) = split_addr_port(dest)
                    name = strip_folder_and_prefix(v['name'])
                    service = {name: {}}
                    service[name]['address'] = vip_addr
                    service[name]['netmask'] = v['mask']
                    service[name]['protocol'] = v['ipProtocol']
                    service[name]['port'] = vip_port
                    virtual_services.append(service)
        elif response.status_code != 404:
            Log.error('virtual', response.text)
            raise exceptions.VirtualServerQueryException(response.text)
        return virtual_services

    @icontrol_rest_folder
    @log
    def _get_virtual_address_traffic_group(self, named_address=None,
                                           folder='Common'):
        """Get vip address traffic group """
        if named_address:
            folder = str(folder).replace('/', '')
            request_url = self.bigip.icr_url + '/ltm/virtual-address/'
            request_url += '~' + folder + '~' + urllib.quote(named_address)
            request_url += '?$select=trafficGroup'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'trafficGroup' in response_obj:
                    return os.path.basename(response_obj['trafficGroup'])
            else:
                Log.error('virtual-address', response.text)
                raise exceptions.VirtualServerQueryException(response.text)
        return None

    @icontrol_rest_folder
    def _set_virtual_address_traffic_group(self, named_address=None,
                                           traffic_group=None,
                                           folder='Common'):
        """Set vip address traffic group """
        if named_address:
            folder = str(folder).replace('/', '')
            if not traffic_group:
                traffic_group = const.SHARED_CONFIG_DEFAULT_TRAFFIC_GROUP
            payload = dict()
            payload['trafficGroup'] = traffic_group
            request_url = self.bigip.icr_url + '/ltm/virtual-address/'
            request_url += '~' + folder + '~' + urllib.quote(named_address)
            response = self.bigip.icr_session.patch(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                Log.error('virtual-address', response.text)
                raise exceptions.VirtualServerUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def exists(self, name=None, folder='Common'):
        """Does vip exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/virtual/'
        request_url += '~' + folder + '~' + name
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return False
        else:
            Log.error('virtual', response.text)
            raise exceptions.VirtualServerQueryException(response.text)

    @icontrol_rest_folder
    @log
    def virtual_address_exists(self, named_address=None, folder='Common'):
        """Does vip address exist? """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/virtual-address/'
        request_url += '~' + folder + '~' + urllib.quote(named_address)
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return False
        else:
            Log.error('virtual-address', response.text)
            raise exceptions.VirtualServerQueryException(response.text)

    def _which_profile(self, profile_name=None, folder='Common'):
        """which profile """
        if not self.common_profiles:
            Log.debug('profiles', 'getting common profile cache')
            self.get_all_profiles(folder='Common')
        if not folder == 'Common':
            if folder not in self.folder_profiles.values():
                Log.debug('profiles',
                          'getting profile cache for %s' % folder)
                self.get_all_profiles(folder=folder)

        if profile_name in self.folder_profiles:
            return profile_name
        if profile_name in self.common_profiles:
            return profile_name
        common_name = strip_folder_and_prefix(profile_name)
        if common_name in self.folder_profiles:
            Log.debug('profiles', 'profile renamed: %s' % common_name)
            return common_name
        if common_name in self.common_profiles:
            Log.debug('profiles', 'profile renamed: %s' % common_name)
            return common_name
        # refesh cache
        Log.debug('profile',
                  'refreshing profile cache for %s on cache miss'
                  % folder)
        self.get_all_profiles(folder=folder)
        if profile_name in self.folder_profiles:
            return profile_name
        return None

    def _which_persistence_profile(self, profile_name=None, folder='Common'):
        """which persistence profile """
        if not self.common_persistence_profiles:
            self.get_all_persistence_profiles(folder='Common')
            Log.debug('persistence',
                      'getting common persistence profile cache')
        if not folder == 'Common':
            if folder not in self.folder_persistence_profiles.values():
                self.get_all_persistence_profiles(folder=folder)
                Log.debug('persistence',
                          'getting persistence profile cache for %s' % folder)

        if profile_name in self.folder_persistence_profiles:
            return profile_name
        if profile_name in self.common_persistence_profiles:
            return profile_name
        common_name = strip_folder_and_prefix(profile_name)
        if common_name in self.folder_persistence_profiles:
            Log.debug('persistence', 'profile renamed: %s' % common_name)
            return common_name
        if common_name in self.common_persistence_profiles:
            Log.debug('persistence', 'profile renamed: %s' % common_name)
            return common_name
        # refesh cache
        Log.debug('persistence',
                  'refreshing persistence profile cache for %s on cache miss'
                  % folder)
        self.get_all_persistence_profiles(folder=folder)
        if profile_name in self.folder_persistence_profiles:
            return profile_name
        return None
