# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""BIG-IP® Network trunk module.

REST URI
    ``http://localhost/mgmt/tm/net/trunk``

GUI Path
    ``Network --> Trunks``

REST Kind
    ``tm:net:trunk:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Trunks(Collection):
    """BIG-IP® network route collection"""
    def __init__(self, net):
        super(Trunks, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Trunk]
        self._meta_data['attribute_registry'] = {
            'tm:net:trunk:trunkstate': Trunk
        }


class Trunk(Resource, ExclusiveAttributesMixin):
    def __init__(self, trunks):
        super(Trunk, self).__init__(trunks)
        self._meta_data['required_json_kind'] = 'tm:net:trunk:trunkstate'
        self._meta_data['read_only_attributes'].append(
            ('network', 'cfgMbrCount', 'workingMbrCount', 'macAddress',
             'bandwidth')
        )
