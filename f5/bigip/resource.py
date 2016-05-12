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

THE MOST IMPORTANT THING TO KNOW ABOUT THIS API IS THAT YOU CAN DIRECTLY INFER
REST URIs FROM PYTHON EXPRESSIONS, AND VICE VERSA.

Examples:

 * Expression:     bigip = BigIP('a', 'b', 'c')
 * URI Returned:   https://a/mgmt/tm/

 * Expression:     bigip.ltm
 * URI Returned:   https://a/mgmt/tm/ltm/

 * Expression:     pools1 = bigip.ltm.pools
 * URI Returned:   https://a/mgmt/tm/ltm/pool

 * Expression:     pool_a = pools1.create(partition="Common", name="foo")
 * URI Returned:   https://a/mgmt/tm/ltm/pool/~Common~foo

There are different types of resources published by the BIG-IP® REST Server,
they are represented by the classes in this module.

We refer to a server-provided resource as a "service".  Thus far all URI
referenced resources are "services" in this sense.

We use methods named Create, Refresh, Update, Load, and Delete to manipulate
BIG-IP® device services.

Methods:

  * create -- uses HTTP POST, creates a new resource and with its own URI on
    the device
  * refresh -- uses HTTP GET, obtains the state of a device resource, and sets
    the representing Python Resource Object tracks device state via its attrs
  * update -- uses HTTP PUT, submits a new configuration to the device resource
     and sets the Resource attrs to the state the device reports
  * load -- uses HTTP GET, obtains the state of an existing resource on the
    device and sets the Resource attrs to that state
  * delete -- uses HTTP DELETE, removes the resource from the device, and sets
    self.__dict__ to {'deleted': True}

Available Classes:
    * ResourceBase -- only `refresh` is generally supported in all resource
      types, this class provides `refresh`. ResourceBase objects are usually
      instantiated via setting lazy attributes. ResourceBase provides a
      constructor to match its call in LazyAttributeMixin.__getattr__. The
      expected behavior is that all resource subclasses depend on this
      constructor to correctly set their self._meta_data['uri'].
      All ResourceBase objects (except BIG-IPs) have a container (BIG-IPs
      contain themselves).  The container is the object the ResourceBase is an
      attribute of.
    * OrganizingCollection -- These resources support lists of "reference"
      "links". These are json blobs without a Python class representation.
        Example URI_path:  /mgmt/tm/ltm/
    * Collection -- These resources support lists of ResourceBase Objects.
        Example URI_path:  /mgmt/tm/ltm/nat
    * Resource -- These resources are the only resources that support
      `create`, `update`, and `delete` operations.  Because they support HTTP
      post (via _create) they uniquely depend on 2 uri's, a uri that supports
      the creating post, and the returned uri of the newly created resource.
        Example URI_path:  /mgmt/tm/ltm/nat/~Common~testnat1
"""
import keyword
import re
import tokenize
import urlparse

from f5.bigip.mixins import LazyAttributeMixin
from f5.bigip.mixins import ToDictMixin
from f5.sdk_exception import F5SDKError
from requests.exceptions import HTTPError


class RequestParamKwargCollision(F5SDKError):
    pass


class KindTypeMismatch(F5SDKError):
    """Raise this when server JSON keys are incorrect for the Resource type."""
    pass


class DeviceProvidesIncompatibleKey(F5SDKError):
    """Raise this when server JSON keys are incompatible with Python."""
    pass


class InvalidResource(F5SDKError):
    """Raise this when a caller tries to invoke an unsupported CRUDL op.

    All resources support `refresh` and `raw`.
    Only `Resource`'s support `load`, `create`, `update`, and `delete`.
    """
    pass


class MissingRequiredCreationParameter(F5SDKError):
    """Various values MUST be provided to create different Resources."""
    pass


class MissingRequiredReadParameter(F5SDKError):
    """Various values MUST be provided to refresh some Resources."""
    pass


class UnregisteredKind(F5SDKError):
    """The returned server JSON `kind` key wasn't expected by this Resource."""
    pass


class GenerationMismatch(F5SDKError):
    """The server reported BIG-IP® is not the expacted value."""
    pass


class InvalidForceType(ValueError):
    """Must be of type bool."""
    pass


class URICreationCollision(F5SDKError):
    """self._meta_data['uri'] can only be assigned once. In create or load."""
    pass


class UnsupportedOperation(F5SDKError):
    """Object does not support the method that was called."""
    pass


