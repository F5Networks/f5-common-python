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


class History_Revisions_s(Collection):
    """BIG-IP® ASM History Revisions sub-collection."""
    def __init__(self, policy):
        super(History_Revisions_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [History_Revision]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:history-revisions:history-revisioncollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:history-revisions:history-revisionstate': History_Revision
        }


class History_Revision(AsmResource):
    """BIG-IP® ASM History Revision resource."""
    def __init__(self, history_revisions_s):
        super(History_Revision, self).__init__(history_revisions_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:history-revisions:history-revisionstate'

    def create(self, **kwargs):
        """Create is not supported for History Revision resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for History Revision resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for History Revision resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )
