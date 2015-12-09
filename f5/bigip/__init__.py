"""Classes and functions for configuring BIG-IP"""
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

from f5.bigip import rest_collection

from f5.bigip.cm import CM as cm
from f5.bigip.cm.device import Device as device
from f5.bigip.ltm import LTM as ltm
from f5.bigip.net import Net as net
from f5.bigip.pycontrol import pycontrol as pc
from f5.bigip.sys import Sys as sys
from f5.common import constants as const

LOG = logging.getLogger(__name__)
root_collection_classes = [cm, device, ltm, net, sys]


class BigIP(object):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, timeout=None,
                 root_collection_classes=root_collection_classes):
        # get icontrol connection stub
        self.root_collection_classes = root_collection_classes
        self.icontrol = self._get_icontrol(hostname, username, password)
        self.icr_session = self._get_icr_session(hostname, username, password)
        self.icr_uri = 'https://%s/mgmt/tm' % hostname

        # interface instance cache
        self.device_name = None
        self.local_ip = None

    def __getattr__(self, name):
        for rcc in self.root_collection_classes:
            if name == rcc.__name__.lower():
                iface_collection = rcc(self)
                setattr(self, name, iface_collection)
                return iface_collection
        error_message = "'%s' object has no attribute '%s'"\
            % (self.__class__, name)
        raise AttributeError(error_message)

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
        return rest_collection.prefixed(folder)

    @staticmethod
    def _get_icontrol(hostname, username, password, timeout=None):
        """Initialize iControl interface"""
        # Logger.log(Logger.DEBUG,
        #           "Opening iControl connections to %s for interfaces %s"
        #            % (self.hostname, self.root_collections))

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
