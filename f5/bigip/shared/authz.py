# coding=utf-8
#
#  Copyright 2017 F5 Networks Inc.
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


from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import ConstraintError
from f5.sdk_exception import MissingUpdateParameter


class Authz(OrganizingCollection):
    def __init__(self, shared):
        super(Authz, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Tokens_s
        ]


class Tokens_s(Collection):
    def __init__(self, authz):
        super(Tokens_s, self).__init__(authz)
        self._meta_data['required_json_kind'] = 'shared:authz:tokens:authtokencollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Token]
        self._meta_data['attribute_registry'] = {
            'shared:authz:tokens:authtokenitemstate': Token
        }


class Token(Resource):
    def __init__(self, tokens):
        super(Token, self).__init__(tokens)
        self._meta_data['required_json_kind'] = 'shared:authz:tokens:authtokenitemstate'

        # The required parameters are a little vague. It turns out that the "user"
        # value that is required is the "link" to the ID
        self._meta_data['required_creation_parameters'] = {'token', 'user'}

    def update(self, **kwargs):
        self._validate_params(**kwargs)
        return self._update(**kwargs)

    def modify(self, **kwargs):
        self._validate_timeout(**kwargs)
        return self._modify(**kwargs)

    def _validate_params(self, **kwargs):
        self._validate_timeout(**kwargs)
        self._validate_user(**kwargs)

    def _validate_user(self, **kwargs):
        try:
            assert 'user' in kwargs
            assert 'link' in kwargs['user']
        except AssertionError:
            raise MissingUpdateParameter(
                "The 'user' parameter is required when updating."
            )

    def _validate_timeout(self, **kwargs):
        timeout = kwargs.get('timeout', None)
        try:
            if timeout is not None and int(timeout) > 36000:
                raise ConstraintError(
                    "The provided timeout exceeds the limit of 36000."
                )
        except ValueError:
            raise ConstraintError(
                "The provided timeout must be a number between 1 and 36000."
            )
