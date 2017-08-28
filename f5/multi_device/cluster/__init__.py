# coding=utf-8
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
    TrustDomain: a group of BIG-IP® devices that have exchanged certificates
                 and trust one another
    DeviceGroup: a group of BIG-IP® device that sync configuration data and
                 failover connections.

Clustering is broken down into three component parts: a cluster manager, a
trust domain, and a device group. The cluster manager presents the external
interface to a user for operations like create, teardown etc....

To create a device service group (aka cluster) of devices, those devices
must trust one another. This is coordinated by the TrustDomain class. Once
those devices trust one another, a device group is created and each is added
to the group. After this step, a cluster exists.

Currently the only supported type of cluster is a 'sync-failover' cluster.
The number of devices supported officially is currently two, for an
active-standby cluster, but the code below can accommodate a four-member
cluster.

Methods:

    * create -- creates a cluster based on kwargs given by user
    * teardown -- tears down an existing cluster

Examples:

There are two major use-cases here:

    * Manage an existing cluster:

        list_of_bigips = [ManagementRoot(...), ManagementRoot(...)]
        cluster_mgr = ClusterManager(
                            devices=list_of_bigips,
                            device_group_name='my_cluster',
                            device_group_type='sync-failover',
                            device_group_partition='Common'
                        )
        assert cluster_mgr.cluster.devices == list_of_bigips

    * Create a new cluster and manage it:

        list_of_bigips = [ManagementRoot(...), ManagementRoot(...)]
        cluster_mgr = ClusterManager()
        cluster_mgr.create(
                    devices=list_of_bigips,
                    device_group_name='my_cluster',
                    device_group_type='sync-failover',
                    device_group_partition='Common
                )
        assert cluster_mgr.cluster.devices == list_of_bigips
'''

from f5.multi_device.device_group import DeviceGroup
from f5.multi_device.trust_domain import TrustDomain

from f5.multi_device.exceptions import AlreadyManagingCluster
from f5.multi_device.exceptions import ClusterNotSupported
from f5.multi_device.exceptions import NoClusterToManage


from collections import namedtuple


Cluster = namedtuple(
    'Cluster', 'device_group_name device_group_type device_group_partition '
    'devices'
)


class ClusterManager(object):
    '''Manage a cluster of BIG-IP® devices.

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
        '''Check if number of devices is between 2 and 4

        :param kwargs: dict -- keyword args in dict
        '''

        if len(devices) < 2 or len(devices) > 4:
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
        '''Create a cluster of BIG-IP® devices.

        :param kwargs: dict -- keyword arguments for cluster manager
        '''

        try:
            cluster = getattr(self, "cluster", None)
        except NoClusterToManage:
            cluster = None
        if cluster is not None:
            msg = 'The ClusterManager is already managing a cluster.'
            raise AlreadyManagingCluster(msg)

        self._check_device_number(kwargs['devices'])
        self.trust_domain.create(
            devices=kwargs['devices'],
            partition=kwargs['device_group_partition']
        )
        self.device_group.create(**kwargs)
        self.cluster = Cluster(**kwargs)

    def teardown(self):
        '''Teardown the cluster of BIG-IP® devices.'''

        self.device_group.teardown()
        self.trust_domain.teardown()
        self.cluster = None
