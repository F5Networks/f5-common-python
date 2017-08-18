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
from f5.sdk_exception import InvalidName


class Headers_s(Collection):
    """BIG-IP® ASM Headers sub-collection."""
    def __init__(self, policy):
        super(Headers_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Header]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:headers:headercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:headers:headerstate': Header
        }


class Header(AsmResource):
    """BIG-IP® ASM Headers resource

    It should be noted that this Resource will cast everything to lowercase on the
    BIG-IP. Therefore, we require that you cast it before sending to the BIGIP.

    """
    def __init__(self, headers_s):
        super(Header, self).__init__(headers_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policies:headers:headerstate'

    def create(self, **kwargs):
        if 'name' in 'kwargs':
            if kwargs['name'] != kwargs['name'].lower():
                raise InvalidName(
                    "The provided Header name must be lowercase"
                )
        return super(Header, self).create(**kwargs)

    def modify(self, **kwargs):
        if 'name' in 'kwargs':
            if kwargs['name'] != kwargs['name'].lower():
                raise InvalidName(
                    "The provided Header name must be lowercase"
                )
        return super(Header, self).modify(**kwargs)

    def update(self, **kwargs):
        if 'name' in 'kwargs':
            if kwargs['name'] != kwargs['name'].lower():
                raise InvalidName(
                    "The provided Header name must be lowercase"
                )
        return super(Header, self).update(**kwargs)

    def delete(self, **kwargs):
        if 'name' in 'kwargs':
            if kwargs['name'] != kwargs['name'].lower():
                raise InvalidName(
                    "The provided Header name must be lowercase"
                )
        return super(Header, self).delete(**kwargs)

    def load(self, **kwargs):
        if 'name' in 'kwargs':
            if kwargs['name'] != kwargs['name'].lower():
                raise InvalidName(
                    "The provided Header name must be lowercase"
                )
        return super(Header, self).load(**kwargs)
