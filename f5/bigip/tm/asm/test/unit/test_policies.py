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

from f5.bigip import ManagementRoot
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.asm import Asm
from f5.bigip.tm.asm.policies import Evasion
from f5.bigip.tm.asm.policies import Header
from f5.bigip.tm.asm.policies import Http_Protocol
from f5.bigip.tm.asm.policies import Parameter
from f5.bigip.tm.asm.policies import Parameters_s
from f5.bigip.tm.asm.policies import ParametersCollection
from f5.bigip.tm.asm.policies import ParametersResource
from f5.bigip.tm.asm.policies import Policy
from f5.bigip.tm.asm.policies import Signature
from f5.bigip.tm.asm.policies import Url
from f5.bigip.tm.asm.policies import UrlParametersCollection
from f5.bigip.tm.asm.policies import UrlParametersResource
from f5.bigip.tm.asm.policies import Violation
from f5.bigip.tm.asm.policies import Web_Services_Security


import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakePolicy(fakeicontrolsession):
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    fake_asm = Asm(mr.tm)
    fake_policy = Policy(fake_asm)
    return fake_policy


def MakePolicy(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.asm.policies_s.policy
    p._meta_data['uri'] = \
        'https://192.168.1.1/mgmt/tm/asm/policies/Lx3553-321'
    return p


@pytest.fixture
def FakeURL():
    pol = mock.MagicMock()
    url = Url(pol)
    url._meta_data['uri'] = \
        'https://192.168.1.1/mgmt/tm/asm/policies/' \
        'Lx3553-321/urls/vIlmHUz1-CQx5yxDEuf0Rw'
    return url


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


@pytest.fixture
def FakeSignature():
    fake_policy = mock.MagicMock()
    fake_sig = Signature(fake_policy)
    fake_sig._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_sig


@pytest.fixture
def FakePolicyParameters():
    fake_policy = mock.MagicMock()
    fake_param = ParametersCollection(fake_policy)
    fake_param._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_param


@pytest.fixture
def FakeUrlParameters():
    fake_policy = mock.MagicMock()
    fake_param = UrlParametersCollection(fake_policy)
    fake_param._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_param


@pytest.fixture
def FakeHeader():
    fake_policy = mock.MagicMock()
    fake_param = Header(fake_policy)
    fake_param._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_param


class TestPolicy(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.policies_s.policy
        t2 = b.tm.asm.policies_s.policy
        assert t1 is t2

    def test_create_no_args(self, FakePolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePolicy.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.policies_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:policies:policystate'
        assert kind in list(iterkeys(test_meta))
        assert Policy in test_meta2
        assert t._meta_data['object_has_stats'] is False

    def test_set_attr_reg_v11(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.policies_s.policy
        v11kind = 'tm:asm:policies:blocking-settings'
        assert v11kind in t1._meta_data['attribute_registry'].keys()

    def test_set_attr_reg_v12(self, fakeicontrolsession_v12):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.policies_s.policy
        v12kind = 'tm:asm:policies:blocking-settings:blocking-' \
                  'settingcollectionstate'
        assert v12kind in t1._meta_data['attribute_registry'].keys()


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


class TestParameters_s(object):
    def test_policycol_new(self, fakeicontrolsession):
        param = Parameters_s(MakePolicy(fakeicontrolsession))
        assert isinstance(param, ParametersCollection)

    def test_urlcol_new(self, FakeURL):
        param = Parameters_s(FakeURL)
        assert isinstance(param, UrlParametersCollection)


class TestParameter(object):
    def test_policyres_new(self, FakePolicyParameters):
        param = Parameter(FakePolicyParameters)
        assert isinstance(param, ParametersResource)

    def test_urlres_new(self, FakeUrlParameters):
        param = Parameter(FakeUrlParameters)
        assert isinstance(param, UrlParametersResource)


class TestSignature(object):
    def test_create_raises(self, FakeSignature):
        with pytest.raises(UnsupportedOperation):
            FakeSignature.create()

    def test_delete_raises(self, FakeSignature):
        with pytest.raises(UnsupportedOperation):
            FakeSignature.delete()


class TestHeader(object):
    def test_create_no_args(self, FakeHeader):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeHeader.create()
