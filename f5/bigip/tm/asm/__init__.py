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

from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.asm.attack_types import Attack_Types_s
from f5.bigip.tm.asm.file_transfer import File_Transfer
from f5.bigip.tm.asm.policies import Policies_s
from f5.bigip.tm.asm.policy_templates import Policy_Templates_s
from f5.bigip.tm.asm.signature_sets import Signature_Sets_s
from f5.bigip.tm.asm.signature_statuses import Signature_Statuses_s
from f5.bigip.tm.asm.signature_systems import Signature_Systems_s
from f5.bigip.tm.asm.signature_update import Signature_Update
from f5.bigip.tm.asm.signatures import Signatures_s
from f5.bigip.tm.asm.tasks import Tasks


class Asm(OrganizingCollection):
    """BIG-IP® Application Security Manager (ASM) organizing

    collection.
    """

    def __init__(self, tm):
        super(Asm, self).__init__(tm)
        self._meta_data['allowed_lazy_attributes'] = [
            Attack_Types_s,
            File_Transfer,
            Policies_s,
            Policy_Templates_s,
            Signature_Sets_s,
            Signature_Statuses_s,
            Signature_Systems_s,
            Signature_Update,
            Signatures_s,
            Tasks,
        ]
