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

from f5.bigip.cm import CM
from f5.bigip.cm.device import Device
from f5.bigip.ltm import LTM
from f5.bigip.net import Net
from f5.bigip.pycontrol import pycontrol as pc
from f5.bigip.sys import Sys
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
    def cm(self):
        """/cm/ REST module interface"""
        if 'cm' in self.interfaces:
            return self.interfaces['cm']
        else:
            cm = CM(self)
            self.interfaces['cm'] = cm
            return cm

    @property
    def ltm(self):
        """/ltm/ REST module interface"""
        if 'ltm' in self.interfaces:
            return self.interfaces['cm']
        else:
            ltm = LTM(self)
            self.interfaces['ltm'] = ltm
            return ltm

    @property
    def net(self):
        """/net/ REST module interface"""
        if 'net' in self.interfaces:
            return self.interfaces['net']
        else:
            net = Net(self)
            self.interfaces['net'] = net
            return net

    @property
    def sys(self):
        """/sys/ REST module interface"""
        if 'sys' in self.interfaces:
            return self.interfaces['sys']
        else:
            sys = Sys(self)
            self.interfaces['sys']
            return sys

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
