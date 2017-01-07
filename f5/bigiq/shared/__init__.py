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

"""

REST URI
    ``http://localhost/mgmt/shared/resolver/``

GUI Path
    ``Device Management --> Inventory``

REST Kind
    N/A -- HTTP GET returns an error
"""

from f5.bigiq.resource import OrganizingCollection
from f5.bigiq.shared.resolver import Resolver


class Shared(OrganizingCollection):
    def __init__(self, bigiq):
        super(Shared, self).__init__(bigiq)
        self._meta_data['allowed_lazy_attributes'] = [
            Resolver
        ]
