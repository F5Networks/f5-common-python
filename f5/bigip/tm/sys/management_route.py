# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""BIG-IP® system management route module

REST URI
    ``http://localhost/mgmt/tm/sys/management-route``

GUI Path
    ``System --> Platform``

REST Kind
    ``tm:sys:management-route:management-routestate``
"""

from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Management_Routes(Collection):
    """BIG-IP® management-route collection"""
    def __init__(self, sys):
        super(Management_Routes, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [Management_Route]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:management-route:management-routestate': Management_Route}


class Management_Route(Resource):
    """BIG-IP® system management-route resource"""
    def __init__(self, Management_Routes):
        super(Management_Route, self).__init__(Management_Routes)
        self._meta_data['required_creation_parameters'].update(
            ('network', 'gateway'))
        self._meta_data['required_json_kind'] = \
            'tm:sys:management-route:management-routestate'

    def update(self, **kwargs):
        # Turns out that versions < 12 are incapable of sending the
        # "network" param when modifying. So, to accommodate the ability
        # to update devices in the standard way, we need to pop off the
        # network value on anything < 12.
        #
        # Actual error is this
        #
        # '{
        #   "code":400,
        #   "message":"\\"network\\" may not be specified in the context
        #             of the \\"modify\\" command. \\"network\\" may be
        #             specified using the following commands: create, list",
        #   "errorStack":[]
        # }'
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            kwargs.pop('network', None)
            self.__dict__.pop('network', None)
        return self._update(**kwargs)

    def modify(self, **kwargs):
        # Turns out that versions < 12 are incapable of sending the
        # "network" param when modifying. So, to accommodate the ability
        # to update devices in the standard way, we need to pop off the
        # network value on anything < 12.
        #
        # Actual error is this
        #
        # '{
        #   "code":400,
        #   "message":"\\"network\\" may not be specified in the context
        #             of the \\"modify\\" command. \\"network\\" may be
        #             specified using the following commands: create, list",
        #   "errorStack":[]
        # }'
        tmos_v = self._meta_data['bigip']._meta_data['tmos_version']
        if LooseVersion(tmos_v) < LooseVersion('12.0.0'):
            kwargs.pop('network', None)
            self.__dict__.pop('network', None)
        return self._modify(**kwargs)
