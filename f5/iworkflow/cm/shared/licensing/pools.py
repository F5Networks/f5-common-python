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

"""iWorkflow® License pool module.

REST URI
    ``http://localhost/mgmt/cm/shared/licensing/pools``

GUI Path
    ``Device Management --> License Management``

REST Kind
    ``cm:shared:licensing:pools:licensepoolworkercollectionstate:*``
"""

from f5.iworkflow.resource import Collection
from f5.iworkflow.resource import Resource


class Pools_s(Collection):
    """iWorkflow® License pool collection"""
    def __init__(self, licensing):
        super(Pools_s, self).__init__(licensing)
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolworkercollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolworkerstate': Pool
        }


class Pool(Resource):
    """iWorkflow® License pool resource"""
    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_creation_parameters'] = set(('baseRegKey',))
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolworkerstate'
