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
"""This module provides classes that specify how RESTful resources are handled.
"""
import urlparse

from f5.bigip.resource import ResourceBase
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import KindTypeMismatch
from f5.bigip.resource import URICreationCollision
from requests.exceptions import HTTPError


class Resource(ResourceBase):
    """Base class to represent a Configurable Resource on the device.

    .. warning::
        Objects instantiated from subclasses of Resource do NOT contain a URI
        (self._meta_data['uri']) at instantiation!

    Resource objects provide the interface for the Creation of new services on
    the device. Once a new service has been created, (via ``self.create`` or
    ``self.load``), the instance constructs its URI and stores it as
    ``self._meta_data['uri']``.

    It is an error to attempt to call
    :meth:`~f5.bigip.resource.Resource.create` or
    :meth:`~f5.bigip.resource.Resource.load` on an instance more than once.
    ``self._meta_data['uri']`` MUST not be changed after creation or load.

    .. note::
        creation query args, and creation hash fragments are stored as
        separate _meta_data values.

    By "Configurable" we mean that submitting JSON via the PUT method to the
    URI managed by subclasses of Resource, changes the state of the
    corresponding service on the device.

    It also means that the URI supports `DELETE`.
    """
    def __init__(self, container):
        """Call to create a client side object to represent a service URI.

        Call _create or _load for a Resource resource to have a
        self._meta_data['uri']!
        """
        super(Resource, self).__init__(container)
        self._meta_data.pop('uri')
        # Creation fails without these.
        self._meta_data['required_creation_parameters'] = set(('uuid',))
        # Refresh fails without these.
        self._meta_data['required_load_parameters'] = set(('uuid',))
        # You can't have more than one of the attrs in any of these sets.
        self._meta_data['exclusive_attributes'] = []
        # You can't set these attributes, only 'read' them.
        self._meta_data['read_only_attributes'] = []

    def _activate_URI(self, selfLinkuri):
        """Call this with a selfLink, after it's returned in _create or _load.

        Each instance is tightly bound to a particular service URI.  When that
        service is created by this library, or loaded from the device, the URI
        is set to self._meta_data['uri'].   This operation can only occur once,
        any subsequent attempt to manipulate self._meta_data['uri'] is
        probably a mistake.

        self.selfLink references a value that is returned as a JSON value from
        the device.  This value contains "localhost" as the domain or the uri.
        "localhost" is only conceivably useful if the client library is run on
        the device itself, so it is replaced with the domain this API used to
        communicate with the device.

        self.selfLink correctly contains a complete uri, that is only _now_
        (post create or load) available to self.

        Now that the complete URI is available to self, it is now possible to
        reference subcollections, as attributes of self!
        e.g. a resource with a uri path like:
        "/mgmt/tm/ltm/pool/~Common~pool_collection1/members"
        The mechanism used to enable this change is to set
        the `allowed_lazy_attributes` _meta_data key to hold values of the
        `attribute_registry` _meta_data key.

        Finally we stash the corrected `uri`, returned hash_fragment, query
        args, and of course allowed_lazy_attributes in _meta_data.

        :param selfLinkuri: the server provided selfLink (contains localhost)
        :raises: URICreationCollision
        """

        # netloc local alias
        uri = urlparse.urlsplit(self._meta_data['bigip']._meta_data['uri'])

        # attrs local alias
        attribute_reg = self._meta_data.get('attribute_registry', {})
        attrs = attribute_reg.values()

        (scheme, domain, path, qarg, frag) = urlparse.urlsplit(selfLinkuri)
        path_uri = urlparse.urlunsplit((scheme, uri.netloc, path, '', ''))
        if not path_uri.endswith('/'):
            path_uri = path_uri + '/'
        qargs = urlparse.parse_qs(qarg)
        self._meta_data.update({'uri': path_uri,
                                'creation_uri_qargs': qargs,
                                'creation_uri_frag': frag,
                                'allowed_lazy_attributes': attrs})

    def _create(self, **kwargs):
        """wrapped by `create` override that in subclasses to customize"""
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this "\
                    "resource, the _meta_data['uri'] is %s and it should"\
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        requests_params = self._handle_requests_params(kwargs)
        key_set = set(kwargs.keys())
        required_minus_received =\
            self._meta_data['required_creation_parameters'] - key_set
        if required_minus_received != set():
            error_message = 'Missing required params: %r'\
                % required_minus_received
            raise MissingRequiredCreationParameter(error_message)

        # Make convenience variable with short names for this method.
        _create_uri = self._meta_data['container']._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # Invoke the REST operation on the device.
        response = session.post(_create_uri, json=kwargs, **requests_params)

        # Post-process the response
        self._local_update(response.json())

        if self.kind != self._meta_data['required_json_kind'] \
           and self.kind != "tm:transaction:commandsstate":
            error_message = "For instances of type '%r' the corresponding"\
                " kind must be '%r' but creation returned JSON with kind: %r"\
                % (self.__class__.__name__,
                   self._meta_data['required_json_kind'],
                   self.kind)
            raise KindTypeMismatch(error_message)

        # Update the object to have the correct functional uri.
        self._activate_URI(self.selfLink)
        return self

    def create(self, **kwargs):
        """Create the resource on the BIG-IP®.

        Uses HTTP POST to the `collection` URI to create a resource associated
        with a new unique URI on the device.

        ..
            Subclasses can customize  this functionality by defining a `create`
            method that wraps and calls this method with appropriate arguments.

            Note this is the one of two fundamental Resource operations that
            returns a different uri (in the returned object) than the uri the
            operation was called on.  The returned uri can be accessed as
            Object.selfLink, the actual uri used by REST operations on the
            object is Object._meta_data['uri'].  The _meta_data['uri'] is the
            same as Object.selfLink with the substring 'localhost' replaced
            with the value of
            Object._meta_data['bigip']._meta_data['hostname'], and without
            query args, or hash fragments.

        :param kwargs: All the key-values needed to create the resource
        NOTE: If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.post method where it will
        be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        :returns: ``self`` - A python object that represents the object's
                  configuration and state on the BIG-IP®.

        """
        self._create(**kwargs)
        return self

    def _load(self, **kwargs):
        """wrapped with load, override that in a subclass to customize"""
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this "\
                    "resource, the _meta_data['uri'] is %s and it should"\
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        requests_params = self._handle_requests_params(kwargs)
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = False
        refresh_session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']
        kwargs.update(requests_params)
        response = refresh_session.get(base_uri, **kwargs)
        self._local_update(response.json())
        self._activate_URI(self.selfLink)
        return self

    def load(self, **kwargs):
        """Load an already configured service into this instance.

        This method uses HTTP GET to obtain a resource from the BIG-IP®.

        ..
            The URI of the target service is constructed from the instance's
            container and **kwargs.
            kwargs typically requires the keys "name" and "partition".
            this may, or may not, be true for a specific service.

        :param kwargs: typically contains "name" and "partition"
        NOTE: If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.get method where it will
        be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        :returns: a Resource Instance (with a populated _meta_data['uri'])
        """
        self._load(**kwargs)
        return self

    def _delete(self, **kwargs):
        """wrapped with delete, override that in a subclass to customize """
        requests_params = self._handle_requests_params(kwargs)
        delete_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # Check the generation for match before delete
        force = self._check_force_arg(kwargs.pop('force', True))
        if not force:
            self._check_generation()

        response = session.delete(delete_uri, **requests_params)
        if response.status_code == 200:
            self.__dict__ = {'deleted': True}

    def delete(self, **kwargs):
        """Delete the resource on the BIG-IP®.

        Uses HTTP DELETE to delete the resource on the BIG-IP®.

        After this method is called, and status_code 200 response is received
        ``instance.__dict__`` is replace with ``{'deleted': True}``

        :param kwargs: The only current use is to pass kwargs to the requests
        API. If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.delete method where it
        will be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!
        """
        # Need to implement checking for ? here.
        self._delete(**kwargs)
        # Need to implement correct teardown here.

    def exists(self, **kwargs):
        """Check for the existence of the named object on the BIG-IP

        Sends an HTTP GET to the URI of the named object and if it fails with
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
        base_uri = self._meta_data['container']._meta_data['uri']
        kwargs.update(requests_params)
        try:
            session.get(base_uri, **kwargs)
        except HTTPError as err:
            if err.response.status_code == 404:
                return False
            else:
                raise
        return True
