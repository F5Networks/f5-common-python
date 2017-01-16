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
from f5.sdk_exception import MissingRequiredCommandParameter
from icontrol.session import iControlUnexpectedHTTPError


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.1.0'),
    reason='util/clientssl-ciphers is only supported in 12.1.0 or greater.'
)
class TestClientSslCiphersV12(object):
    def test_missing_required_params(self, mgmt_root):
        with pytest.raises(MissingRequiredCommandParameter) as err:
            mgmt_root.tm.util.clientssl_ciphers.exec_cmd('run')
        assert "Missing required params: ['utilCmdArgs']" in str(err)

    def test_syntax_message(self, mgmt_root):
        cssl_cipher1 = mgmt_root.tm.util.clientssl_ciphers.exec_cmd(
            'run', utilCmdArgs=''
        )
        assert 'Syntax: clientssl-ciphers \'<cipher-string>\'' in \
               cssl_cipher1.commandResult

    def test_cipher_list_returned(self, mgmt_root):
        cssl_cipher2 = mgmt_root.tm.util.clientssl_ciphers.exec_cmd(
            'run', utilCmdArgs='DEFAULT'
        )
        assert 'DHE-RSA-AES128-GCM-SHA256' in \
               cssl_cipher2.commandResult

    def test_test_unbalanced_quotes_in_command(self, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            mgmt_root.tm.util.clientssl_ciphers.exec_cmd('run',
                                                         utilCmdArgs='"')
        assert 'quotes are not balanced' in err.value.response.text
