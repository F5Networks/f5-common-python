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
from f5.bigip.resource import Resource


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
