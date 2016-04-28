# coding=utf-8
#
# Copyright 2015 F5 Networks Inc.
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

"""BIG-IP® System (sys) module

REST URI
    ``http://localhost/mgmt/tm/sys/``

GUI Path
    ``System``

REST Kind
    ``tm:sys:*``
"""

from f5.bigip.resource import OrganizingCollection
from f5.bigip.sys.application import Applications
from f5.bigip.sys.config import Config
from f5.bigip.sys.db import Dbs
from f5.bigip.sys.failover import Failover
from f5.bigip.sys.folder import Folders
from f5.bigip.sys.global_settings import Global_Settings
from f5.bigip.sys.ntp import Ntp
from f5.bigip.sys.dns import Dns
from f5.bigip.sys.performance import Performance


class Sys(OrganizingCollection):
    def __init__(self, bigip):
        super(Sys, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Config,
            Folders,
            Applications,
            Performance,
            Dbs,
            Global_Settings,
            Ntp,
            Dns,
            Failover,
        ]
