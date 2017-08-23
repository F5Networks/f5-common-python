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

from f5.bigip.tm.asm.policies.character_sets import Character_Sets
from f5.sdk_exception import UnsupportedOperation


import mock
import pytest


@pytest.fixture
def FakeChar():
    fake_policy = mock.MagicMock()
    fake_e = Character_Sets(fake_policy)
    fake_e._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_e


class TestCharacterSets(object):
    def test_create_raises(self, FakeChar):
        with pytest.raises(UnsupportedOperation):
            FakeChar.create()

    def test_delete_raises(self, FakeChar):
        with pytest.raises(UnsupportedOperation):
            FakeChar.delete()
