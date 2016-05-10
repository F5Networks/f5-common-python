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

from f5.bigip.mixins import UnsupportedMethod
from f5.bigip.tm.sys.httpd import Httpd


@pytest.fixture
def FakeHttpd():
    fake_sys = mock.MagicMock()
    return Httpd(fake_sys)


def test_create_raises(FakeHttpd):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeHttpd.create()
    assert EIO.value.message == "Httpd does not support the create method"


def test_delete_raises(FakeHttpd):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeHttpd.delete()
    assert EIO.value.message == "Httpd does not support the delete method"
