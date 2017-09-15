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
from f5.bigip.tm.auth.source import Source
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeSource():
    fake_source = mock.MagicMock()
    return Source(fake_source)


def test_load_two(fakeicontrolsession):
    b = ManagementRoot('localhost', 'admin', 'admin')
    s1 = b.tm.auth.source.load()
    s2 = b.tm.auth.source.load()
    assert s1 is not s2


def test_create_raises(FakeSource):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeSource.create()
    assert str(EIO.value) == "Source does not support the create method"


def test_delete_raises(FakeSource):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeSource.delete()
    assert str(EIO.value) == "Source does not support the delete method"
