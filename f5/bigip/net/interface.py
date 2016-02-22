# Copyright 2014-2016 F5 Networks Inc.
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
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnsupportedOperation


class Interfaces(Collection):
    def __init__(self, net):
        super(Interfaces, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [Interface]
        self._meta_data['attribute_registry'] = {
            'tm:net:interface:interfacestate': Interface
        }


class Interface(Resource, ExclusiveAttributesMixin):
    def __init__(self, interface_s):
        super(Interface, self).__init__(interface_s)
        self._meta_data['required_json_kind'] =\
            'tm:net:interface:interfacestate'
        self._meta_data['exclusive_attributes'].append(('enabled', 'disabled'))

    def create(self, **kwargs):
        raise UnsupportedOperation(
            "BigIP interfaces cannot be created by users")

    def delete(self):
        raise UnsupportedOperation(
            "BigIP interfaces cannot be deleted by users")
