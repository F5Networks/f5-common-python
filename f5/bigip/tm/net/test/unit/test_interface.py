# Copyright 2016 F5 Networks Inc.
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

from f5.bigip.tm.net.interface import Interface
from f5.sdk_exception import UnsupportedOperation


@pytest.fixture
def FakeInterface():
    fake_interface_s = mock.MagicMock()
    return Interface(fake_interface_s)


class TestInterface(object):
    def test_create_raises(self):
        with pytest.raises(UnsupportedOperation):
            i = FakeInterface()
            i.create(name='1.1')

    def test_delete_raises(self):
        with pytest.raises(UnsupportedOperation):
            i = FakeInterface()
            i.delete()
