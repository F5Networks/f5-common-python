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


class Sensitive_Parameters_s(Collection):
    """BIG-IP® ASM Sensitive Parameters sub-collection."""
    def __init__(self, policy):
        super(Sensitive_Parameters_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Sensitive_Parameter]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:sensitive-parameters:sensitive-parametercollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:sensitive-parameters:sensitive-parameterstate': Sensitive_Parameter
        }


class Sensitive_Parameter(AsmResource):
    """BIG-IP® ASM Sensitive Parameters Resource."""
    def __init__(self, sensitive_parameters_s):
        super(Sensitive_Parameter, self).__init__(sensitive_parameters_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:sensitive-parameters:sensitive-parameterstate'

    def modify(self, **kwargs):
        """Modify is not supported for Sensitive Parameters resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )
