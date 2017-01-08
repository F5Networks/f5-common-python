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
    ``http://localhost/mgmt/cm/device/licensing/pool/regkey``

REST Kind
    N/A -- HTTP GET returns an error
"""

from f5.bigiq.cm.device.licensing.pool.regkey.licenses import Licenses_s
from f5.bigiq.resource import OrganizingCollection


class Regkey(OrganizingCollection):
    def __init__(self, pool):
        super(Regkey, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [
            Licenses_s
        ]
