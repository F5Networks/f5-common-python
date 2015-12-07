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

from f5.bigip.ltm.monitor import Monitor
from f5.bigip.ltm.nat import NAT
from f5.bigip.ltm.pool import Pool
from f5.bigip.ltm.rule import Rule
from f5.bigip.ltm.snat import SNAT
from f5.bigip.ltm.ssl import SSL
from f5.bigip.ltm.virtual_server import VirtualServer

base_uri = 'ltm/'


class LTM(object):
    def __init__(self, bigip):
        self.collections = {}
        self.bigip = bigip

    @property
    def monitor(self):
        if 'monitor' in self.collections:
            return self.collections['monitor']
        else:
            monitor = Monitor(self.bigip)
            self.collections['monitor'] = monitor
            return monitor

    @property
    def nat(self):
        if 'nat' in self.collections:
            return self.collections['nat']
        else:
            nat = NAT(self.bigip)
            self.collections['nat'] = nat
            return nat

    @property
    def pool(self):
        if 'pool' in self.collections:
            return self.collections['pool']
        else:
            pool = Pool(self.bigip)
            self.collections['pool'] = pool
            return pool

    @property
    def rule(self):
        if 'rule' in self.collections:
            return self.collections['rule']
        else:
            rule = Rule(self.bigip)
            self.collections['rule'] = rule
            return rule

    @property
    def snat(self):
        if 'snat' in self.collections:
            return self.collections['snat']
        else:
            snat = SNAT(self.bigip)
            self.collections['snat'] = snat
            return snat

    @property
    def ssl(self):
        if 'ssl' in self.collections:
            return self.collections['ssl']
        else:
            ssl = SSL(self.bigip)
            self.collections['ssl'] = ssl
            return ssl

    @property
    def vs(self):
        if 'virtual_server' in self.collections:
            return self.collections['virtual_server']
        else:
            vs = VirtualServer(self.bigip)
            self.collections['virtual_server'] = vs
            return vs
