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

There are different types of resources published by the BigIP REST Server, they
are represented by the classes in this module.

Available Classes:
    * ResourceBase -- only `read` is generally supported in all resource types,
      this class provides `read`. ResourceBase objects are usually instantiated
      via setting lazy attributes. ResourceBase provides a contructor to match
      the lazy constructor. The expected behavior is that all resource
      subclasses depend on this constructor to correctly set their
      self._meta_data['uri'].
      All ResourceBase objects (except BigIPs) have a container (BigIPs contain
      themselves).  The container is the object the ResourceBase is an
      attribute of.
    * Collection -- These resources support lists of ResourceBase Objects.
    * Resource -- These resources are the only resources that support
      `create`, `update`, and `delete` operations.  Because they support HTTP
      post (via _create) they uniquely depend on 2 uri's, a uri that supports
      the creating post, and the returned uri of the newly created resource.
    * InvalidResource -- resources do not generally support all 5 Resource
      operations, if a caller attempts to invoke an unsupported operation this
      Exception is raised.
"""
import urlparse

from f5.bigip.mixins import LazyAttributeMixin
from f5.bigip.mixins import ToDictMixin


class KindTypeMismatch(Exception):
    pass


class DeviceProvidesIncompatibleKey(Exception):
    pass


class InvalidResource(Exception):
    """Raise this when a caller tries to invoke an unsupported CUD op.

    All resources support `read`.
    Only Resources support `create`, `update`, and `delete`.
    """
    pass


class MissingRequiredCreationParameter(Exception):
    pass


class MissingRequiredReadParameter(Exception):
    pass


class UnregisteredKind(Exception):
    pass


class GenerationMismatch(Exception):
    pass


class InvalidForceType(ValueError):
    pass


class ResourceBase(LazyAttributeMixin, ToDictMixin):
    """Every resource that maps to a uri on the device should inherit this.

    Instantiate this with ContainerInstance.NewResourceBaseInstance via the
    LazyAttributeMixin.

    The BigIP is represented by an object that converts device published uri's
    into Python objects.  Each uri maps to a Python object. The mechanism for
    instantatiating these objects is the __getattr__ Special Function in the
    LazyAttributeMixin.  When a registered attribute is `dot` referenced, on
    the device object (e.g. `bigip.ltm` or simply `bigip`), an appropriate
    object is instantiated and attributed to the referencing object, so:
    >>> bigip.ltm = LTM(bigip)
    >>> bigip.ltm.natcollection
    >>> nat1 = bigip.ltm.natcollection.nat.create('Foo', 'Bar', '0.1.2.3',
                                                  '1.2.3.4')

    Shortens to just the last line:
    >>> nat1 = bigip.ltm.natcollection.nat.create('Foo', 'Bar', '0.1.2.3',
                                                  '1.2.3.4')

    More importantly is enforces a convention relating device published uris to
    API objects, in a hierarchy similar to the uri paths.  I.E. the uri
    corresponding to a `NatCollection` object is `mgmt/tm/ltm/nat/`. If you
    query the bigip's uri (e.g. print(bigip._meta_data['uri']) ), you'll see
    that it ends in:
    `mgmt/tm/`, if you query the `ltm` object's uri
    (e.g. print(bigip.ltm._meta_data['uri']) ) you'll see it ends in
    `mgmt/tm/ltm/.

    In general the objects build a required `self._meta_data['uri']` attribute
    by:
    1. Inheriting this class.
    2. calling super(Subclass, self).__init__(container)
    3. self.uri = self.container_uri + base_uri <-- Always defined in the
    module that defines the class.

    The net result is a reasonably succinct mapping between uri's and objects,
    that represents objects in a hierarchical relationship similar to the
    devices uri path hierarchy.
    This is the class that defines `read` for all ResourceBases.

    Public attributes:
    - read: updates itself with the results of an http GET on the resource
    - others: not to be called here

    """
    def __init__(self, container):
        """Call this with containing_object_instance.FOO

        FOO must inherit from this class.  The '.' operator passes "FOO" to
        the __getattr__ method of the containing_object_instance where it is
        instantiated as the appropriate type of ResourceBase.

        Since all ResourceBases support `read` instances of ResourceBase do as
        well.
        The BigIP uri 'mgmt/tm/' uniquely passes itself to this constructor as
        the "container".
        """
        self._meta_data = {'container': container,
                           'bigip': container._meta_data['bigip']}

    def _local_update(self, rdict):
        sanitized = self._check_keys(rdict)
        temp_meta = self._meta_data
        self.__dict__ = sanitized
        self._meta_data = temp_meta

    def _check_keys(self, rdict):
        if '_meta_data' in rdict:
            error_message = "Response contains key '_meta_data' which is " +\
                "incompatible with this API!!\n Response json: %r" % rdict
            raise DeviceProvidesIncompatibleKey(error_message)
        for x in rdict:
            if x.startswith('__'):
                raise DeviceProvidesIncompatibleKey(x)
        return rdict

    def _refresh(self):
        """Use this to make the device resource be represented by self.

        This method is run for its side-effects on self.
        This method makes an HTTP get query against its uri, if successful its
        attribute __dict__ is replaced with the dict representing the device
        state.  To figure out what that state is, run a subsequest query of the
        object like this:
        >>> resource_obj.read()
        >>> print(resource.name)
        """
        read_session = self._meta_data['bigip']._meta_data['icr_session']
        response = read_session.get(self._meta_data['uri'])
        self._local_update(response.json())

    def refresh(self):
        self._refresh()

    def _build_meta_data_uri(self, selfLinkuri):
        hostname = self._meta_data['bigip']._meta_data['hostname']
        (scheme, domain, path, qarg, frag) = urlparse.urlsplit(selfLinkuri)
        path_uri = urlparse.urlunsplit((scheme, hostname, path, '', ''))+'/'
        self._meta_data['uri'] = path_uri
        self._meta_data['creation_uri_qarg'] = qarg
        self._meta_data['creation_uri_frag'] = frag

    def load(self, **kwargs):
        error_message = "Only Resources support 'load'."
        raise InvalidResource(error_message)

    def create(self):
        error_message = "Only Resources support 'create'."
        raise InvalidResource(error_message)

    def update(self):
        error_message = "Only Resources support 'update'."
        raise InvalidResource(error_message)

    def delete(self):
        error_message = "Only Resources support 'delete'."
        raise InvalidResource(error_message)

    @property
    def raw(self):
        return self.__dict__


class OrganizingCollection(ResourceBase):
    def __init__(self, bigip):
        super(OrganizingCollection, self).__init__(bigip)
        base_uri = self.__class__.__name__.lower() + '/'
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + base_uri
        # Collections have a registry which must be reified in the
        # subclass constructor.
        self._meta_data['collection_registry'] = {}

    # Because of the behavior of the BigIP REST server different resource types
    # must handle get_collection differently.
    def get_collection(self):
        self._refresh()
        return self.items


class Collection(ResourceBase):
    """Inherit from this class if the corresponding uri lists other resources.

    Note any subclass must have "Collection" at the end of its name!
    """
    def __init__(self, container):
        super(Collection, self).__init__(container)
        # Handle 'collection'
        endind = len('collection')
        base_uri = self.__class__.__name__.lower()[:-endind] + '/'
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + base_uri

    def get_collection(self):
        """Get an iterator (list maybe upgrade to generator) of objects.

        The objects in returned list are Pythonic ResourceBases that map to the
        most recently `got` state of uris-resources published by the device.
        In order to instantiate the correct types, the concrete subclass must
        populate its registry with acceptable types, based on the `kind` field
        returned by the REST server.
        """
        list_of_contents = []
        # Collections list is likely to become collections.abc.Sequence subtype
        # with support for field based comparison.
        self._refresh()
        if 'items' in self.__dict__:
            for item in self.items:
                kind = item['kind']
                name = item['name']
                partition = item.get('partition', '')
                if kind in self._meta_data['collection_registry']:
                    instance =\
                        self._meta_data['collection_registry'][kind](self)
                    instance.load(name=name, partition=partition)
                    list_of_contents.append(instance)
                else:
                    error_message = '%r is not registered!' % kind
                    raise UnregisteredKind(error_message)
        return list_of_contents


class Resource(ResourceBase):
    """Use this to represent a Configurable Resource on the device.

    1a.  bigip.ltm.natcollection.nat
    or
    1b.  nat_obj = bigip.ltm.natcollection.nat
    2.  call super(Subclass, self).__init__(container) in its __init__
    """
    def __init__(self, container):
        """Call _create for a Resource resource to have a self._meta_data['uri']!

        """
        super(Resource, self).__init__(container)
        # All Creation supporting Resources must update the
        # 'required_creation_parameters' set with the appropriate values.
        self._meta_data['required_creation_parameters'] = set(('name',))
        self._meta_data['required_refresh_parameters'] = set(('name',))
        self._meta_data['exclusive_attributes'] = []
        self._meta_data['read_only_attributes'] = []

    def _create(self, **kwargs):
        """Call this to create.

        Subclasses, should support this functionality by defining a `create`
        method that wraps and calls this method with appropriate arguments.

        :params kwargs: All the key-values needed to create the resource
        :returns: An instance of the Python object that represents the device's
        uri-published resource.  The uri of the resource is part of the
        object's _meta_data.
        :returns: Note this is the only fundamental Resource operation that
        returns a different uri (in the returned object) than the uri the
        operation was called on.  The returned uri can be accessed as
        Object.selfLink, the actual uri used by REST operations on the object
        is Object._meta_data['uri'].  The _meta_data['uri'] is the same as
        Object.selfLink with the substring 'localhost' replaced with the value
        of Object._meta_data['bigip']._meta_data['hostname'].
        """
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
        response = session.post(_create_uri, json=kwargs)

        # Post-process the response
        self._local_update(response.json())

        if self.kind != self._meta_data['required_json_kind']:
            error_message = "For instances of type '%r' the corresponding" +\
                " kind must be '%r' but creation returned JSON with kind: %r"\
                % (self.__class__.__name__,
                   self._meta_data['required_json_kind'],
                   self.kind)
            raise KindTypeMismatch(error_message)

        # Update the object to have the correct functional uri.
        self._build_meta_data_uri(self.selfLink)
        self._update_lazy_attributes()
        return self

    def create(self, **kwargs):
        self._create(**kwargs)
        return self

    def _load(self, **kwargs):
        # For vlan.interfacescollection.interface the partition is not valid
        key_set = set(kwargs.keys())
        required_minus_received =\
            self._meta_data['required_refresh_parameters'] - key_set
        if required_minus_received != set():
            error_message = 'Missing required params: %r'\
                % required_minus_received
            raise MissingRequiredReadParameter(error_message)
        kwargs['uri_as_parts'] = True
        read_session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']
        response = read_session.get(base_uri, **kwargs)
        self._local_update(response.json())
        self._build_meta_data_uri(self.selfLink)
        self._update_lazy_attributes()
        return self

    def load(self, **kwargs):
        self._load(**kwargs)
        return self

    def _update(self, **kwargs):
        update_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        read_only = self._meta_data.get('read_only_attributes', [])

        # Get the current state of the object on BigIP and check the generation
        # Use pop here because we don't want force in the data_dict
        force = self._check_force_arg(kwargs.pop('force', False))
        if not force:
            self._check_generation()

        # Save the meta data so we can add it back into self after we
        # load the new object.
        temp_meta = self.__dict__.pop('_meta_data')

        # Need to remove any of the Collection objects from self.__dict__
        # because these are sub-collections and _meta_data and
        # other non-BIGIP attrs are not removed from the sub-collections
        # See issue #146 for details
        for key, value in self.__dict__.items():
            if isinstance(value, Collection):
                self.__dict__.pop(key, '')
        data_dict = self.to_dict()

        # Remove any read-only attributes from our data_dict before we update
        # the data dict with the attributes.  If they pass in read-only attrs
        # in the method call we are going to let BIGIP let them know about it
        # when it fails
        for attr in read_only:
            data_dict.pop(attr, '')
        data_dict.update(kwargs)
        response = session.put(update_uri, json=data_dict)
        self._meta_data = temp_meta
        self._local_update(response.json())

    def update(self, **kwargs):
        # Need to implement checking for valid params here.
        self._update(**kwargs)

    def _delete(self, **kwargs):
        delete_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # Check the generation for match before delete
        force = self._check_force_arg(kwargs.pop('force', False))
        if not force:
            self._check_generation()

        response = session.delete(delete_uri)
        if response.status_code == 200:
            self.__dict__ = {'deleted': True}

    def delete(self):
        # Need to implement checking for ? here.
        self._delete()
        # Need to implement correct teardown here.

    def _check_force_arg(self, force):
        if not isinstance(force, bool):
            raise InvalidForceType("force parameter must be type bool")
        return force

    def _check_generation(self):
        '''Check that the generation on the BigIP matches the object

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

    def _update_lazy_attributes(self):
        collection_reg = self._meta_data.get('collection_registry', {})
        self._meta_data['allowed_lazy_attributes'] = collection_reg.values()
