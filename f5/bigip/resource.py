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

 * Expression:     bigip = ManagementRoot('a', 'b', 'c')
 * URI Returned:   https://a/mgmt/

 * Expression:     bigip.tm.ltm
 * URI Returned:   https://a/mgmt/tm/ltm/

 * Expression:     pools1 = bigip.tm.ltm.pools
 * URI Returned:   https://a/mgmt/tm/ltm/pool

 * Expression:     pool_a = pools1.create(partition="Common", name="foo")
 * URI Returned:   https://a/mgmt/tm/ltm/pool/~Common~foo

There are different types of resources published by the BIG-IP® REST Server,
they are represented by the classes in this module.

We refer to a server-provided resource as a "service".  Thus far all URI
referenced resources are "services" in this sense.

We use methods named Create, Refresh, Update, Load, Modify, and Delete to
manipulate BIG-IP® device services.

Methods:

  * create -- uses HTTP POST, creates a new resource and with its own URI on
    the device
  * refresh -- uses HTTP GET, obtains the state of a device resource, and sets
    the representing Python Resource Object tracks device state via its attrs
  * update -- uses HTTP PUT, submits a new configuration to the device resource
     and sets the Resource attrs to the state the device reports
  * load -- uses HTTP GET, obtains the state of an existing resource on the
    device and sets the Resource attrs to that state
  * modify -- uses HTTP PATCH to selectively modify named resources submitted
    as keyword arguments
  * delete -- uses HTTP DELETE, removes the resource from the device, and sets
    self.__dict__ to {'deleted': True}

Available Classes:
    * PathElement -- the most fundamental class it represent URI elements that
      serve only as place-holders.  All other Resources inherit from
      PathElement, though the inheritance may be indirect. PathElement provides
      a constructor to match its call in LazyAttributeMixin.__getattr__. The
      expected behavior is that all resource subclasses depend on this
      constructor to correctly set their self._meta_data['uri'].  See
      _set_meta_data_uri for the logic underlying self._meta_data['uri']
      construction.
    * ResourceBase -- only `refresh` is generally supported in all resource
      types, this class provides `refresh`. ResourceBase objects are usually
      instantiated via setting lazy attributes.
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
    * UnnamedResource -- Some resources correspond to URIs that do not have
      unique names, therefore the class does _not_ support create-or-delete,
      and supports a customized 'load' that doesn't require name/partition
      parameters.
