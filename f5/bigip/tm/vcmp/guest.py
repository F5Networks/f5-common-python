# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® Guest (vcmp) module

REST URI
    ``http://localhost/mgmt/tm/vcmp/guest/``

GUI Path
    ``Guest List``

REST Kind
    ``tm:vcmp:guest:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Guests(Collection):
    """BIG-IP® Guests collection."""
    def __init__(self, vcmp):
        super(Guests, self).__init__(vcmp)
        self._meta_data['allowed_lazy_attributes'] = [Guest]
        self._meta_data['required_json_kind'] =\
            'tm:vcmp:guest:guestcollectionstate'
        self._meta_data['attribute_registry'] =\
            {'tm:vcmp:guest:gueststate': Guest}


class Guest(Resource):
    """BIG-IP® Guest resource."""
    def __init__(self, guests):
        super(Guest, self).__init__(guests)
        self._meta_data['required_json_kind'] =\
            'tm:vcmp:guest:gueststate'
