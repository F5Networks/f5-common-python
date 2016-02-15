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
from f5.bigip.ltm.monitor import Monitor
from f5.bigip.ltm.nat import NATs
from f5.bigip.ltm.policy import Policys
from f5.bigip.ltm.pool import Pools
from f5.bigip.ltm.rule import Rules
from f5.bigip.ltm.snat import SNATs
from f5.bigip.ltm.virtual import Virtuals
from f5.bigip.resource import OrganizingCollection


class LTM(OrganizingCollection):
    def __init__(self, bigip):
        super(LTM, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Monitor,
            NATs,
            Policys,
            Pools,
            Rules,
            SNATs,
            Virtuals
        ]