class PathElement(LazyAttributeMixin):
    """Base class to represent a URI path element that does not contain data.

    The BIG-IP® iControl REST API has URIs that are made up of path components
    that do not return data when they are queried.  This class represents
    those elements and does not support any of the CURDLE methods that
    the other objects do.
    """
    def __init__(self, container):
        self._meta_data = {
            'container': container,
            'bigip': container._meta_data['bigip'],
            'icr_session': container._meta_data['icr_session'],
            'icontrol_version': container._meta_data['icontrol_version']
        }
        self._set_meta_data_uri()

    def _set_meta_data_uri(self):
        base_uri = self.__class__.__name__.lower()
        if isinstance(self, Collection):
            # Handle 'terminal s or _s'
            if self.__class__.__name__.lower()[-2:] == '_s':
                endind = 2
            else:
                endind = 1
            base_uri = self.__class__.__name__.lower()[:-endind]
        endpoint = base_uri.replace('_', '-')
        final_uri =\
            self._meta_data['container']._meta_data['uri'] + endpoint + '/'
        self._meta_data['uri'] = final_uri

    def _check_load_parameters(self, **kwargs):
        '''Params given to load should at least satisfy required params.

        :params: kwargs
        :raises: MissingRequiredReadParameter
        '''
        key_set = set(kwargs.keys())
        required_minus_received =\
            self._meta_data['required_load_parameters'] - key_set
        if required_minus_received != set():
            error_message = 'Missing required params: %r'\
                % required_minus_received
            raise MissingRequiredReadParameter(error_message)

    def _local_update(self, rdict):
        """Call this with a response dictionary to update instance attrs.

        If the response has only valid keys, stash meta_data, replace __dict__,
        and reassign meta_data.

        :param rdict: response attributes derived from server JSON
        """
        sanitized = self._check_keys(rdict)
        temp_meta = self._meta_data
        self.__dict__ = sanitized
        self._meta_data = temp_meta

    def _check_keys(self, rdict):
        """Call this from _local_update to validate response keys

        disallowed server-response json keys:
        1. The string-literal '_meta_data'
        2. strings that are not valid Python 2.7 identifiers
        3. strings that are Python keywords
        4. strings beginning with '__'.

        :param rdict: from response.json()
        :raises: DeviceProvidesIncompatibleKey
        :returns: checked response rdict
        """
        if '_meta_data' in rdict:
            error_message = "Response contains key '_meta_data' which is "\
                "incompatible with this API!!\n Response json: %r" % rdict
            raise DeviceProvidesIncompatibleKey(error_message)
        for x in rdict:
            if not re.match(tokenize.Name, x):
                error_message = "Device provided %r which is disallowed"\
                    " because it's not a valid Python 2.7 identifier." % x
                raise DeviceProvidesIncompatibleKey(error_message)
            elif keyword.iskeyword(x):
                error_message = "Device provided %r which is disallowed"\
                    " because it's a Python keyword." % x
                raise DeviceProvidesIncompatibleKey(error_message)
            elif x.startswith('__'):
                error_message = "Device provided %r which is disallowed"\
                    ", it mangles into a Python non-public attribute." % x
                raise DeviceProvidesIncompatibleKey(error_message)
        return rdict

    def _check_force_arg(self, force):
        if not isinstance(force, bool):
            raise InvalidForceType("force parameter must be type bool")
        return force

    def _check_generation(self):
        '''Check that the generation on the BIG-IP® matches the object

        This will do a get to the objects URI and check that the generation
        returned in the JSON matches the one the object currently has.  If it
        does not it will raise the `GenerationMismatch` exception.
        '''

        session = self._meta_data['bigip']._meta_data['icr_session']
        response = session.get(self._meta_data['uri'])
        current_gen = response.json().get('generation', None)
        if current_gen is not None and current_gen != self.generation:
            error_message = ("The generation of the object on the BigIP " +
                             "(" + str(current_gen) + ")" +
                             " does not match the current object" +
                             "(" + str(self.generation) + ")")
            raise GenerationMismatch(error_message)

    @property
    def raw(self):
        """Display the attributes that the current object has and their values.

        :returns: A dictionary of attributes and their values
        """
        return self.__dict__


