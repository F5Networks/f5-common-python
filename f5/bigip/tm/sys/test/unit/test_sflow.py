# Copyright 2017 F5 Networks Inc.
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
from f5.bigip.tm.sys.sflow import Http
from f5.bigip.tm.sys.sflow import Interface
from f5.bigip.tm.sys.sflow import Receiver
from f5.bigip.tm.sys.sflow import System
from f5.bigip.tm.sys.sflow import Vlan
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeSflowReceiver():
    fake_receiver = mock.MagicMock()
    return Receiver(fake_receiver)


@pytest.fixture
def FakeSflowHttp():
    fake_http = mock.MagicMock()
    return Http(fake_http)


@pytest.fixture
def FakeSflowInterface():
    fake_interface = mock.MagicMock()
    return Interface(fake_interface)


@pytest.fixture
def FakeSflowSystem():
    fake_system = mock.MagicMock()
    return System(fake_system)


@pytest.fixture
def FakeSflowVlan():
    fake_vlan = mock.MagicMock()
    return Vlan(fake_vlan)


class TestSflowHttp(object):
    def test_create_raises(self, FakeSflowHttp):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowHttp.create()
        assert str(EIO.value) == "Http does not support the create method"

    def test_delete_raises(self, FakeSflowHttp):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowHttp.delete()
        assert str(EIO.value) == "Http does not support the delete method"


class TestSflowInterface(object):
    def test_create_raises(self, FakeSflowInterface):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowInterface.create()
        assert str(EIO.value) == "Interface does not support the create method"

    def test_delete_raises(self, FakeSflowInterface):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowInterface.delete()
        assert str(EIO.value) == "Interface does not support the delete method"


class TestSflowSystem(object):
    def test_create_raises(self, FakeSflowSystem):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowSystem.create()
        assert str(EIO.value) == "System does not support the create method"

    def test_delete_raises(self, FakeSflowSystem):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowSystem.delete()
        assert str(EIO.value) == "System does not support the delete method"


class TestSflowVlan(object):
    def test_create_raises(self, FakeSflowVlan):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowVlan.create()
        assert str(EIO.value) == "Vlan does not support the create method"

    def test_delete_raises(self, FakeSflowVlan):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeSflowVlan.delete()
        assert str(EIO.value) == "Vlan does not support the delete method"


class TestSflowReceiver(object):
    def test_receiver_create_no_args(self, FakeSflowReceiver):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeSflowReceiver.create()

    def test_receiver_create_missing_args(self, FakeSflowReceiver):
        with pytest.raises(MissingRequiredCreationParameter) as EIO:
            FakeSflowReceiver.create(name='tr1')
        assert 'address' in str(EIO.value)

    def test_receiver_create_two(self, fakeicontrolsession):
        b = ManagementRoot('localhost', 'admin', 'admin', port='10443')
        r1 = b.tm.sys.sflow.receivers.receiver
        r2 = b.tm.sys.sflow.receivers.receiver
        assert r1 is not r2
