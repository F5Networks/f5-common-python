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

"""iWorkflow® Shared (shared) module

REST URI
    ``http://localhost/mgmt/cm/shared/``

GUI Path
    ``Device Management --> License Management``

REST Kind
    N/A -- HTTP GET returns an error
"""

from f5.iworkflow.cm.shared.licensing import Licensing
from f5.iworkflow.resource import OrganizingCollection


class Shared(OrganizingCollection):
    """An organizing collection for Shared resources."""
    def __init__(self, cm):
        super(Shared, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [
            Licensing
        ]
