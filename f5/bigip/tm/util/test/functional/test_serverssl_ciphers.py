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
class TestServerSslCiphersV12(object):
    def test_missing_required_params(self, mgmt_root):
        with pytest.raises(MissingRequiredCommandParameter) as err:
            mgmt_root.tm.util.serverssl_ciphers.exec_cmd('run')
        assert "Missing required params: ['utilCmdArgs']" in str(err)

    def test_syntax_message_present(self, mgmt_root):
        sssl_cipher = mgmt_root.tm.util.serverssl_ciphers.exec_cmd(
            'run', utilCmdArgs=''
        )
        assert 'Syntax: serverssl-ciphers \'<cipher-string>\'' in \
               sssl_cipher.commandResult

    def test_cipher_list_returned(self, mgmt_root):
        args = 'DEFAULT'
        sssl_cipher = mgmt_root.tm.util.serverssl_ciphers.exec_cmd(
            'run', utilCmdArgs=args
        )
        assert 'DHE-RSA-AES128-GCM-SHA256' in \
               sssl_cipher.commandResult

    def test_test_unbalanced_quotes_in_command(self, mgmt_root):
        args = '"'
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.util.serverssl_ciphers.exec_cmd(
                'run', utilCmdArgs=args
            )
        assert 'quotes are not balanced' in err.value.response.text
