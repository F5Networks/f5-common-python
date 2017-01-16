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
from f5.sdk_exception import UtilError
from icontrol.session import iControlUnexpectedHTTPError


def test_missing_required_params(mgmt_root):
    with pytest.raises(MissingRequiredCommandParameter) as err:
        mgmt_root.tm.util.get_dossier.exec_cmd('run')
    assert "Missing required params: ['utilCmdArgs']" in str(err)


def test_command_result_present(mgmt_root):
    dossier1 = mgmt_root.tm.util.get_dossier.exec_cmd(
        'run', utilCmdArgs='-b registration-key')
    assert 'commandResult' in dossier1.__dict__
    assert len(dossier1.commandResult) > 0


def test_invalid_get_dossier_options(mgmt_root):
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.get_dossier.exec_cmd(
            'run', utilCmdArgs='-x registration-key')
    assert 'usage: /usr/bin/get_dossier' in str(err.value)


def test_unbalanced_quotes(mgmt_root):
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.util.get_dossier.exec_cmd('run', utilCmdArgs='"')
    assert 'quotes are not balanced' in err.value.response.text
