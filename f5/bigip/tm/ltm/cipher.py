# coding=utf-8
#
#  Copyright 2021 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager™ (LTM®) cipher module.

REST URI
    ``http://localhost/mgmt/tm/ltm/cipher``

GUI Path
    ``Local Traffic --> Ciphers``

REST Kind
    ``tm:ltm:cipher:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Cipher(OrganizingCollection):
    """BIG-IP® LTM cipher collection"""
    def __init__(self, ltm):
        super(Cipher, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Rules,
            Groups
        ]


class Rules(Collection):
    """BIG-IP® cipher rule sub-collection"""
    def __init__(self, cipher):
        super(Rules, self).__init__(cipher)
        self._meta_data['allowed_lazy_attributes'] = [Rule]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:cipher:rule:rulestate': Rule}


class Rule(Resource):
    """BIG-IP® cipher rule sub-collection resource"""
    def __init__(self, rule_s):
        super(Rule, self).__init__(rule_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:cipher:rule:rulestate'


class Groups(Collection):
    """BIG-IP® cipher group sub-collection"""
    def __init__(self, cipher):
        super(Groups, self).__init__(cipher)
        self._meta_data['allowed_lazy_attributes'] = [Group]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:cipher:group:groupstate': Group}


class Group(Resource):
    """BIG-IP® cipher group sub-collection resource"""
    def __init__(self, group_s):
        super(Group, self).__init__(group_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:cipher:group:groupstate'
