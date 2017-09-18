# coding=utf-8
#
# Copyright 2014 F5 Networks Inc.
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

"""BIG-IP® Local Traffic Manager (LTM) virtual module.

REST URI
    ``http://localhost/mgmt/tm/ltm/virtual``

GUI Path
    ``Local Traffic --> Virtual Servers``

REST Kind
    ``tm:ltm:virtual:*``
"""

from distutils.version import LooseVersion

from f5.bigip.mixins import CheckExistenceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import NonExtantVirtualPolicy
from f5.sdk_exception import UnregisteredKind
from f5.sdk_exception import URICreationCollision

from requests import HTTPError


class Virtuals(Collection):
    """BIG-IP® LTM virtual collection"""
    def __init__(self, ltm):
        super(Virtuals, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Virtual]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:virtualstate': Virtual}


class Virtual(Resource):
    """BIG-IP® LTM virtual resource"""
    def __init__(self, virtual_s):
        super(Virtual, self).__init__(virtual_s)
        self._meta_data['allowed_lazy_attributes'] = [Profiles_s]
        self._meta_data['required_json_kind'] = 'tm:ltm:virtual:virtualstate'
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:profiles:profilescollectionstate': Profiles_s,
             'tm:ltm:virtual:policies:policiescollectionstate': Policies_s}

    def load(self, **kwargs):
        result = self._load(**kwargs)
        if not hasattr(result, 'rules'):
            result.__dict__.update({'rules': []})
        return result

    def create(self, **kwargs):
        result = self._create(**kwargs)
        if not hasattr(result, 'rules'):
            result.__dict__.update({'rules': []})
        return result

    def update(self, **kwargs):
        result = self._update(**kwargs)
        if not hasattr(result, 'rules'):
            self.__dict__.update({'rules': []})

    def modify(self, **kwargs):
        result = self._modify(**kwargs)
        if not hasattr(result, 'rules'):
            self.__dict__.update({'rules': []})


class Profiles(Resource, CheckExistenceMixin):
    """BIG-IP® LTM profile resource"""
    def __init__(self, Profiles_s):
        super(Profiles, self).__init__(Profiles_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            "tm:ltm:virtual:profiles:profilesstate"

    def _exists(self, **kwargs):
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) == LooseVersion('11.6.0'):
            return self._check_existence_by_collection(self._meta_data['container'], kwargs['name'])
        return super(Profiles, self)._exists(**kwargs)


class Profiles_s(Collection):
    """BIG-IP® LTM profile collection"""
    def __init__(self, virtual):
        super(Profiles_s, self).__init__(virtual)
        self._meta_data['allowed_lazy_attributes'] = [Profiles]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:profiles:profilesstate': Profiles}


class Policies(Resource, CheckExistenceMixin):
    """BIG-IP® LTM Policies resource"""
    def __init__(self, Policies_s):
        super(Policies, self).__init__(Policies_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            "tm:ltm:virtual:policies:policiesstate"

    def exists(self, **kwargs):
        """check existence of policy under virtual."""
        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])

    def load(self, **kwargs):
        """Override load to retrieve object based on exists above."""
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if self._check_existence_by_collection(
                self._meta_data['container'], kwargs['name']):
            if LooseVersion(tmos_v) == LooseVersion('11.5.4'):
                return self._load_11_5_4(**kwargs)
            else:
                return self._load(**kwargs)
        msg = 'The Policy named, {}, does not exist on the device.'.format(
            kwargs['name'])
        raise NonExtantVirtualPolicy(msg)

    def _load_11_5_4(self, **kwargs):
        """Custom _load method to accommodate for issue in 11.5.4,

        where an existing object would return 404 HTTP response.
        """
        if 'uri' in self._meta_data:
            error = "There was an attempt to assign a new uri to this " \
                    "resource, the _meta_data['uri'] is %s and it should" \
                    " not be changed." % (self._meta_data['uri'])
            raise URICreationCollision(error)
        requests_params = self._handle_requests_params(kwargs)
        self._check_load_parameters(**kwargs)
        kwargs['uri_as_parts'] = True
        refresh_session = self._meta_data['bigip']._meta_data[
            'icr_session']
        base_uri = self._meta_data['container']._meta_data['uri']
        kwargs.update(requests_params)
        for key1, key2 in self._meta_data['reduction_forcing_pairs']:
            kwargs = self._reduce_boolean_pair(kwargs, key1, key2)
        kwargs = self._check_for_python_keywords(kwargs)
        try:
            response = refresh_session.get(base_uri, **kwargs)
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            if err.response.status_code == 404:
                return self._return_object(self._meta_data['container'],
                                           kwargs['name'])
        # Make new instance of self
        return self._produce_instance(response)

    def create(self, **kwargs):
        """Custom _create method to accommodate for issue 11.5.4 and 12.1.1,

        Where creation of an object would return 404, despite the object
        being created.
        """
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) == LooseVersion('11.5.4') or LooseVersion(
                tmos_v) == LooseVersion('12.1.1'):
            if 'uri' in self._meta_data:
                error = "There was an attempt to assign a new uri to this " \
                        "resource, the _meta_data['uri'] is %s and it should" \
                        " not be changed." % (self._meta_data['uri'])
                raise URICreationCollision(error)
            self._check_exclusive_parameters(**kwargs)
            requests_params = self._handle_requests_params(kwargs)
            self._check_create_parameters(**kwargs)

            # Reduce boolean pairs as specified by the meta_data entry below
            for key1, key2 in self._meta_data['reduction_forcing_pairs']:
                kwargs = self._reduce_boolean_pair(kwargs, key1, key2)

            # Make convenience variable with short names for this method.
            _create_uri = self._meta_data['container']._meta_data['uri']
            session = self._meta_data['bigip']._meta_data['icr_session']
            # We using try/except just in case some HF will fix
            # this in 11.5.4

            try:
                response = session.post(
                    _create_uri, json=kwargs, **requests_params)

            except HTTPError as err:
                if err.response.status_code != 404:
                    raise
                if err.response.status_code == 404:
                    return self._return_object(self._meta_data['container'],
                                               kwargs['name'])
            # Make new instance of self
            return self._produce_instance(response)
        else:
            return self._create(**kwargs)


class Policies_s(Collection):
    """BIG-IP® LTM Policies resource"""
    def __init__(self, virtual):
        super(Policies_s, self).__init__(virtual)
        self._meta_data['allowed_lazy_attributes'] = [Policies]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:policies:policiesstate': Policies}

    def get_collection(self, **kwargs):
        """We need special get collection method to address issue in 11.5.4

        In 11.5.4 collection 'items' were nested under 'policiesReference'
        key. This has caused get_collection() calls to return empty list.
        This fix will update the list if the policiesReference key is found
        and 'items' key do not exists in __dict__.

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

        if 'policiesReference' in self.__dict__ and 'items' not in \
                self.__dict__:
            for item in self.policiesReference['items']:
                kind = item['kind']
                if kind in self._meta_data['attribute_registry']:
                    # If it has a kind, it must be registered.
                    instance = \
                        self._meta_data['attribute_registry'][kind](self)
                    instance._local_update(item)
                    instance._activate_URI(instance.selfLink)
                    list_of_contents.append(instance)
                else:
                    error_message = '%r is not registered!' % kind
                    raise UnregisteredKind(error_message)

        return list_of_contents
