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
from f5.bigip.tm.asm import Asm
from f5.bigip.tm.asm.policies import Brute_Force_Attack_Prevention
from f5.bigip.tm.asm.policies import Csrf_Protection
from f5.bigip.tm.asm.policies import Data_Guard
from f5.bigip.tm.asm.policies import Evasion
from f5.bigip.tm.asm.policies import Geolocation_Enforcement
from f5.bigip.tm.asm.policies import Header
from f5.bigip.tm.asm.policies import History_Revision
from f5.bigip.tm.asm.policies import Http_Protocol
from f5.bigip.tm.asm.policies import Ip_Intelligence
from f5.bigip.tm.asm.policies import Login_Enforcement
from f5.bigip.tm.asm.policies import Login_Page
from f5.bigip.tm.asm.policies import Parameter
from f5.bigip.tm.asm.policies import Parameters_s
from f5.bigip.tm.asm.policies import ParametersCollection
from f5.bigip.tm.asm.policies import ParametersResource
from f5.bigip.tm.asm.policies import Policy
from f5.bigip.tm.asm.policies import Policy_Builder
from f5.bigip.tm.asm.policies import Redirection_Protection
from f5.bigip.tm.asm.policies import Response_Page
from f5.bigip.tm.asm.policies import Sensitive_Parameter
from f5.bigip.tm.asm.policies import Session_Tracking
from f5.bigip.tm.asm.policies import Session_Tracking_Status
from f5.bigip.tm.asm.policies import Signature
from f5.bigip.tm.asm.policies import Url
from f5.bigip.tm.asm.policies import UrlParametersCollection
from f5.bigip.tm.asm.policies import UrlParametersResource
from f5.bigip.tm.asm.policies import Violation
from f5.bigip.tm.asm.policies import Vulnerability_Assessment
from f5.bigip.tm.asm.policies import Web_Services_Security
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation


import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakeSens():
    fake_policy = mock.MagicMock()
    fake_resp = Sensitive_Parameter(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


@pytest.fixture
def FakeLog():
    fake_policy = mock.MagicMock()
    fake_resp = Login_Enforcement(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


@pytest.fixture
def FakeRedir():
    fake_policy = mock.MagicMock()
    fake_resp = Redirection_Protection(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


@pytest.fixture
def FakeCsrf():
    fake_policy = mock.MagicMock()
    fake_resp = Csrf_Protection(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


@pytest.fixture
def FakeIP():
    fake_policy = mock.MagicMock()
    fake_resp = Ip_Intelligence(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


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
def FakeResponsePage():
    fake_policy = mock.MagicMock()
    fake_resp = Response_Page(fake_policy)
    fake_resp._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_resp


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
    fake_head = Header(fake_policy)
    fake_head._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_head


@pytest.fixture
def FakeBuilder():
    fake_policy = mock.MagicMock()
    fake_build = Policy_Builder(fake_policy)
    fake_build._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_build


@pytest.fixture
def FakeHistory():
    fake_policy = mock.MagicMock()
    fake_history = History_Revision(fake_policy)
    fake_history._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_history


@pytest.fixture
def FakeVulnerability():
    fake_policy = mock.MagicMock()
    fake_v = Vulnerability_Assessment(fake_policy)
    fake_v._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_v


@pytest.fixture
def FakeData():
    fake_policy = mock.MagicMock()
    fake_d = Data_Guard(fake_policy)
    fake_d._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_d


@pytest.fixture
def FakeGeo():
    fake_policy = mock.MagicMock()
    fake_g = Geolocation_Enforcement(fake_policy)
    fake_g._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_g


@pytest.fixture
def FakeSessTrack():
    fake_policy = mock.MagicMock()
    fake_g = Session_Tracking(fake_policy)
    fake_g._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_g


@pytest.fixture
def FakeSess():
    fake_policy = mock.MagicMock()
    fake_g = Session_Tracking_Status(fake_policy)
    fake_g._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_g


@pytest.fixture
def FakeLogin():
    fake_policy = mock.MagicMock()
    fake_g = Login_Page(fake_policy)
    fake_g._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_g


@pytest.fixture
def FakeBrute():
    fake_policy = mock.MagicMock()
    fake_g = Brute_Force_Attack_Prevention(fake_policy)
    fake_g._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_g


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


class TestResponsePages(object):
    def test_create_raises(self, FakeResponsePage):
        with pytest.raises(UnsupportedOperation):
            FakeResponsePage.create()

    def test_delete_raises(self, FakeResponsePage):
        with pytest.raises(UnsupportedOperation):
            FakeResponsePage.delete()


class TestPolicyBuilder(object):
    def test_update_raises(self, FakeBuilder):
        with pytest.raises(UnsupportedOperation):
            FakeBuilder.update()


class TestHistoryRevisions(object):
    def test_create_raises(self, FakeHistory):
        with pytest.raises(UnsupportedOperation):
            FakeHistory.create()

    def test_delete_raises(self, FakeHistory):
        with pytest.raises(UnsupportedOperation):
            FakeHistory.delete()

    def test_modify_raises(self, FakeHistory):
        with pytest.raises(UnsupportedOperation):
            FakeHistory.modify()


class TestVulnerabilityAssessment(object):
    def test_update_raises(self, FakeVulnerability):
        with pytest.raises(UnsupportedOperation):
            FakeVulnerability.update()


class TestDataGuard(object):
    def test_update_raises(self, FakeData):
        with pytest.raises(UnsupportedOperation):
            FakeData.update()


class TestGeolocationEnforcement(object):
    def test_update_raises(self, FakeGeo):
        with pytest.raises(UnsupportedOperation):
            FakeGeo.update()


class TestSessionTracking(object):
    def test_update_raises(self, FakeSessTrack):
        with pytest.raises(UnsupportedOperation):
            FakeSessTrack.update()


class TestSessionTrackingStatuses(object):
    def test_update_raises(self, FakeSess):
        with pytest.raises(UnsupportedOperation):
            FakeSess.modify()


class TestLoginPages(object):
    def test_create_no_args(self, FakeLogin):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLogin.create()


class TestIPIntelligence(object):
    def test_update_raises(self, FakeIP):
        with pytest.raises(UnsupportedOperation):
            FakeIP.update()


class TestCrfProtection(object):
    def test_update_raises(self, FakeCsrf):
        with pytest.raises(UnsupportedOperation):
            FakeCsrf.update()


class TestRedirectionProtection(object):
    def test_update_raises(self, FakeRedir):
        with pytest.raises(UnsupportedOperation):
            FakeRedir.update()


class TestLoginEnforcement(object):
    def test_update_raises(self, FakeLog):
        with pytest.raises(UnsupportedOperation):
            FakeLog.update()


class TestSensitiveParameters(object):
    def test_modify_raises(self, FakeSens):
        with pytest.raises(UnsupportedOperation):
            FakeSens.modify()


class TestBruteForce(object):
    def test_create_no_args(self, FakeBrute):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeBrute.create()
