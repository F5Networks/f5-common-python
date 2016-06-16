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

"""BIG-IP® cluster traffic-group submodule

REST URI
    ``http://localhost/mgmt/tm/cm/traffic-group``

GUI Path
    ``Device Management --> Traffic Groups``

REST Kind
    ``tm:cm:traffic-group:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Traffic_Groups(Collection):
    """BIG-IP® cluster traffic-group collection"""
    def __init__(self, cm):
        super(Traffic_Groups, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [Traffic_Group]
        self._meta_data['attribute_registry'] =\
            {'tm:cm:traffic-group:traffic-groupstate': Traffic_Group}


class Traffic_Group(Resource):
    """BIG-IP® cluster traffic-group resource"""
    def __init__(self, traffic_groups):
        super(Traffic_Group, self).__init__(traffic_groups)
        self._meta_data['required_json_kind'] =\
            'tm:cm:traffic-group:traffic-groupstate'
        self._meta_data['required_creation_parameters'].update(('partition',))
