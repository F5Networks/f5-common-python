# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager™ (LTM®) module.

REST URI
    ``http://localhost/mgmt/tm/ltm/``

GUI Path
    ``Local Traffic``

REST Kind
    ``tm:ltm:*``
"""


from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.ltm.auth import Auth
from f5.bigip.tm.ltm.data_group import Data_Group
from f5.bigip.tm.ltm.ifile import Ifiles
from f5.bigip.tm.ltm.monitor import Monitor
from f5.bigip.tm.ltm.nat import Nats
from f5.bigip.tm.ltm.node import Nodes
from f5.bigip.tm.ltm.persistence import Persistence
from f5.bigip.tm.ltm.policy import Policys
from f5.bigip.tm.ltm.pool import Pools
from f5.bigip.tm.ltm.profile import Profile
from f5.bigip.tm.ltm.rule import Rules
from f5.bigip.tm.ltm.snat import Snats
from f5.bigip.tm.ltm.snat_translation import Snat_Translations
from f5.bigip.tm.ltm.snatpool import Snatpools
from f5.bigip.tm.ltm.traffic_class import Traffic_Class_s
from f5.bigip.tm.ltm.virtual import Virtuals
from f5.bigip.tm.ltm.virtual_address import Virtual_Address_s


class Ltm(OrganizingCollection):
    """BIG-IP® Local Traffic Manager (LTM) organizing collection."""
    def __init__(self, tm):
        super(Ltm, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Auth,
            Data_Group,
            Ifiles,
            Monitor,
            Nats,
            Nodes,
            Persistence,
            Policys,
            Pools,
            Profile,
            Rules,
            Snats,
            Snatpools,
            Snat_Translations,
            Traffic_Class_s,
            Virtuals,
            Virtual_Address_s,
        ]
