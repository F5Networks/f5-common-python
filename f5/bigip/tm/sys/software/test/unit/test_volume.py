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


from f5.bigip.tm.sys.software.volume import Volume
from f5.sdk_exception import UnsupportedOperation


@pytest.fixture
def FakeVolume():
    fake_software = mock.MagicMock()
    return Volume(fake_software)


def test_create_raises(FakeVolume):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeVolume.create()
    assert EIO.value.message == "Volume does not support the create method."


def test_update_raises(FakeVolume):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeVolume.update()
    assert EIO.value.message == "Volume does not support the update method."


def test_modify_raises(FakeVolume):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeVolume.modify()
    assert EIO.value.message == "Volume does not support the modify method."
