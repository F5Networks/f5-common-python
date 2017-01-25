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

from f5.iworkflow.resource import OrganizingCollection
from f5.iworkflow.shared.authz import Authz
from f5.iworkflow.shared.identified_devices import Identified_Devices
from f5.iworkflow.shared.resolver import Resolver
from f5.iworkflow.shared.system import System


class Shared(OrganizingCollection):
    """An organizing collection for shared resources."""
    def __init__(self, iworkflow):
        super(Shared, self).__init__(iworkflow)
        self._meta_data['allowed_lazy_attributes'] = [
            Authz,
            Identified_Devices,
            Resolver,
            System
        ]
