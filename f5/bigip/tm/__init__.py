# coding=utf-8
#
"""Classes and functions for configuring BIG-IP"""
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

from f5.bigip.resource import OrganizingCollection

from f5.bigip.tm.asm import Asm
from f5.bigip.tm.auth import Auth
from f5.bigip.tm.cm import Cm
from f5.bigip.tm.gtm import Gtm
from f5.bigip.tm.ltm import Ltm
from f5.bigip.tm.net import Net
from f5.bigip.tm.security import Security
from f5.bigip.tm.shared import Shared
from f5.bigip.tm.sys import Sys
from f5.bigip.tm.transaction import Transactions
from f5.bigip.tm.util import Util
from f5.bigip.tm.vcmp import Vcmp


class Tm(OrganizingCollection):
    """An organizing collection for TM resources."""
    def __init__(self, bigip):
        super(Tm, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Asm,
            Auth,
            Cm,
            Gtm,
            Ltm,
            Net,
            Security,
            Shared,
            Sys,
            Transactions,
            Util,
            Vcmp
        ]
