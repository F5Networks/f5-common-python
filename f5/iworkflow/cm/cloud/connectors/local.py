# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

"""iWorkflow® local cloud connector

REST URI
    ``http://localhost/mgmt/cm/cloud/connectors/local/``

REST Kind
    ``cm:cloud:connectors:*``
"""

from f5.iworkflow.resource import Collection
from f5.iworkflow.resource import Resource

# TODO(Implement device pointer)
# from f5.iworkflow.shared.resolver.device_groups.cm_cloud_managed_devices import Device  # NOQA


class Locals(Collection):
    def __init__(self, connectors):
        super(Locals, self).__init__(connectors)
        self._meta_data['allowed_lazy_attributes'] = [Local]
        self._meta_data['attribute_registry'] = {
            'cm:cloud:connectors:cloudconnectorstate': Local
        }


class Local(Resource):
    def __init__(self, locals):
        super(Local, self).__init__(locals)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:connectors:cloudconnectorstate'
        self._meta_data['required_creation_parameters'] = {'name', }
        self._meta_data['allowed_lazy_attributes'] = [Nodes_s]
        self._meta_data['attribute_registry'] = {'': Nodes_s}


class Nodes_s(Collection):
    def __init__(self, local):
        super(Nodes_s, self).__init__(local)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:nodes:nodecollection'
        self._meta_data['allowed_lazy_attributes'] = [Node]
        self._meta_data['attribute_registry'] = {
            'cm:cloud:nodes:node': Node
        }


class Node(Resource):
    def __init__(self, nodes):
        super(Node, self).__init__(nodes)
        self._meta_data['required_creation_parameters'] = set()
        self._meta_data['required_load_parameters'] = {'uuid', }
        self._meta_data['required_json_kind'] = \
            'cm:cloud:nodes:node'
