# Copyright 2015-2016 F5 Networks Inc.
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
import pytest

from f5.bigip import BigIP
from f5.bigip import ManagementRoot


def pytest_addoption(parser):
    parser.addoption("--bigip", action="store",
                     help="BIG-IP hostname or IP address")
    parser.addoption("--username", action="store", help="BIG-IP REST username",
                     default="admin")
    parser.addoption("--password", action="store", help="BIG-IP REST password",
                     default="admin")
    parser.addoption("--port", action="store", help="BIG-IP port",
                     default=443)
    parser.addoption("--token", action="store_true",
                     help="Token Authentication")
    parser.addoption("--peer", action="store",
                     help="Peer BIG-IP hostname or IP address", default='none')
    parser.addoption("--release", action="store",
                     help="TMOS version, in dotted format, eg. 12.0.0",
                     default='11.6.0')
    parser.addoption("--vcmp-host", action="store",
                     help="IP address of VCMP enabled host.")


@pytest.fixture(scope='session')
def opt_bigip(request):
    return request.config.getoption("--bigip")


@pytest.fixture(scope='session')
def opt_username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope='session')
def opt_password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope='session')
def opt_port(request):
    return request.config.getoption("--port")


@pytest.fixture(scope='session')
def opt_token(request):
    return request.config.getoption("--token")


@pytest.fixture(scope='session')
def opt_vcmp_host(request):
    return request.config.getoption("--vcmp-host")


@pytest.fixture(scope='session')
def opt_release(request):
    return request.config.getoption("--release")


@pytest.fixture
def opt_peer(request):
    return request.config.getoption("--peer")


@pytest.fixture(scope='session')
def mgmt_root(opt_bigip, opt_username, opt_password, opt_port, opt_token):
    '''bigip fixture'''
    try:
        from pytest import symbols
    except ImportError:
        m = ManagementRoot(opt_bigip, opt_username, opt_password,
                           port=opt_port, token=opt_token)
    else:
        if symbols is not None:
            m = ManagementRoot(symbols.bigip_mgmt_ip_public,
                               symbols.bigip_username,
                               symbols.bigip_password,
                               port=opt_port, token=opt_token)
        else:
            m = ManagementRoot(opt_bigip, opt_username, opt_password,
                               port=opt_port, token=opt_token)
    return m


@pytest.fixture
def bigip(mgmt_root):
    '''bigip fixture'''
    return mgmt_root.tm


@pytest.fixture(scope='module')
def vcmp_host(opt_vcmp_host, opt_username, opt_password, opt_port):
    '''vcmp fixture'''
    m = ManagementRoot(
        opt_vcmp_host, opt_username, opt_password, port=opt_port)
    return m


@pytest.fixture
def peer(opt_peer, opt_username, opt_password, scope="module"):
    '''peer bigip fixture'''
    p = BigIP(opt_peer, opt_username, opt_password)
    return p
