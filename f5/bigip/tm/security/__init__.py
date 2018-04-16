# coding=utf-8
#
# Copyright 2015-2017 F5 Networks Inc.
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

"""BIG-IP® Security module.

REST URI
    ``http://localhost/mgmt/tm/security``

GUI Path
    ``Security``

REST Kind
    ``tm:security:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.security.analytics import Analytics
from f5.bigip.tm.security.dos import Dos
from f5.bigip.tm.security.firewall import Firewall
from f5.bigip.tm.security.log import Log
from f5.bigip.tm.security.protocol_inspection import Protocol_Inspection


class Security(OrganizingCollection):
    """BIG-IP® Security organizing collection."""

    def __init__(self, tm):
        super(Security, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Analytics,
            Dos,
            Firewall,
            Log,
            Protocol_Inspection,
        ]
