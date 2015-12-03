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
from f5.bigip.net.route import Route
from f5.bigip.net.selfip import SelfIP
from f5.bigip.net.vlan import Vlan
from f5.bigip.net.vxlan import VXLAN

base_uri = 'net/'


class Net(object):
    def __init__(self, bigip):
        self.interfaces = {}
        self.bigip = bigip

    @property
    def arp(self):
        if 'arp' in self.interfaces:
            return self.interfaces['arp']
        else:
            arp = ARP(self.bigip)
            self.interfaces['arp'] = arp
            return arp

    @property
    def interface(self):
        if 'interface' in self.interfaces:
            return self.interfaces['interface']
        else:
            interface = Interface(self.bigip)
            self.interfaces['interface'] = interface
            return interface

    @property
    def l2gre(self):
        if 'l2gre' in self.interfaces:
            return self.interfaces['l2gre']
        else:
            l2gre = L2GRE(self.bigip)
            self.interfaces['l2gre'] = l2gre
            return l2gre

    @property
    def route(self):
        if 'route' in self.interfaces:
            return self.interfaces['route']
        else:
            route = Route(self.bigip)
            self.interfaces['route'] = route
            return route

    @property
    def selfip(self):
        if 'selfip' in self.interfaces:
            return self.interfaces['selfip']
        else:
            selfip = SelfIP(self.bigip)
            self.interfaces['selfip'] = selfip
            return selfip

    @property
    def vlan(self):
        if 'vlan' in self.interfaces:
            return self.interfaces['vlan']
        else:
            vlan = Vlan(self.bigip)
            self.interfaces['vlan'] = vlan
            return vlan

    @property
    def vxlan(self):
        if 'vxlan' in self.interfaces:
            return self.interfaces['vxlan']
        else:
            vxlan = VXLAN(self.bigip)
            self.interfaces['vxlan'] = vxlan
            return vxlan
