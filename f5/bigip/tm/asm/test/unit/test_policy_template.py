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
from f5.bigip.tm.asm.policy_templates import Policy_Template
from f5.sdk_exception import UnsupportedOperation
from six import iterkeys


@pytest.fixture
def FakePolicyTemplate():
    fake_asm = mock.MagicMock()
    fake_tmpl = Policy_Template(fake_asm)
    fake_tmpl._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_tmpl


class TestPolicyTemplates(object):
    def test_create_raises(self, FakePolicyTemplate):
        with pytest.raises(UnsupportedOperation):
            FakePolicyTemplate.create()

    def test_modify_raises(self, FakePolicyTemplate):
        with pytest.raises(UnsupportedOperation):
            FakePolicyTemplate.modify()

    def test_delete_raises(self, FakePolicyTemplate):
        with pytest.raises(UnsupportedOperation):
            FakePolicyTemplate.delete()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.policy_templates_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:policy-templates:policy-templatestate'
        assert kind in list(iterkeys(test_meta))
        assert Policy_Template in test_meta2
        assert t._meta_data['object_has_stats'] is False
