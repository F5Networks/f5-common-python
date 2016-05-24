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

'''Class to manage a TrustDomain for a set of BIG-IP devices.'''

from f5.multi_device.exceptions import DeviceAlreadyInTrustDomain
from f5.multi_device.exceptions import DeviceNotTrusted

from f5.multi_device.utils import get_device_info
from f5.multi_device.utils import get_device_names_to_objects
from f5.multi_device.utils import pollster


class TrustDomain(object):
    '''Manages the trusted peers of a BigIP device.'''

    iapp_actions = {'definition': {'implementation': None, 'presentation': ''}}

    def __init__(self, **kwargs):
        '''Initialize a trusted peer manager object.

        :param kwargs: dict -- keyword args for devices and partition
        '''

        self.domain = {}
        if kwargs:
            self.devices = kwargs['devices'][:]
            self.partition = kwargs['partition']
            self.validate()

    def validate(self):
        '''Validate that devices are each trusted by one another

        :param kwargs: dict -- keyword args for devices and partition
        :raises: DeviceNotTrusted
        '''

        self._populate_domain()
        missing = []
        for domain_device in self.domain:
            for truster, trustees in self.domain.iteritems():
                if domain_device not in trustees:
                    missing.append((domain_device, truster, trustees))

        if missing:
            msg = ''
            for item in missing:
                msg += '\n%r is not trusted by %r, which trusts: %r' % \
                    (item[0], item[1], item[2])
            raise DeviceNotTrusted(msg)

    def _populate_domain(self):
        '''Populate TrustDomain's domain attribute.'''

        self.domain = {}
        for device in self.devices:
            device_name = get_device_info(device).name
            ca_devices = \
                device.tm.cm.trust_domains.trust_domain.load(
                    name='Root'
                ).caDevices
            self.domain[device_name] = [
                d.replace('/%s/' % self.partition, '') for d in ca_devices
            ]

    def create(self, **kwargs):
        '''Add trusted peers to the root bigip device.

        When adding a trusted device to a device, the trust is reflexive. That
        is, the truster trusts the trustee and the trustee trusts the truster.
        So we only need to add the trusted devices to one device.

        :param kwargs: dict -- devices and partition
        '''

        self.devices = kwargs['devices'][:]
        self.partition = kwargs['partition']
        for device in self.devices[1:]:
            self._add_trustee(device)
        pollster(self.validate)()

    def teardown(self):
        '''Teardown trust domain by removing trusted devices.'''

        for device in self.devices:
            self._remove_trustee(device)
            self._populate_domain()
        self.domain = {}

    def scale_up_by_one(self, device):
        '''Scale up trust domain by one device.

        :param device: ManagementRoot object -- device to scale up
        '''

        self.devices.append(device)
        self._add_trustee(device)
        pollster(self.validate)()

    def scale_down_by_one(self, device, device_group_object=None):
        '''Scale down trust domain by one device.

        :param device: ManagementRoot object -- device to scale down
        '''

        self._remove_trustee(device, device_group_object)
        pollster(self.validate)()

    def _add_trustee(self, device):
        '''Add a single trusted device to the trust domain.

        :param device: ManagementRoot object -- device to add to trust domain
        '''

        device_name = get_device_info(device).name
        if device_name in self.domain:
            msg = 'Device: %r is already in this trust domain.' % device_name
            raise DeviceAlreadyInTrustDomain(msg)
        self._modify_trust(self.devices[0], self._get_add_trustee_cmd, device)

    def _remove_trustee(self, device, device_group_object=None):
        '''Remove a trustee from the trust domain.

        If this is called as part of scale_down_by_one, the device being scaled
        must remove the members of its device group before removing trusted
        devices. This is optional.

        :param device: MangementRoot object -- device to remove
        '''

        trustee_name = get_device_info(device).name
        name_object_map = get_device_names_to_objects(self.devices)
        delete_func = self._get_delete_trustee_cmd

        for truster in self.domain:
            if trustee_name in self.domain[truster] and \
                    truster != trustee_name:
                truster_obj = name_object_map[truster]
                self._modify_trust(truster_obj, delete_func, trustee_name)
            self._populate_domain()

        if device_group_object:
            device_group_object.cleanup_scaled_down_device(device)

        for trustee in self.domain[trustee_name]:
            if trustee_name != trustee:
                self._modify_trust(device, delete_func, trustee)

        self.devices.remove(name_object_map[trustee_name])

    def _modify_trust(self, truster, mod_peer_func, trustee):
        '''Modify a trusted peer device by deploying an iapp.


        :param truster: ManagementRoot object -- device on which to perform
                        commands
        :param mod_peer_func: function -- function to call to modify peer
        :param trustee: ManagementRoot object or str -- device to modify
        '''

        iapp_name = 'trusted_device'
        mod_peer_cmd = mod_peer_func(trustee)
        iapp_actions = self.iapp_actions.copy()
        iapp_actions['definition']['implementation'] = mod_peer_cmd
        self._deploy_iapp(iapp_name, iapp_actions, truster)
        self._delete_iapp(iapp_name, truster)

    def _delete_iapp(self, iapp_name, deploying_device):
        '''Delete an iapp service and template on the root device.

        :param iapp_name: str -- name of iapp
        :param deploying_device: ManagementRoot object -- device where the
                                 iapp will be deleted
        '''

        iapp = deploying_device.tm.sys.applications
        iapp_serv = iapp.services.service.load(
            name=iapp_name, partition=self.partition
        )
        iapp_serv.delete()
        iapp_tmpl = iapp.templates.template.load(
            name=iapp_name, partition=self.partition
        )
        iapp_tmpl.delete()

    def _deploy_iapp(self, iapp_name, actions, deploying_device):
        '''Deploy iapp to add trusted device

        :param iapp_name: str -- name of iapp
        :param actions: dict -- actions definition of iapp sections
        :param deploying_device: ManagementRoot object -- device where the
                                 iapp will be created
        '''

        tmpl = deploying_device.tm.sys.applications.templates.template
        serv = deploying_device.tm.sys.applications.services.service
        tmpl.create(name=iapp_name, partition=self.partition, actions=actions)
        serv.create(
            name=iapp_name,
            partition=self.partition,
            template='/%s/%s' % (self.partition, iapp_name)
        )

    def _get_add_trustee_cmd(self, trustee):
        '''Get tmsh command to add a trusted device.

        :param trustee: ManagementRoot object -- device to add as trusted
        :returns: str -- tmsh command to add trustee
        '''

        trustee_info = pollster(get_device_info)(trustee)
        print('Adding following peer to root: %s' % trustee_info.name)
        username = trustee._meta_data['username']
        password = trustee._meta_data['password']
        return 'tmsh::modify cm trust-domain Root ca-devices add ' \
            '\\{ %s \\} name %s username %s password %s' % \
            (trustee_info.managementIp, trustee_info.name, username, password)

    def _get_delete_trustee_cmd(self, trustee_name):
        '''Get tmsh command to delete a trusted device.

        :param trustee_name: str -- name of device to remove
        :returns: str -- tmsh command to delete trusted device
        '''

        return 'tmsh::modify cm trust-domain Root ca-devices delete ' \
            '\\{ %s \\}' % trustee_name
