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


class Signature_Sets_s(Collection):
    """BIG-IP® ASM Signature-Sets sub-collection."""
    def __init__(self, policy):
        super(Signature_Sets_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Signature_Set]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:signature-sets:signature-setcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:signature-sets:signature-setstate': Signature_Set
        }


class Signature_Set(AsmResource):
    """BIG-IP® ASM Signature-Sets resource."""
    def __init__(self, signature_sets_s):
        super(Signature_Set, self).__init__(signature_sets_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:signature-sets:signature-setstate'
        self._meta_data['required_creation_parameters'] = {
            'signatureSetReference',
        }
