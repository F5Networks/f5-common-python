# coding=utf-8
#
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


try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError as exc:
        message = ("Maybe you're using Python < 2.7 and do not have the "
                   "orderreddict external dependency installed.")
        raise exc(message)

from distutils.version import LooseVersion
from six import iteritems

import logging

from f5.sdk_exception import EmptyContent
from f5.sdk_exception import InvalidCommand
from f5.sdk_exception import LazyAttributesRequired
from f5.sdk_exception import MissingHttpHeader
from f5.sdk_exception import UnsupportedMethod
from f5.sdk_exception import UnsupportedTmosVersion
from f5.sdk_exception import UtilError


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

        # This iteration breaks if the second value comes before
        # the first. We must use ordered dicts here
        tmp = OrderedDict(sorted(iteritems(instance_dict), key=lambda t: t[0]))
        for key, value in iteritems(tmp):
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


class LazyAttributeMixin(object):
    """Allow attributes to be created lazily based on the allowed values"""
    def __getattr__(container, name):
        # ensure this object supports lazy attrs.
        cls_name = container.__class__.__name__
        if 'allowed_lazy_attributes' not in container._meta_data:
            error_message = ('"allowed_lazy_attributes" not in',
                             'container._meta_data for class %s' % cls_name)
            raise LazyAttributesRequired(error_message)

        # ensure the requested attr is present
        attr_names = container.transform_attr_names()
        if name not in attr_names:
            error_message = "'%s' object has no attribute '%s'"\
                % (container.__class__, name)
            raise AttributeError(error_message)

        # Instantiate and potentially set the attr on the object
        # Issue #112 -- Only call setattr here if the lazy attribute
        # is NOT a `Resource`.  This should allow for only 1 ltm attribute
        # but many nat attributes just like the BIGIP device.
        for lazy_attribute in container._meta_data['allowed_lazy_attributes']:
            if name == lazy_attribute.__name__.lower():
                attribute = lazy_attribute(container)
                bases = [base.__name__ for base in lazy_attribute.__bases__]
                # Doing version check per each resource
                container._check_supported_versions(container, attribute)
                if 'Resource' not in bases:
                    setattr(container, name, attribute)
                return attribute

    def transform_attr_names(self):
        attr_names = \
            [la.__name__.lower() for la in
             self._meta_data['allowed_lazy_attributes']]
        return attr_names

    def _check_supported_versions(self, container, attribute):
        tmos_v = container._meta_data['bigip'].tmos_version
        minimum = attribute._meta_data['minimum_version']
        if LooseVersion(tmos_v) < LooseVersion(minimum):
            error = "There was an attempt to access resource: \n{}\n which " \
                    "is not implemented in the device's TMOS version: {}. " \
                    "The minimum TMOS version in which this resource *is* " \
                    "supported is {}".format(
                        attribute._meta_data['uri'],
                        tmos_v,
                        minimum)
            raise UnsupportedTmosVersion(error)

    def _is_version_supported_method(container, method_version):
        """Helper method

         To use in instances where class methods on some resources
         require a specific TMOS version to run.

        Raises::
                UnsupportedTmosVersion
        """
        tmos_v = container._meta_data['bigip'].tmos_version
        if LooseVersion(tmos_v) < LooseVersion(method_version):
            error = "There was an attempt to use a method which " \
                    "has not been implemented or supported " \
                    "in the device's TMOS version: %s. " \
                    "Minimum TMOS version supported is %s" % (
                        tmos_v, method_version)
            raise UnsupportedTmosVersion(error)


class ExclusiveAttributesMixin(object):
    """Overrides ``__setattr__`` to remove exclusive attrs from the object."""
    def __setattr__(self, key, value):
        """Remove any of the existing exclusive attrs from the object

        Objects attributes can be exclusive for example disable/enable.  So
        we need to make sure objects only have one of these attributes at
        at time so that the updates won't fail.
        """
        if '_meta_data' in self.__dict__:
            # Sometimes this is called prior to full object construction
            for attr_set in self._meta_data['exclusive_attributes']:
                if key in attr_set:
                    new_set = set(attr_set) - set([key])
                    [self.__dict__.pop(n, '') for n in new_set]
        # Now set the attribute
        super(ExclusiveAttributesMixin, self).__setattr__(key, value)


class CommandExecutionMixin(object):
    """This adds command execution option on the objects.

    These objects do not support create, delete, load, and require
    a separate method of execution. Commands do not have
    direct mapping to an HTTP method so usage of POST
    and an absolute URI is required.

    """

    def create(self, **kwargs):
        """Create is not supported for command execution

        :raises: UnsupportedOperation
        """
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for command execution

        :raises: UnsupportedOperation
        """
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__
        )

    def load(self, **kwargs):
        """Load is not supported for command execution

                :raises: UnsupportedOperation
        """
        raise UnsupportedMethod(
            "%s does not support the load method" % self.__class__.__name__
        )

    def _is_allowed_command(self, command):
        """Checking if the given command is allowed on a given endpoint."""
        cmds = self._meta_data['allowed_commands']
        if command not in self._meta_data['allowed_commands']:
            error_message = "The command value {0} does not exist. " \
                            "Valid commands are {1}".format(command, cmds)
            raise InvalidCommand(error_message)

    def _check_command_result(self):
        """If command result exists run these checks."""
        if self.commandResult.startswith('/bin/bash'):
            raise UtilError('%s' % self.commandResult.split(' ', 1)[1])
        if self.commandResult.startswith('/bin/mv'):
            raise UtilError('%s' % self.commandResult.split(' ', 1)[1])
        if self.commandResult.startswith('/bin/ls'):
            raise UtilError('%s' % self.commandResult.split(' ', 1)[1])
        if self.commandResult.startswith('/bin/rm'):
            raise UtilError('%s' % self.commandResult.split(' ', 1)[1])
        if 'invalid option' in self.commandResult:
            raise UtilError('%s' % self.commandResult)
        if 'Invalid option' in self.commandResult:
            raise UtilError('%s' % self.commandResult)
        if 'usage: /usr/bin/get_dossier' in self.commandResult:
            raise UtilError('%s' % self.commandResult)

    def exec_cmd(self, command, **kwargs):
        """Wrapper method that can be changed in the inheriting classes."""
        self._is_allowed_command(command)
        self._check_command_parameters(**kwargs)
        return self._exec_cmd(command, **kwargs)

    def _exec_cmd(self, command, **kwargs):
        """Create a new method as command has specific requirements.

        There is a handful of the TMSH global commands supported,
        so this method requires them as a parameter.

        :raises: InvalidCommand
        """

        kwargs['command'] = command
        self._check_exclusive_parameters(**kwargs)
        requests_params = self._handle_requests_params(kwargs)
        session = self._meta_data['bigip']._meta_data['icr_session']
        response = session.post(
            self._meta_data['uri'], json=kwargs, **requests_params)
        new_instance = self._stamp_out_core()
        new_instance._local_update(response.json())
        if 'commandResult' in new_instance.__dict__:
            new_instance._check_command_result()

        return new_instance


class FileUploadMixin(object):
    def _upload_file(self, filepathname, **kwargs):
        with open(filepathname, 'rb') as fileobj:
            self._upload(fileobj, **kwargs)

    def _upload(self, fileinterface, **kwargs):
        size = len(fileinterface.read())
        fileinterface.seek(0)
        requests_params = self._handle_requests_params(kwargs)
        session = self._meta_data['icr_session']
        chunk_size = kwargs.pop('chunk_size', 512 * 1024)
        start = 0
        while True:
            file_slice = fileinterface.read(chunk_size)
            if not file_slice:
                break

            current_bytes = len(file_slice)
            if current_bytes < chunk_size:
                end = size
            else:
                end = start + current_bytes
            headers = {
                'Content-Range': '%s-%s/%s' % (start,
                                               end - 1,
                                               size),
                'Content-Type': 'application/octet-stream'}
            data = {
                'data': file_slice,
                'headers': headers,
                'verify': False
            }
            logging.debug(data)
            requests_params.update(data)
            session.post(self.file_bound_uri,
                         **requests_params)
            start += current_bytes


class FileDownloadMixin(object):
    def _download_file(self, src, dest, **kwargs):
        with open(dest, 'wb') as fileobj:
            self._download(src, fileobj, **kwargs)

    def _download(self, src, fileinterface, **kwargs):
        requests_params = self._handle_requests_params(kwargs)
        session = self._meta_data['icr_session']
        chunk_size = kwargs.pop('chunk_size', 512 * 1024)
        self.file_bound_uri = self._meta_data['uri'] + src
        start = 0
        end = chunk_size - 1
        size = 0
        current_bytes = 0

        while True:
            content_range = "%s-%s/%s" % (start, end, size)
            headers = {
                'Content-Range': content_range,
                'Content-Type': 'application/octet-stream'
            }
            data = {
                'headers': headers,
                'verify': False,
                'stream': True
            }
            logging.debug(data)
            requests_params.update(data)
            response = session.get(self.file_bound_uri,
                                   **requests_params)
            if response.status_code == 200:
                # If the size is zero, then this is the first time through
                # the loop and we don't want to write data because we
                # haven't yet figured out the total size of the file.
                if size > 0:
                    current_bytes += chunk_size
                    for chunk in response.iter_content(chunk_size):
                        fileinterface.write(chunk)
            # Once we've downloaded the entire file, we can break out of
            # the loop
            if end == size:
                break
            crange = response.headers['Content-Range']
            # Determine the total number of bytes to read.
            if size == 0:
                size = int(crange.split('/')[-1]) - 1
                # If the file is smaller than the chunk_size, the BigIP
                # will return an HTTP 400. Adjust the chunk_size down to
                # the total file size...
                if chunk_size > size:
                    end = size
                # ...and pass on the rest of the code.
                continue
            start += chunk_size
            if (current_bytes + chunk_size) > size:
                end = size
            else:
                end = start + chunk_size - 1


class AsmFileMixin(object):
    """Mixin for manipulating files for ASM file-transfer endpoints.


    For ease of code maintenance this is separate from FileUploadMixin
    on purpose.

    """
    def _download_file(self, filepathname):
            self._download(filepathname)

    def _download(self, filepathname):
        session = self._meta_data['icr_session']
        with open(filepathname, 'wb') as writefh:
            headers = {
                'Content-Type': 'application/json'
            }
            req_params = {'headers': headers,
                          'verify': False}
            response = session.get(self.file_bound_uri, **req_params)
            if response.status_code == 200:
                if 'Content-Length' not in response.headers:
                    error_message = "The Content-Length header is not present."
                    raise MissingHttpHeader(error_message)

                length = response.headers['Content-Length']

                if int(length) > 0:
                    writefh.write(response.content)
                else:
                    error = "Invalid Content-Length value returned: %s ," \
                            "the value should be greater than 0" % length
                    raise EmptyContent(error)

    def _upload_file(self, filepathname, **kwargs):
        with open(filepathname, 'rb') as fileobj:
            self._upload(fileobj, **kwargs)

    def _upload(self, fileinterface, **kwargs):
        size = len(fileinterface.read())
        fileinterface.seek(0)
        requests_params = self._handle_requests_params(kwargs)
        session = self._meta_data['icr_session']
        chunk_size = kwargs.pop('chunk_size', 512 * 1024)
        start = 0
        while True:
            file_slice = fileinterface.read(chunk_size)
            if not file_slice:
                break

            current_bytes = len(file_slice)
            if current_bytes < chunk_size:
                end = size
            else:
                end = start + current_bytes
            headers = {
                'Content-Range': '%s-%s/%s' % (start,
                                               end - 1,
                                               size),
                'Content-Type': 'application/octet-stream'}
            data = {'data': file_slice,
                    'headers': headers,
                    'verify': False}
            logging.debug(data)
            requests_params.update(data)
            session.post(self.file_bound_uri,
                         **requests_params)
            start += current_bytes


class DeviceMixin(object):
    '''Manage BigIP device cluster in a general way.'''

    def get_device_info(self, bigip):
        '''Get device information about a specific BigIP device.

        :param bigip: bigip object --- device to inspect
        :returns: bigip object
        '''

        coll = bigip.tm.cm.devices.get_collection()
        device = [device for device in coll if device.selfDevice == 'true']
        assert len(device) == 1
        return device[0]


class CheckExistenceMixin(object):
    '''In 11.6.0 some items return True on exists whether they exist or not'''

    def _check_existence_by_collection(self, container, item_name):
        '''Check existnce of item based on get collection call.

        :param collection: container object -- capable of get_collection()
        :param item_name: str -- name of item to search for in collection
        '''

        coll = container.get_collection()
        for item in coll:
            if item.name == item_name:
                return True
        return False

    def _return_object(self, container, item_name):
        """Helper method to retrieve the object"""
        coll = container.get_collection()
        for item in coll:
            if item.name == item_name:
                return item
