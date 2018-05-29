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
from f5.bigip.tm.security.nat import Rule
from f5.bigip.tm.security.nat import Rules_s
from f5.bigip.tm.security.nat import Source_Translation
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeSrcTranslation():
    fake_col = mock.MagicMock()
    fake_srctranslation = Source_Translation(fake_col)
    return fake_srctranslation


@pytest.fixture
def FakeDstTranslation():
    fake_col = mock.MagicMock()
    fake_Dsttranslation = Destination_Translation(fake_col)
    return fake_Dsttranslation


@pytest.fixture
def FakePolicy():
    fake_col = mock.MagicMock()
    fake_policy = Policy(fake_col)
    return fake_policy


@pytest.fixture
def FakeRule():
    fake_col = mock.MagicMock()
    fake_rule = Rule(fake_col)
    return fake_rule


def MakeSrcTranslation(fakeicontrolsession):
    a = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = a.tm.security.nat.source_translations.source_translation
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/nat/source-translation/~Common' \
        '~testsrctranslatiom/'
    return p


def MakeDstTranslation(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.nat.destination_translations.destination_translation
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/nat/destination-translation/~Common' \
        '~testdesttranslation/'
    return p


def MakeNatPolicy(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    b._meta_data['tmos_version'] = '12.1.0'
    p = b.tm.security.nat.policy_s.policy
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/firewall/policy/' \
        '~Common~fakepolicy/'
    return p


class TestSrcTranslation(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '12.1.0'
        s1 = b.tm.security.nat.source_translations.source_translation
        s2 = b.tm.security.nat.source_translations.source_translation
        assert s1 is not s2

    def test_create_no_args(self, FakeSrcTranslation):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeSrcTranslation.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '12.1.0'
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.nat.source_translations.source_translation.create(
                name='destined_to_fail')


class TestDstTranslation(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '12.1.0'
        d1 = b.tm.security.nat.destination_translations.destination_translation
        d2 = b.tm.security.nat.destination_translations.destination_translation
        assert d1 is not d2

    def test_create_no_args(self, FakeDstTranslation):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeDstTranslation.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '12.1.0'
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.nat.destination_translations.destination_translation.create(
                name='destined_to_fail')


class TestPolicy(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '12.1.0'
        p1 = b.tm.security.nat.policy_s.policy
        p2 = b.tm.security.nat.policy_s.policy
        assert p1 is not p2

    def test_create_no_arguments(self, FakePolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePolicy.create()


class TestPolicyRuleSubCollection(object):
    def test_policy_rule_subcollection(self, fakeicontrolsession):
        pc = Rules_s(MakeNatPolicy(fakeicontrolsession))
        pc._meta_data['tmos_version'] = '12.1.0'
        kind = 'tm:security:nat:policy:rules:rulesstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Rules_s)
        assert kind in list(iterkeys(test_meta))
        assert Rule in test_meta2
