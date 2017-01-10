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

"""Directory: ltm module: virtual-address.

REST URI
    ``https://localhost/mgmt/tm/ltm/virtual-address?ver=11.6.0``

GUI Path
    ``Local Traffic Manager --> Virtual Servers --> Virtual Address List``

REST Kind
    ``tm:ltm:virtual-address:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Virtual_Address_s(Collection):
    """BIG-IP® LTM virtual address collection."""
    def __init__(self, ltm):
        super(Virtual_Address_s, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Virtual_Address]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual-address:virtual-addressstate': Virtual_Address}


class Virtual_Address(Resource):
    """BIG-IP® LTM virtual address resource."""
    def __init__(self, Virtual_Address_s):
        super(Virtual_Address, self).__init__(Virtual_Address_s)
        self._meta_data['required_json_kind'] =\
            "tm:ltm:virtual-address:virtual-addressstate"
        self._meta_data['read_only_attributes'].append('address')
