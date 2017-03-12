# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from f5.bigip.resource import Collection as BigIpCollection
from f5.bigip.resource import HTTPError
from f5.bigip.resource import OrganizingCollection as BigIpOrganizingCollection
from f5.bigip.resource import PathElement as BigIpPathElement
from f5.bigip.resource import Resource as BigIpResource
from f5.bigip.resource import ResourceBase as BigIpResourceBase
from f5.bigip.resource import UnnamedResource as BigIpUnnamedResource
from f5.sdk_exception import UnsupportedOperation
from f5.sdk_exception import URICreationCollision


class PathElement(BigIpPathElement):
    """Base class to represent a URI path element that does not contain data.

    The BIG-IP® iControl REST API has URIs that are made up of path components
    that do not return data when they are queried.  This class represents
    those elements and does not support any of the CURDLE methods that
    the other objects do.
    """

    def __init__(self, container):
        super(PathElement, self).__init__(container)
        self._meta_data['minimum_version'] = '5.0.0'


class Resource(BigIpResource, PathElement):
    def __init__(self, container):
        super(Resource, self).__init__(container)
        self._meta_data['required_load_parameters'] = {'id', }


class ResourceBase(BigIpResourceBase, PathElement):
    pass


class OrganizingCollection(BigIpOrganizingCollection, ResourceBase):
    pass


class UnnamedResource(BigIpUnnamedResource, ResourceBase):
    pass


class Collection(BigIpCollection, ResourceBase):
    pass


class TaskResource(Resource):
    def __init__(self, container):
        """Call to create a client side object to represent a service URI.

        Call _create or _load for a Resource to have a self._meta_data['uri']!
        """
        super(TaskResource, self).__init__(container)
        # Asm endpoints require object 'id' which is a hash created by BIGIP
        # when object is created.
        self._meta_data['required_load_parameters'] = {'id', }
        # No ASM endpoint supports Stats
        self._meta_data['object_has_stats'] = False

    def _load(self, **kwargs):
        """wrapped with load, override that in a subclass to customize"""
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this " \
                    "resource, the _meta_data['uri'] is %s and it should" \
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        requests_params = self._handle_requests_params(kwargs)
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = True
        refresh_session = self._meta_data['bigip']._meta_data['icr_session']
        uri = self._meta_data['container']._meta_data['uri']
        endpoint = kwargs.pop('id', '')
        # Popping name kwarg as it will cause the uri to be invalid. We only
        # require id parameter
        kwargs.pop('name', '')
        base_uri = uri + endpoint + '/'
        kwargs.update(requests_params)
        for key1, key2 in self._meta_data['reduction_forcing_pairs']:
            kwargs = self._reduce_boolean_pair(kwargs, key1, key2)
        response = refresh_session.get(base_uri, **kwargs)
        # Make new instance of self
        return self._produce_instance(response)

    def load(self, **kwargs):
        """Load an already configured service into this instance.

        This method uses HTTP GET to obtain a resource from the BIG-IP®.

        ..
            The URI of the target service is constructed from the instance's
            container and **kwargs.
            kwargs typically for ASM requires "id" in majority of cases,
            as object links in ASM are using hash(id) instead of names,
            this may, or may not, be true for a specific service.

        :param kwargs: typically contains "id"
        NOTE: If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.get method where it will
        be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        :returns: a Resource Instance (with a populated _meta_data['uri'])
        """
        return self._load(**kwargs)

    def _delete(self, **kwargs):
        """wrapped with delete, override that in a subclass to customize """
        requests_params = self._handle_requests_params(kwargs)

        delete_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        response = session.delete(delete_uri, **requests_params)
        if response.status_code == 200 or 201:
            self.__dict__ = {'deleted': True}

    def delete(self, **kwargs):
        """Delete the Task resource on the BIG-IP®.

        Uses HTTP DELETE to delete the Task resource on the BIG-IP®.

        After this method is called, and status_code 200 or 201 response is
        received ``instance.__dict__`` is replace with ``{'deleted': True}``

        :param kwargs: The only current use is to pass kwargs to the requests
        API. If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.delete method where it
        will be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        """
        # Need to implement checking for ? here.
        self._delete(**kwargs)
        # Need to implement correct teardown here.

    def exists(self, **kwargs):
        """Check for the existence of the Task object on the BIG-IP

        Sends an HTTP GET to the URI of the ASM object and if it fails with
        a :exc:~requests.HTTPError` exception it checks the exception for
        status code of 404 and returns :obj:`False` in that case.

        If the GET is successful it returns :obj:`True`.

        For any other errors are raised as-is.

        :param kwargs: Keyword arguments required to get objects
        NOTE: If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.get method where it will
        be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        :returns: bool -- The objects exists on BIG-IP® or not.
        :raises: :exc:`requests.HTTPError`, Any HTTP error that was not status
                 code 404.
        """
        requests_params = self._handle_requests_params(kwargs)
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = True
        session = self._meta_data['bigip']._meta_data['icr_session']
        uri = self._meta_data['container']._meta_data['uri']
        endpoint = kwargs.pop('id', '')
        # Popping name kwarg as it will cause the uri to be invalid
        kwargs.pop('name', '')
        base_uri = uri + endpoint + '/'
        kwargs.update(requests_params)
        try:
            session.get(base_uri, **kwargs)
        except HTTPError as err:
            if err.response.status_code == 404:
                return False
            else:
                raise
        return True

    def update(self, **kwargs):
        """Update is not supported for ASM Resources

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )
