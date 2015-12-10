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

import base64
import json
import time

from f5.bigip import exceptions
from f5.bigip.rest_collection import log
from f5.common import constants as const
from f5.common.logger import Log


# Management - Device
class Device(object):
    def __init__(self, bigip):
        self.bigip = bigip

        self.bigip.icontrol.add_interfaces(['Management.Trust'])
        self.mgmt_trust = self.bigip.icontrol.Management.Trust

        # create empty lock instance ID
        self.lock = None
        self.devicename = None

    @log
    def get_device_name(self):
        """Get device name """
        if not self.devicename:
            request_url = self.bigip.icr_url + '/cm/device'
            request_filter = '/?$select=name,selfDevice'
            request_filter += '&filter partition eq Common'
            request_url += request_filter
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                response_obj = json.loads(response.text)
                if 'items' in response_obj:
                    devices = response_obj['items']
                    for device in devices:
                        if device['selfDevice'] == 'true':
                            self.devicename = device['name']
            else:
                Log.error('device', response.text)
                raise exceptions.DeviceQueryException(response.text)
        return self.devicename

    @log
    def get_all_device_names(self):
        """Get all device name """
        request_url = self.bigip.icr_url + '/cm/device'
        request_filter = '/?$select=name&filter partition eq Common'
        request_url += request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                devices = response_obj['items']
                device_names = []
                for device in devices:
                    device_names.append(device['name'])
                return device_names
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return []

    @log
    def get_lock(self):
        """Get device lock """
        current_lock = self._get_lock()
        new_lock = int(time.time())

        if current_lock:
            if (new_lock - current_lock) > const.CONNECTION_TIMEOUT:
                Log.info('Device', 'Locking device %s with lock %s'
                         % (self.get_device_name(), new_lock))
                self._set_lock(new_lock)
                return True
            else:
                return False
        else:
            Log.info('Device', 'Locking device %s with lock %s'
                     % (self.get_device_name(), new_lock))
            self._set_lock(int(time.time()))
            return True

    @log
    def release_lock(self):
        """Release device lock """
        current_lock = self._get_lock()

        if current_lock == self.lock:
            Log.info('Device', 'Releasing device lock for %s'
                     % self.get_device_name())
            self._set_lock(None)
            return True
        else:
            Log.info('Device', 'Device has foreign lock instance on %s '
                     % self.get_device_name() + ' with lock %s '
                     % current_lock)
            return False

    def _get_lock(self):
        """Get device lock """
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '?$select=selfDevice,comment'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        current_lock = ''
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                devices = response_obj['items']
                for device in devices:
                    if device['selfDevice']:
                        if 'comment' in device:
                            current_lock = device['comment']
        if current_lock.startswith(const.DEVICE_LOCK_PREFIX):
            return int(current_lock.replace(const.DEVICE_LOCK_PREFIX, ''))

    def _set_lock(self, lock):
        """Set device lock """
        dev_name = self.get_device_name()
        if lock:
            self.lock = lock
            lock_comment = const.DEVICE_LOCK_PREFIX + str(lock)
        else:
            lock_comment = ''
        request_url = self.bigip.icr_url + '/cm/device/'
        request_url += '~Common~' + dev_name
        payload = dict()
        payload['comment'] = lock_comment
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        return False

    @log
    def get_mgmt_addr(self):
        """Get device management ip """
        request_url = self.bigip.icr_url + '/cm/device/~Common'
        request_url += '~' + self.get_device_name()
        request_filter = '/?$select=managementIp'
        request_url += request_filter
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            return response_obj['managementIp']
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def get_all_mgmt_addrs(self):
        """Get device management ips """
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '/?$select=managementIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                mgmt_addrs = []
                for device in response_obj['items']:
                    mgmt_addrs.append(device['managementIp'])
            return mgmt_addrs
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def get_mgmt_addr_by_device(self, devicename):
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '/?$select=managementIp,name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for device in response_obj['items']:
                    if device['name'] == devicename:
                        return device['managementIp']
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def get_configsync_addr(self):
        """Get device config sync ip """
        request_url = self.bigip.icr_url + '/cm/device/~Common'
        request_url += '~' + self.get_device_name()
        request_url += '/?$select=configsyncIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            return response_obj['configsyncIp']
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
            return None

    @log
    def set_configsync_addr(self, ip_address=None, folder='/Common'):
        """Set device config sync ip """
        dev_name = self.get_device_name()
        request_url = self.bigip.icr_url + '/cm/device/'
        request_url += '~Common~' + dev_name
        payload = dict()
        if not ip_address:
            payload['configsyncIp'] = None
        else:
            payload['configsyncIp'] = ip_address
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return False

    @log
    def get_primary_mirror_addr(self):
        """Get device primary mirror ip """
        request_url = self.bigip.icr_url + '/cm/device/~Common'
        request_url += '~' + self.get_device_name()
        request_url += '/?$select=mirrorIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            primary = response_obj['mirrorIp']
            if primary == 'any6':
                return None
            else:
                return primary
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def get_secondary_mirror_addr(self):
        """Get device secondary mirror ip """
        request_url = self.bigip.icr_url + '/cm/device/~Common'
        request_url += '~' + self.get_device_name()
        request_url += '/?$select=mirrorSecondaryIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            secondary = response_obj['mirrorSecondaryIp']
            if secondary == 'any6':
                return None
            else:
                return secondary
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def set_primary_mirror_addr(self, ip_address=None, folder='/Common'):
        """Set device primary mirror ip """
        dev_name = self.get_device_name()
        request_url = self.bigip.icr_url + '/cm/device/'
        request_url += '~Common~' + dev_name
        payload = dict()
        if not ip_address:
            payload['mirrorIp'] = '::'
        else:
            payload['mirrorIp'] = ip_address
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceUpdateException(response.text)
        return False

    @log
    def set_secondary_mirror_addr(self, ip_address=None, folder='/Common'):
        """Set device secondary mirror ip """
        dev_name = self.get_device_name()
        request_url = self.bigip.icr_url + '/cm/device/'
        request_url += '~Common~' + dev_name
        payload = dict()
        if not ip_address:
            payload['mirrorSecondaryIp'] = '::'
        else:
            payload['mirrorSecondaryIp'] = ip_address
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceUpdateException(response.text)
        return False

    @log
    def get_failover_addrs(self):
        """Get device failover ips """
        request_url = self.bigip.icr_url + '/cm/device/~Common'
        request_url += '~' + self.get_device_name()
        request_url += '/?$select=unicastAddress'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            return_addresses = []
            if 'unicastAddress' in response_obj:
                uas = response_obj['unicastAddress']
                for ua in uas:
                    return_addresses.append(ua['ip'])
                return return_addresses
            else:
                return []
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return []

    @log
    def set_failover_addrs(self, ip_addrs=None, folder='/Common'):
        """Get device failover ips """
        dev_name = self.get_device_name()
        dev_ip = self.get_mgmt_addr()
        request_url = self.bigip.icr_url + '/cm/device/'
        request_url += '~Common~' + dev_name
        payload = dict()
        unicast_addresses = []
        if len(ip_addrs):
            unicast_addresses.append({'effectiveIp': dev_ip,
                                      'effectivePort': 1026,
                                      'ip': dev_ip,
                                      'port': 1026})
            for ip_address in ip_addrs:
                unicast_addresses.append({'effectiveIp': ip_address,
                                          'effectivePort': 1026,
                                          'ip': ip_address,
                                          'port': 1026})
        payload['unicastAddress'] = unicast_addresses
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceUpdateException(response.text)
        return False

    @log
    def get_failover_state(self):
        """Get device failover state """
        request_url = self.bigip.icr_url + '/cm/device/~Common'
        request_url += '~' + self.get_device_name()
        request_url += '/?$select=failoverState'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            return response_obj['failoverState']
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def get_device_group(self):
        """Get device group """
        request_url = self.bigip.icr_url + '/cm/device-group'
        request_url += '/?$select=name,type'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                dsgs = response_obj['items']
                for dsg in dsgs:
                    if dsg['type'] == 'sync-failover':
                        return dsg['name']
                return None
        elif response.status_code == 404:
            return None
        else:
            Log.error('device-group', response.text)
            raise exceptions.DeviceQueryException(response.text)
        return None

    @log
    def remove_from_device_group(self, name=None, folder='/Common'):
        """Remove device from group """
        device_group = self.get_device_group()
        if device_group:
            return self.bigip.cluster.remove_devices(device_group,
                                                     [self.get_device_name()])

    @log
    def remove_all_peers(self):
        """Remove all peers from group """
        self.bigip.system.set_folder('/Common')
        current_dev_name = self.get_device_name()
        devs_to_remove = []
        for dev in self.get_all_device_names():
            if dev != current_dev_name:
                devs_to_remove.append(dev)
        if devs_to_remove:
            try:
                self.mgmt_trust.remove_device(devs_to_remove)
            except Exception as e:
                Log.error('device', e.message)
                raise exceptions.DeviceUpdateException(e.message)
        try:
            self.remove_metadata(
                None, {'root_device_name': None,
                       'root_device_mgmt_address': None})
        except exceptions.DeviceUpdateException:
            pass

    @log
    def reset_trust(self, new_name):
        """Remove trust """
        self.bigip.system.set_folder('/Common')
        self.remove_all_peers()
        try:
            self.mgmt_trust.reset_all(new_name, False, '', '')
        except Exception as e:
            Log.error('device', e.message)
            raise exceptions.DeviceUpdateException(e.message)
        try:
            self.remove_metadata(
                None, {'root_device_name': None,
                       'root_device_mgmt_address': None})
        except exceptions.DeviceUpdateException:
            pass

        self.devicename = None
        self.get_device_name()

    @log
    def set_metadata(self, name=None, device_dict=None):
        """Set device metadata """
        if not name:
            name = self.get_device_name()
        if isinstance(device_dict, dict):
            str_comment = json.dumps(device_dict)
        else:
            str_comment = device_dict

        request_url = self.bigip.icr_url + '/cm/device/~Common~'
        request_url += name
        payload = dict()
        payload['description'] = base64.encodestring(str_comment)
        response = self.bigip.icr_session.patch(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device', response.text)
            raise exceptions.DeviceUpdateException(response.text)
        return False

    @log
    def get_metadata(self, name=None):
        """Get device metadata """
        if not name:
            name = self.get_device_name()
        request_url = self.bigip.icr_url + '/cm/device/~Common~'
        request_url += name + '?$select=name,description'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        str_comment = None
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if response_obj['name'] == name:
                if 'description' in response_obj:
                    str_comment = response_obj['description']
        elif response.status_code != 404:
            Log.error('device', response.text)
            raise exceptions.DeviceQueryException(response.text)
        if str_comment:
            try:
                return json.loads(base64.decodestring(str_comment))
            except Exception:
                try:
                    return base64.decodestring(str_comment)
                except Exception:
                    return str_comment
        return None

    @log
    def remove_metadata(self, name=None, remove_dict=None):
        """Remove device metadata """
        if not name:
            name = self.get_device_name()
        if isinstance(remove_dict, dict):
            existing_metadata = self.get_metadata(name)
            if isinstance(existing_metadata, dict):
                for key in remove_dict:
                    if key in existing_metadata:
                        del(existing_metadata[key])
                return self.set_metadata(name, existing_metadata)
            else:
                return self.set_metadata(name, '')
        else:
            return self.set_metadata(name, '')

    @log
    def update_metadata(self, name=None, cluster_dict=None):
        """Update device metadata """
        if not name:
            name = self.get_device_name()
        if isinstance(cluster_dict, dict):
            existing_metadata = self.get_metadata(name)
            if isinstance(existing_metadata, dict):
                for key in cluster_dict:
                    existing_metadata[key] = cluster_dict[key]
                return self.set_metadata(name, existing_metadata)
            else:
                return self.set_metadata(name, cluster_dict)
        else:
            return self.set_metadata(name, cluster_dict)
