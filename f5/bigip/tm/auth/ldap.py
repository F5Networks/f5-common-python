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
    ``http://localhost/mgmt/tm/auth/ldap``

GUI Path
    ``System --> Users --> Authentication``

REST Kind
    ``tm:auth:ldap:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import InvalidName


class Ldaps(Collection):
    """BIG-IP® ldap server collection"""
    def __init__(self, auth):
        super(Ldaps, self).__init__(auth)
        self._meta_data['allowed_lazy_attributes'] = [Ldap]
        self._meta_data['attribute_registry'] = \
            {'tm:auth:ldap:ldapstate': Ldap}


class Ldap(Resource):
    """BIG-IP® ldap server resource"""
    def __init__(self, ldaps):
        super(Ldap, self).__init__(ldaps)
        self._meta_data['required_json_kind'] = 'tm:auth:ldap:ldapstate'

    def create(self, **kwargs):
        """name has to be system-auth, raise error if not named correctly"""
        if 'name' in kwargs:
            if kwargs['name'] != 'system-auth':
                raise InvalidName("Name must be 'system-auth'")
        return self._create(**kwargs)
