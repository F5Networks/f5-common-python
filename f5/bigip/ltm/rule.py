# Copyright 2014-2015 F5 Networks Inc.
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


class RuleCollection(Collection):
    def __init__(self, ltm):
        super(RuleCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Rule]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:rule:rulestate': Rule}


class Rule(Resource):
    def __init__(self, rule_collection):
        super(Rule, self).__init__(rule_collection)
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['required_creation_parameters'].update(
            ('name', 'partition', 'apiAnonymous'))

    def create(self, **kwargs):
        return self._create(**kwargs)

    def refresh(self):
        self._refresh()

    def load(self, **kwargs):
        return self._load(**kwargs)

    def update(self, **kwargs):
        self._update(**kwargs)

    def delete(self):
        self._delete()
