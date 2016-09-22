# coding=utf-8
#
# Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Network vlan module.

REST URI
    ``http://localhost/mgmt/tm/net/vlan``

GUI Path
    ``Network --> Vlans``

REST Kind
    ``tm:net:vlan:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import MissingUpdateParameter
from f5.bigip.resource import Resource
from f5.sdk_exception import F5SDKError

from distutils.version import LooseVersion


class TagModeDisallowedForTMOSVersion(F5SDKError):
    pass


class Vlans(Collection):
    """BIG-IP® network Vlan collection."""
    def __init__(self, net):
        super(Vlans, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Vlan]
        self._meta_data['attribute_registry'] =\
            {'tm:net:vlan:vlanstate': Vlan}


class Vlan(Resource):
    """BIG-IP® network Vlan resource."""
    def __init__(self, vlan_s):
        super(Vlan, self).__init__(vlan_s)
        self._meta_data['required_json_kind'] = 'tm:net:vlan:vlanstate'
        self._meta_data['attribute_registry'] =\
            {'tm:net:vlan:interfacescollectionstate': Interfaces_s}


class Interfaces_s(Collection):
    '''BIG-IP® network Vlan interface collection.

    .. note::
        Not to be confused with ``tm/mgmt/net/interface``.  This is object
        is actually called ``interfaces`` with an ``s`` by the BIG-IP's REST
        API.
    '''
    def __init__(self, vlan):
        super(Interfaces_s, self).__init__(vlan)
        self._meta_data['allowed_lazy_attributes'] = [Interfaces]
        self._meta_data['attribute_registry'] =\
            {'tm:net:vlan:interfaces:interfacesstate': Interfaces}


class Interfaces(Resource, ExclusiveAttributesMixin):
    """BIG-IP® network Vlan interface resource."""
    def __init__(self, interfaces_s):
        super(Interfaces, self).__init__(interfaces_s)
        # Vlan intefaces objects do not have a partition
        self._meta_data['required_json_kind'] =\
            'tm:net:vlan:interfaces:interfacesstate'
        # You cannot send both tagged and untagged attributes on update
        self._meta_data['exclusive_attributes'].append(('tagged', 'untagged'))

    def create(self, **kwargs):
        """Create the resource on the BIG-IP®.

        Uses HTTP POST to the `collection` URI to create a resource associated
        with a new unique URI on the device.

        As tagMode parameter will be required
        only if tagged is set to 'True'
        we have to use conditional to capture this logic during create.

        """

        self._check_tagmode_and_tmos_version(**kwargs)
        return self._create(**kwargs)

    def _check_tagmode_and_tmos_version(self, **kwargs):
        '''Raise an exception if tagMode in kwargs and tmos version < 11.6.0

        :param kwargs: dict -- keyword arguments for request
        :raises: TagModeDisallowedForTMOSVersion
        '''

        tmos_version = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_version) < LooseVersion('11.6.0'):
            msg = "The parameter, 'tagMode', is not allowed against the " \
                "following version of TMOS: %s" % (tmos_version)
            if 'tagMode' in kwargs or hasattr(self, 'tagMode'):
                raise TagModeDisallowedForTMOSVersion(msg)

    def update(self, **kwargs):
        self._check_tagmode_and_tmos_version(**kwargs)
        if LooseVersion(self._meta_data['bigip']._meta_data['tmos_version']) \
                >= LooseVersion('11.6.0'):
            if 'tagged' in kwargs:
                if kwargs['tagged'] is True and 'tagMode' not in kwargs:
                    error = 'Missing tagMode parameter value.'
                    raise MissingUpdateParameter(error)
            if hasattr(self, 'tagged'):
                if getattr(self, 'tagged') is True and \
                   getattr(self, 'tagMode') == 'none':
                    error = 'Missing tagMode parameter value.'
                    raise MissingUpdateParameter(error)

        self._update(**kwargs)

        return self
