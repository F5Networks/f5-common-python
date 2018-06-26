# coding=utf-8
#
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


#from f5.bigip import BaseManagement as BigipBaseManagement
from f5.bigiq.cm import Cm
from f5.bigiq.resource import PathElement
from f5.bigiq.shared import Shared
from f5.bigiq.tm import Tm
from f5.sdk_exception import F5SDKError
from icontrol.session import iControlRESTSession

from bigip_override import BaseManagement as BigipBaseManagement

import re


class BaseManagement(object):
    def __init__(self, hostname, username, password, **kwargs):
        icrs = kwargs.pop('icrs', None)
        
        self._args = self.__parse_arguments(
            hostname, username, password, **kwargs
        )
        
        if icrs:
            self.icrs = icrs
        else:
            self.icrs = self._get_icr_session()
            
        self._configure_meta_data()

    def __parse_arguments(self, hostname, username, password, **kwargs):
        result = dict(
            hostname=hostname,
            username=username,
            password=password,
            timeout=kwargs.pop('timeout', 30),
            port=kwargs.pop('port', 443),
            icontrol_version=kwargs.pop('icontrol_version', ''),
            verify=kwargs.pop('verify', False),
            # The BIG-IQ token is called "local", as opposed to BIG-IP's which
            # is called "tmos"
            auth_provider=kwargs.pop('auth_provider', 'local'),
            debug=kwargs.pop('debug', False)
        )
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        return result

    def _get_icr_session(self):
        result = iControlRESTSession(self._args['username'], \
                                     self._args['password'], \
                                     timeout=self._args['timeout'], \
                                     auth_provider=self._args['auth_provider'], \
                                     verify=self._args['verify'])
        result.debug = self._args['debug']
        return result
    
    def _configure_meta_data(self):
        self._meta_data = {
            'allowed_lazy_attributes': [Shared, Cm, Tm],
            'hostname': self._args['hostname'],
            'port': self._args['port'],
            'uri': 'https://{0}:{1}/mgmt/'.format(self._args['hostname'], self._args['port']),
								
            'device_name': None,
            'local_ip': None,
            'bigip': self,
            'icontrol_version': self._args['icontrol_version'],
            'username': self._args['username'],
            'password': self._args['password'],
            'tmos_version': None,
            'icr_session': self.icrs,
        }

    @property
    def _debug(self):
        result = []
        if self.icrs._debug:
            result += self.icrs._debug


class RegularManagementRoot(BaseManagement, PathElement):
    def __init__(self, hostname, username, password, **kwargs):
        super(RegularManagementRoot, self).__init__(
            hostname, username, password, **kwargs
        )
        self._set_metadata_uri(hostname)
        self.post_configuration_setup()

    def _set_metadata_uri(self, hostname):
        self._meta_data['uri'] = 'https://{0}:{1}/mgmt/'.format(
            hostname, self._args['port']
        )

    def post_configuration_setup(self):
        self._get_os_version()

    @property
    def hostname(self):
        return self._meta_data['hostname']

    @property
    def icontrol_version(self):
        return self._meta_data['icontrol_version']

    @property
    def tmos_version(self):
        if self._meta_data['tmos_version'] is None:
            self._get_os_version()
        return self._meta_data['tmos_version']

    def _get_os_version(self):
        connect = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['uri'] + \
            'shared/identified-devices/config/device-info'
        response = connect.get(base_uri)
        version = response.json()['version']
        self._meta_data['tmos_version'] = version


class ManagementProxy(object):
    def __new__(cls, hostname, username, password, **kwargs):
        proxy_to = kwargs.pop('proxy_to', None)
        device_group = kwargs.pop('device_group', 'cm-bigip-allBigIpDevices')

        mgmt = ManagementRoot(hostname, username, password, **kwargs)
        uuid = cls._get_identifier(mgmt, proxy_to)
        if uuid is None:
            raise F5SDKError(
                "The specified device was missing a UUID. "
                "This should not happen!"
            )
        bigip = BigipBaseManagement(
            mgmt._args['hostname'],
            mgmt._args['username'],
            mgmt._args['password'],
            port=mgmt._args['port'],
            auth_provider=mgmt._args['auth_provider'],
            icrs=mgmt.icrs
        )
        bigip._meta_data['uri'] = 'https://{0}:{1}/mgmt/shared/resolver/device-groups/{2}/devices/{3}/rest-proxy/mgmt/' \
            .format(mgmt._args['hostname'], mgmt._args['port'], device_group, uuid)
        bigip.post_configuration_setup()
        return bigip

    @staticmethod
    def _get_identifier(mgmt, proxy_to):
        if proxy_to is None:
            raise F5SDKError(
                "An identifier to a device to proxy to must be provided."
            )

        if re.search(r'([0-9-a-z]+\-){4}[0-9-a-z]+', proxy_to, re.I):
            return proxy_to
        return ManagementProxy._get_device_uuid(mgmt, proxy_to)

    @staticmethod
    def _get_device_uuid(mgmt, proxy_to):
        dg = mgmt.shared.resolver.device_groups
        collection = dg.cm_bigip_allbigipdevices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=hostname+eq+'{0}'&$select=uuid".format(
                    proxy_to
                )
            )
        )
        if len(collection) > 1:
            raise F5SDKError(
                "More that one managed device was found with this hostname. "
                "Proxied devices must be unique."
            )
        elif len(collection) == 0:
            raise F5SDKError(
                "No device was found with that hostname"
            )
        else:
            resource = collection.pop()
            return resource.pop('uuid', None)


class ManagementRoot(BaseManagement, PathElement):
    """An interface to a single BIG-IP"""
    def __new__(cls, *args, **kwargs):
        if 'proxy_to' in kwargs:
            return ManagementProxy(*args, **kwargs)
        else:
            return RegularManagementRoot(*args, **kwargs)
