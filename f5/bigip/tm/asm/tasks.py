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

"""BIG-IP® Application Security Manager™ (ASM®) tasks sub-module.

REST URI
    ``http://localhost/mgmt/tm/asm/tasks/``

GUI Path
    ``Security``

REST Kind
    ``tm:asm:tasks:``
"""
from f5.bigip.resource import AsmResource
from f5.bigip.resource import AsmTaskResource
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.sdk_exception import F5SDKError
from f5.sdk_exception import RequiredOneOf
from f5.sdk_exception import UnsupportedOperation
from six import iterkeys


class Tasks(OrganizingCollection):
    """BIG-IP® ASM Tasks organizing collection."""
    def __init__(self, asm):
        super(Tasks, self).__init__(asm)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [
            Apply_Policy_s,
            Check_Signatures_s,
            Export_Policy_s,
            Export_Signatures_s,
            Import_Policy_s,
            Import_Vulnerabilities_s,
            Update_Signatures_s,
        ]


class Apply_Policy_s(Collection):
    """BIG-IP® ASM Apply Policy Collection."""
    def __init__(self, tasks):
        super(Apply_Policy_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Apply_Policy]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:apply-policy:apply-policy-taskstate': Apply_Policy}


class Apply_Policy(AsmResource):
    """BIG-IP® ASM Apply Policy Resource."""
    def __init__(self, apply_policy_s):
        super(Apply_Policy, self).__init__(apply_policy_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        self._meta_data['required_creation_parameters'] = {'policyReference', }

    def modify(self, **kwargs):
        """Modify is not supported for Apply Policy resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Export_Policy_s(Collection):
    """BIG-IP® ASM Export Policy Collection."""
    def __init__(self, tasks):
        super(Export_Policy_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Export_Policy]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:export-policy:export-policy-taskstate':
                Export_Policy}


class Export_Policy(AsmResource):
    """BIG-IP® ASM Export Policy Resource."""
    def __init__(self, export_policy_s):
        super(Export_Policy, self).__init__(export_policy_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:tasks:export-policy:export-policy-taskstate'
        self._meta_data['required_creation_parameters'] = {
            'policyReference'}
        self._meta_data['exclusive_attributes'] = ['filename', 'inline']
        self._meta_data['minimum_additional_parameters'] = {'filename', 'inline'}

    def modify(self, **kwargs):
        """Modify is not supported for Apply Policy resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Import_Policy_s(Collection):
    """BIG-IP® ASM Import Policy Collection."""
    def __init__(self, tasks):
        super(Import_Policy_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Import_Policy]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:import-policy:import-policy-taskstate':
                Import_Policy}


class Import_Policy(AsmResource):
    """BIG-IP® ASM Import Policy Resource."""
    def __init__(self, import_policy_s):
        super(Import_Policy, self).__init__(import_policy_s)
        self._meta_data['required_json_kind'] = 'tm:asm:tasks:import-policy:import-policy-taskstate'
        self._meta_data['required_creation_parameters'] = set()
        self._meta_data['exclusive_attributes'] = ['filename', 'file']
        self._meta_data['minimum_additional_parameters'] = {'filename', 'file', 'policyTemplateReference'}

    def create(self, **kwargs):
        required_one_of = ['name', 'fullPath']
        has_any = [x for x in iterkeys(kwargs) if x in required_one_of]

        if 'partition' in kwargs and 'name' in kwargs and 'fullPath' not in kwargs:
            partition = kwargs.pop('partition', None)
            name = kwargs.pop('name', None)
            if partition is not None and not partition.startswith('/'):
                kwargs['fullPath'] = '/{0}/{1}'.format(partition, name)
            elif partition is None:
                raise F5SDKError(
                    "The partition name, if specified, cannot be none"
                )
            elif partition.startswith('/'):
                kwargs['fullPath'] = '{0}/{1}'.format(partition, name)

        if len(has_any) == 1:
            return self._create(**kwargs)

        raise RequiredOneOf(required_one_of)

    def modify(self, **kwargs):
        """Modify is not supported for Apply Policy resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Check_Signatures_s(Collection):
    """BIG-IP® ASM Tasks Check Signatures Collection."""
    def __init__(self, tasks):
        super(Check_Signatures_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['allowed_lazy_attributes'] = [Check_Signature]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:check-signatures:check-signatures-taskstate':
                Check_Signature}


class Check_Signature(AsmTaskResource):
    """BIG-IP® ASM Tasks Check Signature Resource


        To create this resource on the ASM, one must utilize fetch() method
        from AsmTaskResource class, create() is not supported.
    """
    def __init__(self, check_signatures_s):
        super(Check_Signature, self).__init__(check_signatures_s)
        self._meta_data['required_json_kind'] =\
            'tm:asm:tasks:check-signatures:check-signatures-taskstate'


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
        self._meta_data['required_creation_parameters'] = {'filename', }

    def modify(self, **kwargs):
        """Modify is not supported for Export Signature resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Update_Signatures_s(Collection):
    """BIG-IP® ASM Tasks Update Signatures Collection."""
    def __init__(self, tasks):
        super(Update_Signatures_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '12.0.0'
        self._meta_data['allowed_lazy_attributes'] = [Update_Signature]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:update-signatures:update-signatures-taskstate': Update_Signature
        }


class Update_Signature(AsmTaskResource):
    """BIG-IP® ASM Tasks Update Signature Resource resource

        To create this resource on the ASM, one must utilize fetch() method
        from AsmTaskResource class, create() is not supported.
    """
    def __init__(self, update_signatures_s):
        super(Update_Signature, self).__init__(update_signatures_s)
        self._meta_data['minimum_version'] = '12.0.0'
        self._meta_data['required_json_kind'] = 'tm:asm:tasks:update-signatures:update-signatures-taskstate'


class Import_Vulnerabilities_s(Collection):
    """BIG-IP® ASM Import Vulnerabilities Collection."""
    def __init__(self, tasks):
        super(Import_Vulnerabilities_s, self).__init__(tasks)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Import_Vulnerabilities]
        self._meta_data['attribute_registry'] = {
            'tm:asm:tasks:import-vulnerabilities:'
            'import-vulnerabilities-taskstate': Import_Vulnerabilities}


class Import_Vulnerabilities(AsmResource):
    """BIG-IP® ASM Import Vulnerabilities Resource."""
    def __init__(self, import_vulnerabilities_s):
        super(Import_Vulnerabilities, self).__init__(import_vulnerabilities_s)
        self._meta_data['required_json_kind'] = \
            'tm:asm:tasks:import-vulnerabilities:' \
            'import-vulnerabilities-taskstate'
        self._meta_data['required_creation_parameters'] = {
            'policyReference', 'filename'}
        self._meta_data['minimum_additional_parameters'] = {
            'onlyGetDomainNames', 'importAllDomainNames', 'domainNames'}

    def modify(self, **kwargs):
        """Modify is not supported for Import Vulnerabilities resource

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )
