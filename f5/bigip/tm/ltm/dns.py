# coding=utf-8
#
#  Copyright 2018 F5 Networks Inc.
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

"""BIG-IP® LTM DNS submodule.

REST URI
    ``http://localhost/mgmt/tm/ltm/dns/``

GUI Path
    ``DNS --> Delivery``

REST Kind
    ``tm:ltm:dns:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Dns(OrganizingCollection):
    def __init__(self, ltm):
        super(Dns, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Nameservers,
        ]


class Nameservers(Collection):
    def __init__(self, dns):
        super(Nameservers, self).__init__(dns)
        self._meta_data['allowed_lazy_attributes'] = [Nameserver]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:dns:nameserver:nameserverstate': Nameserver
        }


class Nameserver(Resource):
    def __init__(self, nameservers):
        super(Nameserver, self).__init__(nameservers)
        self._meta_data['required_json_kind'] = 'tm:ltm:dns:nameserver:nameserverstate'
