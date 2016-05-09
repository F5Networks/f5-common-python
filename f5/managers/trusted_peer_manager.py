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

from f5.bigip.mixins import DeviceMixin


class TrustedPeerManager(DeviceMixin):
    '''Manages the trusted peers of a BigIP device.'''

    iapp_actions = {'definition': {'implementation': None, 'presentation': ''}}

    def __init__(self, trust_name, partition):
        self.trust_name = trust_name
        self.partition = partition
        self.peer_iapp_prefix = 'cluster_iapp'

    def add_trusted_peers(self, root_bigip, peers):
        for peer in peers:
            self._modify_trusted_peer(peer, self._get_add_peer_cmd, root_bigip)

    def remove_trusted_peers(self, bigip, peer_to_remove=None):
        tds = bigip.cm.trust_domains.trust_domain.load(name=self.trust_name)
        bigip_info = self.get_device_info(bigip)
        peer_list = [dv for dv in tds.caDevices if bigip_info.name not in dv]
        if peer_to_remove:
            peer_name = self.get_device_info(peer_to_remove)
            peer_list = [peer for peer in peer_list if peer_name.name in peer]
        for peer in peer_list:
            peer_hostname = peer.replace('/%s/' % self.partition, '')
            self._modify_trusted_peer(
                peer_hostname, self._get_delete_peer_cmd, bigip
            )

    def _modify_trusted_peer(
            self, peer, mod_peer_func, deploy_bigip
    ):
        '''Modify a trusted peer device by deploying an iapp.


        :param peer: bigip object -- peer to modify
        :param mod_peer_func: function -- function to call to modify peer
        '''

        iapp_name = '%s_peer' % (self.peer_iapp_prefix)
        mod_peer_cmd = mod_peer_func(peer)
        iapp_actions = self.iapp_actions.copy()
        iapp_actions['definition']['implementation'] = mod_peer_cmd
        self._deploy_iapp(iapp_name, iapp_actions, deploy_bigip)
        self._delete_iapp(iapp_name, deploy_bigip)

    def _delete_iapp(self, iapp_name, deploy_bigip):
        '''Delete an iapp service and template on the root device.

        :param iapp_name: str -- name of iapp
        '''

        iapp = deploy_bigip.sys.applications
        iapp_service = iapp.services.service.load(
            name=iapp_name, partition=self.partition
        )
        iapp_service.delete()
        iapp_template = iapp.templates.template.load(
            name=iapp_name, partition=self.partition
        )
        iapp_template.delete()

    def _deploy_iapp(self, iapp_name, actions, deploy_bigip):
        '''Deploy iapp on the root device.

        :param iapp_name: str -- name of iapp
        :param actions: dict -- actions definition of iapp sections
        '''

        tmpl = deploy_bigip.sys.applications.templates.template
        serv = deploy_bigip.sys.applications.services.service
        tmpl.create(name=iapp_name, partition=self.partition, actions=actions)
        serv.create(
            name=iapp_name, partition=self.partition, template=iapp_name
        )

    def _get_add_peer_cmd(self, peer):
        '''Get tmsh command to add a trusted peer.

        :param peer: bigip object -- peer device
        :returns: str -- tmsh command to add trusted peer
        '''

        peer_device = self.get_device_info(peer)
        return 'tmsh::modify cm trust-domain Root ca-devices add ' \
            '\\{{ {0} \\}} name {1} username admin password admin'.format(
                peer_device.managementIp, peer_device.name
            )

    def _get_delete_peer_cmd(self, peer_name):
        '''Get tmsh command to delete a trusted peer.

        :param peer: bigip object -- peer device
        :returns: str -- tmsh command to delete trusted peer
        '''

        return 'tmsh::modify cm trust-domain Root ca-devices delete ' \
            '\\{ %s \\}' % peer_name
