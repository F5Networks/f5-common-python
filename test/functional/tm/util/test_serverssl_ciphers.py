
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

from distutils.version import LooseVersion
from f5.bigip.resource import MissingRequiredCommandParameter
from icontrol.session import iControlUnexpectedHTTPError

@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.1.0'),
    reason='util/serverssl-ciphers is only supported in 12.1.0 or greater.'
)
def test_E_serverssl_ciphers(mgmt_root):

    with pytest.raises(MissingRequiredCommandParameter) as err:
        mgmt_root.tm.util.serverssl_ciphers.exec_cmd('run')
        assert "Missing required params: ['utilCmdArgs']" in err.response.text

    sssl_cipher1 = mgmt_root.tm.util.serverssl_ciphers.exec_cmd('run',
                                                                utilCmdArgs='')

    # syntax message should be present
    assert 'Syntax: serverssl-ciphers \'<cipher-string>\'' in \
           sssl_cipher1.commandResult

    sssl_cipher2 = mgmt_root.tm.util.serverssl_ciphers.exec_cmd(
        'run', utilCmdArgs='DEFAULT')

    # cipher list should be returned, match the header row
    assert 'DHE-RSA-AES128-GCM-SHA256' in \
           sssl_cipher2.commandResult

    # iControlUnexpectedHTTPError should be raised if quotes don't match
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.util.serverssl_ciphers.exec_cmd('run', utilCmdArgs='"')
        assert err.response.status_code == 400
        assert 'quotes are not balanced' in err.response.text
