
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

from f5.bigip.resource import MissingRequiredCommandParameter
from f5.utils.util_exceptions import UtilError
from icontrol.session import iControlUnexpectedHTTPError


def test_E_bash(mgmt_root):

    with pytest.raises(MissingRequiredCommandParameter) as err:
        mgmt_root.tm.util.bash.exec_cmd('run')
        assert "Missing required params: ['utilCmdArgs']" in err.response.text

    # use bash to create a test file
    bash1 = mgmt_root.tm.util.bash.exec_cmd(
        'run',
        utilCmdArgs='-c "echo hello >> /var/tmp/test.txt"')

    # commandResult should not be present if this was successful
    assert 'commandResult' not in bash1.__dict__

    bash2 = mgmt_root.tm.util.bash.exec_cmd(
        'run',
        utilCmdArgs='-c df -k')

    # commandResult should be present with data from 'df -k'
    assert 'commandResult' in bash2.__dict__

    # UtilError should be raised if -c is not specified
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.bash.exec_cmd('run',
                                        utilCmdArgs='-9 hello')
        assert 'Required format is "-c <bash command and arguments>"'\
               in err.response.text

    # UtilError should be raised if command isn't found
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.bash.exec_cmd('run',
                                        utilCmdArgs='-c hello')
        assert 'command not found' in err.response.text

    # clean up test file
    mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs='/var/tmp/test.txt')

    # iControlUnexpectedHTTPError should be raised if quotes don't match
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.util.bash.exec_cmd('run',
                                        utilCmdArgs='-c "df -k')
        assert err.response.status_code == 400
        assert 'quotes are not balanced' in err.response.text
