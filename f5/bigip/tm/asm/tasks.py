# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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
    ``http://localhost/mgmt/tm/asm/``

GUI Path
    ``Security``

REST Kind
    ``tm:asm:*``
"""

from f5.bigip.resource import AsmResource
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.sdk_exception import UnsupportedMethod


class Tasks(OrganizingCollection):
    """BIG-IP® ASM Tasks organizing collection."""

    def __init__(self, asm):
        super(Tasks, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Check_Signatures_s
            ]


class Check_Signatures_s(Collection):
    """BIG-IP® ASM Tasks Check Signatures Collection.

    This object is not a collection strictly speaking, although in version
    11.x, the object has collection kind:

    tm:asm:tasks:check-signatures:check-signatures-taskcollectionstate

    In version 12.x however this kind is set to:
    tm:asm:tasks:check-signatures:check-signatures-taskstate

    This should not affect in the way this object works, so we will make it
    a collection arbitrarily.
    """

    def __init__(self, tasks):
        super(Check_Signatures_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Check_Signature]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:check-signatures:check-signatures-taskstate':
                Check_Signature}


class Check_Signature(AsmResource):
    """BIG-IP® ASM Tasks Check Signature Resource


        To create this resource on the ASM, one must utilize fetch() method
        from AsmResource class, create() is not supported.
    """
    def __init__(self, check_signatures_s):
        super(Check_Signature, self).__init__(check_signatures_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:tasks:check-signatures:check-signatures-taskstate'

    def create(self, **kwargs):
        """Create is not supported for Check Signature

                :raises: UnsupportedOperation
        """
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for Check Signature

                :raises: UnsupportedOperation
        """
        raise UnsupportedMethod(
            "%s does not support the modify method" % self.__class__.__name__
        )
