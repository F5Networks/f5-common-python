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

    def __init__(self, bigips, cluster_name, partition):
        if len(bigips) != 2:
            raise ClusterNotSupported(
                'The number of devices to cluster is not supported. '
                'Only Active/Standby is supported currently.'
            )
        assert len(bigips) == 2
        self.bigips = bigips
        self.bigip_trust_root = self.bigips[0]
        self.peers = self.bigips[1:]
        self.cluster_name = cluster_name
        self.device_iapp_name = 'device_iapp'
        self.cluster_iapp_name = 'cluster_iapp'
        self.partition = partition

    def cluster_bigips(self):
        assert len(self._get_bigips_by_state('active')) == len(self.bigips)
        for peer in self.peers:
            self._add_peer(peer)
        self._create_cluster()
        self._ensure_active_standby()

    def _ensure_active_standby(self):
        # If active/standby cluster, one bigip should go into standby
        standby_bigip = self._one_device_in_standby()
        standby_bigip.cm.sync(self.cluster_name)
        self._all_devices_in_sync()

    @pollster.poll_by_method
    def _all_devices_in_sync(self):
        assert len(self._get_bigips_by_failover_status('In Sync')) == \
            len(self.bigips)

    @pollster.poll_by_method
    def _one_device_in_standby(self):
        bigips = self._get_bigips_by_state('standby')
        assert len(bigips) == 1
        return bigips[0]

    def _create_cluster(self):
        self.bigip_trust_root.cm.device_groups.device_group.create(
            name=self.cluster_name,
            partition=self.partition,
            type='sync-failover'
        )
        self._add_devices_to_device_group()

    def _get_bigips_by_failover_status(self, status):
        bigips = []
        for bigip in self.bigips:
            sync_status = bigip.cm.sync_status
            sync_status.refresh()
            current_status = (sync_status.entries[self.sync_status_entry]
                              ['nestedStats']['entries']['status']
                              ['description'])
            if status == current_status:
                bigips.append(bigip)
        return bigips

    def _get_bigips_by_state(self, state):
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
        standby_bigip = self._one_device_in_standby()
        standby_bigip.cm.sync(self.cluster_name)
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

    def _add_devices_to_device_group(self):
        for bigip in self.bigips:
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

    def _deploy_iapp(self, iapp_name, actions):
        iapp_tmpl = self.bigip_trust_root.sys.applications.templates.template
        iapp_service = self.bigip_trust_root.sys.applications.services.service
        iapp_tmpl.create(
            name=iapp_name, partition=self.partition, actions=actions
        )
        iapp_service.create(
            name=iapp_name, partition=self.partition, template=iapp_name
        )

    def _add_peer(self, peer):
        peer_device = self._get_device_info(peer)
        impl = 'tmsh::modify cm trust-domain Root ca-devices add \\{{ {0} \\}} ' \
            'name {1} username admin password admin'.format(
                peer_device.managementIp, peer_device.name)
        iapp_actions_dict = self.iapp_actions.copy()
        iapp_actions_dict['definition']['implementation'] = impl
        self._deploy_iapp(self.cluster_iapp_name, iapp_actions_dict)
