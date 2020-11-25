# coding=utf-8
#
# Copyright 2020 F5 Networks Inc.
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

"""BIG-IP® Network bwc module.

REST URI
    ``http://localhost/mgmt/tm/net/bwc``

GUI Path
    ``Acceleration --> Bandwidth Controllers``

REST Kind
    ``tm:net:bwc:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Bwc(OrganizingCollection):
    """BIG-IP® network bwc collection"""
    def __init__(self, net):
        super(Bwc, self).__init__(net)
        self._meta_data['allowed_lazy_attributes'] = [
            Policys,
        ]


class Policys(Collection):
    """BIG-IP® bwc policy sub-collection"""
    def __init__(self, bwc):
        super(Policys, self).__init__(bwc)
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] =\
            {'tm:net:bwc:policy:policystate': Policy}


class Policy(Resource):
    """BIG-IP® bwc policy sub-collection resource"""
    def __init__(self, policy_s):
        super(Policy, self).__init__(policy_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:net:bwc:policy:policystate'
