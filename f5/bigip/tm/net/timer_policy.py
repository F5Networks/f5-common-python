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

"""Directory: net module: timer-policy.

REST URI
    ``https://localhost/mgmt/tm/net/timer-policy``

GUI Path
    ``Network --> Service Policies --> Timer Policies``

REST Kind
    ``tm:net:timer-policy:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Timer_Policys(Collection):
    def __init__(self, net):
        super(Timer_Policys, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Timer_Policy]
        self._meta_data['attribute_registry'] = {
            'tm:net:timer-policy:timer-policystate': Timer_Policy
        }


class Timer_Policy(Resource):
    def __init__(self, timer_policys):
        super(Timer_Policy, self).__init__(timer_policys)
        self._meta_data['required_json_kind'] = "tm:net:timer-policy:timer-policystate"
