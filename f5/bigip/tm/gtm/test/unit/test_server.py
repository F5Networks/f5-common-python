# Copyright 2014-2017 F5 Networks Inc.
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
from f5.bigip.tm.gtm.server import Server
from f5.bigip.tm.gtm.server import Virtual_Server
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeServer():
    fake_servers = mock.MagicMock()
    fake_server = Server(fake_servers)
    return fake_server


@pytest.fixture
def FakeVS():
    fake_server = mock.MagicMock()
    fake_vs = Virtual_Server(fake_server)
    return fake_vs


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        s1 = b.tm.gtm.servers.server
        s2 = b.tm.gtm.servers.server
        assert s1 is not s2

    def test_create_no_args(self, FakeServer):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeServer.create()

    def test_create_no_datacenter(self, FakeServer):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeServer.create(name='fakeserver',
                              addresses=[{'name': '1.1.1.1'}])

    def test_create_no_address(self, FakeServer):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeServer.create(name='fakeserver', datacenter='fakedc')


class Test_VS_Subcoll(object):
    def test_vs_attr_exists(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        s = b.tm.gtm.servers.server
        test_meta = s._meta_data['attribute_registry']
        kind = 'tm:gtm:server:virtual-servers:virtual-serverscollectionstate'
        assert kind in list(iterkeys(test_meta))

    def test_create_no_args(self, FakeVS):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeVS.create()
