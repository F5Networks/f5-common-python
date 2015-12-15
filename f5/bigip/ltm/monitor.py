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

import f5.bigip.exceptions
from f5.bigip.rest_collection import icontrol_rest_folder
from f5.bigip.rest_collection import log
from f5.common import constants as const
from f5.common.logger import Log

import json


class Monitor(object):
    """Class for configuring monitors on bigip """
    def __init__(self, bigip):
        self.bigip = bigip

        self.monitor_type = {
            'ping': {'name': 'gateway-icmp',
                     'url': '/ltm/monitor/gateway-icmp'},
            'icmp': {'name': 'gateway-icmp',
                     'url': '/ltm/monitor/gateway-icmp'},
            'tcp': {'name': 'tcp',
                    'url': '/ltm/monitor/tcp'},
            'http': {'name': 'http',
                     'url': '/ltm/monitor/http'},
            'https': {'name': 'https',
                      'url': '/ltm/monitor/https'},
            'udp': {'name': 'udp', 'url': '/ltm/monitor/udp'},
            'inband': {'name': 'inband',
                       'url': '/ltm/monitor/inband'}}

    @icontrol_rest_folder
    @log
    def create(self, name=None, mon_type=None, interval=5,
               timeout=16, send_text=None, recv_text=None,
               folder='Common'):
        """Create monitor """
        folder = str(folder).replace('/', '')
        mon_type = self._get_monitor_rest_type(mon_type)
        payload = dict()
        payload['name'] = name
        payload['partition'] = folder
        parent = mon_type.replace('-', '_')
        payload['defaultsFrom'] = '/Common/' + parent
        payload['timeout'] = timeout
        payload['interval'] = interval
        if send_text:
            payload['send'] = send_text
        if recv_text:
            payload['recv'] = recv_text
        request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type
        response = self.bigip.icr_session.post(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 409:
            return True
        else:
            Log.error('monitor', response.text)
            raise exceptions.MonitorCreationException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete(self, name=None, mon_type=None, folder='Common'):
        """Delete monitor """
        if name and mon_type:
            folder = str(folder).replace('/', '')
            mon_type = self._get_monitor_rest_type(mon_type)
            request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('monitor', response.text)
                raise exceptions.MonitorDeleteException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def delete_all(self, folder='Common'):
        """Create all monitors """
        request_url = self.bigip.icr_url + '/ltm/monitor'
        folder = str(folder).replace('/', '')
        request_filter = 'partition eq ' + folder
        request_url += '?$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            monitor_types = []
            if 'items' in return_obj:
                for monitor_type in return_obj['items']:
                    ref = monitor_type['reference']['link']
                    monitor_types.append(
                        self.bigip.icr_link(ref).split('?')[0])
            for monitor in monitor_types:
                mon_req = monitor
                mon_req += '?$select=name,selfLink'
                if folder:
                    mon_req += '&$filter=' + request_filter
                mon_resp = self.bigip.icr_session.get(
                    mon_req, timeout=const.CONNECTION_TIMEOUT)
                if mon_resp.status_code < 400:
                    mon_resp_obj = json.loads(mon_resp.text)
                    if 'items' in mon_resp_obj:
                        for mon_def in mon_resp_obj['items']:
                            if mon_def['name'].startswith(self.OBJ_PREFIX):
                                response = self.bigip.icr_session.delete(
                                    self.bigip.icr_link(mon_def['selfLink']),
                                    timeout=const.CONNECTION_TIMEOUT)
                                if response.status_code > 400 and \
                                   response.status_code != 404:
                                    Log.error('monitor', response.text)
                                    raise exceptions.MonitorDeleteException(
                                        response.text)
            return True
        elif response.status_code != 404:
            Log.error('monitor', response.text)
            raise exceptions.MonitorQueryException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_type(self, name=None, folder='Common'):
        """Get monitor type """
        folder = str(folder).replace('/', '')
        request_url = self.bigip.icr_url + '/ltm/monitor'
        request_filter = 'partition eq ' + folder
        request_url += '?$filter=' + request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return_obj = json.loads(response.text)
            monitor_types = []
            if 'items' in return_obj:
                for monitor_type in return_obj['items']:
                    ref = monitor_type['reference']['link']
                    monitor_types.append(ref.replace(
                        'https://localhost/mgmt/tm', '').split('?')[0])
            for monitor in monitor_types:
                mon_req = self.bigip.icr_url + monitor
                mon_req += '?$select=name,defaultsFrom'
                if folder:
                    mon_req += '&$filter=' + request_filter
                mon_resp = self.bigip.icr_session.get(
                    mon_req, timeout=const.CONNECTION_TIMEOUT)
                if mon_resp.status_code < 400:
                    mon_resp_obj = json.loads(mon_resp.text)
                    if 'items' not in mon_resp_obj:
                        continue
                    for mon_def in mon_resp_obj['items']:
                        if mon_def['name'] != name:
                            continue
                        def_from = mon_def['defaultsFrom']
                        mon_type = def_from.replace('/Common/', '')
                        return self._get_monitor_type_from_parent(mon_type)
                else:
                    Log.error('monitor', mon_resp.text)
                    raise exceptions.MonitorQueryException(mon_resp.text)
        else:
            Log.error('monitor', response.text)
            raise exceptions.MonitorQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def get_interval(self, name=None, mon_type=None, folder='Common'):
        """Get monitor interval """
        folder = str(folder).replace('/', '')
        if name and mon_type:
            mon_type = self._get_monitor_rest_type(mon_type)
            request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=interval'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'interval' in return_obj:
                    return return_obj['interval']
            else:
                Log.error('monitor', response.text)
                raise exceptions.MonitorQueryException(response.text)
        return 0

    @icontrol_rest_folder
    @log
    def set_interval(self, name=None,
                     mon_type=None, interval=5, folder='Common'):
        """Set monitor interval """
        folder = str(folder).replace('/', '')
        payload = dict()
        payload['interval'] = interval

        mon_type = self._get_monitor_rest_type(mon_type)
        request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('monitor', response.text)
            raise exceptions.MonitorUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_timeout(self, name=None, mon_type=None, folder='Common'):
        """Get monitor timeout """
        folder = str(folder).replace('/', '')
        if name and mon_type:
            mon_type = self._get_monitor_rest_type(mon_type)
            request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=timeout'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'timeout' in return_obj:
                    return return_obj['timeout']
            else:
                Log.error('monitor', response.text)
                raise exceptions.MonitorQueryException(response.text)
        return 0

    @icontrol_rest_folder
    @log
    def set_timeout(self, name=None, mon_type=None,
                    timeout=16, folder='Common'):
        """Set monitor timeout """
        folder = str(folder).replace('/', '')
        payload = dict()
        payload['timeout'] = timeout

        mon_type = self._get_monitor_rest_type(mon_type)
        request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('monitor', response.text)
            raise exceptions.MonitorUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_send_string(self, name=None, mon_type=None, folder='Common'):
        """Get monitor send string """
        folder = str(folder).replace('/', '')
        if name and mon_type:
            mon_type = self._get_monitor_rest_type(mon_type)
            request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=send'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'send' in return_obj:
                    return return_obj['send']
            else:
                Log.error('monitor', response.text)
                raise exceptions.MonitorQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_send_string(self, name=None, mon_type=None,
                        send_text=None, folder='Common'):
        """Set monitor send string """
        folder = str(folder).replace('/', '')
        payload = dict()
        if send_text:
            payload['send'] = send_text
        else:
            payload['send'] = ''

        mon_type = self._get_monitor_rest_type(mon_type)
        request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('monitor', response.text)
            raise exceptions.MonitorUpdateException(response.text)
        return False

    @icontrol_rest_folder
    @log
    def get_recv_string(self, name=None, mon_type=None, folder='Common'):
        """Get monitor receive string """
        folder = str(folder).replace('/', '')
        if name and mon_type:
            mon_type = self._get_monitor_rest_type(mon_type)
            request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
            request_url += '~' + folder + '~' + name
            request_url += '/?$select=recv'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return_obj = json.loads(response.text)
                if 'recv' in return_obj:
                    return return_obj['recv']
            else:
                Log.error('monitor', response.text)
                raise exceptions.MonitorQueryException(response.text)
        return None

    @icontrol_rest_folder
    @log
    def set_recv_string(self, name=None, mon_type=None,
                        recv_text=None, folder='Common'):
        """Set monitor receive string """
        folder = str(folder).replace('/', '')
        payload = dict()
        if recv_text:
            payload['recv'] = recv_text
        else:
            payload['recv'] = ''

        mon_type = self._get_monitor_rest_type(mon_type)
        request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
        request_url += '~' + folder + '~' + name
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('monitor', response.text)
            raise exceptions.MonitorQueryException(response.text)
        return False

    def _get_monitor_rest_type(self, type_str):
        """Get monitor reset type """
        type_str = type_str.lower()
        if type_str in self.monitor_type:
            return self.monitor_type[type_str]['name']
        else:
            raise exceptions.UnknownMonitorType(
                'Unknown monitor %s' % type_str)

    def _get_monitor_type_from_parent(self, parent):
        """Get monitor type from parent """
        parent = parent.upper()
        if parent == 'GATEWAY_ICMP':
            return 'PING'
        else:
            return parent

    @icontrol_rest_folder
    @log
    def exists(self, name=None, mon_type=None, folder='Common'):
        """Does monitor exist ? """
        folder = str(folder).replace('/', '')
        if name and mon_type:
            mon_type = self._get_monitor_rest_type(mon_type)
            request_url = self.bigip.icr_url + '/ltm/monitor/' + mon_type + '/'
            request_url += '~' + folder + '~' + name
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            else:
                return False
        else:
            return False

    @icontrol_rest_folder
    @log
    def get_monitors(self, folder='Common'):
        """Get monitors """
        folder = str(folder).replace('/', '')
        request_filter = 'partition eq ' + folder
        return_monitors = []
        urls = {}
        for mon in self.monitor_type:
            if not self.monitor_type[mon]['url'] in urls:
                mon_req = self.bigip.icr_url + self.monitor_type[mon]['url']
                mon_req += '?$select=name,partition'
                if folder:
                    mon_req += '&$filter=' + request_filter
                mon_resp = self.bigip.icr_session.get(
                    mon_req, timeout=const.CONNECTION_TIMEOUT)
                urls[self.monitor_type[mon]['url']] = mon_resp.status_code
                if mon_resp.status_code < 400:
                    mon_resp_obj = json.loads(mon_resp.text)
                    if 'items' in mon_resp_obj:
                        for mon_def in mon_resp_obj['items']:
                            return_monitors.append(mon_def['name'])
        return return_monitors
