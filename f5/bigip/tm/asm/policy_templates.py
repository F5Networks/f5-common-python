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
#

"""BIG-IP® Application Security Manager™ (ASM®) module.

REST URI
    ``http://localhost/mgmt/tm/asm/policy-templates``

GUI Path
    ``Security -> Options -> Advanced Configuration -> Policy Templates``

REST Kind
    ``tm:asm:policy-templates:*``
"""

from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from f5.sdk_exception import UnsupportedOperation


class Policy_Templates_s(Collection):
    """BIG-IP® ASM Policiy Templates collection."""
    def __init__(self, asm):
        super(Policy_Templates_s, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Policy_Template]
        self._meta_data['attribute_registry'] = {
            'tm:asm:policy-templates:policy-templatestate': Policy_Template}


class Policy_Template(AsmResource):
    """BIG-IP® ASM Policy Template resource."""
    def __init__(self, policy_templates_s):
        super(Policy_Template, self).__init__(policy_templates_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:policy-templates:policy-templatestate'

    def create(self, **kwargs):
        """Create is not supported for Policy Template resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Policy Template resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )

    def modify(self, **patch):
        """Modify is not supported for Policy Template resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )
