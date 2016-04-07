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

from f5.bigip.mixins import UnnamedResourceMixin, ExclusiveAttributesMixin
from f5.bigip.resource import Resource, MissingRequiredCreationParameter, KindTypeMismatch

class Trust(UnnamedResourceMixin, ExclusiveAttributesMixin, Resource):
    """ Helper class which contains shared methods and attributes of
        Add_To_Trust and Remove_From_Trust classes.

     .. note::
         This class inherits from 3 classes due to the requirement of exclusive attributes

    """

    def __init__(self, cm):
        super(Trust, self).__init__(cm)
        endpoint = self.__class__.__name__.lower().replace('_', '-')
        self._meta_data['uri'] = \
            self._meta_data['container']._meta_data['uri'] + endpoint + '/'

    def update(self, **kwargs):
        """Update is not supported for trust operations

        :raises: UnsupportedOperation
        """
        raise self.UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__)

    def load(self, **kwargs):
        """Load is not supported for trust operations

        :raises: UnsupportedOperation
        """
        raise self.UnsupportedMethod(
            "%s does not support the update method" % self.__class__.__name__)

    def _kwadd(self, kwargs):
        """Helper method to append kwargs
           without unpacking them with "command":"run"
        """
        kwargs['command'] = 'run'

    def run(self, **kwargs):
        """Run command on the resource on the BIG-IP®.

        Modified version of the _create method in Resource class. Uses HTTP POST
        on the unnamed resource URI which allows only POST methods.

        .. note::
            This object is similar to failover object in the sys module


        :param kwargs: All the key-values needed to create the resource.

        .. note::
            If kwargs has a 'requests_params' key the corresponding dict will
            be passed to the underlying requests.session.post method where it will
            be handled according to that API. THIS IS HOW TO PASS QUERY-ARGS!

        :raises: KindTypeMismatch, MissingRequiredCreationParameter
        :returns: ``self`` - A python object that represents the object's
                  configuration and state on the BIG-IP®

        """
        # Add "command":"run" entry to kwargs
        self._kwadd(kwargs)
        requests_params = self._handle_requests_params(kwargs)
        key_set = set(kwargs.keys())
        required_minus_received = \
            self._meta_data['required_creation_parameters'] - key_set
        if required_minus_received != set():
            error_message = 'Missing required params: %r' \
                            % required_minus_received
            raise MissingRequiredCreationParameter(error_message)

        session = self._meta_data['bigip']._meta_data['icr_session']

        # Invoke the REST operation on the device.
        response = session.post(self._meta_data['uri'], json=kwargs, **requests_params)

        # Post-process the response
        self._local_update(response.json())

        if self.kind != self._meta_data['required_json_kind']:
            error_message = "For instances of type '%r' the corresponding" \
                        " kind must be '%r' but creation returned JSON with kind: %r" \
                        % (self.__class__.__name__,
                        self._meta_data['required_json_kind'],
                        self.kind)
            raise KindTypeMismatch(error_message)

        return self

class Add_To_Trust(Trust):
    """BIG-IP® Add-To-Trust resource

    Use this object to set or overwrite device trust

    """
    def __init__(self, Trust):
        super(Add_To_Trust, self).__init__(Trust)
        self._meta_data['exclusive_attributes'].append(
            ('caDevice', 'nonCaDevice'))
        self._meta_data['required_creation_parameters'].update(
            ('device', 'deviceName', 'username', 'password'))
        self._meta_data['required_json_kind'] = \
            'tm:cm:add-to-trust:runstate'


class Remove_From_Trust(Trust):
    """BIG-IP® Remove-From-Trust resource

    Use this object to remove device trust

    .. note::
        This will only remove trust setting on a single BIG-IP®.
        Full trust removal requires that the operation is
        carried out on both target devices

    """
    def __init__(self, Trust):
        super(Remove_From_Trust, self).__init__(Trust)
        self._meta_data['required_creation_parameters'].update(
            ('deviceName',))
        self._meta_data['required_json_kind'] = \
            'tm:cm:remove-from-trust:runstate'


