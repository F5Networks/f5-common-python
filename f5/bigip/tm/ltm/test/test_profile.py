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

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.ltm.profile import Classification
from f5.bigip.tm.ltm.profile import Ocsp_Stapling_Params
from f5.bigip.tm.ltm.profile import Web_Security


@pytest.fixture
def fake_klass():
    fake_kl = mock.MagicMock()
    return Classification(fake_kl)


@pytest.fixture
def fake_ocsp_staple():
    fake_ocsp = mock.MagicMock()
    return Ocsp_Stapling_Params(fake_ocsp)


@pytest.fixture
def fake_websec():
    fake_websec = mock.MagicMock()
    return Web_Security(fake_websec)


class TestClassification(object):
    def test_create_raises(self):
        with pytest.raises(UnsupportedOperation):
            k = fake_klass()
            k.create(name='random')

    def test_delete_raises(self):
        with pytest.raises(UnsupportedOperation):
            k = fake_klass()
            k.delete()


class TestOcspStaple(object):
    def test_create_conflict(self):
        with pytest.raises(MissingRequiredCreationParameter):
            ocsp = fake_ocsp_staple()
            ocsp.create(name='fake.ocsp', useProxyServer='enabled',
                        trustedCa='/partition/fakeCA', dnsResolver='fake.dns')


class TestWebSecurity(object):
    def test_create_raises(self):
        with pytest.raises(UnsupportedOperation):
            ws = fake_websec()
            ws.create(name='random')

    def test_update_raises(self):
        with pytest.raises(UnsupportedOperation):
            ws = fake_websec()
            ws.update()

    def test_refresh_raises(self):
        with pytest.raises(UnsupportedOperation):
            ws = fake_websec()
            ws.refresh()

    def test_delete_raises(self):
        with pytest.raises(UnsupportedOperation):
            ws = fake_websec()
            ws.delete()
