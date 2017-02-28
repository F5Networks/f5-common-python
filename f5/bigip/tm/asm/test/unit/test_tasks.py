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
from f5.bigip.tm.asm.tasks import Export_Policy
from f5.bigip.tm.asm.tasks import Export_Signature
from f5.bigip.tm.asm.tasks import Import_Policy
from f5.bigip.tm.asm.tasks import Import_Vulnerabilities
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
def FakeExportPolicy():
    fake_asm = mock.MagicMock()
    fake_exppol = Export_Policy(fake_asm)
    fake_exppol._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_exppol


@pytest.fixture
def FakeImportPolicy():
    fake_asm = mock.MagicMock()
    fake_imppol = Import_Policy(fake_asm)
    fake_imppol._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_imppol


@pytest.fixture
def FakeUpdateSignature():
    fake_asm = mock.MagicMock()
    fake_updsig = Update_Signature(fake_asm)
    fake_updsig._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_updsig


@pytest.fixture
def FakeImportVuln():
    fake_asm = mock.MagicMock()
    fake_imppol = Import_Vulnerabilities(fake_asm)
    fake_imppol._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_imppol


class TestTasksOC(object):
    def test_OC(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks
        assert isinstance(t1, OrganizingCollection)
        assert hasattr(t1, 'check_signatures_s')
        assert hasattr(t1, 'export_signatures_s')
        assert hasattr(t1, 'update_signatures_s')
        assert hasattr(t1, 'apply_policy_s')
        assert hasattr(t1, 'export_policy_s')
        assert hasattr(t1, 'import_policy_s')


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


class TestExportPolicy(object):
    def test_modify_raises(self, FakeExportPolicy):
        with pytest.raises(UnsupportedOperation):
            FakeExportPolicy.modify()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks.export_policy_s.export_policy
        t2 = b.tm.asm.tasks.export_policy_s.export_policy
        assert t1 is t2

    def test_create_no_args(self, FakeExportPolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeExportPolicy.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.export_policy_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Export_Policy in test_meta2
        assert t._meta_data['object_has_stats'] is False


class TestImportPolicy(object):
    def test_modify_raises(self, FakeImportPolicy):
        with pytest.raises(UnsupportedOperation):
            FakeImportPolicy.modify()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks.import_policy_s.import_policy
        t2 = b.tm.asm.tasks.import_policy_s.import_policy
        assert t1 is t2

    def test_create_no_args(self, FakeImportPolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeImportPolicy.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.import_policy_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Import_Policy in test_meta2
        assert t._meta_data['object_has_stats'] is False


class TestImportVulnerabilities(object):
    def test_modify_raises(self, FakeImportVuln):
        with pytest.raises(UnsupportedOperation):
            FakeImportVuln.modify()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.tasks.import_vulnerabilities_s.import_vulnerabilities
        t2 = b.tm.asm.tasks.import_vulnerabilities_s.import_vulnerabilities
        assert t1 is t2

    def test_create_no_args(self, FakeImportVuln):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeImportVuln.create()

    def test_create_missing_additional_arguments(self, FakeImportVuln):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeImportVuln.create(filename='fake.xml',
                                  policyReference={'link': 'http://fake'})

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.tasks.import_vulnerabilities_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:tasks:import-vulnerabilities:' \
               'import-vulnerabilities-taskstate'
        assert kind in list(iterkeys(test_meta))
        assert Import_Vulnerabilities in test_meta2
        assert t._meta_data['object_has_stats'] is False
