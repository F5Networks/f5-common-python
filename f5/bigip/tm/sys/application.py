# coding=utf-8
#
# Copyright 2014-2016 F5 Networks Inc.
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

"""BIG-IP® iApp (application) module

REST URI
    ``http://localhost/mgmt/sys/application/``

GUI Path
    ``iApps``

REST Kind
    ``tm:sys:application:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource

from requests import HTTPError


class Application(OrganizingCollection):
    """BIG-IP® iApp collection."""
    def __init__(self, sys):
        super(Application, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Aplscripts,
            Customstats,
            Services,
            Templates
        ]


class Aplscripts(Collection):
    """BIG-IP® iApp script collection."""
    def __init__(self, application):
        super(Aplscripts, self).__init__(application)
        self._meta_data['allowed_lazy_attributes'] = [Aplscript]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:application:apl-script:apl-scriptstate': Aplscript}


class Aplscript(Resource):
    """BIG-IP® iApp script resource."""
    def __init__(self, apl_script_s):
        super(Aplscript, self).__init__(apl_script_s)
        self._meta_data['required_json_kind'] =\
            'tm:sys:application:apl-script:apl-scriptstate'


class Customstats(Collection):
    """BIG-IP® iApp custom stats sub-collection."""
    def __init__(self, application):
        super(Customstats, self).__init__(application)
        self._meta_data['allowed_lazy_attributes'] = [Customstat]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:application:custom-stat:custom-statstate': Customstat}


class Customstat(Resource):
    """BIG-IP® iApp custom stats sub-collection resource."""
    def __init__(self, custom_stat_s):
        super(Customstat, self).__init__(custom_stat_s)
        self._meta_data['required_json_kind'] =\
            'tm:sys:application:custom-stat:custom-statstate'


class Services(Collection):
    """BIG-IP® iApp service sub-collection."""
    def __init__(self, application):
        super(Services, self).__init__(application)
        self._meta_data['allowed_lazy_attributes'] = [Service]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:application:service:servicestate': Service}


class Service(Resource):
    """BIG-IP® iApp service sub-collection resource"""
    def __init__(self, service_s):
        super(Service, self).__init__(service_s)
        self._meta_data['required_creation_parameters'].update(
            ('template', 'partition')
        )
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:sys:application:service:servicestate'
        self._meta_data['disallowed_load_parameters'] = \
            set(['template', 'trafficGroup'])

    def _create(self, **kwargs):
        '''Create service on device and create accompanying Python object.

        :params kwargs: keyword arguments passed in from create call
        :raises: HTTPError
        :returns: Python Service object
        '''

        try:
            return super(Service, self)._create(**kwargs)
        except HTTPError as ex:
            if "The configuration was updated successfully but could not be " \
                    "retrieved" not in ex.response.text:
                raise

            # BIG-IP® will create in Common partition if none is given.
            # In order to create the uri properly in this class's load,
            # drop in Common as the partition in kwargs.
            if 'partition' not in kwargs:
                kwargs['partition'] = 'Common'
            # Pop all but the necessary load kwargs from the kwargs given to
            # create. Otherwise, load may fail.
            kwargs_copy = kwargs.copy()
            for key in kwargs_copy:
                if key not in self._meta_data['required_load_parameters']:
                    kwargs.pop(key)
            # If response was created successfully, do a local_update.
            # If not, call to overridden _load method via load
            return self.load(**kwargs)

    def update(self, **kwargs):
        '''Push local updates to the object on the device.

        :params kwargs: keyword arguments for accessing/modifying the object
        :returns: updated Python object
        '''

        inherit_device_group = self.__dict__.get('inheritedDevicegroup', False)
        if inherit_device_group == 'true':
            self.__dict__.pop('deviceGroup')
        return self._update(**kwargs)

    def _load(self, **kwargs):
        '''Load python Service object with response JSON from BIG-IP®.

        :params kwargs: keyword arguments for talking to the device
        :returns: populated Service object
        '''
        # Some kwargs should be popped before we do a load
        for key in self._meta_data['disallowed_load_parameters']:
            if key in kwargs:
                kwargs.pop(key)

        self._check_load_parameters(**kwargs)
        name = kwargs.pop('name', '')
        partition = kwargs.pop('partition', '')
        read_session = self._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']

        load_uri = self._build_service_uri(base_uri, partition, name)
        response = read_session.get(load_uri, uri_as_parts=False, **kwargs)
        return self._produce_instance(response)

    def _build_service_uri(self, base_uri, partition, name):
        '''Build the proper uri for a service resource.

        This follows the scheme:
            <base_uri>/~<partition>~<<name>.app>~<name>

        :param base_uri: str -- base uri for container
        :param partition: str -- partition for this service
        :param name: str -- name of the service
        :returns: str -- uri to access this service
        '''
        name = name.replace('/', '~')
        return '%s~%s~%s.app~%s' % (base_uri, partition, name, name)

    def exists(self, **kwargs):
        '''Check for the existence of the named object on the BIG-IP

        Override of resource.Resource exists() to build proper URI unique to
        service resources.

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
        '''

        requests_params = self._handle_requests_params(kwargs)
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = False
        session = self._meta_data['bigip']._meta_data['icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']
        partition = kwargs.pop('partition')
        name = kwargs.pop('name')

        exists_uri = self._build_service_uri(base_uri, partition, name)
        kwargs.update(requests_params)
        try:
            session.get(exists_uri, **kwargs)
        except HTTPError as err:
            if err.response.status_code == 404:
                return False
            else:
                raise
        return True


class Templates(Collection):
    """BIG-IP® iApp template sub-collection"""
    def __init__(self, application):
        super(Templates, self).__init__(application)
        self._meta_data['allowed_lazy_attributes'] = [Template]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:application:template:templatestate': Template}


class Template(Resource):
    """BIG-IP® iApp template sub-collection resource"""
    def __init__(self, template_s):
        super(Template, self).__init__(template_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            'tm:sys:application:template:templatestate'
