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
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.asm.tasks import Apply_Policy
from f5.bigip.tm.asm.tasks import Check_Signature
from f5.bigip.tm.asm.tasks import Export_Signature
from f5.bigip.tm.asm.tasks import Update_Signature
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation

import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakeCheckSignature():
    fake_asm = mock.MagicMock()
    fake_chksig = Check_Signature(fake_asm)
    fake_chksig._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_chksig


@pytest.fixture
def FakeExportSignature():
    fake_asm = mock.MagicMock()
    fake_expsig = Export_Signature(fake_asm)
    fake_expsig._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_expsig


@pytest.fixture
def FakeApplyPolicy():
    fake_asm = mock.MagicMock()
    fake_apppol = Apply_Policy(fake_asm)
    fake_apppol._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_apppol


@pytest.fixture
def FakeUpdateSignature():
    fake_asm = mock.MagicMock()
    fake_updsig = Update_Signature(fake_asm)
    fake_updsig._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_updsig


class TestTasksOC(object):
    def test_OC(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks
        assert isinstance(t1, OrganizingCollection)
        assert hasattr(t1, 'check_signatures_s')
        assert hasattr(t1, 'export_signatures_s')
        assert hasattr(t1, 'update_signatures_s')


class TestCheckSignature(object):
    def test_create_raises(self, FakeCheckSignature):
        with pytest.raises(UnsupportedOperation):
            FakeCheckSignature.create()

    def test_modify_raises(self, FakeCheckSignature):
        with pytest.raises(UnsupportedOperation):
            FakeCheckSignature.modify()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.check_signatures_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:check-signatures:check-signatures-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Check_Signature in test_meta2
        assert t._meta_data['object_has_stats'] is False


class TestExportSignature(object):
    def test_modify_raises(self, FakeExportSignature):
        with pytest.raises(UnsupportedOperation):
            FakeExportSignature.modify()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks.export_signatures_s.export_signature
        t2 = b.tm.asm.tasks.export_signatures_s.export_signature
        assert t1 is t2

    def test_create_no_args(self, FakeExportSignature):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeExportSignature.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.export_signatures_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Export_Signature in test_meta2
        assert t._meta_data['object_has_stats'] is False


class TestUpdateSignature(object):
    def test_create_raises(self, FakeUpdateSignature):
        with pytest.raises(UnsupportedOperation):
            FakeUpdateSignature.create()

    def test_modify_raises(self, FakeUpdateSignature):
        with pytest.raises(UnsupportedOperation):
            FakeUpdateSignature.modify()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.update_signatures_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:update-signatures:update-signatures-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Update_Signature in test_meta2
        assert t._meta_data['object_has_stats'] is False


class TestApplyPolicy(object):
    def test_modify_raises(self, FakeApplyPolicy):
        with pytest.raises(UnsupportedOperation):
            FakeApplyPolicy.modify()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks.apply_policy_s.apply_policy
        t2 = b.tm.asm.tasks.apply_policy_s.apply_policy
        assert t1 is t2

    def test_create_no_args(self, FakeApplyPolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeApplyPolicy.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.apply_policy_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Apply_Policy in test_meta2
        assert t._meta_data['object_has_stats'] is False
