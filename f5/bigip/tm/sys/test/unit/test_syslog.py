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

from f5.bigip.tm.sys.syslog import Syslog
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeSyslog():
    fake_sys = mock.MagicMock()
    return Syslog(fake_sys)


def test_create_raises(FakeSyslog):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeSyslog.create()
    assert str(EIO.value) == "Syslog does not support the create method"


def test_delete_raises(FakeSyslog):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeSyslog.delete()
    assert str(EIO.value) == "Syslog does not support the delete method"
