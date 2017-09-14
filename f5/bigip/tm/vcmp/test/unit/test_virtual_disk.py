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

from f5.bigip.tm.vcmp.virtual_disk import Virtual_Disk
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeResource():
    mo = mock.MagicMock()
    return Virtual_Disk(mo)


def test_create(FakeResource):
    with pytest.raises(UnsupportedMethod) as ex:
        FakeResource.create()
    assert "does not support the create method" in str(ex.value)


def test_update(FakeResource):
    with pytest.raises(UnsupportedMethod) as ex:
        FakeResource.update()
    assert "does not support the update method" in str(ex.value)


def test_modify(FakeResource):
    with pytest.raises(UnsupportedMethod) as ex:
        FakeResource.modify()
    assert "does not support the modify method" in str(ex.value)
