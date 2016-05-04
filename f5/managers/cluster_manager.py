# Copyright 2016 F5 Networks Inc.

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
#

from f5.common import pollster


class BigIPDeviceNotInExpectedState(Exception):
    pass


class ClusterNotSupported(Exception):
    pass


class UnexpectedBigIPState(Exception):
    pass


class ClusterManager(object):
    '''Manage a cluster of BigIPs.

    This is accomplished with REST URI calls only, but some operations are
    only permitted through the CLI (such as adding peers via cm/trust-domain).
    We get around this issue by deploying iApps (sys/application).
    '''

    iapp_actions = {'definition': {'implementation': None, 'presentation': ''}}
    sync_status_entry = 'https://localhost/mgmt/tm/cm/sync-status/0'

    def __init__(self, bigips, cluster_name, partition, cluster_type):
        if len(bigips) > 4:
            raise ClusterNotSupported(
                'The number of devices to cluster is not supported.'
            )
        self.bigips = bigips
        self.bigip_trust_root = self.bigips[0]
        self.peers = self.bigips[1:]
        self.cluster_name = cluster_name
        self.device_iapp_name = 'device_iapp'
        self.cluster_iapp_name = 'cluster_iapp'
        self.partition = partition
        self.cluster_type = cluster_type

    def cluster_bigips(self):
        if len(self._get_bigips_by_activation_state('active')) != \
                len(self.bigips):
            raise BigIPDeviceNotInExpectedState(
                'One or more BigIP devices was not in a active/licensed state.'
            )
        print('Adding trusted peers...')
        self._add_peers()
        print('Creating cluster group...')
        self._create_cluster_group()
        if self.cluster_type == 'sync-failover':
            print('Ensure cluster has settled into active/standby...')
            self._ensure_active_standby()
        elif self.cluster_type == 'sync-only':
            print('Ensure devices are all in sync and active...')
        self.bigip_trust_root.cm.sync(self.cluster_name)
        self._all_devices_in_sync()

    def _add_peers(self):
        peer_cmds = []
        for peer in self.peers:
            peer_cmds.append(self._get_add_peer_command(peer))
        iapp_actions = self.iapp_actions.copy()
        iapp_actions['definition']['implementation'] = '\n'.join(peer_cmds)
        self._deploy_iapp(self.cluster_iapp_name, iapp_actions)

    def _create_cluster_group(self):
        self.bigip_trust_root.cm.device_groups.device_group.create(
            name=self.cluster_name,
            partition=self.partition,
            type=self.cluster_type
        )
        for bigip in self.bigips:
            self._add_device_to_device_group(bigip)

    def _ensure_active_standby(self):
        self._devices_in_standby()

    @pollster.poll_by_method
    def _all_devices_in_sync(self):
        assert len(self._get_bigips_by_failover_status('In Sync')) == \
            len(self.bigips)

    @pollster.poll_by_method
    def _devices_in_standby(self):
        standby_bigips = \
            self._get_bigips_by_activation_state('standby')
        assert len(standby_bigips) == (len(self.bigips)-1)
        return standby_bigips

    def _get_bigips_by_failover_status(self, status):
        bigips = []
        for bigip in self.bigips:
            sync_status = bigip.cm.sync_status
            sync_status.refresh()
            current_status = (sync_status.entries[self.sync_status_entry]
                              ['nestedStats']['entries']['status']
                              ['description'])
            print(current_status)
            if status == current_status:
                bigips.append(bigip)
        return bigips

    def _get_bigips_by_activation_state(self, state):
        bigips = []
        for bigip in self.bigips:
            reg = bigip.shared.licensing.registration.load()
            act = bigip.cm.devices.device.load(
                name=self._get_device_info(bigip).name,
                partition=self.partition
            )
            if reg.licensedVersion != '' and act.failoverState == state:
                bigips.append(bigip)
        return bigips

    def teardown_cluster(self):
        self._remove_iapp(self.cluster_iapp_name)
        if self.cluster_type == 'sync-failover':
            self._devices_in_standby()
        self.bigip_trust_root.cm.sync(self.cluster_name)
        dg = self.bigip_trust_root.cm.device_groups.device_group.load(
            name=self.cluster_name, partition=self.partition
        )
        for bigip in self.bigips:
            bigip_info = self._get_device_info(bigip)
            dgd = dg.devices_s.devices.load(
                name=bigip_info.name, partition=self.partition
            )
            dgd.delete()
        dg.delete()

    def _remove_iapp(self, iapp_name):
        iapp = self.bigip_trust_root.sys.applications
        iapp_service = iapp.services.service.load(
            name=iapp_name, partition=self.partition
        )
        iapp_service.delete()
        iapp_template = iapp.templates.template.load(
            name=iapp_name, partition=self.partition
        )
        iapp_template.delete()

    def _get_device_info(self, bigip):
        coll = bigip.cm.devices.get_collection()
        device = [device for device in coll if device.selfDevice == 'true']
        assert len(device) == 1
        return device[0]

    def _add_device_to_device_group(self, bigip):
        bigip_info = self._get_device_info(bigip)
        poll_for_dg = pollster.poll_by_method(
            bigip.cm.device_groups.device_group.load
        )
        dg = poll_for_dg(
            name=self.cluster_name, partition=self.partition
        )
        dg.devices_s.devices.create(
            name=bigip_info.name, partition=self.partition
        )
        root_dg = self.bigip_trust_root.cm.device_groups.device_group.load(
            name=self.cluster_name, partition=self.partition
        )
        trust_root_poll = pollster.poll_by_method(
            root_dg.devices_s.devices.load
        )
        trust_root_poll(name=bigip_info.name, partition=self.partition)

    def _deploy_iapp(self, iapp_name, actions):
        tmpl = self.bigip_trust_root.sys.applications.templates.template
        serv = self.bigip_trust_root.sys.applications.services.service
        tmpl.create(name=iapp_name, partition=self.partition, actions=actions)
        serv.create(
            name=iapp_name, partition=self.partition, template=iapp_name
        )

    def _get_add_peer_command(self, peer):
        peer_device = self._get_device_info(peer)
        add_peer_cmd = 'tmsh::modify cm trust-domain Root ca-devices add ' \
            '\\{{ {0} \\}} name {1} username admin password admin'.format(
                peer_device.managementIp, peer_device.name
            )
        return add_peer_cmd
