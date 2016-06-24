# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IQ® License pool module.

REST URI
    ``http://localhost/mgmt/cm/shared/licensing/pools``

GUI Path
    ``Device Management --> License Management``

REST Kind
    ``cm:shared:licensing:pools:licensepoolworkercollectionstate:*``
"""

from requests.exceptions import HTTPError

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import F5SDKError


class LicensePoolMemberReadOnly(F5SDKError):
    pass


class LicensePoolMemberDeleteError(F5SDKError):
    pass


class LicensePoolManagedDeviceError(F5SDKError):
    pass


class Pools_s(Collection):
    """BIG-IQ® License pool collection"""
    def __init__(self, licensing):
        super(Pools_s, self).__init__(licensing)
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] =\
            {'cm:shared:licensing:pools:licensepoolworkerstate':
             Pool}


class Pool(Resource):
    """BIG-IP® License pool resource"""
    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolworkerstate'
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolmembercollectionstate':
            Members_s
        }

    def license_unmanaged_device(self,
                                 hostname=None,
                                 username=None,
                                 password=None):
        pool_members_uri = "%s%s" % (self._meta_data['uri'], 'members')
        unmanaged_device = {"deviceAddress": hostname,
                            "username": username,
                            "password": password}

        self._meta_data['icr_session'].post(pool_members_uri,
                                            json=unmanaged_device)

    def license_managed_device(self,
                               device=None):
        if hasattr(device, 'uuid') and hasattr(device, 'selfLink'):
            pool_members_uri = "%s%s" % (self._meta_data['uri'], 'members')
            device_data = {"deviceReference": {"link": device['selfLink']}}
            self._meta_data['icr_session'].post(
                pool_members_uri, device_data
            )
        else:
            raise LicensePoolManagedDeviceError(
                'supplied device is not a valid Device object'
            )


class Members_s(Collection):
    """BIQ-IQ® License pool members sub-collection"""
    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['required_json_kind'] =\
            'cm:shared:licensing:pools:licensepoolmembercollectionstate'
        self._meta_data['attribute_registry'] =\
            {'cm:shared:licensing:pools:licensepoolmemberstate': Member}


class Member(Resource):
    """BIG-IQ® License pool member sub-collection resource"""
    def __init__(self, members_s):
        super(Member, self).__init__(members_s)
        self._meta_data['required_json_kind'] =\
            'cm:shared:licensing:pools:licensepoolmemberstate'
        self._meta_data['required_creation_parameters'] = {'deviceAddress',
                                                           'username',
                                                           'password'}

    def create(self, **kwargs):
        """Licese Pool Member are created through registration
        on the license pool, not member creation.
            pool.license_managed_device(device)
        or

        pool.license_unmanaged_device(deviceAddress, username, password)
        """
        raise LicensePoolMemberReadOnly(
            'create handled through pool.license_managed_device' +
            ' or pool.license_unmanaged_device methods ')

    def update(self, **kwargs):
        """License Pool Members are Read Only."""
        raise LicensePoolMemberReadOnly('License Pool Members are Read Only')

    def delete(self, **kwargs):
        """Remove license from device
        :param username=: user name for the device to remove license
        :param passsword=: user password for the device to remove license
        :param device_id=: managed device id to remove license
        """
        if hasattr(self, 'deviceReference'):
            self._meta_data['icr_session'].delete(self._meta_data['uri'])
        else:
            try:
                username = kwargs.pop('username')
                password = kwargs.pop('password')
                delete_args = {"uuid": self.uuid,
                               "username": username,
                               "password": password}
                self._meta_data['icr_session'].delete(
                    self._meta_data['uri'], json=delete_args)
            except KeyError:
                error_message = 'You must supply a value for "username"' +\
                                ' and "password" for unmanaged devices'
                raise LicensePoolMemberDeleteError(error_message)

    def exists(self, **kwargs):
        """Check for the existence of the object uuid in the BigIQ
        license pool.

        Sends an HTTP GET to the URI of the named object and if it fails with
        a :exc:~requests.HTTPError` exception it checks the exception for
        status code of 404 and returns :obj:`False` in that case.

        :param kwargs: Keyword arguments required to get objects, "uuid"
        is required.
        """

        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = False
        session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = "%s%s" % (
            self._meta_data['container']._meta_data['uri'],
            kwargs['uuid']
        )
        try:
            response = session.get(base_uri)
        except HTTPError as err:
            if err.response.status_code == 404:
                return False
            else:
                raise
        rdict = response.json()
        if u"uuid" not in rdict:
            # We can add 'or' conditions to be more restrictive.
            return False
        # Only after all conditions are met...
        return True

    def load(self, **kwargs):
        """Loaded the uuid object on the BigIQ

        Sends an HTTP GET to the URI of the named object and if it fails with
        a :exc:~requests.HTTPError` exception it checks the exception for
        status code of 404 and returns :obj:`False` in that case.

        :param kwargs: Keyword arguments required to get objects, "uuid"
        is required.
        """

        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = False
        session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = "%s%s" % (
            self._meta_data['container']._meta_data['uri'],
            kwargs['uuid']
        )
        try:
            response = session.get(base_uri)
            self._local_update(response.json())
            self._activate_URI(self.selfLink)
            return self
        except HTTPError as err:
            if err.response.status_code == 404:
                return None
            else:
                raise