"""
try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError as exc:
        message = ("Maybe you're using Python < 2.7 and do not have the "
                   "orderreddict external dependency installed.")
        raise exc(message)
import copy
import keyword
import re
import time
import tokenize
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from f5.bigip.mixins import LazyAttributeMixin
from f5.bigip.mixins import ToDictMixin
from f5.sdk_exception import AttemptedMutationOfReadOnly
from f5.sdk_exception import BooleansToReduceHaveSameValue
from f5.sdk_exception import DeviceProvidesIncompatibleKey
from f5.sdk_exception import ExclusiveAttributesPresent
from f5.sdk_exception import GenerationMismatch
from f5.sdk_exception import InvalidForceType
from f5.sdk_exception import InvalidResource
from f5.sdk_exception import KindTypeMismatch
from f5.sdk_exception import MissingRequiredCommandParameter
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import MissingRequiredReadParameter
from f5.sdk_exception import RequestParamKwargCollision
from f5.sdk_exception import UnregisteredKind
from f5.sdk_exception import UnsupportedMethod
from f5.sdk_exception import UnsupportedOperation
from f5.sdk_exception import URICreationCollision
from icontrol.exceptions import iControlUnexpectedHTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from six import iteritems
from six import iterkeys
from six import itervalues


def _missing_required_parameters(rqset, **kwargs):
    """Helper function to do operation on sets.

    Checks for any missing required parameters.
    Returns non-empty or empty list. With empty
    list being False.

    ::returns list
    """
    key_set = set(list(iterkeys(kwargs)))
    required_minus_received = rqset - key_set
    if required_minus_received != set():
        return list(required_minus_received)


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
        # Supported versions for each class will be defined here.
        # List can be modified downstream in each sub-class
        self._meta_data['minimum_version'] = '11.5.0'
        # Commands you can run on a resource or collection, we define it here
        self._meta_data['allowed_commands'] = []
        # Define required command parameters
        self._meta_data['required_command_parameters'] = set()
        # You can't have more than one of the attributes in any of these sets.
        self._meta_data['exclusive_attributes'] = []
        # As some objects do not support Stats we need this setting,
        # by default Stats are enabled on all endpoints. Override in
        # subclass as required
        self._meta_data['object_has_stats'] = True
        # Some endpoints have mandatory parameters that can be one of x,
        # this means that all or at least 1 need to be present during create
        self._meta_data['minimum_additional_parameters'] = set()

    def _set_meta_data_uri(self):
        base_uri = self._get_base_uri()
        endpoint = base_uri.replace('_', '-')
        final_uri = self._build_final_uri(endpoint)
        self._meta_data['uri'] = final_uri

    def _get_base_uri(self):
        if isinstance(self, Collection):
            return self._format_collection_name()
        return self._format_resource_name()

    def _build_final_uri(self, endpoint):
        return self._meta_data['container']._meta_data['uri'] + endpoint + '/'

    def _format_collection_name(self):
        """Formats a name from Collection format

        Collections are of two name formats based on their actual URI
        representation in the REST service.

        1. For cases where the actual URI of a collection is singular, for
           example,

               /mgmt/tm/ltm/node

           The name of the collection, as exposed to the user, will be made
           plural. For example,

               mgmt.tm.ltm.nodes

        2. For cases where the actual URI of a collection is plural, for
           example,

               /mgmt/cm/shared/licensing/pools/

           The name of the collection, as exposed to the user, will remain
           plural, but will have an `_s` appended to it. For example,

               mgmt.cm.shared.licensing.pools_s

        This method is responsible for undoing the user provided plurality.
        It ensures that the URI that is being sent to the REST service is
        correctly plural, or plural plus.

        Returns:
            A string representation of the user formatted Collection with its
            plurality identifier removed appropriately.
        """
        base_uri = self._format_resource_name()
        if base_uri[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        return base_uri[:-endind]

    def _format_resource_name(self):
        """Formats the name of a Resource

        When the names of Resources are used to create URIs, their names are
        automatically cast to lowercase to match the actual URI expected by
        the REST service.

        There are certain URIs, however, that must not be cast in this way.

        For these URIs, this method should be overloaded in the Resource
        class itself to specify how to handle the Resource name.

        An example of this difference in behavior, refer to the BIG-IQ or
        iWorkflow APIs such as,

            /mgmt/shared/resolver/device-groups/cm-bigip-allBigIpDevices/

        Returns:
            A string representation of the Resource as it should be
            represented when contructing the final URI used to reach that
            Resource.
        """
        return self.__class__.__name__.lower()

    def _check_command_parameters(self, **kwargs):
        """Params given to exec_cmd should satisfy required params.

        :params: kwargs
        :raises: MissingRequiredCommandParameter
        """
        rset = self._meta_data['required_command_parameters']
        check = _missing_required_parameters(rset, **kwargs)
        if check:
            error_message = 'Missing required params: %s' % check
            raise MissingRequiredCommandParameter(error_message)

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

    def _handle_requests_params(self, kwargs):
        """Validate parameters that will be passed to the requests verbs.

        This method validates that there is no conflict in the names of the
        requests_params passed to the function and the other kwargs.  It also
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

    def _check_exclusive_parameters(self, **kwargs):
        """Check for mutually exclusive attributes in kwargs.

        :raises ExclusiveAttributesPresent
        """
        if len(self._meta_data['exclusive_attributes']) > 0:
            attr_set = set(list(iterkeys(kwargs)))
            ex_set = set(self._meta_data['exclusive_attributes'][0])
            common_set = sorted(attr_set.intersection(ex_set))
            if len(common_set) > 1:
                cset = ', '.join(common_set)
                error = 'Mutually exclusive arguments submitted. ' \
                        'The following arguments cannot be set ' \
                        'together: "%s".' % cset
                raise ExclusiveAttributesPresent(error)

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

    def _modify(self, **patch):
        """Wrapped with modify, override in a subclass to customize."""

        requests_params, patch_uri, session, read_only = \
            self._prepare_put_or_patch(patch)
        self._check_for_boolean_pair_reduction(patch)
        read_only_mutations = []
        for attr in read_only:
            if attr in patch:
                read_only_mutations.append(attr)
        if read_only_mutations:
            msg = 'Attempted to mutate read-only attribute(s): %s' \
                % read_only_mutations
            raise AttemptedMutationOfReadOnly(msg)

        patch = self._prepare_request_json(patch)
        response = session.patch(patch_uri, json=patch, **requests_params)
        self._local_update(response.json())

    def modify(self, **patch):
        """Modify the configuration of the resource on device based on patch

        """

        self._modify(**patch)

    def _check_for_boolean_pair_reduction(self, kwargs):
        """Check if boolean pairs should be reduced in this resource."""

        if 'reduction_forcing_pairs' in self._meta_data:
            for key1, key2 in self._meta_data['reduction_forcing_pairs']:
                kwargs = self._reduce_boolean_pair(kwargs, key1, key2)
        return kwargs

    def _prepare_put_or_patch(self, kwargs):
        """Retrieve the appropriate request items for put or patch calls."""

        requests_params = self._handle_requests_params(kwargs)
        update_uri = self._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        read_only = self._meta_data.get('read_only_attributes', [])
        return requests_params, update_uri, session, read_only

    def _prepare_request_json(self, kwargs):
        '''Prepare request args for sending to device as JSON.'''

        # Check for python keywords in dict
        kwargs = self._check_for_python_keywords(kwargs)

        # Check for the key 'check' in kwargs
        if 'check' in kwargs:
            od = OrderedDict()
            od['check'] = kwargs['check']
            kwargs.pop('check')
            od.update(kwargs)
            return od
        return kwargs

    def _iter_list_for_dicts(self, check_list):
        '''Iterate over list to find dicts and check for python keywords.'''

        list_copy = copy.deepcopy(check_list)
        for index, elem in enumerate(check_list):
            if isinstance(elem, dict):
                list_copy[index] = self._check_for_python_keywords(elem)
            elif isinstance(elem, list):
                list_copy[index] = self._iter_list_for_dicts(elem)
            else:
                list_copy[index] = elem
        return list_copy

    def _check_for_python_keywords(self, kwargs):
        '''When Python keywords seen, mutate to remove trailing underscore.'''

        kwargs_copy = copy.deepcopy(kwargs)
        for key, val in iteritems(kwargs):
            if isinstance(val, dict):
                kwargs_copy[key] = self._check_for_python_keywords(val)
            elif isinstance(val, list):
                kwargs_copy[key] = self._iter_list_for_dicts(val)
            else:
                if key.endswith('_'):
                    strip_key = key.rstrip('_')
                    if keyword.iskeyword(strip_key):
                        kwargs_copy[strip_key] = val
                        kwargs_copy.pop(key)
        return kwargs_copy

    def _check_keys(self, rdict):
        """Call this from _local_update to validate response keys

        disallowed server-response json keys:
        1. The string-literal '_meta_data'
        2. strings that are not valid Python 2.7 identifiers
        3. strings beginning with '__'.

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
                # If attribute is keyword, append underscore to attribute name
                rdict[x + '_'] = rdict[x]
                rdict.pop(x)
            elif x.startswith('__'):
                error_message = "Device provided %r which is disallowed"\
                    ", it mangles into a Python non-public attribute." % x
                raise DeviceProvidesIncompatibleKey(error_message)
        return rdict

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

    def _update(self, **kwargs):
        """wrapped with update, override that in a subclass to customize"""

        requests_params, update_uri, session, read_only = \
            self._prepare_put_or_patch(kwargs)

        read_only_mutations = []
        for attr in read_only:
            if attr in kwargs:
                read_only_mutations.append(attr)
        if read_only_mutations:
            msg = 'Attempted to mutate read-only attribute(s): %s' \
                  % read_only_mutations
            raise AttemptedMutationOfReadOnly(msg)

        # Get the current state of the object on BIG-IP® and check the
        # generation Use pop here because we don't want force in the data_dict
        force = self._check_force_arg(kwargs.pop('force', True))
        if not force:
            # generation has a known server-side error
            self._check_generation()

        kwargs = self._check_for_boolean_pair_reduction(kwargs)

        # Save the meta data so we can add it back into self after we
        # load the new object.
        temp_meta = self.__dict__.pop('_meta_data')

        # Need to remove any of the Collection objects from self.__dict__
        # because these are subCollections and _meta_data and
        # other non-BIG-IP® attrs are not removed from the subCollections
        # See issue #146 for details
        tmp = dict()
        for key, value in iteritems(self.__dict__):
            # In Python2 versions we were changing a dictionary in place,
            # but this cannot be done with an iterator as an error is raised.
            # So instead we create a temporary holder for the modified dict
            # and then re-assign it afterwards.
            if isinstance(value, Collection):
                pass
            else:
                tmp[key] = value
        self.__dict__ = tmp
        data_dict = self.to_dict()

        # Remove any read-only attributes from our data_dict before we update
        # the data dict with the attributes.  If they pass in read-only attrs
        # in the method call we are going to let BIG-IP® let them know about it
        # when it fails
        for attr in read_only:
            data_dict.pop(attr, '')

        data_dict.update(kwargs)
        data_dict = self._prepare_request_json(data_dict)

        # Handles ConnectionAborted errors
        #
        # @see https://github.com/F5Networks/f5-ansible/issues/317
        # @see https://github.com/requests/requests/issues/2364
        for _ in range(0, 30):
            try:
                response = session.put(update_uri, json=data_dict, **requests_params)
                self._meta_data = temp_meta
                self._local_update(response.json())
                break
            except iControlUnexpectedHTTPError:
                response = session.get(update_uri, **requests_params)
                self._meta_data = temp_meta
                self._local_update(response.json())
                raise
            except ConnectionError as ex:
                if 'Connection aborted' in str(ex):
                    time.sleep(1)
                    continue
                else:
                    raise

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

    def _refresh(self, **kwargs):
        """wrapped by `refresh` override that in a subclass to customize"""
        requests_params = self._handle_requests_params(kwargs)
        refresh_session = self._meta_data['bigip']._meta_data['icr_session']

        if self._meta_data['uri'].endswith('/stats/'):
            # Slicing off the trailing slash here for Stats enpoints because
            # iWorkflow doesn't consider those `stats` URLs valid if they
            # include the trailing slash.
            #
            # Other than that, functionality does not change
            uri = self._meta_data['uri'][0:-1]
        else:
            uri = self._meta_data['uri']

        response = refresh_session.get(uri, **requests_params)
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

    def _stamp_out_core(self):
        container = self._meta_data['container']
        core = self.__class__.__new__(self.__class__)
        core.__init__(container)
        return core

    def _produce_instance(self, response):
        '''Generate a new self, which is an instance of the self.'''
        new_instance = self._stamp_out_core()
        # Post-process the response
        new_instance._local_update(response.json())

        if new_instance.kind != new_instance._meta_data['required_json_kind'] \
           and new_instance.kind != "tm:transaction:commandsstate":
            error_message = "For instances of type '%r' the corresponding"\
                " kind must be '%r' but creation returned JSON with kind: %r"\
                % (new_instance.__class__.__name__,
                   new_instance._meta_data['required_json_kind'],
                   new_instance.kind)
            raise KindTypeMismatch(error_message)

        # Update the object to have the correct functional uri.
        new_instance._activate_URI(new_instance.selfLink)
        return new_instance

    def _reduce_boolean_pair(self, config_dict, key1, key2):
        """Ensure only one key with a boolean value is present in dict.

        :param config_dict: dict -- dictionary of config or kwargs
        :param key1: string -- first key name
        :param key2: string -- second key name
        :raises: BooleansToReduceHaveSameValue
        """

        if key1 in config_dict and key2 in config_dict \
                and config_dict[key1] == config_dict[key2]:
            msg = 'Boolean pair, %s and %s, have same value: %s. If both ' \
                'are given to this method, they cannot be the same, as this ' \
                'method cannot decide which one should be True.' \
                % (key1, key2, config_dict[key1])
            raise BooleansToReduceHaveSameValue(msg)
        elif key1 in config_dict and not config_dict[key1]:
            config_dict[key2] = True
            config_dict.pop(key1)
        elif key2 in config_dict and not config_dict[key2]:
            config_dict[key1] = True
            config_dict.pop(key2)
        return config_dict

    @property
    def attrs(self):
        no_meta_dict = {k: v for k, v in iteritems(self.__dict__)
                        if k != '_meta_data'}
        return no_meta_dict


class OrganizingCollection(ResourceBase):
    """Base class for objects that collect resources under them.

    ``OrganizingCollection`` objects fulfill the following functions:

    * represent a uri path fragment immediately 'below' /mgmt/tm
    * provide a list of dictionaries that contain uri's to other
      resources on the device.
    """

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
                    instance = self._meta_data['attribute_registry'][kind](self)
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
        self._meta_data['required_creation_parameters'] = {'name', }
        # Refresh fails without these.
        self._meta_data['required_load_parameters'] = {'name', }
        # You can't set these attributes, only 'read' them.
        self._meta_data['read_only_attributes'] = []
        self._meta_data['reduction_forcing_pairs'] = \
            [
                ('enabled', 'disabled'),
                ('online', 'offline'),
                ('vlansEnabled', 'vlansDisabled')
            ]

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
        uri = urlparse.urlsplit(str(self._meta_data['bigip']._meta_data['uri']))

        # attrs local alias
        attribute_reg = self._meta_data.get('attribute_registry', {})
        attrs = list(itervalues(attribute_reg))
        attrs = self._assign_stats(attrs)

        (scheme, domain, path, qarg, frag) = urlparse.urlsplit(selfLinkuri)
        path_uri = urlparse.urlunsplit((scheme, uri.netloc, path, '', ''))
        if not path_uri.endswith('/'):
            path_uri = path_uri + '/'
        qargs = urlparse.parse_qs(qarg)
        self._meta_data.update({'uri': path_uri,
                                'creation_uri_qargs': qargs,
                                'creation_uri_frag': frag,
                                'allowed_lazy_attributes': attrs})

    def _assign_stats(self, attrs):
        if self._meta_data['object_has_stats']:
            attrs.append(Stats)
        return attrs

    def _check_create_parameters(self, **kwargs):
        """Params given to create should satisfy required params.

        :params: kwargs
        :raises: MissingRequiredCreateParameter
        """
        rset = self._meta_data['required_creation_parameters']
        check = _missing_required_parameters(rset, **kwargs)
        if check:
            error_message = 'Missing required params: %s' % check
            raise MissingRequiredCreationParameter(error_message)

    def _minimum_one_is_missing(self, **kwargs):
        """Helper function to do operation on sets

        Verify if at least one of the elements
        is present in **kwargs. If no items of rqset
        are contained in **kwargs  the function
        raises exception.

        Note: This check will only trigger
              if rqset is not empty.

        Raises:

             MissingRequiredCreationParameter
        """
        rqset = self._meta_data['minimum_additional_parameters']
        if rqset:
            kwarg_set = set(iterkeys(kwargs))
            if kwarg_set.isdisjoint(rqset):
                args = sorted(rqset)
                error_message = 'This resource requires at least one of the ' \
                                'mandatory additional ' \
                                'parameters to be provided: %s' % ', '.join(args)
                raise MissingRequiredCreationParameter(error_message)

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
        return self._create(**kwargs)

    def _check_load_parameters(self, **kwargs):
        """Params given to load should at least satisfy required params.

        :params: kwargs
        :raises: MissingRequiredReadParameter
        """
        rset = self._meta_data['required_load_parameters']
        check = _missing_required_parameters(rset, **kwargs)
        if check:
            check.sort()
            error_message = 'Missing required params: %s' % check
            raise MissingRequiredReadParameter(error_message)

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
        for key1, key2 in self._meta_data['reduction_forcing_pairs']:
            kwargs = self._reduce_boolean_pair(kwargs, key1, key2)
        kwargs = self._check_for_python_keywords(kwargs)
        response = refresh_session.get(base_uri, **kwargs)
        # Make new instance of self
        return self._produce_instance(response)

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
        return self._load(**kwargs)

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
        return self._exists(**kwargs)

    def _exists(self, **kwargs):
        """wrapped with exists, override that in a subclass to customize """
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


class UnnamedResource(ResourceBase):
    """This makes a resource object work if there is no name.

    These objects do not support create or delete and are often found
    as Resources that are under an organizing collection.  For example
    the `mgmt/tm/sys/global-settings` is one of these and has a kind of
    `tm:sys:global-settings:global-settingsstate` and the URI does not
    match the kind.
    """

    def create(self, **kwargs):
        """Create is not supported for unnamed resources

        :raises: UnsupportedMethod
        """
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for unnamed resources

        :raises: UnsupportedMethod
        """
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__
        )

    def load(self, **kwargs):
        newinst = self._stamp_out_core()
        newinst._refresh(**kwargs)
        return newinst


class Stats(UnnamedResource):
    """For stats resources."""

    def modify(self, **kwargs):
        """Modify is not supported for stats resources

        :raises: UnsupportedMethod
        """
        raise UnsupportedMethod(
            "%s does not support the modify method" % self.__class__.__name__
        )

    def load(self, **kwargs):
        # TODO(pjbreaux) add try-except and custom exception here.
        return super(Stats, self).load(**kwargs)


class AsmResource(Resource):
    """ASM Resource class represents a configurable ASM endpoint on the device.

    ASM resources are unique in BIG-IP® in the sense that their direct URI
    endpoints are hash based IDs of the resources.

    The IDs are generated by BIG-IP® when the objects are created.

    Moreover, the ASM resources do not have 'generation' property,
    therefore some of the other methods needed to be adjusted to accommodate
    that.
    """

    def __init__(self, container):
        """Call to create a client side object to represent a service URI.

        Call _create or _load for a Resource to have a self._meta_data['uri']!
        """
        super(AsmResource, self).__init__(container)
        # Asm endpoints require object 'id' which is a hash created by BIGIP
        # when object is created.
        self._meta_data['required_load_parameters'] = {'id', }
        # No ASM endpoint supports Stats
        self._meta_data['object_has_stats'] = False

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
        """Delete the ASM resource on the BIG-IP®.

        Uses HTTP DELETE to delete the ASM resource on the BIG-IP®.

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
        """Check for the existence of the ASM object on the BIG-IP

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


