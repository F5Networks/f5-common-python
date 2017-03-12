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

"""iWorkflow® tenants module

REST URI
    ``http://localhost/mgmt/cm/cloud/tenants``

GUI Path
    ``Clouds and Services --> Tenants``

REST Kind
    ``cm:cloud:tenants:*``
"""

from f5.iworkflow.resource import Collection
from f5.iworkflow.resource import Resource


class Tenants_s(Collection):
    def __init__(self, cloud):
        super(Tenants_s, self).__init__(cloud)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:tenants:tenantcollectionworkerstate'
        self._meta_data['allowed_lazy_attributes'] = [Tenant]
        self._meta_data['attribute_registry'] = {
            'cm:cloud:tenants:tenantworkerstate': Tenant
        }


class Tenant(Resource):
    def __init__(self, tenants_s):
        super(Tenant, self).__init__(tenants_s)
        self._meta_data['required_creation_parameters'] = {'name', }
        self._meta_data['required_load_parameters'] = {'name', }
        self._meta_data['required_json_kind'] = \
            'cm:cloud:tenants:tenantworkerstate'
