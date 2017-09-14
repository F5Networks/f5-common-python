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

"""BIG-IP® Guest (vcmp) module

REST URI
    ``http://localhost/mgmt/tm/vcmp/virtual-disk/``

GUI Path
    ``Virtual Disk List``

REST Kind
    ``tm:vcmp:virtual-disk:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import DisallowedCreationParameter
from f5.sdk_exception import DisallowedReadParameter
from f5.sdk_exception import F5SDKError
from f5.sdk_exception import UnsupportedMethod


class Virtual_Disks(Collection):
    def __init__(self, vcmp):
        super(Virtual_Disks, self).__init__(vcmp)
        self._meta_data['allowed_lazy_attributes'] = [Virtual_Disk]
        self._meta_data['required_json_kind'] = 'tm:vcmp:virtual-disk:virtual-diskcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:vcmp:virtual-disk:virtual-diskstate': Virtual_Disk
        }


class Virtual_Disk(Resource):
    def __init__(self, collection):
        super(Virtual_Disk, self).__init__(collection)
        self._meta_data['required_json_kind'] = 'tm:vcmp:virtual-disk:virtual-diskstate'

    def load(self, **kwargs):
        """Loads a given resource

        Loads a given resource provided a 'name' and an optional 'slot'
        parameter. The 'slot' parameter is not a required load parameter
        because it is provided as an optional way of constructing the
        correct 'name' of the vCMP resource.

        :param kwargs:
        :return:
        """
        kwargs['transform_name'] = True
        kwargs = self._mutate_name(kwargs)
        return self._load(**kwargs)

    def exists(self, **kwargs):
        kwargs['transform_name'] = True
        kwargs = self._mutate_name(kwargs)
        return self._exists(**kwargs)

    def delete(self, **kwargs):
        kwargs['transform_name'] = True
        kwargs = self._mutate_name(kwargs)
        return self._delete(**kwargs)

    def modify(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def create(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__
        )

    def update(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

    def _check_load_parameters(self, **kwargs):
        """Override method for one in resource.py to check partition

        The partition cannot be included as a parameter to load a guest.
        Raise an exception if a consumer gives the partition parameter.

        :raises: DisallowedReadParameter
        """

        if 'partition' in kwargs:
            msg = "'partition' is not allowed as a load parameter. Vcmp " \
                "guests are accessed by name."
            raise DisallowedReadParameter(msg)
        super(Virtual_Disk, self)._check_load_parameters(**kwargs)

    def _check_create_parameters(self, **kwargs):
        """Override method for one in resource.py to check partition

        The partition cannot be included as a parameter to create a guest.
        Raise an exception if a consumer gives the partition parameter.

        :raises: DisallowedCreationParameter
        """

        if 'partition' in kwargs:
            msg = "'partition' is not allowed as a create parameter. Vcmp " \
                "guests are created with the 'name' at least."
            raise DisallowedCreationParameter(msg)
        super(Virtual_Disk, self)._check_create_parameters(**kwargs)

    def _mutate_name(self, kwargs):
        slot = kwargs.pop('slot', None)
        if slot is not None:
            try:
                kwargs['name'] = '{0}/{1}'.format(kwargs['name'], int(slot))
            except ValueError:
                raise F5SDKError(
                    "The provided 'slot' must be a number"
                )
        return kwargs
