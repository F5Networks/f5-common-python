# coding=utf-8
#
#  Copyright 2014-2017 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager™ (GTM®) Region module.

REST URI
    ``http://localhost/mgmt/tm/gtm/region``

GUI Path
    ``DNS --> GSLB : Topology : Regions``

REST Kind
    ``tm:gtm:region:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Regions(Collection):
    """BIG-IP® GTM Region collection"""
    def __init__(self, gtm):
        super(Regions, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Region]
        self._meta_data['attribute_registry'] = \
            {'tm:gtm:region:regionstate': Region}


class Region(Resource):
    """BIG-IP® GTM Region resource"""
    def __init__(self, regions):
        super(Region, self).__init__(regions)
        self._meta_data['required_json_kind'] = 'tm:gtm:region:regionstate'
