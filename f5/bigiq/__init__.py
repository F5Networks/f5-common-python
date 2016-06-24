# coding=utf-8
#
"""Classes and functions for configuring BIG-IQ"""
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
from urlparse import parse_qs
from urlparse import urlparse


from f5.bigiq.cm import Cm
from f5.bigiq.tm import Tm
from f5.bigiq.shared import Shared
from f5.bigip.resource import PathElement


class ManagementRoot(PathElement):
    """An interface to a single BIG-IQ"""
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
            'allowed_lazy_attributes': [Cm, Tm, Shared],
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
        version = parse_qs(urlparse(ver['selfLink']).query)['ver'][0]
        self._meta_data['tmos_version'] = version
