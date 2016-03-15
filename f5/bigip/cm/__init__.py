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
"""BIG-IP cluster module

REST URI
    ``http://localhost/mgmt/tm/cm/``

GUI Path
    ``Device Management``

REST Kind
    ``tm:cm:*``
"""


from f5.bigip.cm.device import Devices
from f5.bigip.cm.device_group import Device_Groups
from f5.bigip.cm.traffic_group import Traffic_Groups
from f5.bigip.resource import OrganizingCollection


class Cm(OrganizingCollection):
    """BIG-IP Cluster Organizing Collection."""
    def __init__(self, bigip):
        super(Cm, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Devices, Device_Groups, Traffic_Groups,
        ]
