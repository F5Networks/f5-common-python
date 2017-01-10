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

"""Directory: net module: route-domain.

REST URI
    ``https://localhost/mgmt/tm/net/route-domain?ver=11.6.0``

GUI Path
    ``XXX``

REST Kind
    ``tm:net:route-domain:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Route_Domains(Collection):
    """BIG-IP® Route Domain collection."""
    def __init__(self, net):
        super(Route_Domains, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Route_Domain]
        self._meta_data['attribute_registry'] =\
            {'tm:net:route-domain:route-domainstate': Route_Domain}


class Route_Domain(Resource):
    """BIG-IP® Route Domain collection."""
    def __init__(self, Route_Domains):
        super(Route_Domain, self).__init__(Route_Domains)
        self._meta_data['read_only_attributes'].append('id')
        self._meta_data['required_json_kind'] =\
            "tm:net:route-domain:route-domainstate"
