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
    ``http://localhost/mgmt/tm/security/blacklist-publisher``

GUI Path
    ``Security --> Option --> Network Firewall -->  External Redirection
    --> Blacklist Publisher``

REST Kind
    ``tm:security:blacklist-publisher:blacklist-publishercollectionstate:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Blacklist_Publisher(OrganizingCollection):
    """BIG-IP® AFM® Blacklist Publisher organizing collection."""

    def __init__(self, security):
        super(Blacklist_Publisher, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Category_s,
            Profile_s]


class Category_s(Collection):
    """BIG-IP® AFM® Blacklist Publisher Category collection"""

    def __init__(self, blacklist_publisher):
        super(Category_s, self).__init__(blacklist_publisher)
        self._meta_data['allowed_lazy_attributes'] = [Category]
        self._meta_data['attribute_registry'] = \
            {'tm:security:blacklist-publisher:category:categorystate':
                Category}


class Category(Resource):
    """BIG-IP® AFM® Blacklist Publisher Category resource"""

    def __init__(self, category_s):
        super(Category, self).__init__(category_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:blacklist-publisher:category:categorystate'
        self._meta_data['required_creation_parameters'].update(('partition', 'name'))
        self._meta_data['required_load_parameters'].update(('partition', 'name'))


class Profile_s(Collection):
    """BIG-IP® AFM® Blacklist Publisher Profile collection"""

    def __init__(self, blacklist_publisher):
        super(Profile_s, self).__init__(blacklist_publisher)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = \
            {'tm:security:blacklist-publisher:profile:profilestate':
                Profile}


class Profile(Resource):
    """BIG-IP® AFM® Blacklist Publisher Profile resource"""

    def __init__(self, profile_s):
        super(Profile, self).__init__(profile_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:blacklist-publisher:profile:profilestate'
        self._meta_data['required_creation_parameters'].update(('partition', 'name'))
        self._meta_data['required_load_parameters'].update(('partition', 'name'))
