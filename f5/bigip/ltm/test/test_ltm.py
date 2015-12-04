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
from f5.bigip.ltm import LTM
from f5.bigip.ltm.monitor import Monitor
from f5.bigip.ltm.nat import NAT
from f5.bigip.ltm.pool import Pool
from f5.bigip.ltm.rule import Rule
from f5.bigip.ltm.snat import SNAT
from f5.bigip.ltm.ssl import SSL
from f5.bigip.ltm.virtual_server import VirtualServer
from mock import MagicMock

import pytest


@pytest.fixture
def ltm():
    bigip = MagicMock()
    ltm = LTM(bigip)
    return ltm


def test_ltm_init(ltm):
    assert isinstance(ltm.interfaces, dict)
    assert not ltm.interfaces


def test_ltm_uri():
    from f5.bigip.ltm import base_uri
    assert base_uri == 'ltm/'


def test_ltm_monitor(ltm):
    ltm.monitor.delete()
    assert isinstance(ltm.monitor, Monitor)
    assert 'monitor' in ltm.interfaces


def test_ltm_nat(ltm):
    ltm.nat.delete()
    assert isinstance(ltm.nat, NAT)
    assert 'nat' in ltm.interfaces


def test_ltm_pool(ltm):
    ltm.pool.delete()
    assert isinstance(ltm.pool, Pool)
    assert 'pool' in ltm.interfaces


def test_ltm_rule(ltm):
    ltm.rule.delete()
    assert isinstance(ltm.rule, Rule)
    assert 'rule' in ltm.interfaces


def test_ltm_snat(ltm):
    ltm.snat.exists = MagicMock()
    ltm.snat.exists()
    assert isinstance(ltm.snat, SNAT)
    assert 'snat' in ltm.interfaces


def test_ltm_ssl(ltm):
    ltm.ssl.client_profile_exits = MagicMock()
    ltm.ssl.client_profile_exits()
    assert isinstance(ltm.ssl, SSL)
    assert 'ssl' in ltm.interfaces


def test_ltm_virtual_server(ltm):
    ltm.vs.delete()
    assert isinstance(ltm.vs, VirtualServer)
    assert 'virtual_server' in ltm.interfaces
