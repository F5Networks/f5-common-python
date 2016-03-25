# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager (LTM) policy module.

REST URI
    ``http://localhost/mgmt/tm/ltm/policy``

GUI Path
    ``Local Traffic --> policy``

REST Kind
    ``tm:ltm:policy:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Policys(Collection):
    """BIG-IP® LTM policy collection."""
    def __init__(self, ltm):
        super(Policys, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:policystate': Policy}


class Policy(Resource):
    """BIG-IP® LTM policy resource."""
    def __init__(self, policy_s):
        super(Policy, self).__init__(policy_s)
        self._meta_data['required_json_kind'] = 'tm:ltm:policy:policystate'
        self._meta_data['required_creation_parameters'].update(('strategy',))
        temp = {'tm:ltm:policy:rules:rulescollectionstate': Rules_s}
        self._meta_data['attribute_registry'] = temp


class Rules_s(Collection):
    """BIG-IP® LTM policy rules sub-collection."""
    def __init__(self, policy):
        super(Rules_s, self).__init__(policy)
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:rulesstate': Rules}
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:rulescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Rules]


class Rules(Resource):
    """BIG-IP® LTM policy rules sub-collection resource."""
    def __init__(self, rules_s):
        super(Rules, self).__init__(rules_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:rulesstate'
        temp = {'tm:ltm:policy:rules:actions:actionscollectionstate':
                Actions_s,
                'tm:ltm:policy:rules:conditions:conditionscollectionstate':
                Conditions_s}
        self._meta_data['attribute_registry'] = temp


class Actions_s(Collection):
    """BIG-IP® LTM policy actions sub-collection."""
    def __init__(self, rules):
        super(Actions_s, self).__init__(rules)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:actions:actionscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Actions]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:actions:actionsstate': Actions}


class Actions(Resource):
    """BIG-IP® LTM policy actions sub-collection resource."""
    def __init__(self, actions_s):
        super(Actions, self).__init__(actions_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:actions:actionsstate'


class Conditions_s(Collection):
    """BIG-IP® LTM policy conditions sub-collection."""
    def __init__(self, rules):
        super(Conditions_s, self).__init__(rules)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:conditions:conditionscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Conditions]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:conditions:conditionsstate': Conditions}


class Conditions(Resource):
    """BIG-IP® LTM policy conditions sub-collection resource."""
    def __init__(self, conditions_s):
        super(Conditions, self).__init__(conditions_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:conditions:conditionsstate'
