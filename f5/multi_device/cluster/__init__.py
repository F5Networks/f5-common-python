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

'''The classes within define the management of a cluster of BIG_IP devices.

Definitions:
    Cluster: The manager of the TrustDomain and DeviceGroup objects.
    TrustDomain: a group of BIG-IP devices that have exchanged certificates
                 and trust one another
    DeviceGroup: a group of BIG-IP device that sync configuration data and
                 failover connections.

Clustering is broken down into three component parts: a cluster manager, a
trust domain, and a device group. The cluster manager presents the external
interface to a user for operations like create, teardown etc....

To create a device service group (aka cluster) of devices, those devices
must trust one another. This is coordinated by the TrustDomain class. Once
those devices trust one another, a device group is created and each is added
to the group. After this step, a cluster exists.

Currently the only supported type of cluster is a 'sync-failover' cluster.

ClusterManager Methods:

    * create -- creates a cluster based on kwargs given by user
    * teardown -- tears down an existing cluster
    * scale_up_by_one -- add one device to the cluster
    * scale_down_by_one -- remove one device from the cluster

Classes:

    * ClusterManager -- manages a cluster of devices with the methods above
    * TrustDomain -- manages the trust domain for a cluster
    * DeviceGroup -- manages the device group for a cluster
'''

from f5.sdk_exception import F5SDKError
from f5.utils.decorators import poll_for_exceptionless_callable

from collections import namedtuple


class ClusterError(F5SDKError):
    def __init__(self, *args, **kwargs):
        super(ClusterError, self).__init__(*args, **kwargs)


class DeviceGroupError(F5SDKError):
    pass


class TrustDomainError(F5SDKError):
    pass


class AlreadyManagingCluster(ClusterError):
    pass


class ClusterNotSupported(ClusterError):
    pass


class ClusterOperationNotSupported(ClusterError):
    pass


class DeviceAlreadyInTrustDomain(TrustDomainError):
    pass


class MissingRequiredDeviceGroupParameter(ClusterError):
    pass


class NoClusterToManage(ClusterError):
    pass


class DeviceGroupNotSupported(DeviceGroupError):
    pass


class DeviceGroupOperationNotSupported(DeviceGroupError):
    pass


class DeviceNotTrusted(TrustDomainError):
    pass


class TrusteeNotInTrustDomain(TrustDomainError):
    pass


class UnexpectedDeviceGroupState(DeviceGroupError):
    pass


class UnexpectedDeviceGroupDevices(DeviceGroupError):
    pass


class UnexpectedDeviceGroupType(DeviceGroupError):
    pass

Cluster = namedtuple(
    'Cluster', 'device_group_name device_group_type device_group_partition '
    'devices'
)


def pollster(callable):
    '''Wraps the poll to get attempts and interval applicable for cluster.

    :param callable: callable -- callable to pass into poll
    '''

    return poll_for_exceptionless_callable(callable, 20, 2)


def get_device_info(bigip):
    '''Get device information about a specific BigIP device.

    :param bigip: ManagementRoot object --- device to inspect
    :returns: ManagementRoot object
    '''

    coll = pollster(bigip.tm.cm.devices.get_collection)()
    device = [device for device in coll if device.selfDevice == 'true']
    assert len(device) == 1
    return device[0]


def get_device_names_to_objects(devices):
    '''Map a list of devices to their hostnames.

    :param devices: list -- list of ManagementRoot objects
    :returns: dict -- mapping of hostnames to ManagementRoot objects
    '''

    name_to_object = {}
    for device in devices:
        device_name = get_device_info(device).name
        name_to_object[device_name] = device
    return name_to_object


