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
from f5.bigip.tm.security.protocol_inspection import Compliance
from f5.bigip.tm.security.protocol_inspection import Compliances
from f5.bigip.tm.security.protocol_inspection import Profile
from f5.bigip.tm.security.protocol_inspection import Signature

from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeProfile():
    fake_col = mock.MagicMock()
    fake_profile = Profile(fake_col)
    return fake_profile


@pytest.fixture
def FakeSignature():
    fake_col = mock.MagicMock()
    fake_signature = Signature(fake_col)
    return fake_signature


def MakeCompliancelist(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.protocol_inspection.compliances.compliance
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/protocol-inspection/compliance/~Common' \
        '~compliancelst/'
    return p


class TestProfile(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.protocol_inspection.profiles.profile
        r2 = b.tm.security.protocol_inspection.profiles.profile
        assert r1 is not r2

    def test_create_no_args(self, FakeProfile):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeProfile.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.protocol_inspection.profiles.profile.create(
                name='destined_to_fail')


class TestSignature(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.protocol_inspection.signatures.signature
        r2 = b.tm.security.protocol_inspection.signatures.signature
        assert r1 is not r2

    def test_create_no_args(self, FakeSignature):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeSignature.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.protocol_inspection.signatures.signature.create(
                name='destined_to_fail', partition='Common')


class TestCompliance(object):
    def test_compliance_subcollection(self, fakeicontrolsession):
        pc = Compliances(MakeCompliancelist(fakeicontrolsession))
        kind = 'tm:security:protocol-inspection:compliance:compliancestate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Compliances)
        assert kind in list(iterkeys(test_meta))
        assert Compliance in test_meta2
