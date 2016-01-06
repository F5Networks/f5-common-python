# Copyright 2015 F5 Networks Inc.
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
"""This module provides classes that specify how Resources are handled.

There are different types of resources published by the BigIP REST Server, they
are represented by the "Resource" class hierarchy.

Available Classes:
    * InvalidCRUD -- resources do not generally support all 4 CRUD
      operations, if a caller attempts to invoke an unsupported operation this
      Exception is raised
    * Resource -- only `read` is generally supported in all resource types,
      this class provides `read`. Resource objects are usually instantiated via
      setting lazy attributes.  Resource provides a contructor to match the
      lazy constructor. The expected behavior is that all resource subclasses
      depend on this constructor to correctly set their self._meta_data['uri'].
      All Resource objects (except BigIPs) have a container (BigIPs contain
      themselves).  The container is the object the Resource is an attribute
      of.
    * CollectionResource -- These resources support lists of Resource Objects.
    * CRUDResource -- These resources are the only resources that support
      `create`, `update`, and `delete` operations.  Because they support HTTP
      post (via _create) they uniquely depend on 2 uri's, a uri that supports
      the creating post, and the returned uri of the newly created resource.

"""
from f5.bigip.mixins import LazyAttributeMixin
from f5.bigip.mixins import ToDictMixin


class KindTypeMismatch(Exception):
    pass


class DeviceProvidesIncompatibleKey(Exception):
    pass


class InvalidCRUD(Exception):
    """Raise this when a caller tries to invoke an unsupported CUD op.

    All resources support `read`.
    Only CRUDResources support `create`, `update`, and `delete`.
    """
    pass


class MissingRequiredCreationParameter(Exception):
    pass


class MissingRequiredReadParameter(Exception):
    pass


class Resource(LazyAttributeMixin, ToDictMixin):
    """Every resource that maps to a uri on the device should inherit this.

    Instantiate this with ContainerInstance.NewResourceInstance via the
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
    This is the class that defines `read` for all Resources.

    Public attributes:
    - read: updates itself with the results of an http GET on the resource
    - others: not to be called here

    """
    def __init__(self, container):
        """Call this with containing_object_instance.FOO

        FOO must inherit from this class.  The '.' operator passes "FOO" to
        the __getattr__ method of the containing_object_instance where it is
        instantiated as the appropriate type of Resource.

        Since all Resources support `read` instances of Resource do as well.
        The BigIP uri 'mgmt/tm/' uniquely passes itself to this constructor
        as the "container".
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

    def _load(self, **kwargs):
        if ('name' not in kwargs) or ('partition' not in kwargs):
            raise MissingRequiredReadParameter(str(kwargs))
        kwargs['uri_as_parts'] = True
        hostname = self._meta_data['bigip']._meta_data['hostname']
        read_session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']
        response = read_session.get(base_uri, **kwargs)
        self._local_update(response.json())
        self._meta_data['uri'] = self.selfLink.replace('localhost', hostname)

    def create(self):
        error_message = "Only CRUDResources support http 'create'."
        raise InvalidCRUD(error_message)

    def update(self):
        error_message = "Only CRUDResources support http 'update'."
        raise InvalidCRUD(error_message)

    def delete(self):
        error_message = "Only CRUDResources support http 'delete'."
        raise InvalidCRUD(error_message)


class CollectionResource(Resource):
    """Inherit from this class if the corresponding uri lists other resources.

    Note any subclass must append "Collection" to its name!
    """
    def __init__(self, container):
        super(CollectionResource, self).__init__(container)
        base_uri = self.__class__.__name__.lower()
        if base_uri.endswith('collection'):
            base_uri = base_uri[:-len('collection')] + '/'
        else:
            base_uri = base_uri + '/'
        self._meta_data['uri'] =\
            self._meta_data['container']._meta_data['uri'] + base_uri

    def get_managed(self):
        """Get an iterator (list maybe upgrade to generator) of objects.

        The objects in the returned list are Pythonic Resources that map to the
        uris-resources published by the device.

        Note: The "self.ManagedType" must be correctly assigned when the
        ManagerResource is instantiated.
        """
        list_of_managed = []
        response = self.read()
        # This will need to be updated
        res_dict = response.json()
        for item in res_dict['items']:
            list_of_managed.append(self.ManagedType(item))
        return list_of_managed


class CRUDResource(Resource):
    """Use this to represent a Configurable Resource on the device.

    1a.  bigip.ltm.natcollection.nat
    or
    1b.  nat_obj = bigip.ltm.natcollection.nat
    2.  call super(Subclass, self).__init__(container) in its __init__
    """
    def __init__(self, container):
        """Call _create for a CRUD resource to have a self._meta_data['uri']!

        """
        super(CRUDResource, self).__init__(container)

    def _create(self, **kwargs):
        """Call this to create.

        Subclasses, should support this functionality by defining a `create`
        method that wraps and calls this method with appropriate arguments.

        :params kwargs: All the key-values needed to create the resource
        :returns: An instance of the Python object that represents the device's
        uri-published resource.  The uri of the resource is part of the
        object's _meta_data.
        :returns: Note this is the only fundamental CRUD operation that returns
        a different uri (in the returned object) than the uri the operation was
        called on.  The returned uri can be accessed as Object.selfLink, the
        actual uri used by REST operations on the object is
        Object._meta_data['uri'].  The _meta_data['uri'] is the same as
        Object.selfLink with the substring 'localhost' replaced with the value
        of Object._meta_data['bigip']._meta_data['hostname'].
        """
        # Make convenience variable with short names for this method.
        _create_uri = self._meta_data['container']._meta_data['uri']
        hostname = self._meta_data['bigip']._meta_data['hostname']
        session = self._meta_data['bigip']._meta_data['icr_session']

        # Invoke the REST operation on the device.
        response = session.post(_create_uri, json=kwargs)

        # Post-process the response
        self._local_update(response.json())

        # Update the object to have the correct functional uri.
        self._meta_data['uri'] = self.selfLink.replace('localhost', hostname)

    def _update(self, **kwargs):
        update_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        temp_meta = self.__dict__.pop('_meta_data')
        # TOD: data_dict = self.to_dict()
        # TOD: data_dict.update(kwargs)
        # TOD: print('data_dict: %r' % data_dict)
        response = session.put(update_uri, json=kwargs)
        self._meta_data = temp_meta
        self._local_update(response.json())

    def _delete(self):
        delete_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        response = session.delete(delete_uri, partition=self.partition,
                                  name=self.name)
        if response.status_code == 200:
            self.__dict__ = {'deleted': True}
