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

"""iWorkflow® License pool module.

REST URI
    ``http://localhost/mgmt/cm/shared/licensing/pools``

REST Kind
    ``cm:shared:licensing:pools:*``
"""

from f5.iworkflow.resource import Collection
from f5.iworkflow.resource import Resource
from f5.sdk_exception import RequiredOneOf
from six import iterkeys


class Pools_s(Collection):
    """iWorkflow® License pool collection"""
    def __init__(self, licensing):
        super(Pools_s, self).__init__(licensing)
        self._meta_data['required_json_kind'] = \
            'cm:shared:licensing:pools:licensepoolworkercollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Pool]
        self._meta_data['attribute_registry'] = {
            'cm:shared:licensing:pools:licensepoolworkerstate': Pool
        }


class Pool(Resource):
    """iWorkflow® License pool resource"""
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
            ['address', 'username', 'password'],
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
