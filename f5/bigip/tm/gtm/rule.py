# coding=utf-8
#
# Copyright 2014-2017 F5 Networks Inc.
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

"""BIG-IP® Global Traffic Manager (GTM) rule module.

REST URI
    ``http://localhost/mgmt/tm/gtm/rule``

GUI Path
    ``DNS --> GSLB : iRules``

REST Kind
    ``tm:gtm:rule:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Rules(Collection):
    """BIG-IP® GTM rule collection"""
    def __init__(self, gtm):
        super(Rules, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [Rule]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:rule:rulestate': Rule}


class Rule(Resource):
    """BIG-IP® GTM rule resource"""
    def __init__(self, rule_s):
        super(Rule, self).__init__(rule_s)
        self._meta_data['required_json_kind'] = 'tm:gtm:rule:rulestate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'partition', 'apiAnonymous'))