class ClusterManager(object):
    '''Manage a cluster of BigIPs.

    This is accomplished with REST URI calls only, but some operations are
    only permitted via tmsh commands (such as adding cm/trust-domain peers).
    We get around this issue by deploying iApps (sys/application).
    '''

    def __init__(self, **kwargs):
        '''Initialize a cluster manager object.

        :param bigips: list -- list of bigip.ManagementRoot ojects to cluster
        :param cluster_name: str -- name of device service group
        :param partition: str -- partition to associate cluster with
        :param cluster_type: str -- type of cluster configuration
        '''

        if kwargs:
            self.manage_extant(**kwargs)
        else:
            self.trust_domain = TrustDomain()
            self.device_group = DeviceGroup()

    def __getattr__(self, name):
        '''If ClusterManager.cluster is not found come here.

        :param name: str -- name of attribute
        :raises: AttributeError
        '''

        if name == 'cluster':
            msg = 'The ClusterManager is not managing a cluster.'
            raise NoClusterToManage(msg)
        raise AttributeError(name)

    def _check_device_number(self, devices):
        '''Check if number of devices is < 2 or > 8.

        :param kwargs: dict -- keyword args in dict
        '''

        if len(devices) < 2 or len(devices) > 8:
            msg = 'The number of devices to cluster is not supported.'
            raise ClusterNotSupported(msg)

    def manage_extant(self, **kwargs):
        '''Manage an existing cluster

        :param kwargs: dict -- keyword args in dict
        '''

        self._check_device_number(kwargs['devices'])
        self.trust_domain = TrustDomain(
            devices=kwargs['devices'],
            partition=kwargs['device_group_partition']
        )
        self.device_group = DeviceGroup(**kwargs)
        self.cluster = Cluster(**kwargs)

    def create(self, **kwargs):
        '''Create a cluster of BigIP devices.

        :param kwargs: dict -- keyword arguments for cluster manager
        '''

        if hasattr(self, 'cluster'):
            msg = 'The ClusterManager is already managing a cluster.'
            raise AlreadyManagingCluster(msg)
        print('Adding trusted peers to root BigIP...')
        self.trust_domain.create(
            devices=kwargs['devices'],
            partition=kwargs['device_group_partition']
        )
        print('Creating device group...')
        self.device_group.create(**kwargs)
        print('Cluster created...')
        self.cluster = Cluster(**kwargs)

    def teardown(self):
        '''Teardown the cluster of BigIP devices.'''

        print('Tearing down the cluster...')
        self.device_group.teardown()
        self.trust_domain.teardown()
        self.cluster = None

    def scale_up_by_one(self, device):
        '''Scale cluster up by one device.

        :param bigip: bigip object -- bigip to add
        :raises: ClusterNotSupported
        '''

        if len(self.cluster.devices) == 8:
            msg = 'The number of devices to cluster is not supported.'
            raise ClusterNotSupported(msg)
        print('Scaling cluster up by one device...')
        self.trust_domain.scale_up_by_one(device)
        self.device_group.scale_up_by_one(device)
        self.cluster.devices.append(device)
        self.device_group.ensure_all_devices_in_sync()

    def scale_down_by_one(self, device):
        '''Scale cluster down by one device.

        :param device: ManagementRoot object -- device to delete
        :raises: ClusterNotSupported
        '''

        if len(self.cluster.devices) < 3:
            msg = 'The number of devices to cluster is not supported.'
            raise ClusterNotSupported(msg)
        print('Scaling cluster down by one device...')
        self.device_group.scale_down_by_one(device)
        self.trust_domain.scale_down_by_one(device, self.device_group)
        self.cluster.devices.remove(device)
        self.device_group.ensure_all_devices_in_sync()


