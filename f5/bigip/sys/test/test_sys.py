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
from f5.bigip.sys.iapp import IApp
from f5.bigip.sys.stat import Stat
from f5.bigip.sys import Sys
from f5.bigip.sys.system import System
from mock import MagicMock

import pytest


@pytest.fixture
def sys():
    bigip = MagicMock()
    sys = Sys(bigip)
    return sys


def test_cm_init(sys):
    assert isinstance(sys.collections, dict)
    assert not sys.collections


def test_sys_uri():
    from f5.bigip.sys import base_uri
    assert base_uri == 'sys/'


def test_sys_iapp(sys):
    sys.iapp.get_service = MagicMock()
    sys.iapp.get_service()
    assert isinstance(sys.iapp, IApp)
    assert 'iapp' in sys.collections


def test_sys_stat(sys):
    sys.stat.get_throughput = MagicMock()
    sys.stat.get_throughput()
    assert isinstance(sys.stat, Stat)
    assert 'stat' in sys.collections


def test_sys_system(sys):
    sys.system.get_service = MagicMock()
    sys.system.get_service()
    assert isinstance(sys.system, System)
    assert 'system' in sys.collections
