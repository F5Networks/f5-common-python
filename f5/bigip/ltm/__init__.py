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

from f5.common import constants as const
from f5.bigip.ltm.monitor import Monitor
from f5.bigip.ltm.nat import NAT
from f5.bigip.ltm.pool import Pool
from f5.bigip.ltm.rule import Rule
from f5.bigip.ltm.snat import SNAT
from f5.bigip.ltm.ssl import SSL
from f5.bigip.ltm.virtual_server import VirtualServer
from requests.exceptions import HTTPError

base_uri = 'ltm/'


class LTM(object):
    def __init__(self, bigip):
        self.collections = {}
        self.bigip = bigip
        self.base_uri = self.bigip.icr_uri + 'ltm/'

    def create_nat(self, name, translation_address, originating_address,
                   folder=const.DEFAULT_FOLDER, **kwargs):
        data = {
            'name': name,
            'partition': folder,
            'translationAddress': translation_address,
            'originatingAddress': originating_address,
        }
        data.update(kwargs)
        response = self.bigip.icr_session.post(
            self.base_uri + 'nat/', json=data)
        return NAT(self.bigip, response.json())

    def get_nats(self, folder=const.DEFAULT_FOLDER):
        params = {'$filter': 'partition eq ' + folder}
        try:
            response = self.bigip.icr_session.get(
                self.base_uri + 'nat/',
                params=params)
        except HTTPError as e:
            if e.response.status_code == 404:
                print e.response.text
                return []
            raise

        return [NAT(self.bigip, json_data=nat)
                for nat in response.json().get('items', [])]



    @property
    def monitor(self):
        if 'monitor' in self.collections:
            return self.collections['monitor']
        else:
            monitor = Monitor(self.bigip)
            self.collections['monitor'] = monitor
            return monitor

    '''
    @property
    def nat(self):
        if 'nat' in self.collections:
            return self.collections['nat']
        else:
            nat = NAT(self.bigip)
            self.collections['nat'] = nat
            return nat
    '''
    def nat(self, name, folder=const.DEFAULT_FOLDER):
        nat = NAT(self.bigip)
        nat.read(name, folder)
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
