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

from f5.bigip.cm import CM
from f5.bigip.cm.device import Device
from f5.bigip.ltm import LTM
from f5.bigip.net import Net
from f5.bigip.pycontrol import pycontrol as pc
from f5.bigip.sys import Sys
from f5.common import constants as const
from icontrol.session import iControlRESTSession

LOG = logging.getLogger(__name__)
root_collection_classes = [CM, Device, LTM, Net, Sys]


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


class BigIP(object):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, timeout=None,
                 root_collection_classes=root_collection_classes):
        # get icontrol connection stub
        self.root_collection_classes = root_collection_classes
        self.icontrol = _get_icontrol(hostname, username, password)
        self.icr_uri = 'https://%s/mgmt/tm/' % hostname
        self.icr_session = iControlRESTSession(username, password)

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
