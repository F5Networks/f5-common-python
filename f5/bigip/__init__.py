# coding=utf-8
#
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


from icontrol.session import iControlRESTSession
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from f5.bigip.cm import Cm
from f5.bigip.resource import PathElement
from f5.bigip.shared import Shared
from f5.bigip.tm.auth import Auth as TmAuth
from f5.bigip.tm.cm import Cm as TmCm
from f5.bigip.tm.gtm import Gtm
from f5.bigip.tm.ltm import Ltm
from f5.bigip.tm.net import Net
from f5.bigip.tm.shared import Shared as TmShared
from f5.bigip.tm.sys import Sys
from f5.bigip.tm import Tm
from f5.bigip.tm.transaction import Transactions


class ManagementRoot(PathElement):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, **kwargs):
        timeout = kwargs.pop('timeout', 30)
        port = kwargs.pop('port', 443)
        icontrol_version = kwargs.pop('icontrol_version', '')
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        # _meta_data variable values
        iCRS = iControlRESTSession(username, password, timeout=timeout)
        # define _meta_data
        self._meta_data = {
            'allowed_lazy_attributes': [Tm, Cm, Shared],
            'hostname': hostname,
            'port': port,
            'uri': 'https://%s:%s/mgmt/' % (hostname, port),
            'icr_session': iCRS,
            'device_name': None,
            'local_ip': None,
            'bigip': self,
            'icontrol_version': icontrol_version,
            'username': username,
            'password': password,
            'tmos_version': None,
        }
        self._get_tmos_version()

    @property
    def hostname(self):
        return self._meta_data['hostname']

    @property
    def icontrol_version(self):
        return self._meta_data['icontrol_version']

    @property
    def tmos_version(self):
        return self._meta_data['tmos_version']

    def _get_tmos_version(self):
        connect = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['uri'] + 'tm/sys/'
        response = connect.get(base_uri)
        ver = response.json()
        version = urlparse.parse_qs(
            urlparse.urlparse(ver['selfLink']).query)['ver'][0]
        self._meta_data['tmos_version'] = version


class BigIP(ManagementRoot):
    """A shim class used to access the default config resources in 'mgmt/tm.'

    PLEASE DO NOT ADD ATTRIBUTES TO THIS CLASS.

    This class is depcrated in favor of MangementRoot above. Do not add any
    more objects to the allowed_lazy_attributes list here!

    This class is solely implemented for backwards compatibility.
    """
    def __init__(self, hostname, username, password, **kwargs):
        super(BigIP, self).__init__(hostname, username, password, **kwargs)
        self._meta_data['uri'] = self._meta_data['uri'] + 'tm/'
        self._meta_data['allowed_lazy_attributes'] =\
            [TmAuth, TmCm, Ltm, Gtm, Net, TmShared, Sys, Transactions]
