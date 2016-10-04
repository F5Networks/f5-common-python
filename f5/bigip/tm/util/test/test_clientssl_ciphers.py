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
from f5.bigip.mixins import UnsupportedTmosVersion
from f5.bigip.resource import MissingRequiredCommandParameter
from f5.bigip.tm.util.Clientssl_Ciphers import Clientssl_Ciphers


@pytest.fixture
def FakeClientsslCiphers():
    fake_sys = mock.MagicMock()
    fake_clientssl_ciphers = Clientssl_Ciphers(fake_sys)
    fake_clientssl_ciphers._meta_data['bigip'].tmos_version = '12.0.0'
    return fake_clientssl_ciphers


@pytest.fixture
def FakeiControl(fakeicontrolsession_v12):
    mr = ManagementRoot('host', 'fake_admin', 'fake_admin')
    mock_session = mock.MagicMock()
    mock_session.post.return_value.json.return_value = {}
    mr._meta_data['icr_session'] = mock_session
    return mr.tm.util.clientssl_ciphers


def test_cssl_exec_missing_args(FakeClientsslCiphers):
    with pytest.raises(MissingRequiredCommandParameter):
        FakeClientsslCiphers.exec_cmd('run')


def test_command_clientssl_ciphers_wrong_ver(FakeClientsslCiphers):
    with pytest.raises(UnsupportedTmosVersion):
        FakeClientsslCiphers.exec_cmd('run', utilCmdArgs='')


def test_command_clientssl_ciphers(FakeiControl):
    FakeiControl.exec_cmd('run', utilCmdArgs='DEFAULT')
    session = FakeiControl._meta_data['bigip']._meta_data['icr_session']
    assert session.post.call_args == mock.call(
        'https://host:443/mgmt/tm/util/clientssl-ciphers/',
        json={'utilCmdArgs': 'DEFAULT', 'command': 'run'}
    )
