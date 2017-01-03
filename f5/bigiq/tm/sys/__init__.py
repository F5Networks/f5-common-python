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

"""BIG-IQ® System (sys) module

REST URI
    ``http://localhost/mgmt/tm/sys/``

GUI Path
    ``System``

REST Kind
    ``tm:sys:*``
"""

from f5.bigiq.resource import OrganizingCollection
from f5.bigiq.tm.sys.dns import Dns
from f5.bigiq.tm.sys.global_settings import Global_Settings
from f5.bigiq.tm.sys.httpd import Httpd
from f5.bigiq.tm.sys.software import Software
from f5.bigiq.tm.sys.sshd import Sshd


class Sys(OrganizingCollection):
    def __init__(self, tm):
        super(Sys, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Dns,
            Global_Settings,
            Httpd,
            Software,
            Sshd
        ]
