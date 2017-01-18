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

from f5.bigip.mixins import CheckExistenceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import NonExtantVirtualPolicy


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


class Profiles(Resource):
    """BIG-IP® LTM profile resource"""
    def __init__(self, Profiles_s):
        super(Profiles, self).__init__(Profiles_s)
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['required_json_kind'] =\
            "tm:ltm:virtual:profiles:profilesstate"


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

    def _load(self, **kwargs):
        """Override _load to retrieve object based on exists above."""

        if self._check_existence_by_collection(
                self._meta_data['container'], kwargs['name']):
            return super(Policies, self)._load(**kwargs)
        msg = 'The Policy named, {}, does not exist on the device.'.format(
            kwargs['name'])
        raise NonExtantVirtualPolicy(msg)


class Policies_s(Collection):
    """BIG-IP® LTM Policies resource"""
    def __init__(self, virtual):
        super(Policies_s, self).__init__(virtual)
        self._meta_data['allowed_lazy_attributes'] = [Policies]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:virtual:policies:policiesstate': Policies}