class ResourceBase(PathElement, ToDictMixin):
    """Base class for all BIG-IP® iControl REST API endpoints.

    The BIG-IP® is represented by an object that converts device-published
    uri's into Python objects. Each uri maps to a Python object. The
    mechanism for instantiating these objects is the __getattr__ Special
    Function in the LazyAttributeMixin. When a registered attribute is `dot`
    referenced, on the device object (e.g. ``bigip.ltm`` or simply ``bigip``),
    an appropriate object is instantiated and attributed to the referencing
    object:

    .. code-block:: python

        bigip.ltm = LTM(bigip)
        bigip.ltm.nats
        nat1 = bigip.ltm.nats.nat.create('Foo', 'Bar', '0.1.2.3', '1.2.3.4')

    This can be shortened to just the last line:

    .. code-block:: python

        nat1 = bigip.ltm.nats.nat.create('Foo', 'Bar', '0.1.2.3', '1.2.3.4')

    Critically this enforces a convention relating device published uris to
    API objects, in a hierarchy similar to the uri paths.  I.E. the uri
    corresponding to a ``Nats`` object is ``mgmt/tm/ltm/nat/``. If you
    query the BIG-IP's uri (e.g. print(bigip._meta_data['uri']) ), you'll see
    that it ends in:
    ``/mgmt/tm/``, if you query the ``ltm`` object's uri
    (e.g. print(bigip.ltm._meta_data['uri']) ) you'll see it ends in
    ``/mgmt/tm/ltm/``.

    In general the objects build a required `self._meta_data['uri']` attribute
    by:
    1. Inheriting this class.
    2. calling super(Subclass, self).__init__(container)
    3. self.uri = self.container_uri['uri'] + '/' + self.__class__.__name__

    The net result is a succinct mapping between uri's and objects,
    that represents objects in a hierarchical relationship similar to the
    device's uri path hierarchy.
    """
    def __init__(self, container):
        """Call this with containing_object_instance.FOO

        Where FOO is a concrete subclass of this class, ResourceBase.  The '.'
        operator passes "FOO" to the __getattr__ method of the
        containing_object_instance which instantiates it as the appropriate
        sub-type of ResourceBase.

        Since all ResourceBases sub-types must support the `refresh` method, it
        is defined here, in the base class.
        NOTE: The BIG-IP® uri 'mgmt/tm/' uniquely passes itself to this
        constructor as the "container".

        :param container: instance is an attribute of a ResourceBase container
        """
        super(ResourceBase, self).__init__(container)

    def _update(self, **kwargs):
        """wrapped with update, override that in a subclass to customize"""
        requests_params = self._handle_requests_params(kwargs)
        update_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        read_only = self._meta_data.get('read_only_attributes', [])

        # Get the current state of the object on BIG-IP® and check the
        # generation Use pop here because we don't want force in the data_dict
        force = self._check_force_arg(kwargs.pop('force', False))
        if not force:
            self._check_generation()

        # Save the meta data so we can add it back into self after we
        # load the new object.
        temp_meta = self.__dict__.pop('_meta_data')

        # Need to remove any of the Collection objects from self.__dict__
        # because these are subCollections and _meta_data and
        # other non-BIG-IP® attrs are not removed from the subCollections
        # See issue #146 for details
        for key, value in self.__dict__.items():
            if isinstance(value, Collection):
                self.__dict__.pop(key, '')
        data_dict = self.to_dict()

        # Remove any read-only attributes from our data_dict before we update
        # the data dict with the attributes.  If they pass in read-only attrs
        # in the method call we are going to let BIG-IP® let them know about it
        # when it fails
        for attr in read_only:
            data_dict.pop(attr, '')

        data_dict.update(kwargs)
        response = session.put(update_uri, json=data_dict, **requests_params)
        self._meta_data = temp_meta
        self._local_update(response.json())

    def update(self, **kwargs):
        """Update the configuration of the resource on the BIG-IP®.

        This method uses HTTP PUT alter the resource state on the BIG-IP®.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.

        Various edge cases are handled:
        * read-only attributes that are unchangeable are removed

        :param kwargs: keys and associated values to alter on the device
        NOTE: If kwargs has a 'requests_params' key the corresponding dict will
        be passed to the underlying requests.session.put method where it will
        be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!

        """
        # Need to implement checking for valid params here.
        self._update(**kwargs)

    def _handle_requests_params(self, kwargs):
        """Validate parameters that will be passed to the requests verbs.

        This method validates that there is no conflict in the names of the
        requests_params passed to the function an the other kwargs.  It also
        ensures that the required request parameters for the object are
        added to the request params that are passed into the verbs.  An
        example of the latter is ensuring that a certain version of the API
        is always called to add 'ver=11.6.0' to the url.
        """
        requests_params = kwargs.pop('requests_params', {})
        for param in requests_params:
            if param in kwargs:
                error_message = 'Requests Parameter %r collides with a load'\
                    ' parameter of the same name.' % param
                raise RequestParamKwargCollision(error_message)

        # If we have an icontrol version we need to add 'ver' to params
        if self._meta_data['icontrol_version']:
            params = requests_params.pop('params', {})
            params.update({'ver': self._meta_data['icontrol_version']})
            requests_params.update({'params': params})
        return requests_params

    def _refresh(self, **kwargs):
        """wrapped by `refresh` override that in a subclass to customize"""
        requests_params = self._handle_requests_params(kwargs)
        refresh_session = self._meta_data['bigip']._meta_data['icr_session']
        response = refresh_session.get(self._meta_data['uri'],
                                       **requests_params)
        self._local_update(response.json())

    def refresh(self, **kwargs):
        """Use this to make the device resource be represented by self.

        This method makes an HTTP GET query against the device service.
        This method is run for its side-effects on self.
        If successful the instance attribute __dict__ is replaced
        with the dict representing the device state.  To figure out what that
        state is, run a subsequest query of the object like this:
        As with all CURDLE methods use a "requests_params" dict to pass
        parameters to requests.session.HTTPMETHOD. See test_requests_params.py
        for an example.
        >>> resource_obj.refresh()
        >>> print(resource_obj.raw)
        """
        self._refresh(**kwargs)

    def load(self, **kwargs):
        error_message = "Only Resources support 'load'."
        raise InvalidResource(error_message)

    def create(self, **kwargs):
        """Implement this by overriding it in a subclass of `Resource`

        :raises: InvalidResource
        """
        error_message = "Only Resources support 'create'."
        raise InvalidResource(error_message)

    def delete(self, **kwargs):
        """Implement this by overriding it in a subclass of `Resource`

        :raises: InvalidResource
        """
        error_message = "Only Resources support 'delete'."
        raise InvalidResource(error_message)


