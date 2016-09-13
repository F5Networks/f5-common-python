# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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

"""BIG-IP® Application Security Manager™ (ASM®) module.

REST URI
    ``http://localhost/mgmt/tm/asm/``

GUI Path
    ``Security``

REST Kind
    ``tm:asm:*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.bigip.resource import OrganizingCollection


class Tasks(OrganizingCollection):
    """BIG-IP® ASM Tasks organizing collection."""

    def __init__(self, tm):
        super(Tasks, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Check_Signatures_s,
            Export_Signatures_s,
            Signature_Statuses_s,
            Signature_Systems_s,
            Update_Signatures_s,
            ]


class Check_Signatures_s(Collection):
    pass


class Check_Signatures(Resource):
    pass


class Export_Signatures_s(Collection):
    pass


class Export_Signatures(Resource):
    pass


class Signature_Statuses_s(Collection):
    pass


class Signature_Statuses(Resource):
    pass


class Signature_Systems_s(Collection):
    pass


class Signature_Systems(Resource):
    pass


class Update_Signatures_s(Collection):
    pass


class Update_Signatures(Resource):
    pass