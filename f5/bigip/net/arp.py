# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® Network ARP module.

REST URI
    ``http://localhost/mgmt/tm/net/arp``

GUI Path
    ``Network --> ARP``

REST Kind
    ``tm:net:arp:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Arps(Collection):
    """BIG-IP® network ARP collection"""
    def __init__(self, net):
        super(Arps, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Arp]
        self._meta_data['attribute_registry'] = {
            'tm:net:arp:arpstate': Arp
        }


class Arp(Resource):
    """BIG-IP® network ARP resource"""
    def __init__(self, arp_s):
        super(Arp, self).__init__(arp_s)
        self._meta_data['required_json_kind'] = 'tm:net:arp:arpstate'
        self._meta_data['required_creation_parameters'].update(
            ('partition', 'name', 'ipAddress', 'macAddress')
        )
        self._meta_data['read_only_attributes'].append('ipAddress')
