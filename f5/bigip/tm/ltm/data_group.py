# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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
"""BIG-IP® LTM data-group submodule.

REST URI
    ``http://localhost/mgmt/tm/ltm/data-group/``

GUI Path
    ``Local Traffic --> iRules --> Data Group List``

REST Kind
    ``tm:ltm:data-group*``
"""

from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Data_Group(OrganizingCollection):
    def __init__(self, ltm):
        super(Data_Group, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Internals,
            Internal,
            Externals,
            External
        ]


class Internals(Collection):
    def __init__(self, data_groups):
        super(Internals, self).__init__(data_groups)
        self._meta_data['allowed_lazy_attributes'] = [Internal]
        self._meta_data['required_json_kind'] = \
            u'tm:ltm:data-group:internal:internalcollectionstate'
        self._meta_data['attribute_registry'] = \
            {u'tm:ltm:data-group:internal:internalstate': Internal}
        self._meta_data['uri'] = self._meta_data['uri'].replace('_', '-')


class Internal(Resource):
    def __init__(self, internals):
        super(Internal, self).__init__(internals)
        self._meta_data['required_json_kind'] = \
            u'tm:ltm:data-group:internal:internalstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'type', 'records')
        )

    def update(self, **kwargs):
        if 'type' in self.__dict__:
            del self.__dict__['type']
        return self._update(**kwargs)


class Externals(Collection):
    def __init__(self, data_groups):
        super(Externals, self).__init__(data_groups)
        self._meta_data['allowed_lazy_attributes'] = [External]
        self._meta_data['required_json_kind'] =\
            u'tm:ltm:data-group:external:externalcollectionstate'
        self._meta_data['attribute_registry'] =\
            {u'tm:ltm:data-group:external:externalstate': External}
        self._meta_data['uri'] = self._meta_data['uri'].replace('_', '-')


class External(Resource):
    def __init__(self, externals):
        super(External, self).__init__(externals)
        self._meta_data['required_json_kind'] =\
            u'tm:ltm:data-group:external:externalstate'
        self._meta_data['required_creation_parameters'].update(
            ('name', 'externalFileName')
        )

    def update(self, **kwargs):
        if LooseVersion(self._meta_data['bigip']._meta_data['tmos_version']) \
                < LooseVersion('12.0.0'):
            if 'externalFileName' in self.__dict__:
                del self.__dict__['externalFileName']
            if 'type' in self.__dict__:
                del self.__dict__['type']
        return self._update(**kwargs)
