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
from f5.sdk_exception import UnsupportedMethod
from f5.sdk_exception import UnsupportedOperation
from f5.sdk_exception import URICreationCollision


class Authn(OrganizingCollection):
    def __init__(self, shared):
        super(Authn, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Roots
        ]


class Roots(Collection):
    def __init__(self, authn):
        super(Roots, self).__init__(authn)
        self._meta_data['allowed_lazy_attributes'] = [Root]

    def get_collection(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support get_collection" % self.__class__.__name__
        )


class Root(Resource):
    def __init__(self, roots):
        super(Root, self).__init__(roots)
        self._meta_data['required_json_kind'] = 'shared:authn:authrootitemstate'

        # The required parameters are a little vague. It turns out that the "user"
        # value that is required is the "link" to the ID
        self._meta_data['required_creation_parameters'] = {'oldPassword', 'newPassword'}

    def _create(self, **kwargs):
        """wrapped by `create` override that in subclasses to customize"""
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this "\
                    "resource, the _meta_data['uri'] is %s and it should"\
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        self._check_exclusive_parameters(**kwargs)
        requests_params = self._handle_requests_params(kwargs)
        self._minimum_one_is_missing(**kwargs)
        self._check_create_parameters(**kwargs)
        kwargs = self._check_for_python_keywords(kwargs)

        # Reduce boolean pairs as specified by the meta_data entry below
        for key1, key2 in self._meta_data['reduction_forcing_pairs']:
            kwargs = self._reduce_boolean_pair(kwargs, key1, key2)

        # Make convenience variable with short names for this method.
        _create_uri = self._meta_data['container']._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        kwargs = self._prepare_request_json(kwargs)

        # Invoke the REST operation on the device.
        response = session.post(_create_uri, json=kwargs, **requests_params)

        # Make new instance of self
        result = self._produce_instance(response)
        return result

    def _local_update(self, rdict):
        super(Root, self)._local_update(rdict)

        # This API returns no kind, so we need to make our own
        self.__dict__.update(dict(kind='shared:authn:authrootitemstate'))

        # This API returns no selfLink, so we need to make our own
        tmos_version = self._meta_data['bigip']._meta_data['tmos_version']
        self_link = 'https://localhost/mgmt/shared/authn/root?ver={0}'.format(tmos_version)
        self.__dict__.update(dict(selfLink=self_link))

    def update(self, **kwargs):
        raise UnsupportedOperation(
            "%s does not support update" % self.__class__.__name__
        )

    def load(self, **kwargs):
        raise UnsupportedOperation(
            "%s does not support load" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        raise UnsupportedOperation(
            "%s does not support modify" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        raise UnsupportedOperation(
            "%s does not support delete" % self.__class__.__name__
        )