class AsmTaskResource(AsmResource):
    """ASM Task Resource class represents an ASM Tasks endpoint on the

    device.

    Tasks resources do not support create() method in the strict sense,
    as they require an HTTP POST with an empty json{} to prompt BIGIP to
    create them, therefore a new method fetch() was created.

    """

    def __init__(self, container):
        """Call to create a client side object to represent a service URI.

        Call  _fetch for a Resource to have a self._meta_data['uri']!
        """
        super(AsmTaskResource, self).__init__(container)

    def _fetch(self):
        """wrapped by `fetch` override that in subclasses to customize"""
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this "\
                    "resource, the _meta_data['uri'] is %s and it should"\
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        # Make convenience variable with short names for this method.
        _create_uri = self._meta_data['container']._meta_data['uri']
        session = self._meta_data['bigip']._meta_data['icr_session']
        # Invoke the REST operation on the device.
        response = session.post(_create_uri, json={})
        # Make new instance of self
        return self._produce_instance(response)

    def fetch(self):
        """Fetch the ASM resource on the BIG-IP®.

        This is a heavily modified version of create, that does not allow
        any arguments when executing. It uses an emtpy json{} HTTP POST to
        prompt the BIG-IP® to create the object, mainly used by 'Tasks'
        endpoint.
        """
        return self._fetch()

    def create(self, **kwargs):
        """Create is not supported for Task ASM resources

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        """Modify is not supported for Task ASM resources

                :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the modify method" % self.__class__.__name__
        )


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
