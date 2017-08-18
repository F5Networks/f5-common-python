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


class Whitelist_Ips_s(Collection):
    """BIG-IP® ASM Whitelist-Ips sub-collection."""
    def __init__(self, policy):
        super(Whitelist_Ips_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Whitelist_Ip]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:whitelist-ips:whitelist-ipcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:whitelist-ips:whitelist-ipstate': Whitelist_Ip
        }


class Whitelist_Ip(AsmResource):
    """BIG-IP® ASM Whitelist-Ip resource."""
    def __init__(self, whitelist_ips_s):
        super(Whitelist_Ip, self).__init__(whitelist_ips_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        self._meta_data['read_only_attributes'] = ['ipMask']
        self._meta_data['required_creation_parameters'] = {'ipAddress', }
