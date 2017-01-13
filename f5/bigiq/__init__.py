# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

from f5.bigiq.cm import Cm
from f5.bigiq.resource import PathElement
from f5.bigiq.shared import Shared
from f5.bigiq.tm import Tm
from icontrol.session import iControlRESTSession


class ManagementRoot(PathElement):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, **kwargs):
        timeout = kwargs.pop('timeout', 30)
        port = kwargs.pop('port', 443)
        icontrol_version = kwargs.pop('icontrol_version', '')

        # The BIG-IQ token is called "local", as opposed to BIG-IP's which
        # is called "tmos"
        token = kwargs.pop('token', 'local')
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        # _meta_data variable values
        iCRS = iControlRESTSession(username, password, timeout=timeout,
                                   token=token)
        # define _meta_data
        self._meta_data = {
            'allowed_lazy_attributes': [Cm, Shared, Tm],
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
        self._get_os_version()

    @property
    def hostname(self):
        return self._meta_data['hostname']

    @property
    def icontrol_version(self):
        return self._meta_data['icontrol_version']

    @property
    def tmos_version(self):
        return self._meta_data['tmos_version']

    def _get_os_version(self):
        connect = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['uri'] + \
            'shared/identified-devices/config/device-info'
        response = connect.get(base_uri)
        version = response.json()['version']
        self._meta_data['tmos_version'] = version
