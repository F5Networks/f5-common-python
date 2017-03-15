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


from f5.bigip import BaseManagement as BigipBaseManagement
from f5.iworkflow.cm import Cm
from f5.iworkflow.resource import PathElement
from f5.iworkflow.shared import Shared
from f5.iworkflow.tm import Tm
from f5.sdk_exception import F5SDKError
from icontrol.session import iControlRESTSession

import copy
import re


class BaseManagement(object):
    def __init__(self, hostname, username, password, **kwargs):
        self.args = self.parse_arguments(
            hostname, username, password, **kwargs
        )
        self.icrs = self._get_icr_session(**self.args)
        self.configure_meta_data(**self.args)
        self.set_icr_metadata(self.icrs)

    def parse_arguments(self, *args, **kwargs):
        result = dict(
            timeout=kwargs.pop('timeout', 30),
            port=kwargs.pop('port', 443),
            icontrol_version=kwargs.pop('icontrol_version', ''),
            token=kwargs.pop('token', False)
        )
        if kwargs:
            raise TypeError('Unexpected **kwargs: %r' % kwargs)
        result.update(dict(
            hostname=args[0],
            username=args[1],
            password=args[2]
        ))
        return result

    def _get_icr_session(self, *args, **kwargs):
        return iControlRESTSession(
            username=kwargs['username'],
            password=kwargs['password'],
            timeout=kwargs['timeout'],
            token=kwargs['token']
        )

    def configure_meta_data(self, *args, **kwargs):
        self._meta_data = {
            'allowed_lazy_attributes': [Tm, Cm, Shared],
            'hostname': kwargs['hostname'],
            'port': kwargs['port'],
            'device_name': None,
            'local_ip': None,
            'bigip': self,
            'icontrol_version': kwargs['icontrol_version'],
            'username': kwargs['username'],
            'password': kwargs['password'],
            'tmos_version': None,
        }

    def set_icr_metadata(self, icrs):
        self._meta_data['icr_session'] = icrs


class ManagementRoot(BaseManagement, PathElement):
    """An interface to a single BIG-IP"""
    def __init__(self, hostname, username, password, **kwargs):
        super(ManagementRoot, self).__init__(
            hostname, username, password, **kwargs
        )
        self.set_metadata_uri(**self.args)
        self.post_configuration_setup()

    def set_metadata_uri(self, *args, **kwargs):
        self._meta_data['uri'] = 'https://{0}:{1}/mgmt/'.format(
            kwargs['hostname'], kwargs['port']
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
        return self._meta_data['tmos_version']

    def _get_os_version(self):
        connect = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['uri'] + \
            'shared/identified-devices/config/device-info'
        response = connect.get(base_uri)
        version = response.json()['version']
        self._meta_data['tmos_version'] = version


class ManagementProxy(object):
    def __new__(cls, *args, **kwargs):
        device_group = kwargs.pop('device_group', 'cm-cloud-managed-devices')
        hostname = kwargs.pop('hostname', None)
        uuid = kwargs.pop('uuid', None)
        rest_proxy = kwargs.pop('rest_proxy', None)
        if not uuid and not hostname:
            raise F5SDKError(
                "One of either 'uuid' or 'hostname must be specified."
            )
        elif uuid is not None and hostname is not None:
            raise F5SDKError(
                "The 'uuid' and 'hostname' parameters are mutually exclusive. "
                "You may specify one or the other, but not both."
            )
        if not rest_proxy:
            raise F5SDKError(
                "You must provide a device to proxy REST requests through"
            )
        proxy = copy.deepcopy(rest_proxy)
        uuid = cls._get_identifier(proxy, hostname=hostname, uuid=uuid)
        if uuid is None:
            raise F5SDKError(
                "The specified device was missing a UUID. "
                "This should not happen!"
            )
        bigip = BigipBaseManagement(
            proxy.args['hostname'],
            proxy.args['username'],
            proxy.args['password'],
            port=proxy.args['port']
        )
        bigip.icrs = proxy.icrs
        uri = ''.join([
            'https://{0}:{1}/mgmt/shared/resolver/device-groups/',
            '{2}/devices/{3}/rest-proxy/mgmt/'
        ])
        bigip._meta_data['uri'] = uri.format(
            proxy.args['hostname'],
            proxy.args['port'],
            device_group,
            uuid
        )
        bigip.post_configuration_setup()
        return bigip

    @staticmethod
    def _get_identifier(proxy, hostname=None, uuid=None):
        if uuid is not None:
            if re.search(r'([0-9-a-z]+\-){4}[0-9-a-z]+', uuid, re.I):
                return uuid
        return ManagementProxy._get_device_uuid(proxy, hostname)

    @staticmethod
    def _get_device_uuid(proxy, name):
        dg = proxy.shared.resolver.device_groups
        collection = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=dict(
                params="$filter=hostname+eq+'{0}'&$select=uuid".format(name)
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
