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

from f5.sdk_exception import MissingRequiredCommandParameter
from f5.sdk_exception import UtilError
from icontrol.session import iControlUnexpectedHTTPError


def test_required_params(mgmt_root):
    with pytest.raises(MissingRequiredCommandParameter) as err:
        mgmt_root.tm.util.bash.exec_cmd('run')
    assert "Missing required params: ['utilCmdArgs']" in str(err)


def test_command_result_not_present(mgmt_root):
    args = '-c "echo hello >> /var/tmp/test.txt"'
    bash = mgmt_root.tm.util.bash.exec_cmd('run', utilCmdArgs=args)

    assert 'commandResult' not in bash.__dict__
    mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs='/var/tmp/test.txt')


def test_command_result_present(mgmt_root):
    bash = mgmt_root.tm.util.bash.exec_cmd('run', utilCmdArgs='-c df -k')
    assert 'commandResult' in bash.__dict__


def test_missing_dash_c_argument(mgmt_root):
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.bash.exec_cmd('run', utilCmdArgs='-9 hello')
    assert 'Required format is "-c <bash command and arguments>"' in str(err)


def test_command_not_found(mgmt_root):
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.bash.exec_cmd('run', utilCmdArgs='-c hello')
    assert 'command not found' in str(err)


def test_test_unbalanced_quotes_in_command(mgmt_root):
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.util.bash.exec_cmd('run', utilCmdArgs='-c "df -k')
    assert 'quotes are not balanced' in err.value.response.text
