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

"""BIG-IP® system folder (partition) module

REST URI
    ``http://localhost/mgmt/tm/sys/folder``

GUI Path
    ``System --> Users --> Partition List``

REST Kind
    ``tm:auth:partition:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Partitions(Collection):
    def __init__(self, auth):
        super(Partitions, self).__init__(auth)
        self._meta_data['required_json_kind'] = \
            'tm:auth:partition:partitioncollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Partition]
        self._meta_data['attribute_registry'] = \
            {'tm:auth:partition:partitionstate': Partition}


class Partition(Resource):
    def __init__(self, users):
        super(Partition, self).__init__(users)
        self._meta_data['required_json_kind'] = \
            'tm:auth:partition:partitionstate'
