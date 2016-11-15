
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

import pytest

from f5.bigip.mixins import UtilError
from f5.bigip.resource import MissingRequiredCommandParameter
from icontrol.session import iControlUnexpectedHTTPError


def test_E_dig(mgmt_root):

    with pytest.raises(MissingRequiredCommandParameter) as err:
        mgmt_root.tm.util.dig.exec_cmd('run')
        assert "Missing required params: ['utilCmdArgs']" in err.response.text

    dig1 = mgmt_root.tm.util.dig.exec_cmd('run', utilCmdArgs='f5.com NS')

    # commandResult should be present with data from 'f5.com NS'
    assert 'commandResult' in dig1.__dict__
    assert 'DiG' in dig1.commandResult

    # UtilError should be raised if there is an invalid option for dig
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.dig.exec_cmd('run', utilCmdArgs='-9 f5.com NS')
        assert 'Invalid option' in err.response.text

    # iControlUnexpectedHTTPError should be raised if quotes don't match
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.util.dig.exec_cmd('run', utilCmdArgs='"')
        assert err.response.status_code == 400
        assert 'quotes are not balanced' in err.response.text
