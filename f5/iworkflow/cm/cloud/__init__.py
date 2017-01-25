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
"""Classes and functions for configuring iWorkflow"""

from f5.iworkflow.cm.cloud.connectors import Connectors
from f5.iworkflow.cm.cloud.provider import Provider
from f5.iworkflow.cm.cloud.tasks import Configure_Device_Nodes
from f5.iworkflow.cm.cloud.templates import Templates
from f5.iworkflow.cm.cloud.tenants import Tenants_s
from f5.iworkflow.resource import OrganizingCollection


class Cloud(OrganizingCollection):
    def __init__(self, cm):
        super(Cloud, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [
            Configure_Device_Nodes,
            Connectors,
            Provider,
            Templates,
            Tenants_s
        ]
