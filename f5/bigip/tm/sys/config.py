# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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
"""BIG-IP® system config module

REST URI
    ``http://localhost/mgmt/tm/sys/config``

GUI Path
    N/A

REST Kind
    ``tm:sys:config:*``
"""

from f5.bigip.mixins import UnnamedResourceMixin
from f5.bigip.resource import ResourceBase


class Config(UnnamedResourceMixin, ResourceBase):
    def __init__(self, sys):
        super(Config, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['attribute_registry'] = {}

    def update(self, **kwargs):
        '''Update is not supported for Config

        :raises: UnsupportedOperation
        '''
        raise self.UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__
        )

    def save(self):
        '''Save the configuration on the device. '''
        payload = {'command': 'save'}
        session = self._meta_data['bigip']._meta_data['icr_session']
        uri = self._meta_data['uri']
        response = session.post(uri, json=payload)
        self._local_update(response.json())
