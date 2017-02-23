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


from f5.bigip.tm.sys.management_ip import Management_Ip
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeMgmtIp():
    fake_sys = mock.MagicMock()
    return Management_Ip(fake_sys)


def test_create_no_args(FakeMgmtIp):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeMgmtIp.create()


def test_update_raises(FakeMgmtIp):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeMgmtIp.update()
    assert EIO.value.message == "Management_Ip does not support the update " \
                                "method"


def test_modify_raises(FakeMgmtIp):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeMgmtIp.modify()
    assert EIO.value.message == "Management_Ip does not support the modify " \
                                "method"
