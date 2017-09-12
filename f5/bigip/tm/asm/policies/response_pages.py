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


class Response_Pages_s(Collection):
    """BIG-IP® ASM Response Pages sub-collection."""
    def __init__(self, policy):
        super(Response_Pages_s, self).__init__(policy)
        self._meta_data['object_has_stats'] = False
        self._meta_data['minimum_version'] = '11.6.0'
        self._meta_data['allowed_lazy_attributes'] = [Response_Page]
        self._meta_data['required_json_kind'] = 'tm:asm:policies:response-pages:response-pagecollectionstate'
        self._meta_data['attribute_registry'] = {
            'tm:asm:policies:response-pages:response-pagestate': Response_Page
        }


class Response_Page(AsmResource):
    """BIG-IP® ASM Response Page resource."""
    def __init__(self, response_pages_s):
        super(Response_Page, self).__init__(response_pages_s)
        self._meta_data['required_json_kind'] = 'tm:asm:policies:response-pages:response-pagestate'

    def create(self, **kwargs):
        """Create is not supported for Response Page resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Response Page resources

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )
