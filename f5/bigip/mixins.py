# Copyright 2015-2016 F5 Networks Inc.
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
# NOTE:  Code taken from Effective Python Item 26

from f5.sdk_exception import F5SDKError


class ToDictMixin(object):
    """Convert an object's attributes to a dictionary"""
    traversed = {}
    Containers = tuple, list, set, frozenset, dict

    def to_dict(self):
        ToDictMixin.traversed = {}
        return self._to_dict()

    def _to_dict(self):
        result = self._traverse_dict(self.__dict__)
        return result

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin.Containers) or\
           hasattr(value, '__dict__'):
            if id(value) in ToDictMixin.traversed:
                return ToDictMixin.traversed[id(value)]
            else:
                ToDictMixin.traversed[id(value)] = ['TraversalRecord', key]
        if isinstance(value, ToDictMixin):
            return value._to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, item) for item in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class LazyAttributesRequired(F5SDKError):
    """Raised when a object accesses a lazy attribute that is not listed"""
    pass


class LazyAttributeMixin(object):
    """Allow attributes to be created lazily based on the allowed values"""
    def __getattr__(self, name):
        # ensure this object supports lazy attrs.
        cls_name = self.__class__.__name__
        if '_meta_data' not in self.__dict__:
            error_message = '%r does not have self._meta_data' % cls_name
            raise LazyAttributesRequired(error_message)
        elif 'allowed_lazy_attributes' not in self._meta_data:
            error_message = ('"allowed_lazy_attributes" not in',
                             'self._meta_data for class %s' % cls_name)
            raise LazyAttributesRequired(error_message)

        # ensure the requested attr is present
        lower_attr_names =\
            [la.__name__.lower() for la in
                self._meta_data['allowed_lazy_attributes']]
        if name not in lower_attr_names:
            error_message = "'%s' object has no attribute '%s'"\
                % (self.__class__, name)
            raise AttributeError(error_message)

        # Instantiate and potentially set the attr on the object
        # Issue #112 -- Only call setattr here if the lazy attribute
        # is NOT a `Resource`.  This should allow for only 1 ltm attribute
        # but many nat attributes just like the BIGIP device.
        for lazy_attribute in self._meta_data['allowed_lazy_attributes']:
            if name == lazy_attribute.__name__.lower():
                attribute = lazy_attribute(self)
                # Use the name of ResourceResource because importing causes
                # a circular reference
                bases = [base.__name__ for base in lazy_attribute.__bases__]
                if 'Resource' not in bases:
                    setattr(self, name, attribute)
                return attribute


class ExclusiveAttributesMixin(object):
    """Overrides ``__setattr__`` to remove exclusive attrs from the object."""
    def __setattr__(self, key, value):
        '''Remove any of the existing exclusive attrs from the object

        Objects attributes can be exclusive for example disable/enable.  So
        we need to make sure objects only have one of these attributes at
        at time so that the updates won't fail.
        '''
        if '_meta_data' in self.__dict__:
            # Sometimes this is called prior to full object construction
            for attr_set in self._meta_data['exclusive_attributes']:
                if key in attr_set:
                    new_set = set(attr_set) - set([key])
                    [self.__dict__.pop(n, '') for n in new_set]
        # Now set the attribute
        super(ExclusiveAttributesMixin, self).__setattr__(key, value)


class UnnamedResourceMixin(object):
    '''This makes a resource object work if there is no name.

    These objects do not support create or delete and are often found
    as Resources that are under an organizing collection.  For example
    the `mgmt/tm/sys/global-settings` is one of these and has a kind of
    `tm:sys:global-settings:global-settingsstate` and the URI does not
    match the kind.
    '''
    class UnsupportedMethod(F5SDKError):
        pass

    def create(self, **kwargs):
        '''Create is not supported for unnamed resources

        :raises: UnsupportedOperation
        '''
        raise self.UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        '''Delete is not supported for unnamed resources

        :raises: UnsupportedOperation
        '''
        raise self.UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__
        )

    def load(self, **kwargs):
        return self._load(**kwargs)

    def _load(self, **kwargs):
        '''Override _load because Unnamed Resources use their uri directly.

        The Unnamed resources don't have URIs that match their kinds so
        we need to use their URI directly instead of the container's URI
        with name/partitions.
        '''
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = True
        read_session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['uri']
        response = read_session.get(base_uri, **kwargs)
        self._local_update(response.json())
        return self
