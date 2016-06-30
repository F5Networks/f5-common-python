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


import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.mixins import UnsupportedTmosVersion
from f5.bigip.tm.sys.ucs import Ucs


@pytest.fixture
def FakeUcs():
    fake_sys = mock.MagicMock()
    fake_ucs = Ucs(fake_sys)
    fake_ucs._meta_data['bigip'].tmos_version = '12.0.0'
    return fake_ucs


@pytest.fixture
def FakeiControl(fakeicontrolsession_v12):
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mock_session = mock.MagicMock()
    mock_session.post.return_value.json.return_value = {}
    mr._meta_data['icr_session'] = mock_session
    return mr.tm.sys.ucs


class TestUCSCommand(object):
    def test_command_ucs_load(self, FakeiControl):
        FakeiControl.exec_cmd('load', name='foo.ucs')
        session = FakeiControl._meta_data['bigip']._meta_data['icr_session']
        assert session.post.call_args == mock.call(
            'https://FAKENETLOC:443/mgmt/tm/sys/ucs/',
            json={'name': 'foo.ucs', 'command': 'load'}
        )

    def test_command_ucs_save(self, FakeiControl):
        FakeiControl.exec_cmd('save', name='foo.ucs')
        session = FakeiControl._meta_data['bigip']._meta_data['icr_session']
        assert session.post.call_args == mock.call(
            'https://FAKENETLOC:443/mgmt/tm/sys/ucs/',
            json={'name': 'foo.ucs', 'command': 'save'}
        )

    def test_list_ucs_wrong_tmos_version(self, FakeUcs):
        with pytest.raises(UnsupportedTmosVersion) as EIO:
            FakeUcs.load()
            assert EIO.value.message == \
                "There was an attempt to use a method which " \
                "has not been implemented or supported " \
                "in the device's TMOS version: 12.0.0. " \
                "Minimum TMOS version supported is 12.1.0"

