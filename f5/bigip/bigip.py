"""Classes and functions for configuring BIG-IQ """
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
#

import logging
import os
import requests
import socket

from f5.bigip import interfaces as bigip_interfaces

from f5.bigip.interfaces.arp import ARP
from f5.bigip.interfaces.cluster import Cluster
from f5.bigip.interfaces.device import Device
from f5.bigip.interfaces.iapp import IApp
from f5.bigip.interfaces.interface import Interface
from f5.bigip.interfaces.l2gre import L2GRE
from f5.bigip.interfaces.monitor import Monitor
from f5.bigip.interfaces.nat import NAT
from f5.bigip.interfaces.pool import Pool
from f5.bigip.interfaces.route import Route
from f5.bigip.interfaces.rule import Rule
from f5.bigip.interfaces.selfip import SelfIP
from f5.bigip.interfaces.snat import SNAT
from f5.bigip.interfaces.ssl import SSL
from f5.bigip.interfaces.stat import Stat
from f5.bigip.interfaces.system import System
from f5.bigip.interfaces.virtual_server import VirtualServer
from f5.bigip.interfaces.vlan import Vlan
from f5.bigip.interfaces.vxlan import VXLAN
from f5.bigip.pycontrol import pycontrol as pc
from f5.common import constants as const

LOG = logging.getLogger(__name__)


