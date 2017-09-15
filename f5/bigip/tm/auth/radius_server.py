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

"""BIG-IP® auth module

REST URI
    ``http://localhost/mgmt/tm/auth/radius-server``

GUI Path
    ``System --> Users --> Authentication``

REST Kind
    ``tm:auth:radius-server:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Radius_Servers(Collection):
    """BIG-IP® tacacs server collection"""
    def __init__(self, auth):
        super(Radius_Servers, self).__init__(auth)
        self._meta_data['allowed_lazy_attributes'] = [Radius_Server]
        self._meta_data['attribute_registry'] = \
            {'tm:auth:radius-server:radius-serverstate': Radius_Server}


class Radius_Server(Resource):
    """BIG-IP® tacacs server resource"""
    def __init__(self, radius_servers):
        super(Radius_Server, self).__init__(radius_servers)
        self._meta_data['required_json_kind'] = \
            'tm:auth:radius-server:radius-serverstate'
