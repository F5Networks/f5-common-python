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
from f5.sdk_exception import UnsupportedOperation


class Suggestions_s(Collection):
    """BIG-IP® ASM Suggestions sub-collection."""
    def __init__(self, policy):
        super(Suggestions_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '12.0.0'
        self._meta_data['allowed_lazy_attributes'] = [Suggestion]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:suggestions:suggestioncollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:suggestions:suggestionstate': Suggestion
        }


class Suggestion(AsmResource):
    """BIG-IP® ASM Suggestions Resource."""
    def __init__(self, suggestions_s):
        super(Suggestion, self).__init__(suggestions_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:suggestions:suggestionstate'

    def create(self, **kwargs):
        """Modify is not supported for Suggestions resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )
