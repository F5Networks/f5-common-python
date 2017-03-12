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
    ``http://localhost/mgmt/cm/cloud/tasks/configure-device-node``

REST Kind
    ``cm:cloud:tasks:configure-device-node:*``
"""

from f5.bigiq.resource import Collection
from f5.bigiq.resource import OrganizingCollection
from f5.bigiq.resource import TaskResource


class Tasks(OrganizingCollection):
    def __init__(self, cloud):
        super(Tasks, self).__init__(cloud)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Configure_Device_Nodes
        ]


class Configure_Device_Nodes(Collection):
    def __init__(self, tasks):
        super(Configure_Device_Nodes, self).__init__(tasks)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:tasks:configure-device-node:configdevicenodetaskcollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Configure_Device_Node]
        self._meta_data['attribute_registry'] = {
            'cm:cloud:tasks:configure-device-node:configdevicenodetaskstate':
                Configure_Device_Node
        }


class Configure_Device_Node(TaskResource):
    def __init__(self, nodes):
        super(Configure_Device_Node, self).__init__(nodes)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:tasks:configure-device-node:configdevicenodetaskstate'
        self._meta_data['required_load_parameters'] = {'id', }


class Reset_Devices(Collection):
    def __init__(self, tasks):
        super(Reset_Devices, self).__init__(tasks)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:tasks:reset-device:resetdeviceconfigtaskcollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Reset_Device]
        self._meta_data['attribute_registry'] = {
            'cm:cloud:tasks:reset-device:resetdeviceconfigtaskstate':
                Reset_Device
        }


class Reset_Device(TaskResource):
    def __init__(self, resets):
        super(Reset_Device, self).__init__(resets)
        self._meta_data['required_json_kind'] = \
            'cm:cloud:tasks:reset-device:resetdeviceconfigtaskstate'
        self._meta_data['required_load_parameters'] = {'id', }
        self._meta_data['required_creation_parameters'] = {'deviceUUID', }
