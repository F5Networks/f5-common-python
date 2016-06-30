# coding=utf-8
#
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

"""BIG-IP® Local Traffic Manager (LTM) virtual module.

REST URI
    ``http://localhost/mgmt/tm/ltm/virtual``

GUI Path
    ``Local Traffic --> Virtual Servers``

REST Kind
    ``tm:ltm:virtual:*``
"""

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.mixins import StatsMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Virtuals(Collection):
    """BIG-IP® LTM virtual collection"""
    def __init__(self, ltm):
        super(Virtuals, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Virtual]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:virtualstate': Virtual}


class Virtual(Resource, StatsMixin, CommandExecutionMixin):
    """BIG-IP® LTM virtual resource"""
    def __init__(self, virtual_s):
        super(Virtual, self).__init__(virtual_s)
        self._meta_data['allowed_lazy_attributes'] = [Profiles_s]
        self._meta_data['required_json_kind'] = 'tm:ltm:virtual:virtualstate'
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:profiles:profilescollectionstate': Profiles_s}
        self._meta_data['allowed_commands'] = 'reset-stats'


class Profiles(Resource):
    """BIG-IP® LTM profiles subclass resource."""
    def __init__(self, Profiles_s):
        super(Profiles, self).__init__(Profiles_s)
        self._meta_data['required_json_kind'] =\
            "tm:ltm:virtual:profiles:profilesstate"



class Profiles_s(Collection):
    """BIG-IP® LTM profiles subclass collection."""
    def __init__(self, virtual):
        super(Profiles_s, self).__init__(virtual)
        self._meta_data['allowed_lazy_attributes'] = [Profiles]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:profiles:profilesstate': Profiles}
