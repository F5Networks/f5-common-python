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


class Plain_Text_Profiles_s(Collection):
    """BIG-IP® ASM Plain Text Profiles sub-collection."""
    def __init__(self, policy):
        super(Plain_Text_Profiles_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '12.1.0'
        self._meta_data['allowed_lazy_attributes'] = [Plain_Text_Profile]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:plain-text-profiles:plain-text-profilecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:plain-text-profiles:plain-text-profilestate': Plain_Text_Profile
        }


class Plain_Text_Profile(AsmResource):
    """BIG-IP® ASM Plain Text Profile Resource."""
    def __init__(self, plain_text_profiles_s):
        super(Plain_Text_Profile, self).__init__(plain_text_profiles_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:plain-text-profiles:plain-text-profilestate'
