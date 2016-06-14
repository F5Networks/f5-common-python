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
"""BIG-IP® system failover module

REST URI
    ``http://localhost/mgmt/tm/shared/license``

GUI Path
    ``System --> License``

REST Kind
    ``tm:shared:licensing:*``
"""

from f5.bigip.mixins import UnsupportedMethod
from f5.bigip.resource import PathElement
from f5.bigip.resource import UnnamedResource


class Licensing(PathElement):
    """BIG-IP® licensing stats and states.

    Licensing objects themselves do not support any methods and are just
    containers for lower level objects.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """
    def __init__(self, shared):
        super(Licensing, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Activation,
            Registration,
        ]
        self._meta_data['attribute_registry'] = {
            'tm:shared:licensing:activation:activatelicenseresponse':
                Activation,
            'tm:shared:licensing:registration:registrationlicenseresponse':
                Registration,
        }


class Activation(UnnamedResource):
    """BIG-IP® license activation status

    Activation state objects only support the
    :meth:`~f5.bigip.resource.Resource.load` method because they cannot be
    modified via the API.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, licensing):
        super(Activation, self).__init__(licensing)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:shared:licensing:activation:activatelicenseresponse'

    def update(self, **kwargs):
        '''Update is not supported for License Activation

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )


class Registration(UnnamedResource):
    """BIG-IP® license registration status

    Registration state objects only support the
    :meth:`~f5.bigip.resource.Resource.load` method because they cannot be
    modified via the API.

    .. note::

        This is an unnamed resource so it has not ~Partition~Name pattern
        at the end of its URI.
    """

    def __init__(self, licensing):
        super(Registration, self).__init__(licensing)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:shared:licensing:activation:activatelicenseresponse'

    def update(self, **kwargs):
        '''Update is not supported for License Registration

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )
