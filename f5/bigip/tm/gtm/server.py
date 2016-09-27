# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager™ (GTM®) pool module.

REST URI
    ``http://localhost/mgmt/tm/gtm/server``

GUI Path
    ``DNS --> GSLB : Servers``

REST Kind
    ``tm:gtm:server:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Servers(Collection):
    """BIG-IP® GTM server collection"""
    def __init__(self, gtm):
        super(Servers, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Server]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:server:serverstate': Server}


class Server(Resource):
    """BIG-IP® GTM server resource"""
    def __init__(self, servers):
        super(Server, self).__init__(servers)
        self._meta_data['required_json_kind'] = 'tm:gtm:server:serverstate'
        self._meta_data['required_creation_parameters'].update(
            ('datacenter', 'addresses'))
        self._meta_data['attribute_registry'] = {
            'tm:gtm:server:virtual-servers:virtual-serverscollectionstate':
                Virtual_Servers_s
        }


class Virtual_Servers_s(Collection):
    """BIG-IP® GTM virtual server sub-collection"""
    def __init__(self, server):
        super(Virtual_Servers_s, self).__init__(server)
        self._meta_data['allowed_lazy_attributes'] = [Virtual_Server]
        self._meta_data['required_json_kind'] = \
            'tm:gtm:server:virtual-servers:virtual-serverscollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:gtm:server:virtual-servers:virtual-serversstate':
                Virtual_Server}


class Virtual_Server(Resource):
    """BIG-IP® GTM virtual server resource"""
    def __init__(self, virtual_servers_s):
        super(Virtual_Server, self).__init__(virtual_servers_s)
        self._meta_data['required_creation_parameters'].update((
            'destination',))
        self._meta_data['required_json_kind'] = \
            'tm:gtm:server:virtual-servers:virtual-serversstate'
