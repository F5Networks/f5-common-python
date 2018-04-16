# coding=utf-8
#
#  Copyright 2017 F5 Networks Inc.
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
    ``http://localhost/mgmt/tm/security/log``

GUI Path
    ``Security --> Log
    ``

REST Kind
    ``tm:security:log*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Log(OrganizingCollection):
    """BIG-IP® Log Organizing collection"""
    def __init__(self, security):
        super(Log, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Profiles,
        ]


class Profiles(Collection):
    """"BIG-IP® Log Profile collection"""
    def __init__(self, protocol_inspection):
        super(Profiles, self).__init__(protocol_inspection)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = \
            {'tm:security:log:profile:profilestate':
                Profile}


class Profile(Resource):
    """BIG-IP® Log Profile resource"""
    def __init__(self, profiles):
        super(Profile, self).__init__(profiles)
        self._meta_data['required_json_kind'] = \
            'tm:security:log:profile:profilestate'
        self._meta_data['required_creation_parameters'].update(('partition',))
