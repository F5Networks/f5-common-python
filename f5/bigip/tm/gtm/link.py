# coding=utf-8
#
# Copyright 2018 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager (GTM) link module.

REST URI
    ``http://localhost/mgmt/tm/gtm/link``

GUI Path
    ``DNS --> GSLB : Links``

REST Kind
    ``tm:gtm:link:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Links(Collection):
    """BIG-IP® GTM link collection"""
    def __init__(self, gtm):
        super(Links, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Link]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:link:linkstate': Link}


class Link(Resource):
    """BIG-IP® GTM link resource"""
    def __init__(self, links):
        super(Link, self).__init__(links)
        self._meta_data['required_json_kind'] = 'tm:gtm:link:linkstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'datacenter', 'routerAddresses'))
