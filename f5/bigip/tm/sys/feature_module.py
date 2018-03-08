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

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import UnnamedResource
from f5.sdk_exception import UnsupportedOperation


class Feature_Module(OrganizingCollection):
    def __init__(self, feature_module):
        super(Feature_Module, self).__init__(feature_module)
        self._meta_data['allowed_lazy_attributes'] = [Cgnat]
        self._meta_data['attribute_registry'] = {'tm:sys:feature-module:feature-modulestate': Cgnat}


class Cgnat(UnnamedResource, ExclusiveAttributesMixin):
    def __init__(self, feature_module):
        super(Cgnat, self).__init__(feature_module)
        self._meta_data['required_json_kind'] = 'tm:sys:feature-module:feature-modulestate'
        self._meta_data['exclusive_attributes'].append(('enabled', 'disabled'))

    def _endis_attrs(self):
        if 'disabled' in self.__dict__:
            self.__dict__['enabled'] = not self.__dict__['disabled']
        if 'enabled' in self.__dict__:
            self.__dict__['disabled'] = not self.__dict__['enabled']
        return None

    def load(self, **kwargs):
        kwargs = self._reduce_boolean_pair(kwargs, 'enabled', 'disabled')
        newinst = self._stamp_out_core()
        newinst._refresh(**kwargs)
        newinst._endis_attrs()
        return newinst

    def refresh(self, **kwargs):
        kwargs = self._reduce_boolean_pair(kwargs, 'enabled', 'disabled')
        self._refresh(**kwargs)
        self._endis_attrs()
        return self

    def update(self, **kwargs):
        if 'enabled' in kwargs or 'disabled' in kwargs:
            self.__dict__.pop('enabled')
            self.__dict__.pop('disabled')
        self._update(**kwargs)
        self._endis_attrs()

    def modify(self, **kwargs):
        if 'enabled' in kwargs or 'disabled' in kwargs:
            self.__dict__.pop('enabled')
            self.__dict__.pop('disabled')
        self._modify(**kwargs)
        self._endis_attrs()

    def create(self, **kwargs):
        '''Create is not supported for db resources.

        :raises: UnsupportedOperation
        '''
        raise UnsupportedOperation(
            "Resource doesn't support create."
        )

    def delete(self, **kwargs):
        '''Delete is not supported for db resources.

        :raises: UnsupportedOperation
        '''
        raise UnsupportedOperation(
            "Resource doesn't support delete."
        )
