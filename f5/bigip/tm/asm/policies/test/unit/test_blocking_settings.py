# Copyright 2015 F5 Networks Inc.
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


from f5.bigip.tm.asm.policies.blocking_settings import Evasion
from f5.bigip.tm.asm.policies.blocking_settings import Http_Protocol
from f5.bigip.tm.asm.policies.blocking_settings import Violation
from f5.bigip.tm.asm.policies.blocking_settings import Web_Services_Security
from f5.sdk_exception import UnsupportedOperation


import mock
import pytest


@pytest.fixture
def FakeEvasion():
    fake_policy = mock.MagicMock()
    fake_eva = Evasion(fake_policy)
    fake_eva._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_eva


@pytest.fixture
def FakeHttp():
    fake_policy = mock.MagicMock()
    fake_eva = Http_Protocol(fake_policy)
    fake_eva._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_eva


@pytest.fixture
def FakeViolation():
    fake_policy = mock.MagicMock()
    fake_eva = Violation(fake_policy)
    fake_eva._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_eva


@pytest.fixture
def FakeWebsec():
    fake_policy = mock.MagicMock()
    fake_eva = Web_Services_Security(fake_policy)
    fake_eva._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_eva


class TestEvasion(object):
    def test_create_raises(self, FakeEvasion):
        with pytest.raises(UnsupportedOperation):
            FakeEvasion.create()

    def test_delete_raises(self, FakeEvasion):
        with pytest.raises(UnsupportedOperation):
            FakeEvasion.delete()


class TestHttp(object):
    def test_create_raises(self, FakeHttp):
        with pytest.raises(UnsupportedOperation):
            FakeHttp.create()

    def test_delete_raises(self, FakeHttp):
        with pytest.raises(UnsupportedOperation):
            FakeHttp.delete()


class TestViolation(object):
    def test_create_raises(self, FakeViolation):
        with pytest.raises(UnsupportedOperation):
            FakeViolation.create()

    def test_delete_raises(self, FakeViolation):
        with pytest.raises(UnsupportedOperation):
            FakeViolation.delete()


class TestWebSec(object):
    def test_create_raises(self, FakeWebsec):
        with pytest.raises(UnsupportedOperation):
            FakeWebsec.create()

    def test_delete_raises(self, FakeWebsec):
        with pytest.raises(UnsupportedOperation):
            FakeWebsec.delete()
