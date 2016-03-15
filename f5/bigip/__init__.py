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

from f5.bigip.cm import Cm
from f5.bigip.ltm import Ltm
from f5.bigip.net import Net
from f5.bigip.pycontrol import pycontrol as pc
from f5.bigip.resource import OrganizingCollection
from f5.bigip.sys import Sys
from f5.common import constants as const
from icontrol.session import iControlRESTSession

LOG = logging.getLogger(__name__)
allowed_lazy_attributes = [Cm, Ltm, Net, Sys]


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


class BigIP(OrganizingCollection):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, **kwargs):
        timeout = kwargs.pop('timeout', 30)
        allowed_lazy_attrs = kwargs.pop('allowed_lazy_attributes',
                                        allowed_lazy_attributes)
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        # _meta_data variable values
        iCRS = iControlRESTSession(username, password, timeout=timeout)
        icontrol_inst = _get_icontrol(hostname, username, password)
        # define _meta_data
        self._meta_data = {'allowed_lazy_attributes': allowed_lazy_attrs,
                           'icontrol': icontrol_inst,
                           'hostname': hostname,
                           'uri': 'https://%s/mgmt/tm/' % hostname,
                           'icr_session': iCRS,
                           'device_name': None,
                           'local_ip': None,
                           'bigip': self}
