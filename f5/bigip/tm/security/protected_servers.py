# coding=utf-8
#
# Copyright 2015-2017 F5 Networks Inc.
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

"""BIG-IP® Advanced Firewall Manager™ (AFM®) module.

REST URI
    ``http://localhost/mgmt/tm/security/protected-servers``

GUI Path
    ``Security --> DoS Protection --> Protected Objects``

REST Kind
    ``tm:security:protected-servers:protected-serverscollectionstate:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Protected_Servers(OrganizingCollection):
    """BIG-IP® AFM® Protected servers organizing collection."""

    def __init__(self, security):
        super(Protected_Servers, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Traffic_Matching_Criteria_s,
            Netflow_Protected_Server_s]


class Traffic_Matching_Criteria_s(Collection):
    """BIG-IP® AFM® Traffic Matching Criteria collection"""

    def __init__(self, protected_servers):
        super(Traffic_Matching_Criteria_s, self).__init__(protected_servers)
        self._meta_data['allowed_lazy_attributes'] = [Traffic_Matching_Criteria]
        self._meta_data['attribute_registry'] = \
            {'tm:security:protected-servers:traffic-matching-criteria:traffic-matching-criteriastate':
                Traffic_Matching_Criteria}


class Traffic_Matching_Criteria(Resource):
    """BIG-IP® AFM® Traffic Matching Criteria resource"""

    def __init__(self, traffic_matching_criteria_s):
        super(Traffic_Matching_Criteria, self).__init__(traffic_matching_criteria_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:protected-servers:traffic-matching-criteria:traffic-matching-criteriastate'
        self._meta_data['required_creation_parameters'].update(('partition', ))


class Netflow_Protected_Server_s(Collection):
    """BIG-IP® AFM® Netflow Protected Server collection"""

    def __init__(self, protected_servers):
        super(Netflow_Protected_Server_s, self).__init__(protected_servers)
        self._meta_data['allowed_lazy_attributes'] = [Netflow_Protected_Server]
        self._meta_data['attribute_registry'] = \
            {'tm:security:protected-servers:netflow-protected-server:netflow-protected-serverstate':
                Netflow_Protected_Server}


class Netflow_Protected_Server(Resource):
    """BIG-IP® AFM® Netflow Protected Server resource"""

    def __init__(self, netflow_protected_server_s):
        super(Netflow_Protected_Server, self).__init__(netflow_protected_server_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:protected-servers:netflow-protected-server:netflow-protected-serverstate'
        self._meta_data['required_creation_parameters'].update(('name', 'trafficMatchingCriteria', 'partition'))
