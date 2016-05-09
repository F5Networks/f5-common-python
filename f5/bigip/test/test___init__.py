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

import pytest
import urlparse

from f5.bigip import BigIP

from f5.bigip.tm.auth import Auth
from f5.bigip.tm.ltm import Ltm
from f5.bigip.tm.net import Net
from f5.bigip.tm.shared import Shared
from f5.bigip.tm.sys import Sys


@pytest.fixture
def FakeBigIP():
    FBIP = BigIP('FakeHostName', 'admin', 'admin')
    FBIP.icontrol = mock.MagicMock()
    return FBIP


@pytest.fixture
def FakeBigIPWithPort():
    FBIP = BigIP('FakeHostName', 'admin', 'admin', port='10443')
    FBIP.icontrol = mock.MagicMock()
    return FBIP


def test___get__attr(FakeBigIP):
    bigip_dot_auth = FakeBigIP.auth
    assert isinstance(bigip_dot_auth, Auth)
    bigip_dot_ltm = FakeBigIP.ltm
    assert isinstance(bigip_dot_ltm, Ltm)
    bigip_dot_net = bigip.net
    assert isinstance(bigip_dot_net, Net)
    bigip_dot_shared = bigip.shared
    assert isinstance(bigip_dot_shared, Shared)
    bigip_dot_sys = bigip.sys
    assert isinstance(bigip_dot_sys, Sys)
    with pytest.raises(AttributeError):
        FakeBigIP.this_is_not_a_real_attribute
    assert FakeBigIP.hostname == 'FakeHostName'


def test_non_default_port_number(FakeBigIPWithPort):
    uri = urlparse.urlsplit(FakeBigIPWithPort._meta_data['uri'])
    assert uri.port == 10443
