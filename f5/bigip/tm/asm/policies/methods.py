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


class Methods_s(Collection):
    """BIG-IP® ASM Methods sub-collection."""
    def __init__(self, policy):
        super(Methods_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Method]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:methods:methodcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:methods:methodstate': Method
        }


class Method(AsmResource):
    """BIG-IP® ASM Methods Resource."""
    def __init__(self, methods_s):
        super(Method, self).__init__(methods_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:methods:methodstate'
