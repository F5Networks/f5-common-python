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
from f5.bigip.net.arp import ARP
from f5.bigip.net.interface import Interface
from f5.bigip.net.l2gre import L2GRE
from f5.bigip.net import Net
from f5.bigip.net.route import Route
from f5.bigip.net.selfip import SelfIP
from f5.bigip.net.vlan import Vlan
from f5.bigip.net.vxlan import VXLAN
from mock import MagicMock

import pytest


@pytest.fixture
def net():
    bigip = MagicMock()
    net = Net(bigip)
    return net


def test_net_init(net):
    assert isinstance(net.interfaces, dict)
    assert not net.interfaces


def test_net_uri():
    from f5.bigip.net import base_uri
    assert base_uri == 'net/'


def test_net_arp(net):
    net.arp.exists = MagicMock()
    net.arp.exists()
    assert isinstance(net.arp, ARP)
    assert 'arp' in net.interfaces


def test_net_interface(net):
    net.interface.get_interfaces = MagicMock()
    net.interface.get_interfaces()
    assert isinstance(net.interface, Interface)
    assert 'interface' in net.interfaces


def test_net_l2gre(net):
    net.l2gre.profile_exists = MagicMock()
    net.l2gre.profile_exists()
    assert isinstance(net.l2gre, L2GRE)
    assert 'l2gre' in net.interfaces


def test_net_route(net):
    net.route.exists = MagicMock()
    net.route.exists()
    assert isinstance(net.route, Route)
    assert 'route' in net.interfaces


def test_net_selfip(net):
    net.selfip.exists = MagicMock()
    net.selfip.exists()
    assert isinstance(net.selfip, SelfIP)
    assert 'selfip' in net.interfaces


def test_net_vlan(net):
    net.vlan.exists = MagicMock()
    net.vlan.exists()
    assert isinstance(net.vlan, Vlan)
    assert 'vlan' in net.interfaces


def test_net_vxlan(net):
    net.vxlan.exists = MagicMock()
    net.vxlan.exists()
    assert isinstance(net.vxlan, VXLAN)
    assert 'vxlan' in net.interfaces
