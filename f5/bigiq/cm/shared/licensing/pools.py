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

REST Kind
    ``cm:shared:licensing:pools:*``
"""

from f5.bigiq.resource import Collection
from f5.bigiq.resource import Resource
from f5.sdk_exception import RequiredOneOf
from six import iterkeys


class Pools_s(Collection):
    """BIG-IQ® License pool collection"""
    def __init__(self, licensing):
        super(Pools_s, self).__init__(licensing)
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolworkercollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolworkerstate': Pool
        }


class Pool(Resource):
    """BIG-IQ® License pool resource"""
    def __init__(self, pool_s):
        super(Pool, self).__init__(pool_s)
        self._meta_data['required_creation_parameters'] = {'baseRegKey', }
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolworkerstate'
        self._meta_data['allowed_lazy_attributes'] = [
            Members_s
        ]
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolmembercollectionstate':
                Members_s
        }


class Members_s(Collection):
    def __init__(self, pool):
        super(Members_s, self).__init__(pool)
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolmembercollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Member]
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolmemberstate': Member
        }


class Member(Resource):
    def __init__(self, members_s):
        super(Member, self).__init__(members_s)
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolmemberstate'

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
        """Deletes a member from an unmanaged license pool

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
        if 'uuid' not in kwargs:
            kwargs['uuid'] = str(self.uuid)

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
