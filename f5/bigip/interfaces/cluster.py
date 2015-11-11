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

from f5.common import constants as const
from f5.common.logger import Log
from f5.bigip import exceptions
from f5.bigip.interfaces import log

import time
import os
import json
import base64


# Management - Cluster
class Cluster(object):
    def __init__(self, bigip):
        self.bigip = bigip

        self.bigip.icontrol.add_interfaces(['Management.Trust'])
        self.mgmt_trust = self.bigip.icontrol.Management.Trust

    @log
    def get_sync_status(self):
        """ Get the sync status description for the bigip """
        request_url = self.bigip.icr_url + '/cm/sync-status?$select=status'
        response = self.bigip.icr_session.get(request_url,
                                              timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            entries = response_obj['entries']
            status = entries['https://localhost/mgmt/tm/cm/sync-status/0']
            desc = status['nestedStats']['entries']['status']['description']
            return desc
        else:
            Log.error('sync-status', response.text)
            raise exceptions.ClusterQueryException(response.text)
        return None

    @log
    def get_sync_color(self):
        """ Get the sync color for the bigip """
        request_url = self.bigip.icr_url + '/cm/sync-status?$select=color'
        response = self.bigip.icr_session.get(request_url,
                                              timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            entries = response_obj['entries']
            status = entries['https://localhost/mgmt/tm/cm/sync-status/0']
            desc = status['nestedStats']['entries']['color']['description']
            return desc
        else:
            Log.error('sync-info', response.text)
            raise exceptions.ClusterQueryException(response.text)
        return None

    @log
    def save_config(self):
        """ Save the bigip configuration """
        request_url = self.bigip.icr_url + '/sys/config'
        payload = dict()
        payload['command'] = 'save'
        response = self.bigip.icr_session.post(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('config', response.text)
            raise exceptions.BigIPClusterConfigSaveFailure(response.text)
        return False

    @log
    def get_local_device_name(self):
        """ Get local device name """
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '?$select=selfDevice,name,hostname,managementIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for device in response_obj['items']:
                    if device['selfDevice'].lower() == 'true':
                        return device['name']
        else:
            Log.error('device', response.text)
            raise exceptions.ClusterQueryException(response.text)
        return None

    @log
    def get_local_device_addr(self):
        """ Get local device management ip """
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '?$select=selfDevice,name,hostname,managementIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for device in response_obj['items']:
                    if device['selfDevice'].lower() == 'true':
                        return device['managementIp']
        else:
            Log.error('device', response.text)
            raise exceptions.ClusterQueryException(response.text)
        return None

    @log
    def sync_local_device_to_group(self, device_group_name):
        """ Sync local device to group """
        request_url = self.bigip.icr_url + '/cm'
        payload = dict()
        payload['command'] = 'run'
        payload['options'] = [{'config-sync': 'to-group ' + device_group_name}]
        response = self.bigip.icr_session.post(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('sync', response.text)
            raise exceptions.BigIPClusterSyncFailure(response.text)
        return False

    # force_now=True is typically used for initial sync.
    # In order to avoid sync problems, you should wait until devices
    # in the group are connected.
    @log
    def sync(self, name, force_now=False):
        """ Ensure local device in sync with group """
        sync_start_time = time.time()
        dev_name = self.get_local_device_name()
        sleep_delay = const.SYNC_DELAY

        attempts = 0
        if force_now:
            self.sync_local_device_to_group(name)
            time.sleep(sleep_delay)
            attempts += 1

        while attempts < const.MAX_SYNC_ATTEMPTS:
            state = self.get_sync_status()
            if state in ['Standalone', 'In Sync']:
                break

            elif state == 'Awaiting Initial Sync':
                attempts += 1
                Log.info(
                    'Cluster',
                    "Device %s - Synchronizing initial config to group %s"
                    % (dev_name, name))
                self.sync_local_device_to_group(name)
                time.sleep(sleep_delay)

            elif state in ['Disconnected',
                           'Not All Devices Synced',
                           'Changes Pending']:
                attempts += 1

                last_log_time = 0
                now = time.time()
                wait_start_time = now
                # Keep checking the sync state in a quick loop.
                # We want to detect In Sync as quickly as possible.
                while now - wait_start_time < sleep_delay:
                    # Only log once per second
                    if now - last_log_time >= 1:
                        Log.info(
                            'Cluster',
                            'Device %s, Group %s not synced. '
                            % (dev_name, name) +
                            'Waiting. State is: %s'
                            % state)
                        last_log_time = now
                    state = self.get_sync_status()
                    if state in ['Standalone', 'In Sync']:
                        break
                    time.sleep(.5)
                    now = time.time()
                else:
                    # if we didn't break out due to the group being in sync
                    # then attempt to force a sync.
                    self.sync_local_device_to_group(name)
                    sleep_delay += const.SYNC_DELAY
                    # no need to sleep here because we already spent the sleep
                    # interval checking status.
                    continue

                # Only a break from the inner while loop due to Standalone or
                # In Sync will reach here.
                # Normal exit of the while loop reach the else statement
                # above which continues the outer loop
                break

            elif state == 'Sync Failure':
                Log.info('Cluster',
                         "Device %s - Synchronization failed for %s"
                         % (dev_name, name))
                Log.debug('Cluster', 'SYNC SECONDS (Sync Failure): ' +
                          str(time.time() - sync_start_time))
                raise exceptions.BigIPClusterSyncFailure(
                    'Device service group %s' % name +
                    ' failed after ' +
                    '%s attempts.' % const.MAX_SYNC_ATTEMPTS +
                    ' Correct sync problem manually' +
                    ' according to sol13946 on ' +
                    ' support.f5.com.')
            else:
                attempts += 1
                Log.info('Cluster',
                         "Device %s " % dev_name +
                         "Synchronizing config attempt %s to group %s:"
                         % (attempts, name) + " current state: %s" % state)
                self.sync_local_device_to_group(name)
                time.sleep(sleep_delay)
                sleep_delay += const.SYNC_DELAY
        else:
            if state == 'Disconnected':
                Log.debug('Cluster',
                          'SYNC SECONDS(Disconnected): ' +
                          str(time.time() - sync_start_time))
                raise exceptions.BigIPClusterSyncFailure(
                    'Device service group %s' % name +
                    ' could not reach a sync state' +
                    ' because they can not communicate' +
                    ' over the sync network. Please' +
                    ' check connectivity.')
            else:
                Log.debug('Cluster', 'SYNC SECONDS(Timeout): ' +
                          str(time.time() - sync_start_time))
                raise exceptions.BigIPClusterSyncFailure(
                    'Device service group %s' % name +
                    ' could not reach a sync state after ' +
                    '%s attempts.' % const.MAX_SYNC_ATTEMPTS +
                    ' It is in %s state currently.' % state +
                    ' Correct sync problem manually' +
                    ' according to sol13946 on ' +
                    ' support.f5.com.')

        Log.debug('Cluster', 'SYNC SECONDS(Success): ' +
                  str(time.time() - sync_start_time))

    @log
    def sync_failover_dev_group_exists(self, name):
        """ Does the sync failover device group exist? """
        request_url = self.bigip.icr_url + '/cm/device-group/'
        request_url += '~Common~' + name
        request_url += '?$select=type'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'type' in response_obj:
                if response_obj['type'] == 'sync-failover':
                    return True
                else:
                    return False
        elif response.status_code == 404:
            return False
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterQueryException(response.text)
        return False

    @log
    def wait_for_insync_status(self):
        """ Wait until sync status is 'in sync' and color is 'green'. """
        sync_status_attempts = 0
        max_status_attempts = 60
        while sync_status_attempts < max_status_attempts:
            sync_color = self.get_sync_color().lower()
            sync_status = self.get_sync_status().lower()
            if sync_color != u'green' and sync_status != u'in sync':
                sync_status_attempts += 1
                time.sleep(2)
                continue
            return
        raise exceptions.BigIPClusterPeerAddFailure(
            'Group failed to sync in 60 seconds while adding peer.'
        )

    @log
    def add_peer(self, name, mgmt_ip_address, username, password):
        """ Add a peer to the local trust group """
        if not self.peer_exists(name):
            if self.bigip.device.get_lock():
                local_device = self.get_local_device_name()
                local_mgmt_address = self.get_local_device_addr()
                root_mgmt_dict = {'root_device_name': local_device,
                                  'root_device_mgmt_address':
                                  local_mgmt_address}
                local_md = self.bigip.device.get_metadata()
                if local_md and 'root_device_name' in local_md.keys():
                    md_device_name = os.path.basename(
                        local_md['root_device_name'])
                    if md_device_name:
                        if not md_device_name == local_device:
                            raise exceptions.BigIPClusterPeerAddFailure(
                                'the device used to peer %s ' % name +
                                ' was already itself peered from root' +
                                ' device: %s'
                                % local_md['root_device_name'])
                self.bigip.device.update_metadata(None, root_mgmt_dict)
                Log.info('Cluster', 'Device %s - adding peer %s'
                                    % (local_device, name))

                self.mgmt_trust.add_authority_device(mgmt_ip_address,
                                                     username,
                                                     password,
                                                     name,
                                                     '', '',
                                                     '', '')
                attempts = 0
                while attempts < const.PEER_ADD_ATTEMPTS_MAX:
                    if self.get_sync_status() == "OFFLINE":
                        self.mgmt_trust.remove_device([name])
                        self.mgmt_trust.add_authority_device(mgmt_ip_address,
                                                             username,
                                                             password,
                                                             name,
                                                             '', '',
                                                             '', '')
                    else:
                        self.wait_for_insync_status()
                        self.bigip.device.release_lock()
                        return
                    time.sleep(const.PEER_ADD_ATTEMPT_DELAY)
                    attempts += 1
                else:
                    raise exceptions.BigIPClusterPeerAddFailure(
                        'Could not add peer device %s' % name +
                        ' as a trust for device %s'
                        % os.path.basename(self.mgmt_dev.get_local_device()) +
                        ' after % attempts' % const.PEER_ADD_ATTEMPTS_MAX)
            else:
                raise exceptions.BigIPDeviceLockAcquireFailed(
                    'Unable to obtain device lock for device %s'
                    % os.path.basename(self.mgmt_dev.get_local_device())
                    )

    @log
    def get_peer_addr(self, name):
        """ Get a peer management ip """
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '?$select=selfDevice,name,hostname,managementIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for device in response_obj['items']:
                    if device['name'] == name:
                        return device['managementIp']
        else:
            Log.error('device', response.text)
            raise exceptions.ClusterQueryException(response.text)
        return None

    @log
    def peer_exists(self, name):
        """ Does a peer exist by name? """
        request_url = self.bigip.icr_url + '/cm/device'
        request_url += '?$select=selfDevice,name,hostname,managementIp'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for device in response_obj['items']:
                    if device['name'] == name:
                        return True
        elif response.status_code == 404:
            return False
        else:
            Log.error('device', response.text)
        return False

    @log
    def cluster_exists(self, name):
        """ Does a cluster exist by name? """
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        request_filter = '/?$select=name,type'
        request_url += request_filter
        response = self.bigip.icr_session.get(
            request_url, data=None, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if response_obj['type'] == 'sync-failover':
                return True
            else:
                return False
        elif response.status_code == 404:
            return False
        else:
            Log.error('device-group', response.text)
            return False

    @log
    def create(self, name, autosync=True):
        """ Create a device group """
        request_url = self.bigip.icr_url + '/cm/device-group'
        payload = dict()
        payload['name'] = name
        if autosync:
            payload['autoSync'] = 'enabled'
        payload['networkFailover'] = 'enabled'
        payload['type'] = 'sync-failover'
        response = self.bigip.icr_session.post(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 409:
            return True
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterCreationException(response.text)

    @log
    def delete(self, name):
        """ Delete a device group """
        if self.cluster_exists(name):
            self.remove_all_devices(name)
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        response = self.bigip.icr_session.delete(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterDeleteException(response.text)

    @log
    def enable_auto_sync(self, name):
        """ Enable autosync on a device group """
        payload = dict()
        payload['autoSync'] = 'enabled'
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterUpdateException(response.text)

    @log
    def disable_auto_sync(self, name):
        """ Disable autosync on a device group """
        payload = dict()
        payload['autoSync'] = 'disabled'
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterUpdateException(response.text)

    @log
    def devices(self, name):
        """ Get device group devices """
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        request_url += "/devices?$select=name"
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        return_devices = []
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if 'items' in response_obj:
                for device in response_obj['items']:
                    return_devices.append(device['name'])
            return return_devices
        if response.status_code == 404:
            return []
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterQueryException(response.text)

    @log
    def add_devices(self, name, device_names):
        """ Add devices to device group """
        existing_devices = self.devices(name)
        if not isinstance(device_names, list):
            device_names = [device_names]
        need_to_update = False
        for device in device_names:
            if device not in existing_devices:
                existing_devices.append(device)
                need_to_update = True
        if need_to_update:
            request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
            request_url += name
            payload = dict()
            devices_list = list()
            for device in existing_devices:
                devices_list.append({'name': device})
            payload['devices'] = devices_list
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 409:
                return True
            else:
                Log.error('device-group', response.text)
                exceptions.ClusterUpdateException(response.text)

    @log
    def remove_devices(self, name, device_names):
        """ Remove devices from device group """
        existing_devices = self.devices(name)
        if not isinstance(device_names, list):
            device_names = [device_names]
        need_to_update = False
        for device in device_names:
            if device in existing_devices:
                existing_devices.remove(device)
                need_to_update = True
        if need_to_update:
            request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
            request_url += name
            payload = dict()
            devices_list = list()
            for device in existing_devices:
                devices_list.append({'name': device})
            payload['devices'] = devices_list
            response = self.bigip.icr_session.put(
                request_url, data=json.dumps(payload),
                timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('device-group', response.text)
                raise exceptions.ClusterUpdateException(response.text)

    @log
    def remove_all_devices(self, name):
        """ Remove all devices from device group """
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        payload = dict()
        payload['devices'] = list()
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 404:
            return True
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterQueryException(response.text)

    @log
    def remove_device(self, name, device_name):
        """ Remove device from device group """
        self.remove_devices(name, [device_name])

    @log
    def set_metadata(self, name, cluster_dict):
        """ Set metadata on device group """
        if isinstance(cluster_dict, dict):
            str_comment = json.dumps(cluster_dict)
        else:
            str_comment = cluster_dict

        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name
        payload = dict()
        payload['description'] = base64.encodestring(str_comment)
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        else:
            Log.error('device-group', response.text)
            raise exceptions.ClusterUpdateException(response.text)

    @log
    def get_metadata(self, name):
        """ Get metadata on device group """
        request_url = self.bigip.icr_url + '/cm/device-group/~Common~'
        request_url += name + '?$select=name,description'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        str_comment = None
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            if response_obj['name'] == name:
                if 'description' in response_obj:
                    str_comment = response_obj['description']
        if str_comment:
            try:
                return json.loads(base64.decodestring(str_comment))
            except:
                try:
                    return base64.decodestring(str_comment)
                except Exception as e:
                    Log.error('device-group', e.message)
                    return str_comment
        return None

    @log
    def remove_metadata(self, name, remove_dict=None):
        """ Remove metadata on device group """
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
    def update_metadata(self, name, cluster_dict):
        """ Update metadata on device group """
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

    @log
    def get_traffic_groups(self):
        """ Get traffic groups """
        request_url = self.bigip.icr_url + '/cm/traffic-group'
        request_url += '?$select=name'
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            response_obj = json.loads(response.text)
            traffic_groups = []
            if 'items' in response_obj:
                for tg in response_obj['items']:
                    traffic_groups.append(tg['name'])
            return traffic_groups
        return None

    @log
    def traffic_group_exists(self, name):
        """ Does traffic group exist? """
        if name:
            request_url = self.bigip.icr_url + '/cm/traffic-group/'
            request_url += '~Common~' + name
            request_url += '?$select=name'
            response = self.bigip.icr_session.get(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return False
            else:
                Log.error('traffic-group', response.text)
                raise exceptions.ClusterQueryException(response.text)

    @log
    def create_traffic_group(self,
                             name=None, autofailback=False,
                             failbacktimer=60, loadfactor=1,
                             floating=True, ha_order=None):
        """ Create traffic group """
        request_url = self.bigip.icr_url + '/cm/traffic-group'
        payload = dict()
        payload['name'] = name
        payload['autoFailbackEnabled'] = autofailback
        payload['autoFailbackTime'] = failbacktimer
        payload['haLoadFactor'] = loadfactor
        payload['isFloating'] = floating
        if ha_order:
            ha_order_list = []
            devices = self.bigip.device.get_all_device_names()
            for device in ha_order:
                dev_name = os.path.basename(device)
                if dev_name in devices:
                    ha_order_list.append('/Common/' + dev_name)
            payload['haOrder'] = ha_order_list
        response = self.bigip.icr_session.post(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 409:
            return True
        else:
            Log.error('traffic-group', response.text)
            raise exceptions.ClusterCreationException(response.text)

    @log
    def update_traffic_group(self,
                             name=None, autofailback=False,
                             failbacktimer=60, loadfactor=1,
                             floating=True, ha_order=None):
        """ Update traffic group """
        request_url = self.bigip.icr_url + '/cm/traffic-group/'
        request_url += '~Common~' + name
        response = self.bigip.icr_session.get(
            request_url, timeout=const.CONNECTION_TIMEOUT)
        if response.status_code >= 400:
            Log.error('traffic-group', response.text)
            raise exceptions.ClusterUpdateException(response.text)
        payload = json.loads(response.text)

        payload['autoFailbackEnabled'] = autofailback
        payload['autoFailbackTime'] = failbacktimer
        payload['haLoadFactor'] = loadfactor
        payload['isFloating'] = floating
        if ha_order:
            ha_order_list = []
            devices = self.bigip.device.get_all_device_names()
            for device in ha_order:
                dev_name = os.path.basename(device)
                if dev_name in devices:
                    ha_order_list.append('/Common/' + dev_name)
            payload['haOrder'] = ha_order_list
        response = self.bigip.icr_session.put(
            request_url, data=json.dumps(payload),
            timeout=const.CONNECTION_TIMEOUT)
        if response.status_code < 400:
            return True
        elif response.status_code == 409:
            return True
        else:
            Log.error('traffic-group', response.text)
            raise exceptions.ClusterUpdateException(response.text)

    @log
    def delete_traffic_group(self, name):
        """ Delete traffic group """
        if name:
            request_url = self.bigip.icr_url + '/cm/traffic-group/'
            request_url += '~Common~' + name
            response = self.bigip.icr_session.delete(
                request_url, timeout=const.CONNECTION_TIMEOUT)
            if response.status_code < 400:
                return True
            elif response.status_code == 404:
                return True
            else:
                Log.error('traffic-group', response.text)
                raise exceptions.ClusterDeleteException(response.text)
