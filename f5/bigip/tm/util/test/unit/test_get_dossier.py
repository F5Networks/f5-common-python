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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.util.get_dossier import Get_Dossier


@pytest.fixture
def FakeGetDossier():
    fake_sys = mock.MagicMock()
    fake_get_dossier = Get_Dossier(fake_sys)
    return fake_get_dossier


@pytest.fixture
def FakeiControl(fakeicontrolsession):
    mr = ManagementRoot('host', 'fake_admin', 'fake_admin')
    mock_session = mock.MagicMock()
    mock_session.post.return_value.json.return_value = {}
    mr._meta_data['icr_session'] = mock_session
    return mr.tm.util.get_dossier


class TestGetDossierCommand(object):
    def test_command_get_dossier(self, FakeiControl):
        FakeiControl.exec_cmd('run', utilCmdArgs='-b registration-key')
        session = FakeiControl._meta_data['bigip']._meta_data['icr_session']
        assert session.post.call_args == mock.call(
            'https://host:443/mgmt/tm/util/get-dossier/',
            json={'utilCmdArgs': '-b registration-key', 'command': 'run'}
        )