class BigIP(object):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, timeout=None):
        # get icontrol connection stub
        self.icontrol = self._get_icontrol(hostname, username, password)
        self.icr_session = self._get_icr_session(hostname, username, password)
        self.icr_url = 'https://%s/mgmt/tm' % hostname

        # interface instance cache
        self.interfaces = {}
        self.device_name = None
        self.local_ip = None

    @property
    def iapp(self):
        """iApp interface"""
        if 'iapp' in self.interfaces:
            return self.interfaces['iapp']
        else:
            iapp = IApp(self)
            self.interfaces['iapp'] = iapp
            iapp.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return iapp

    @property
    def system(self):
        """System interface"""
        if 'system' in self.interfaces:
            return self.interfaces['system']
        else:
            system = System(self)
            self.interfaces['system'] = system
            system.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return system

    @property
    def device(self):
        """Device interface"""
        if 'device' in self.interfaces:
            return self.interfaces['device']
        else:
            device = Device(self)
            self.interfaces['device'] = device
            device.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return device

    @property
    def devicename(self):
        """Device Name interface"""
        if not self.devicename:
            if 'device' in self.interfaces:
                self.devicename = self.interfaces['device'].get_device_name()
            else:
                device = Device(self)
                self.interfaces['device'] = device
                self.devicename = device.get_device_name()
        return self.devicename

    @property
    def cluster(self):
        """Cluster interface"""
        if 'cluster' in self.interfaces:
            return self.interfaces['cluster']
        else:
            cluster = Cluster(self)
            self.interfaces['cluster'] = cluster
            cluster.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return cluster

    @property
    def stat(self):
        """Stat interface"""
        if 'stat' in self.interfaces:
            return self.interfaces['stat']
        else:
            stat = Stat(self)
            self.interfaces['stat'] = stat
            stat.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return stat

    @property
    def interface(self):
        """Network Interface interface"""
        if 'interface' in self.interfaces:
            return self.interfaces['interface']
        else:
            interface = Interface(self)
            self.interfaces['interface'] = interface
            interface.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return interface

    @property
    def vlan(self):
        """VLAN interface"""
        if 'vlan' in self.interfaces:
            return self.interfaces['vlan']
        else:
            vlan = Vlan(self)
            self.interfaces['vlan'] = vlan
            vlan.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return vlan

    @property
    def vxlan(self):
        """VXLAN Tunnel interface"""
        if 'vxlan' in self.interfaces:
            return self.interfaces['vxlan']
        else:
            vxlan = VXLAN(self)
            self.interfaces['vxlan'] = vxlan
            vxlan.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return vxlan

    @property
    def l2gre(self):
        """GRE Tunnel interface"""
        if 'l2gre' in self.interfaces:
            return self.interfaces['l2gre']
        else:
            l2gre = L2GRE(self)
            self.interfaces['l2gre'] = l2gre
            l2gre.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return l2gre

    @property
    def arp(self):
        """ARP interface"""
        if 'arp' in self.interfaces:
            return self.interfaces['arp']
        else:
            arp = ARP(self)
            self.interfaces['arp'] = arp
            arp.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return arp

    @property
    def selfip(self):
        """Self IP interface"""
        if 'selfip' in self.interfaces:
            return self.interfaces['selfip']
        else:
            selfip = SelfIP(self)
            self.interfaces['selfip'] = selfip
            selfip.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return selfip

    @property
    def snat(self):
        """SNAT Interface"""
        if 'snat' in self.interfaces:
            return self.interfaces['snat']
        else:
            snat = SNAT(self)
            self.interfaces['snat'] = snat
            snat.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return snat

    @property
    def nat(self):
        """NAT interface"""
        if 'nat' in self.interfaces:
            return self.interfaces['nat']
        else:
            nat = NAT(self)
            self.interfaces['nat'] = nat
            nat.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return nat

    @property
    def route(self):
        """Route interface"""
        if 'route' in self.interfaces:
            return self.interfaces['route']
        else:
            route = Route(self)
            self.interfaces['route'] = route
            route.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return route

    @property
    def rule(self):
        """Rule interface"""
        if 'rule' in self.interfaces:
            return self.interfaces['rule']
        else:
            rule = Rule(self)
            self.interfaces['rule'] = rule
            rule.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return rule

    @property
    def virtual_server(self):
        """Virtual Server interface"""
        if 'virtual_server' in self.interfaces:
            return self.interfaces['virtual_server']
        else:
            virtual_server = VirtualServer(self)
            self.interfaces['virtual_server'] = virtual_server
            virtual_server.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return virtual_server

    @property
    def monitor(self):
        """Monitor interface"""
        if 'monitor' in self.interfaces:
            return self.interfaces['monitor']
        else:
            monitor = Monitor(self)
            self.interfaces['monitor'] = monitor
            monitor.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return monitor

    @property
    def pool(self):
        """Pool interface"""
        if 'pool' in self.interfaces:
            return self.interfaces['pool']
        else:
            pool = Pool(self)
            self.interfaces['pool'] = pool
            pool.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return pool

    @property
    def ssl(self):
        """SSL interface"""
        if 'ssl' in self.interfaces:
            return self.interfaces['ssl']
        else:
            ssl = SSL(self)
            self.interfaces['ssl'] = ssl
            ssl.OBJ_PREFIX = bigip_interfaces.OBJ_PREFIX
            return ssl

    def set_timeout(self, timeout):
        """Set iControl timeout"""
        self.icontrol.set_timeout(timeout)

    def set_folder(self, name, folder='/Common'):
        """Set iControl folder"""
        if not folder.startswith("/"):
            folder = "/" + folder
        self.system.set_folder(folder)
        if name:
            if not name.startswith(folder + "/"):
                return folder + "/" + name
            else:
                return name
        else:
            return None

    def icr_link(self, selfLink):
        """Create iControl REST link"""
        return selfLink.replace('https://localhost/mgmt/tm', self.icr_url)

    def decorate_folder(self, folder='Common'):
        """Decorate folder name"""
        folder = str(folder).replace('/', '')
        return bigip_interfaces.prefixed(folder)

    @staticmethod
    def _get_icontrol(hostname, username, password, timeout=None):
        """Initialize iControl interface"""
        # Logger.log(Logger.DEBUG,
        #           "Opening iControl connections to %s for interfaces %s"
        #            % (self.hostname, self.interfaces))

        if os.path.exists(const.WSDL_CACHE_DIR):
            icontrol = pc.BIGIP(hostname=hostname,
                                username=username,
                                password=password,
                                directory=const.WSDL_CACHE_DIR,
                                wsdls=[])
        else:
            icontrol = pc.BIGIP(hostname=hostname,
                                username=username,
                                password=password,
                                fromurl=True,
                                wsdls=[])

        if timeout:
            icontrol.set_timeout(timeout)
        else:
            icontrol.set_timeout(const.CONNECTION_TIMEOUT)

        return icontrol

    @staticmethod
    def _get_icr_session(hostname, username, password, timeout=None):
        """Get iControl REST Session"""
        icr_session = requests.session()
        icr_session.auth = (username, password)
        icr_session.verify = False
        if hasattr(requests, 'packages'):
            ul3 = requests.packages.urllib3  # @UndefinedVariable
            ul3.disable_warnings(
                category=ul3.exceptions.InsecureRequestWarning
            )
        icr_session.headers.update({'Content-Type': 'application/json'})
        if timeout:
            socket.setdefaulttimeout(timeout)
        else:
            socket.setdefaulttimeout(const.CONNECTION_TIMEOUT)
        return icr_session

    @staticmethod
    def ulong_to_int(ulong_64):
        """Convert ulong to int"""
        high = ulong_64.high
        low = ulong_64.low

        if high < 0:
            high += (1 << 32)
        if low < 0:
            low += (1 << 32)

        return long((high << 32) | low)

    @staticmethod
    def add_folder(folder, name):
        """Add a BIG-IP folder"""
        folder = str(folder).replace("/", "")
        if not str(name).startswith("/" + folder + "/"):
            return "/" + folder + "/" + name
        else:
            return name

    def add_rest_folder(self, url, folder, name):
        """Add a BIG-IP REST folder that uses ~ instead of /"""
        folder = str(folder).replace("/", "")
        if not str(name).startswith("~" + folder + "~"):
            return url + "~" + folder + "~" + name
        else:
            return url + name
