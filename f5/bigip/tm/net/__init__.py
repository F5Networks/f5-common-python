# coding=utf-8
#
# Copyright 2015 F5 Networks Inc.
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

"""BIG-IP® net module

REST URI
    ``http://localhost/mgmt/tm/net/``

GUI Path
    ``Network``

REST Kind
    ``tm:net:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.net.arp import Arps
from f5.bigip.tm.net.dns_resolver import Dns_Resolvers
from f5.bigip.tm.net.fdb import Fdb
from f5.bigip.tm.net.interface import Interfaces
from f5.bigip.tm.net.route import Routes
from f5.bigip.tm.net.route_domain import Route_Domains
from f5.bigip.tm.net.selfip import Selfips
from f5.bigip.tm.net.trunk import Trunks
from f5.bigip.tm.net.tunnels import TunnelS
from f5.bigip.tm.net.vlan import Vlans


class Net(OrganizingCollection):
    def __init__(self, tm):
        super(Net, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Arps,
            Dns_Resolvers,
            Fdb,
            Interfaces,
            Routes,
            Route_Domains,
            Selfips,
            Trunks,
            TunnelS,
            Vlans
        ]
