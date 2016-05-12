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
    ``http://localhost/mgmt/tm/net/dns-resolver``

GUI Path
    ``Network --> Dns Resolvers``

REST Kind
    ``tm:net:dns:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Dns_Resolvers(Collection):
    """BIG-IP® network Dns Resolver collection"""
    def __init__(self, net):
        super(Dns_Resolvers, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Dns_Resolver]
        self._meta_data['attribute_registry'] = {
            'tm:net:dns-resolver:dns-resolverstate': Dns_Resolver
        }


class Dns_Resolver(Resource):
    """BIG-IP® Dns Resolver resource."""
    def __init__(self, Dns_Resolvers):
        super(Dns_Resolver, self).__init__(Dns_Resolvers)
        self._meta_data['required_json_kind'] = \
            'tm:net:dns-resolver:dns-resolverstate'
