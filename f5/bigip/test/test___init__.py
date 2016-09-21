# Copyright 2014 F5 Networks Inc.
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

import mock
import pytest

from f5.bigip import BigIP

from f5.bigip.ltm import Ltm
from f5.bigip.net import Net
from f5.bigip.shared import Shared
from f5.bigip.sys import Sys


@pytest.fixture
def FakeBigIP():
    FBIP = BigIP('FakeHostName', 'admin', 'admin')
    FBIP.icontrol = mock.MagicMock()
    return FBIP


def test___get__attr(FakeBigIP):
    bigip_dot_ltm = FakeBigIP.ltm
    assert isinstance(bigip_dot_ltm, Ltm)
    bigip_dot_net = FakeBigIP.net
    assert isinstance(bigip_dot_net, Net)
    bigip_dot_shared = FakeBigIP.shared
    assert isinstance(bigip_dot_shared, Shared)
    bigip_dot_sys = FakeBigIP.sys
    assert isinstance(bigip_dot_sys, Sys)
    with pytest.raises(AttributeError):
        FakeBigIP.this_is_not_a_real_attribute
