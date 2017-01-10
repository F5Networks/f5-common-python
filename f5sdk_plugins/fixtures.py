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


@pytest.fixture(scope='session')
def bigip(opt_bigip, opt_username, opt_password, opt_port, scope="module"):
    '''bigip fixture'''
    b = BigIP(opt_bigip, opt_username, opt_password, port=opt_port)
    return b


@pytest.fixture(scope='module')
def mgmt_root(opt_bigip, opt_username, opt_password, opt_port, opt_token,
              scope="module"):
    '''bigip fixture'''
    m = ManagementRoot(opt_bigip, opt_username, opt_password, port=opt_port,
                       token=opt_token)
    return m


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
