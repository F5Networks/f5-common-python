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
from f5.bigip.tm.asm.attack_types import Attack_Type
from f5.sdk_exception import UnsupportedOperation

import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakeAttackTypes():
    fake_asm = mock.MagicMock()
    fake_atk = Attack_Type(fake_asm)
    fake_atk._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_atk


class TestAttackSignatures(object):
    def test_create_raises(self, FakeAttackTypes):
        with pytest.raises(UnsupportedOperation):
            FakeAttackTypes.create()

    def test_modify_raises(self, FakeAttackTypes):
        with pytest.raises(UnsupportedOperation):
            FakeAttackTypes.modify()

    def test_delete_raises(self, FakeAttackTypes):
        with pytest.raises(UnsupportedOperation):
            FakeAttackTypes.delete()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.attack_types_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:attack-types:attack-typestate'
        assert kind in list(iterkeys(test_meta))
        assert Attack_Type in test_meta2
        assert t._meta_data['object_has_stats'] is False
