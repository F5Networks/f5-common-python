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
from f5.bigip.tm.asm.policies.parameters import Parameters_s


class Urls_s(Collection):
    """BIG-IP® ASM Urls sub-collection."""
    def __init__(self, policy):
        super(Urls_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Url]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:urls:urlcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:urls:urlstate': Url
        }


class Url(AsmResource):
    """BIG-IP® ASM Urls resource."""
    def __init__(self, urls_s):
        super(Url, self).__init__(urls_s)
        self._meta_data['allowed_lazy_attributes'] = [Parameters_s]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:urls:urlstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:urls:parameters:parametercollectionstate': Parameters_s
        }
