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
from f5.bigip.resource import UnsupportedOperation


class Tasks(OrganizingCollection):
    """BIG-IP® ASM Tasks organizing collection."""
    def __init__(self, asm):
        super(Tasks, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Check_Signatures_s,
            Export_Signatures_s,
            Update_Signatures_s,
            ]


class Check_Signatures_s(Collection):
    """BIG-IP® ASM Tasks Check Signatures Collection."""
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
        """Create is not supported for Check Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for Check Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Export_Signatures_s(Collection):
    """BIG-IP® ASM Tasks Export Signatures Collection."""
    def __init__(self, tasks):
        super(Export_Signatures_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Export_Signature]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:export-signatures:export-signatures-taskstate':
                Export_Signature}


class Export_Signature(AsmResource):
    """BIG-IP® ASM Tasks Export Signature Resource"""
    def __init__(self, export_signatures_s):
        super(Export_Signature, self).__init__(export_signatures_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        self._meta_data['required_load_parameters'] = set(('id',))
        self._meta_data['required_creation_parameters'] = set(('filename',))

    def modify(self, **kwargs):
        """Modify is not supported for Export Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def fetch(self):
        """Fetch is not supported for Export Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )


class Update_Signatures_s(Collection):
    """BIG-IP® ASM Tasks Update Signatures Collection."""
    def __init__(self, tasks):
        super(Update_Signatures_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Update_Signature]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:update-signatures:update-signatures-taskstate':
                Update_Signature}


class Update_Signature(AsmResource):
    """BIG-IP® ASM Tasks Update Signature Resource resource


        To create this resource on the ASM, one must utilize fetch() method
        from AsmResource class, create() is not supported.
    """
    def __init__(self, update_signatures_s):
        super(Update_Signature, self).__init__(update_signatures_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:tasks:update-signatures:update-signatures-taskstate'

    def create(self, **kwargs):
        """Create is not supported for Update Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for Update Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )
