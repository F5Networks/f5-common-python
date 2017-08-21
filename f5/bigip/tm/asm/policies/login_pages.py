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


class Login_Pages_s(Collection):
    """BIG-IP® ASM Login Pages sub-collection."""
    def __init__(self, policy):
        super(Login_Pages_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Login_Page]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:login-pages:login-pagecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:login-pages:login-pagestate': Login_Page
        }


class Login_Page(AsmResource):
    """BIG-IP® ASM Login Page Resource."""
    def __init__(self, login_pages_s):
        super(Login_Page, self).__init__(login_pages_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:login-pages:login-pagestate'
        self._meta_data['required_creation_parameters'] = {
            'accessValidation', 'urlReference'
        }
