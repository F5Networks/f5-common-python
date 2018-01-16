# coding=utf-8
#
# Copyright 2018 F5 Networks Inc.
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

"""BIG-IP® SMTP Server module

REST URI
    ``http://localhost/mgmt/sys/smtp-server/``

GUI Path
    ``Systems > Configuration > Device > SMTP``

REST Kind
    ``tm:sys:smtp-server:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Smtp_Servers(Collection):
    def __init__(self, sys):
        super(Smtp_Servers, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Smtp_Server]
        self._meta_data['attribute_registry'] = {
            'tm:sys:smtp-server:smtp-serverstate': Smtp_Server
        }


class Smtp_Server(Resource, ExclusiveAttributesMixin):
    def __init__(self, smtp_servers):
        super(Smtp_Server, self).__init__(smtp_servers)
        self._meta_data['required_json_kind'] = 'tm:sys:smtp-server:smtp-serverstate'
        self._meta_data['exclusive_attributes'].append(('authenticationDisabled', 'authenticationEnabled'))

    def _endis_attrs(self):
        if 'authenticationDisabled' in self.__dict__:
            self.__dict__['authenticationEnabled'] = not self.__dict__['authenticationDisabled']
        if 'authenticationEnabled' in self.__dict__:
            self.__dict__['authenticationDisabled'] = not self.__dict__['authenticationEnabled']
        return None

    def create(self, **kwargs):
        inst = self._create(**kwargs)
        inst._endis_attrs()
        return inst

    def load(self, **kwargs):
        kwargs = self._reduce_boolean_pair(kwargs, 'authenticationEnabled', 'authenticationDisabled')
        inst = self._load(**kwargs)
        inst._endis_attrs()
        return inst

    def refresh(self, **kwargs):
        kwargs = self._reduce_boolean_pair(kwargs, 'authenticationEnabled', 'authenticationDisabled')
        self._refresh(**kwargs)
        self._endis_attrs()
        return self

    def update(self, **kwargs):
        if 'authenticationEnabled' in kwargs or 'authenticationDisabled' in kwargs:
            self.__dict__.pop('authenticationEnabled')
            self.__dict__.pop('authenticationDisabled')
        kwargs = self._reduce_boolean_pair(kwargs, 'authenticationEnabled', 'authenticationDisabled')
        self.__dict__ = self._reduce_boolean_pair(self.__dict__, 'authenticationEnabled', 'authenticationDisabled')
        self._update(**kwargs)
        self._endis_attrs()
