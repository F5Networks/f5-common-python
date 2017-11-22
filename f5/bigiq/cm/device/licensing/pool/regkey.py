# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""BIG-IQ® license pool regkeys.

REST URI
    ``http://localhost/mgmt/cm/device/licensing/pool/regkey/licenses``

REST Kind
    ``cm:device:licensing:pool:regkey:licenses:*``
"""

import os
import time
import uuid

from f5.bigiq.resource import Collection
from f5.bigiq.resource import OrganizingCollection
from f5.bigiq.resource import Resource
from f5.sdk_exception import F5SDKError
from f5.sdk_exception import RequiredOneOf
from six import iterkeys


class Regkey(OrganizingCollection):
    def __init__(self, pool):
        super(Regkey, self).__init__(pool)
        self._meta_data['allowed_lazy_attributes'] = [
            Licenses_s
        ]


class Licenses_s(Collection):
    def __init__(self, regkey):
        super(Licenses_s, self).__init__(regkey)
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:regkeypoollicensecollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Licenses]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:regkeypoollicensestate': Licenses  # NOQA
        }


class Licenses(Resource):
    def __init__(self, licenses_s):
        super(Licenses, self).__init__(licenses_s)
        self._meta_data['required_creation_parameters'] = {'name', }
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:regkeypoollicensestate'
        self._meta_data['allowed_lazy_attributes'] = [
            Offerings_s
        ]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingcollectionstate': Offerings_s  # NOQA
        }


class Offerings_s(Collection):
    def __init__(self, license):
        super(Offerings_s, self).__init__(license)
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingcollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Offerings]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingstate': Offerings  # NOQA
        }


class Offerings(Resource):
    def __init__(self, offerings_s):
        super(Offerings, self).__init__(offerings_s)
        self._meta_data['required_creation_parameters'] = {'regKey', }
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Members_s]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkey:members:regkeypoollicensemembercollectionstate': Members_s
        }


class Members_s(Collection):
    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkey:members:regkeypoollicensemembercollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Members]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkey:members:regkeypoollicensememberstate': Members
        }


class Members(Resource):
    def __init__(self, members_s):
        super(Members, self).__init__(members_s)
        self._meta_data['required_json_kind'] = 'cm:device:licensing:pool:regkey:licenses:item:offerings:regkey:members:regkeypoollicensememberstate'

        # This set is empty because the creation checking is done as
        # a required_one_of in the create() method
        self._meta_data['required_creation_parameters'] = set()

    def create(self, **kwargs):
        required_one_of = [
            ['deviceAddress', 'username', 'password'],
            ['deviceReference']
        ]

        args = set(iterkeys(kwargs))

        # Check to see if the user supplied any of the sets of required
        # arguments.
        has_any = [set(x).issubset(args) for x in required_one_of]

        if len([x for x in has_any if x is True]) == 1:
            # Only one of the required argument sets can be provided
            # so if more than that are provided, it is an error.
            return self._create(**kwargs)

        raise RequiredOneOf(required_one_of)

    def delete(self, **kwargs):
        """Deletes a member from a license pool

        You need to be careful with this method. When you use it, and it
        succeeds on the remote BIG-IP, the configuration of the BIG-IP
        will be reloaded. During this process, you will not be able to
        access the REST interface.

        This method overrides the Resource class's method because it requires
        that extra json kwargs be supplied. This is not a behavior that is
        part of the normal Resource class's delete method.

        :param kwargs:
        :return:
        """
        if 'id' not in kwargs:
            # BIG-IQ requires that you provide the ID of the members to revoke
            # a license from. This ID is already part of the deletion URL though.
            # Therefore, if you do not provide it, we enumerate it for you.
            delete_uri = self._meta_data['uri']
            if delete_uri.endswith('/'):
                delete_uri = delete_uri[0:-1]
                kwargs['id'] = os.path.basename(delete_uri)
            uid = uuid.UUID(kwargs['id'], version=4)
            if uid.hex != kwargs['id'].replace('-', ''):
                raise F5SDKError(
                    "The specified ID is invalid"
                )

        requests_params = self._handle_requests_params(kwargs)
        kwargs = self._check_for_python_keywords(kwargs)
        kwargs = self._prepare_request_json(kwargs)

        delete_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # Check the generation for match before delete
        force = self._check_force_arg(kwargs.pop('force', True))
        if not force:
            self._check_generation()

        response = session.delete(delete_uri, json=kwargs, **requests_params)
        if response.status_code == 200:
            self.__dict__ = {'deleted': True}

        # This sleep is necessary to prevent BIG-IQ from being able to remove
        # a license. It happens in certain cases that assignments can be revoked
        # (and license deletion started) too quickly. Therefore, we must introduce
        # an artificial delay here to prevent revoking from returning before
        # BIG-IQ would be ready to remove the license.
        time.sleep(1)
