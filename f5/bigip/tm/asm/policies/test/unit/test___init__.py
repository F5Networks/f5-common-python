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
from f5.bigip.tm.asm.policies.parameters import Parameter
from f5.bigip.tm.asm.policies.parameters import Parameters_s
from f5.bigip.tm.asm.policies.parameters import ParametersCollection
from f5.bigip.tm.asm.policies.parameters import ParametersResource
from f5.bigip.tm.asm.policies.parameters import UrlParametersCollection
from f5.bigip.tm.asm.policies.parameters import UrlParametersResource
from f5.bigip.tm.asm.policies import Policy
from f5.bigip.tm.asm.policies.urls import Url
from f5.sdk_exception import MissingRequiredCreationParameter
from six import iterkeys

import mock
import pytest


@pytest.fixture
def FakeURL():
    pol = mock.MagicMock()
    url = Url(pol)
    url._meta_data['uri'] = \
        'https://192.168.1.1/mgmt/tm/asm/policies/' \
        'Lx3553-321/urls/vIlmHUz1-CQx5yxDEuf0Rw'
    return url


@pytest.fixture
def FakeUrlParameters():
    fake_policy = mock.MagicMock()
    fake_param = UrlParametersCollection(fake_policy)
    fake_param._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_param


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
def FakePolicyParameters():
    fake_policy = mock.MagicMock()
    fake_param = ParametersCollection(fake_policy)
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
        v12kind = 'tm:asm:policies:blocking-settings:blocking-settingcollectionstate'
        assert v12kind in t1._meta_data['attribute_registry'].keys()


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
