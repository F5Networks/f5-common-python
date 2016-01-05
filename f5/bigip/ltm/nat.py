# Copyright 2014 F5 Networks Inc.
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
from f5.bigip.resource import CollectionResource
from f5.bigip.resource import CRUDResource
from f5.bigip.resource import KindTypeMismatchException


class NATCollection(CollectionResource):
    def __init__(self, ltm):
        super(NATCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [NAT]


class NAT(CRUDResource):
    def __init__(self, nat_collection):
        super(NAT, self).__init__(nat_collection)
        self._meta_data['allowed_lazy_attributes'] = []

    def create(self, **kwargs):
        self._create(**kwargs)
        if not self.kind == 'tm:ltm:nat:natstate':
            error_message = "For instances of type 'NAT' the corresponding" +\
                " kind must be 'tm:ltm:nat:natstate' but creation returned" +\
                " JSON with kind: %r" % self.kind
            raise KindTypeMismatchException(error_message)
