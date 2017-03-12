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
    ``http://localhost/mgmt/cm/asm/tasks/declare-mgmt-authority``

REST Kind
    ``cm:device:licensing:pool:regkey:licenses:*``
"""

from f5.bigiq.resource import Collection
from f5.bigiq.resource import OrganizingCollection
from f5.bigiq.resource import TaskResource


class Tasks(OrganizingCollection):
    def __init__(self, asm):
        super(Tasks, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Declare_Mgmt_Authority_s
        ]


class Declare_Mgmt_Authority_s(Collection):
    def __init__(self, tasks):
        super(Declare_Mgmt_Authority_s, self).__init__(tasks)
        self._meta_data['required_json_kind'] = \
            'cm:asm:tasks:declare-mgmt-authority:dmataskcollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Declare_Mgmt_Authority]
        self._meta_data['attribute_registry'] = {
            'cm:asm:tasks:declare-mgmt-authority:dmataskitemstate':
                Declare_Mgmt_Authority
        }


class Declare_Mgmt_Authority(TaskResource):
    def __init__(self, authorities):
        super(Declare_Mgmt_Authority, self).__init__(authorities)
        self._meta_data['required_json_kind'] = \
            'cm:asm:tasks:declare-mgmt-authority:dmataskitemstate'
        self._meta_data['required_load_parameters'] = {'id', }
