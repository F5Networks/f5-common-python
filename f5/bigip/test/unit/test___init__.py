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
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from f5.bigip import ManagementRoot

from f5.bigip.tm.asm import Asm
from f5.bigip.tm.auth import Auth
from f5.bigip.tm.cm import Cm
from f5.bigip.tm.gtm import Gtm
from f5.bigip.tm.ltm import Ltm
from f5.bigip.tm.net import Net
from f5.bigip.tm.shared import Shared
from f5.bigip.tm.sys import Sys
from f5.bigip.tm.util import Util
from f5.bigip.tm.vcmp import Vcmp


@pytest.fixture
def FakeBigIP(fakeicontrolsession):
    FBIP = ManagementRoot('FakeHostName', 'admin', 'admin')
    FBIP.icontrol = mock.MagicMock()
    return FBIP


@pytest.fixture
def FakeBigIPWithPort(fakeicontrolsession):
    FBIP = ManagementRoot('FakeHostName', 'admin', 'admin', port='10443')
    FBIP.icontrol = mock.MagicMock()
    return FBIP


def test___get__attr(FakeBigIP):
    bigip_dot_asm = FakeBigIP.tm.asm
    assert isinstance(bigip_dot_asm, Asm)
    bigip_dot_auth = FakeBigIP.tm.auth
    assert isinstance(bigip_dot_auth, Auth)
    bigip_dot_cm = FakeBigIP.tm.cm
    assert isinstance(bigip_dot_cm, Cm)
    bigip_dot_gtm = FakeBigIP.tm.gtm
    assert isinstance(bigip_dot_gtm, Gtm)
    bigip_dot_ltm = FakeBigIP.tm.ltm
    assert isinstance(bigip_dot_ltm, Ltm)
    bigip_dot_net = FakeBigIP.tm.net
    assert isinstance(bigip_dot_net, Net)
    bigip_dot_shared = FakeBigIP.tm.shared
    assert isinstance(bigip_dot_shared, Shared)
    bigip_dot_sys = FakeBigIP.tm.sys
    assert isinstance(bigip_dot_sys, Sys)
    bigip_dot_util = FakeBigIP.tm.util
    assert isinstance(bigip_dot_util, Util)
    bigip_dot_vcmp = FakeBigIP.tm.vcmp
    assert isinstance(bigip_dot_vcmp, Vcmp)
    with pytest.raises(AttributeError):
        FakeBigIP.tm.this_is_not_a_real_attribute
    assert FakeBigIP.hostname == 'FakeHostName'


def test_invalid_args():
    with pytest.raises(TypeError) as err:
        ManagementRoot('FakeHostName', 'admin', 'admin', badArgs='foobar')
    assert 'Unexpected **kwargs' in str(err.value)


def test_icontrol_version(FakeBigIPWithPort):
    assert hasattr(FakeBigIPWithPort, 'icontrol_version')


def test_non_default_port_number(FakeBigIPWithPort):
    uri = urlparse.urlsplit(FakeBigIPWithPort._meta_data['uri'])
    assert uri.port == 10443
