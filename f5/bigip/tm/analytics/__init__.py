# coding=utf-8
#
# Copyright 2018 F5 Networks Inc.
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

"""BIG-IP® Application Visibility and Reporting™ (AVR®) module.

REST URI
    ``http://localhost/mgmt/tm/analytics/``

GUI Path
    ``Statistics --> Analytics``

REST Kind
    ``tm:analytics:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.analytics.dos_vis_common import Dos_Vis_Common
from f5.bigip.tm.analytics.protocol_inspection import Protocol_Inspection


class Analytics(OrganizingCollection):
    """BIG-IP® Application Visibility and Reporting (AVR) organizing

    collection.
    """

    def __init__(self, tm):
        super(Analytics, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Dos_Vis_Common,
            Protocol_Inspection
        ]
