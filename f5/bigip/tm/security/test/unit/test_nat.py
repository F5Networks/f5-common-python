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
from f5.bigip.tm.security.nat import Destination_Translation
from f5.bigip.tm.security.nat import Policy
from f5.bigip.tm.security.nat import Rules
from f5.bigip.tm.security.nat import Rules_s
from f5.bigip.tm.security.nat import Source_Translation
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys

MIN_BIGIP_VERSION = '12.1.0'


@pytest.fixture
def FakeDestinationTranslation():
    fake_dst_xlat_s = mock.MagicMock()
    fake_dst_xlat_s._meta_data['bigip'].tmos_version = MIN_BIGIP_VERSION
    fake_dst_xlat = Destination_Translation(fake_dst_xlat_s)
    return fake_dst_xlat


@pytest.fixture
def FakeSourceTranslation():
    fake_src_xlat_s = mock.MagicMock()
    fake_src_xlat_s._meta_data['bigip'].tmos_version = MIN_BIGIP_VERSION
    fake_src_xlat = Source_Translation(fake_src_xlat_s)
    return fake_src_xlat


@pytest.fixture
def FakePolicy():
    fake_policy_s = mock.MagicMock()
    fake_policy_s._meta_data['bigip'].tmos_version = MIN_BIGIP_VERSION
    fake_policy = Policy(fake_policy_s)
    return fake_policy


def MakePolicyRules(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    b._meta_data['tmos_version'] = MIN_BIGIP_VERSION
    p = b.tm.security.nat.policys.policy

    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/nat/policy/' \
        '~Common~fakepolicy/'
    return p


class TestSourceTranslation(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = MIN_BIGIP_VERSION
        r1 = b.tm.security.nat.source_translations.source_translation
        r2 = b.tm.security.nat.source_translations.source_translation
        assert r1 is not r2

    def test_create_no_args(self, FakeSourceTranslation):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeSourceTranslation.create()


class TestDestinationTranslation(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = MIN_BIGIP_VERSION
        r1 = b.tm.security.nat.destination_translations.destination_translation
        r2 = b.tm.security.nat.destination_translations.destination_translation
        assert r1 is not r2

    def test_create_no_args(self, FakeDestinationTranslation):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeDestinationTranslation.create()


class TestPolicy(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = MIN_BIGIP_VERSION
        r1 = b.tm.security.nat.policys.policy
        r2 = b.tm.security.nat.policys.policy
        assert r1 is not r2

    def test_create_no_args(self, FakePolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePolicy.create()


class TestPolicyRuleSubCollection(object):
    def test_policy_rule_subcollection(self, fakeicontrolsession):
        pc = Rules_s(MakePolicyRules(fakeicontrolsession))
        kind = 'tm:security:nat:policy:rules:rulesstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Rules_s)
        assert kind in list(iterkeys(test_meta))
        assert Rules in test_meta2
