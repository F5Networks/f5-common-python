# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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



class Signature_Statuses_s(Collection):
    """BIG-IP® ASM Signature Statuses collection."""
    def __init__(self, asm):
        super(Signature_Statuses_s, self).__init__(asm)
        self._meta_data['allowed_lazy_attributes'] = [Client_Ssl]
        self._meta_data['attribute_registry'] = \
        {'tm:ltm:profile:client-ssl:client-sslstate': Client_Ssl}

class Signature_Status(Resource):
    """BIG-IP® ASM Signature Statuses resource"""

    def __init__(self, signature_statuses_s):
        super(Signature_Status, self).__init__(signature_statuses_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:profile:client-ssl:client-sslstate'