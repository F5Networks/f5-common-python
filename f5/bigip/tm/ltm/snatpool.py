# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
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

"""BIG-IP Local Traffic Manager (LTM) SNAT pool module.

REST URI
    ``https://localhost/mgmt/tm/ltm/snatpool?ver=11.6.0``

GUI Path
    ``Local Traffic --> Address Translation --> SNAT Pool List``

REST Kind
    ``tm:ltm:snatpool:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Snatpools(Collection):
    """BIG-IP® SNAT Pool collection"""
    def __init__(self, ltm):
        super(Snatpools, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Snatpool]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:snatpool:snatpoolstate': Snatpool}


class Snatpool(Resource):
    """BIG-IP® SNAT Pool resource"""
    def __init__(self, Snatpools):
        super(Snatpool, self).__init__(Snatpools)
        self._meta_data['required_json_kind'] =\
            "tm:ltm:snatpool:snatpoolstate"
