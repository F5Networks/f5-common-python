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


class Xml_Validation_Files_s(Collection):
    """BIG-IP® ASM Xml Validation Files sub-collection."""
    def __init__(self, policy):
        super(Xml_Validation_Files_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Xml_Validation_File]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:xml-validation-files:xml-validation-filecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:xml-validation-files:xml-validation-filestate': Xml_Validation_File
        }


class Xml_Validation_File(AsmResource):
    """BIG-IP® ASM Xml Validation File Resource."""
    def __init__(self, xml_validation_files_s):
        super(Xml_Validation_File, self).__init__(xml_validation_files_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:xml-validation-files:xml-validation-filestate'
        self._meta_data['required_creation_parameters'] = {
            'contents', 'fileName'
        }

    def modify(self, **kwargs):
        """Modify is not supported for Xml Validation File resource

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )
