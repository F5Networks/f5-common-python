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

"""BIG-IQ® License (shared) module

REST URI
    ``http://localhost/mgmt/cm/shared/licensing/``

GUI Path
    ``Device Management --> License Management``

REST Kind
    N/A -- HTTP GET returns an error
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigiq.cm.shared.licensing.pool import Pools_s


class Licensing(OrganizingCollection):
    def __init__(self, bigip):
        super(Licensing, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Pools_s
        ]
