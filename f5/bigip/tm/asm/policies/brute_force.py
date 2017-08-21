# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection


class Brute_Force_Attack_Preventions_s(Collection):
    """BIG-IP® ASM Brute Force Attack Preventions sub-collection."""
    def __init__(self, policy):
        super(Brute_Force_Attack_Preventions_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Brute_Force_Attack_Prevention]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventioncollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventionstate': Brute_Force_Attack_Prevention
        }


class Brute_Force_Attack_Prevention(AsmResource):
    """BIG-IP® ASM Brute Force Attack Prevention Resource."""
    def __init__(self, brute_force_attack_preventions_s):
        super(Brute_Force_Attack_Prevention, self).__init__(
            brute_force_attack_preventions_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventionstate'
        self._meta_data['required_creation_parameters'] = {'urlReference'}
