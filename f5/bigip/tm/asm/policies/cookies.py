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


class Cookies_s(Collection):
    """BIG-IP® ASM Cookies sub-collection."""
    def __init__(self, policy):
        super(Cookies_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Cookie]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:cookies:cookiecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:cookies:cookiestate': Cookie
        }


class Cookie(AsmResource):
    """BIG-IP® ASM Cookies Resource."""
    def __init__(self, cookies_s):
        super(Cookie, self).__init__(cookies_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:cookies:cookiestate'
