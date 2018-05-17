# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® system disk module.

REST URI
    ``http://localhost/mgmt/tm/sys/disk/*``

GUI Path
    ``System --> Disk Management --> *``

REST Kind
    ``tm:sys:disk:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedMethod


class Disk(OrganizingCollection):
    def __init__(self, sys):
        super(Disk, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Logical_Disks,
        ]


class Directory(object):
    """Directory stats class, has 2 endpoints producing the same output:

    "https://localhost/mgmt/tm/sys/disk/directory" and

    "https://localhost/mgmt/tm/sys/disk/directory/stats/"

    This will require careful thought on the implementation. This is a placeholder for future
    """
    pass


class Application_Volume(object):
    """Placeholder for another endpoint"""
    pass


class Logical_Disks(Collection):
    """BIG-IP® system logical disk collection"""
    def __init__(self, sys):
        super(Logical_Disks, self).__init__(sys)
        self._meta_data['object_has_stats'] = False
        self._meta_data['attribute_registry'] = \
            {'tm:sys:disk:logical-disk:logical-diskstate': Logical_Disk}
        self._meta_data['allowed_lazy_attributes'] = [Logical_Disk]


class Logical_Disk(Resource):
    """BIG-IP® system logical disk unnamed resource"""
    def __init__(self, logical_disks):
        super(Logical_Disk, self).__init__(logical_disks)
        self._meta_data['required_json_kind'] =\
            'tm:sys:disk:logical-disk:logical-diskstate'

    def update(self, **kwargs):
        """Update is not supported for logical disk.

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedMethod`
        """
        raise UnsupportedMethod("{0} does not support the update method, only load and refresh".format(self.__class__.__name__))

    def create(self, **kwargs):
        """Create is not supported for logical disk.

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedMethod`
        """
        raise UnsupportedMethod("{0} does not support the create method, only load and refresh".format(self.__class__.__name__))

    def modify(self, **kwargs):
        """Modify is not supported for logical disk.

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedMethod`
        """
        raise UnsupportedMethod("{0} does not support the modify method, only load and refresh".format(self.__class__.__name__))

    def delete(self, **kwargs):
        """Delete is not supported for logical disk.

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedMethod``
        """
        raise UnsupportedMethod("{0} does not support the delete method, only load and refresh".format(self.__class__.__name__))