class DeviceGroup(object):
    '''Class to manage device service group.'''

    available_types = ['sync-failover']
    sync_status_entry = 'https://localhost/mgmt/tm/cm/sync-status/0'

    def __init__(self, **kwargs):
        '''Initialize a device group manager.

        '''

        if kwargs:
            self.manage_extant(**kwargs)

    def _set_attributes(self, **kwargs):
        '''Set instance attributes based on kwargs

        :param kwargs: dict -- kwargs to set as attributes
        '''

        try:
            self.devices = kwargs['devices'][:]
            self.name = kwargs['device_group_name']
            self.type = kwargs['device_group_type']
            self.partition = kwargs['device_group_partition']
        except KeyError as ex:
            raise MissingRequiredDeviceGroupParameter(ex)

    def validate(self, **kwargs):
        '''Validate device group state among given devices.

        :param kwargs: dict -- keyword args of device group information
        :raises: UnexpectedDeviceGroupType, UnexpectedDeviceGroupDevices
        '''

        self._set_attributes(**kwargs)
        self._check_type()
        self.dev_group_uri_res = self._get_device_group(self.devices[0])
        if self.dev_group_uri_res.type != self.type:
            msg = 'Device group type found: %r does not match expected ' \
                'device group type: %r' % (
                    self.dev_group_uri_res.type, self.type
                )
            raise UnexpectedDeviceGroupType(msg)
        queried_device_names = self._get_device_names_in_group()
        given_device_names = []
        for device in self.devices:
            device_name = get_device_info(device).name
            given_device_names.append(device_name)
        if sorted(queried_device_names) != sorted(given_device_names):
            msg = ''
            raise UnexpectedDeviceGroupDevices(msg)

    def _check_type(self):
        '''Check that the device group type is correct.

        :raises: DeviceGroupOperationNotSupported, DeviceGroupNotSupported
        '''

        if self.type not in self.available_types:
            msg = 'Unsupported cluster type was given: %s' % self.type
            raise DeviceGroupNotSupported(msg)

    def manage_extant(self, **kwargs):
        self.validate(**kwargs)

    def create(self, **kwargs):
        '''Create the device service cluster group and add devices to it.'''

        self._set_attributes(**kwargs)
        self._check_type()
        pollster(self._check_all_devices_in_sync)()
        dg = self.devices[0].tm.cm.device_groups.device_group
        dg.create(name=self.name, partition=self.partition, type=self.type)
        for device in self.devices:
            self._add_device_to_device_group(device)
            device.tm.sys.config.exec_cmd('save')
        self.ensure_all_devices_in_sync()

    def teardown(self):
        '''Teardown device service cluster group.'''

        self.ensure_all_devices_in_sync()
        for device in self.devices:
            self._delete_device_from_device_group(device)
            self._sync_to_group(device)
            pollster(self._ensure_device_active)(device)
            self.ensure_all_devices_in_sync()
        dg = pollster(self._get_device_group)(self.devices[0])
        dg.delete()
        pollster(self._check_devices_active_licensed)()
        pollster(self._check_all_devices_in_sync)()

    def scale_up_by_one(self, device):
        '''Scale device group up by one device

        :param device: ManagementRoot object -- device to add to device group
        '''

        device_name = get_device_info(device).name
        if device_name in self._get_device_names_in_group():
            msg = 'Device: %r is already in device group' % device_name
            raise DeviceGroupOperationNotSupported(msg)
        self._check_device_failover_status(device, 'In Sync')
        self._add_device_to_device_group(device)
        device.tm.sys.config.exec_cmd('save')
        self.devices.append(device)
        self.ensure_all_devices_in_sync()

    def scale_down_by_one(self, device):
        '''Scale device group down by one device

        :param device: ManagementRoot object -- device to delete from device
                       group
        '''

        device_name = get_device_info(device).name
        if device_name not in self._get_device_names_in_group():
            msg = 'Device: %r is not in device group' % device_name
            raise DeviceGroupOperationNotSupported(msg)
        self._delete_device_from_device_group(device)
        device.tm.sys.config.exec_cmd('save')
        name_to_objects = get_device_names_to_objects(self.devices)
        self.devices.remove(name_to_objects[device_name])
        self.ensure_all_devices_in_sync()

    def cleanup_scaled_down_device(self, device):
        '''Remove all devices from device group on orphaned device.

        :param device: bigip object -- device to cleanup
        '''

        dg = self._delete_all_devices_from_device_group(device)
        dg.delete()

    def _get_device_names_in_group(self):
        '''_get_device_names_in_group

        :returns: list -- list of device names in group
        '''

        device_names = []
        dg = pollster(self._get_device_group)(self.devices[0])
        members = dg.devices_s.get_collection()
        for member in members:
            device_names.append(member.name)
        return device_names

    def _get_device_group(self, device):
        '''Get the device group through a device.

        :param device: bigip object -- device
        :returns: tm.cm.device_groups.device_group object
        '''

        return device.tm.cm.device_groups.device_group.load(
            name=self.name, partition=self.partition
        )

    def _check_devices_active_licensed(self):
        '''All devices should be in an active/licensed state.

        :raises: UnexpectedClusterState
        '''

        if len(self._get_devices_by_activation_state('active')) != \
                len(self.devices):
            msg = "One or more devices not in 'Active' and licensed state."
            raise UnexpectedDeviceGroupState(msg)

    def _add_device_to_device_group(self, device):
        '''Add device to device service cluster group.

        :param device: bigip object -- device to add to group
        '''

        device_name = get_device_info(device).name
        dg = pollster(self._get_device_group)(device)
        dg.devices_s.devices.create(name=device_name, partition=self.partition)
        pollster(self._check_device_exists_in_device_group)(device_name)
        print('added following device to group: ' + device_name)

    def _check_device_exists_in_device_group(self, device_name):
        '''Check whether a device exists in the device group

        :param device: ManagementRoot object -- device to look for
        '''

        dg = self._get_device_group(self.devices[0])
        dg.devices_s.devices.load(name=device_name, partition=self.partition)

    def _delete_all_devices_from_device_group(self, device):
        '''Remove all devices from device service cluster group.

        :param device: ManagementRoot object -- device from which to remove
        '''

        dg = pollster(self._get_device_group)(device)
        dg_devices = dg.devices_s.get_collection()
        for device in dg_devices:
            device.delete()
        return dg

    def _delete_device_from_device_group(self, device):
        '''Remove device from device service cluster group.

        :param device: ManagementRoot object -- device to delete from group
        '''

        device_name = get_device_info(device).name
        dg = pollster(self._get_device_group)(device)
        device_to_remove = dg.devices_s.devices.load(
            name=device_name, partition=self.partition
        )
        device_to_remove.delete()

    def _ensure_device_active(self, device):
        '''Ensure a single device is in an active state

        :param device: ManagementRoot object -- device to inspect
        :raises: UnexpectedClusterState
        '''

        act = device.tm.cm.devices.device.load(
            name=get_device_info(device).name,
            partition=self.partition
        )
        if act.failoverState != 'active':
            msg = "A device in the cluster was not in the 'Active' state."
            raise UnexpectedDeviceGroupState(msg)

    def _sync_to_group(self, device):
        '''Sync the device to the cluster group

        :param device: bigip object -- device to sync to group
        '''

        config_sync_cmd = 'config-sync to-group %s' % self.name
        device.tm.cm.exec_cmd('run', utilCmdArgs=config_sync_cmd)

    def ensure_all_devices_in_sync(self):
        """Ensure all devices have 'In Sync' status are sync is done."""

        self._sync_to_group(self.devices[0])
        pollster(self._check_all_devices_in_sync)()

    def _check_all_devices_in_sync(self):
        '''Wait until all devices have failover status of 'In Sync'.

        :raises: UnexpectedClusterState
        '''

        if len(self._get_devices_by_failover_status('In Sync')) != \
                len(self.devices):
            msg = "Expected all devices in group to have 'In Sync' status."
            raise UnexpectedDeviceGroupState(msg)

    def _get_devices_by_failover_status(self, status):
        '''Get a list of bigips by failover status.

        :param status: str -- status to filter the returned list of devices
        :returns: list -- list of devices that have the given status
        '''

        devices_with_status = []
        for device in self.devices:
            if (self._check_device_failover_status(device, status)):
                devices_with_status.append(device)
        return devices_with_status

    def _check_device_failover_status(self, device, status):
        '''Determine if a device has a specific failover status.

        :param status: str -- status to check against
        :returns: bool -- True is it has status, False otherwise
        '''

        sync_status = device.tm.cm.sync_status
        sync_status.refresh()
        current_status = (sync_status.entries[self.sync_status_entry]
                          ['nestedStats']['entries']['status']
                          ['description'])
        if status == current_status:
            return True
        return False

    def _get_devices_by_activation_state(self, state):
        '''Get a list of bigips by activation statue.

        :param state: str -- state to filter the returned list of devices
        :returns: list -- list of devices that are in the given state
        '''

        devices_with_state = []
        for device in self.devices:
            act = device.tm.cm.devices.device.load(
                name=get_device_info(device).name,
                partition=self.partition
            )
            if act.failoverState == state:
                devices_with_state.append(device)
        return devices_with_state


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
