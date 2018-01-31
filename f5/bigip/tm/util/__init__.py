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

"""BIG-IP® Utility (util) module

REST URI
    ``http://localhost/mgmt/tm/util/``

GUI Path
    ``System``

REST Kind
    N/A -- HTTP GET returns an error
"""

from f5.bigip.resource import PathElement
from f5.bigip.tm.util.bash import Bash
from f5.bigip.tm.util.clientssl_ciphers import Clientssl_Ciphers
from f5.bigip.tm.util.dig import Dig
from f5.bigip.tm.util.get_dossier import Get_Dossier
from f5.bigip.tm.util.qkview import Qkview
from f5.bigip.tm.util.serverssl_ciphers import Serverssl_Ciphers
from f5.bigip.tm.util.unix_ls import Unix_Ls
from f5.bigip.tm.util.unix_mv import Unix_Mv
from f5.bigip.tm.util.unix_rm import Unix_Rm


class Util(PathElement):
    def __init__(self, bigip):
        super(Util, self).__init__(bigip)
        self._meta_data['allowed_lazy_attributes'] = [
            Bash,
            Clientssl_Ciphers,
            Dig,
            Get_Dossier,
            Qkview,
            Serverssl_Ciphers,
            Unix_Ls,
            Unix_Mv,
            Unix_Rm
        ]
