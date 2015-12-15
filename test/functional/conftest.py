# Copyright 2015 F5 Networks Inc.
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

from f5.bigip import BigIP
import pytest


def pytest_addoption(parser):
    parser.addoption("--bigip", action="store",
                     help="BIG-IP hostname or IP address")
    parser.addoption("--username", action="store", help="BIG-IP REST username",
                     default="admin")
    parser.addoption("--password", action="store", help="BIG-IP REST password",
                     default="admin")


def pytest_generate_tests(metafunc):
    assert metafunc.config.option.bigip


@pytest.fixture
def opt_bigip(request):
    return request.config.getoption("--bigip")


@pytest.fixture
def opt_username(request):
    return request.config.getoption("--username")


@pytest.fixture
def opt_password(request):
    return request.config.getoption("--password")


@pytest.fixture
def bigip(opt_bigip, opt_username, opt_password, scope="module"):
    '''bigip fixture'''
    b = BigIP(opt_bigip, opt_username, opt_password)
    return b
