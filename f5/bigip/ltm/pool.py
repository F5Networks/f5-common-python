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

from f5.bigip.resource import Collection
from f5.bigip.resource import CRLUD


class PoolCollection(Collection):
    def __init__(self, ltm):
        super(PoolCollection, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:pool:poolstate': Pool}


class Pool(CRLUD):
    def __init__(self, pool_collection):
        super(Pool, self).__init__(pool_collection)
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['required_json_kind'] = 'tm:ltm:pool:poolstate'
