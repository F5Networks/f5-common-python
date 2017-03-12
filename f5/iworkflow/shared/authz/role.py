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

"""

REST URI
    ``http://localhost/mgmt/cm/shared/authz/roles``

REST Kind
    ``shared:authz:roles:*``
"""

from f5.iworkflow.resource import Collection
from f5.iworkflow.resource import Resource


class Roles_s(Collection):
    def __init__(self, authz):
        super(Roles_s, self).__init__(authz)
        self._meta_data['required_json_kind'] = \
            'shared:authz:roles:rolescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Role]
        self._meta_data['attribute_registry'] = {
            'shared:authz:roles:rolesworkerstate': Role
        }


class Role(Resource):
    def __init__(self, roles_s):
        super(Role, self).__init__(roles_s)
        self._meta_data['required_load_parameters'] = {'name', }
        self._meta_data['required_creation_parameters'] = {'name', }
        self._meta_data['required_json_kind'] = \
            'shared:authz:roles:rolesworkerstate'
