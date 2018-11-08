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
    ``http://localhost/mgmt/tm/security/flowspec-route-injector``

GUI Path
    ``Security --> Option --> Network Firewall -->  External Redirection
    --> Flowspec Route Injector``

REST Kind
    ``tm:security:flowspec-route-injector:flowspec-route-injectorcollectionstate:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Flowspec_Route_Injector(OrganizingCollection):
    """BIG-IP® AFM® Flowspec Route Injector organizing collection."""

    def __init__(self, security):
        super(Flowspec_Route_Injector, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [Profile_s]


class Profile_s(Collection):
    """BIG-IP® AFM® Flowspec Route Injector Profile collection"""

    def __init__(self, flowspec_route_injector):
        super(Profile_s, self).__init__(flowspec_route_injector)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = \
            {'tm:security:flowspec-route-injector:profile:profilestate':
                Profile}


class Profile(Resource):
    """BIG-IP® AFM® Flowspec Route Injector Profile resource"""

    def __init__(self, profile_s):
        super(Profile, self).__init__(profile_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:flowspec-route-injector:profile:profilestate'
        self._meta_data['required_creation_parameters'].update(('partition', 'name', 'routeDomain', 'neighbor'))
        self._meta_data['required_load_parameters'].update(('partition', 'name'))
        self._meta_data['allowed_lazy_attributes'] = [Neighbor_s]
        self._meta_data['attribute_registry'] = \
            {'tm:security:flowspec-route-injector:profile:neighbor:neighborcollectionstate':
                Neighbor_s}


class Neighbor_s(Collection):
    """BIG-IP® AFM® Flowspec Route Injector Neighbor collection"""

    def __init__(self, profile):
        super(Neighbor_s, self).__init__(profile)
        self._meta_data['required_json_kind'] = \
            'tm:security:flowspec-route-injector:profile:neighbor:neighborcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Neighbor]
        self._meta_data['attribute_registry'] = \
            {'tm:security:flowspec-route-injector:profile:neighbor:neighborstate':
                Neighbor}


class Neighbor(Resource):
    """BIG-IP® AFM® Flowspec Route Injector Neighbor resource"""

    def __init__(self, neighbor_s):
        super(Neighbor, self).__init__(neighbor_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:flowspec-route-injector:profile:neighbor:neighborstate'
        self._meta_data['required_creation_parameters'].update(('name', 'local-address', 'local-as', 'remote-as'))
