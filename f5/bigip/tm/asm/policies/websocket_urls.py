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


class Websocket_Urls_s(Collection):
    """BIG-IP® ASM Websocket Urls sub-collection."""
    def __init__(self, policy):
        super(Websocket_Urls_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '12.1.0'
        self._meta_data['allowed_lazy_attributes'] = [Websocket_Url]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:websocket-urls:websocket-urlcollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:websocket-urls:websocket-urlstate': Websocket_Url
        }


class Websocket_Url(AsmResource):
    """BIG-IP® ASM Websocket UrlResource."""
    def __init__(self, websocket_urls_s):
        super(Websocket_Url, self).__init__(websocket_urls_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:websocket-urls:websocket-urlstate'
        self._meta_data['required_creation_parameters'].update(
            ('checkPayload',)
        )

    def create(self, **kwargs):
        """Custom create method to accommodate different endpoint behavior."""
        self._check_create_parameters(**kwargs)
        if kwargs['checkPayload'] is True:
            self._meta_data['minimum_additional_parameters'] = {
                'allowTextMessage', 'allowJsonMessage', 'allowBinaryMessage'
            }
        if 'allowTextMessage' in kwargs:
            self._meta_data['required_creation_parameters'].update((
                'plainTextProfileReference',)
            )
        if 'allowJsonMessage' in kwargs:
            self._meta_data['required_creation_parameters'].update((
                'jsonProfileReference',)
            )
        return super(Websocket_Url, self)._create(**kwargs)
