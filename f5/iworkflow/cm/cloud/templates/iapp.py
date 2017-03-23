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

"""iWorkflow® iApp templates

REST URI
    ``http://localhost/mgmt/cm/cloud/provider/templates/iapp``

REST Kind
    ``cm:cloud:provider:templates:iapp*``
"""

from f5.iworkflow.resource import Collection
from f5.iworkflow.resource import Resource


class Iapps(Collection):
    def __init__(self, templates):
        super(Iapps, self).__init__(templates)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:templates:iapp:iapptemplatecollectionworkerstate'
        self._meta_data['allowed_lazy_attributes'] = [
            Iapp
        ]
        self._meta_data['attribute_registry'] = {
            'cm:cloud:templates:iapp:iapptemplateitemstate': Iapp
        }


class Iapp(Resource):
    def __init__(self, iapps):
        super(Iapp, self).__init__(iapps)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:templates:iapp:iapptemplateitemstate'
        self._meta_data['required_load_parameters'] = {'name', }