class OrganizingCollection(ResourceBase):
    """Base class for objects that collect resources under them.

    ``OrganizingCollection`` objects fulfill the following functions:

    * represent a uri path fragment immediately 'below' /mgmt/tm
    * provide a list of dictionaries that contain uri's to other
      resources on the device.
    """
    def __init__(self, container):
        """Call this to construct an OC. It should be an attribute of BIG-IP®.

        :param bigip: all OCs are attributes of a BIG-IP® instance
        """
        super(OrganizingCollection, self).__init__(container)

    def get_collection(self, **kwargs):
        """Call to obtain a list of the reference dicts in the instance `items`

        :returns: List of self.items
        """
        self.refresh(**kwargs)
        return self.items


class Collection(ResourceBase):
    """Base class for objects that collect a list of ``Resources``

    The Collection Resource is responsible for providing a list of Python
    objects, where each object represents a unique URI, the URI contains the
    URI of the Collection at the front of its path, and the 'kind' of the
    URI-associated-JSON has been registered with the attribute registry of the
    Collection subclass.

    .. note::

        Any subclass of this base class must have ``s`` at the end of its name
        unless it ends in ``s`` then it must have ``_s``.

    """
    def __init__(self, container):
        """Call this with the __get_attr__ of a Resource or OC.

        The contained-by-an-OC-or-Resource pattern is observed, and not a
        strictly enforced part of the model.

        URIs are constructed _from_ Collection subclass names.  All Collection
        subclass names MUST end in 's' or '_s', to distinguish them from their
        associated Resource (which is always accessible as an attribute of the
        subclass instance.

        :param container: instances of Collection are attributes of container
        """
        super(Collection, self).__init__(container)

    def get_collection(self, **kwargs):
        """Get an iterator of Python ``Resource`` objects that represent URIs.

        The returned objects are Pythonic `Resource`s that map to the most
        recently `refreshed` state of uris-resources published by the device.
        In order to instantiate the correct types, the concrete subclass must
        populate its registry with acceptable types, based on the `kind` field
        returned by the REST server.

        .. note::
            This method implies a single REST transaction with the
            Collection subclass URI.

        :raises: UnregisteredKind
        :returns: list of reference dicts and Python ``Resource`` objects
        """
        list_of_contents = []
        self.refresh(**kwargs)
        if 'items' in self.__dict__:
            for item in self.items:
                # It's possible to have non-"kind" JSON returned. We just
                # append the corresponding dict. PostProcessing is the caller's
                # responsibility.
                if 'kind' not in item:
                    list_of_contents.append(item)
                    continue
                kind = item['kind']
                if kind in self._meta_data['attribute_registry']:
                    # If it has a kind, it must be registered.
                    instance =\
                        self._meta_data['attribute_registry'][kind](self)
                    instance._local_update(item)
                    instance._activate_URI(instance.selfLink)
                    list_of_contents.append(instance)
                else:
                    error_message = '%r is not registered!' % kind
                    raise UnregisteredKind(error_message)
        return list_of_contents


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
        self._meta_data['required_creation_parameters'] = set(('name',))
        # Refresh fails without these.
        self._meta_data['required_load_parameters'] = set(('name',))
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
        kwargs['uri_as_parts'] = True
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
