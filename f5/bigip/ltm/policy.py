# Copyright 2014-2016 F5 Networks Inc.
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

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class PolicyCollection(Collection):
    def __init__(self, ltm):
        super(PolicyCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:policystate': Policy}


class Policy(Resource):
    def __init__(self, policy_collection):
        super(Policy, self).__init__(policy_collection)
        self._meta_data['required_json_kind'] = 'tm:ltm:policy:policystate'
        self._meta_data['required_creation_parameters'].update(('strategy',))
        temp = {'tm:ltm:policy:rules:rulescollectionstate': RulesCollection}
        self._meta_data['attribute_registry'] = temp


class RulesCollection(Collection):
    def __init__(self, policy):
        super(RulesCollection, self).__init__(policy)
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:policy:rules:rulesstate': Rules}
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:rulescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Rules]


class Rules(Resource):
    def __init__(self, rules_collection):
        super(Rules, self).__init__(rules_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:rulesstate'
        self._meta_data['allowed_lazy_attributes'] =\
            [ActionsCollection, ConditionsCollection]


class ActionsCollection(Collection):
    def __init__(self, rules):
        super(ActionsCollection, self).__init__(rules)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:actions:actionscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Actions]


class Actions(Resource):
    def __init__(self, actions_collection):
        super(Actions, self).__init__(actions_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:actions:actionsstate'


class ConditionsCollection(Collection):
    def __init__(self, rules):
        super(ConditionsCollection, self).__init__(rules)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:conditions:conditionscollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Conditions]


class Conditions(Resource):
    def __init__(self, conditions_collection):
        super(Conditions, self).__init__(conditions_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:policy:rules:conditions:conditionsstate'
