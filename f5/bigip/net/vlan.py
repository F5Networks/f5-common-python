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

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class VLANCollection(Collection):
    def __init__(self, net):
        super(VLANCollection, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [VLAN]
        self._meta_data['collection_registry'] =\
            {'tm:net:vlan:vlanstate': VLAN}


class VLAN(Resource):
    def __init__(self, vlan_collection):
        super(VLAN, self).__init__(vlan_collection)
        self._meta_data['required_json_kind'] = 'tm:net:vlan:vlanstate'
        self._meta_data['collection_registry'] =\
            {'tm:net:vlan:interfacescollectionstate': InterfacesCollection}


class InterfacesCollection(Collection):
    '''Represents a VLAN interface list.

    Not to be confused with tm/mgmt/net/interface.  This is actually called
    interfaces with an 's' by the BIGIP's REST API.

    *Note* We may need to come back and revist this if it turns out that
    the actual representation of the interface and interfaces objects are
    the same.
    '''
    def __init__(self, vlan):
        super(InterfacesCollection, self).__init__(vlan)
        self._meta_data['allowed_lazy_attributes'] = [Interfaces]
        self._meta_data['collection_registry'] =\
            {'tm:net:vlan:interfaces:interfacesstate': Interfaces}


class Interfaces(Resource, ExclusiveAttributesMixin):
    def __init__(self, interfaces_collection):
        super(Interfaces, self).__init__(interfaces_collection)
        # VLAN intefaces objects do not have a partition
        self._meta_data['required_json_kind'] =\
            'tm:net:vlan:interfaces:interfacesstate'
        # You cannot send both tagged and untagged attributes on update
        self._meta_data['exclusive_attributes'].append(('tagged', 'untagged'))

    def create(self, **kwargs):
        self._create(**kwargs)
        return self

    def load(self, **kwargs):
        self._load(**kwargs)
        return self
