# coding=utf-8
#
#  Copyright 2017 F5 Networks Inc.
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


from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedMethod


class System(OrganizingCollection):
    def __init__(self, shared):
        super(System, self).__init__(shared)
        self._meta_data['allowed_lazy_attributes'] = [
            Authn
        ]


class Authn(OrganizingCollection):
    def __init__(self, system):
        super(Authn, self).__init__(system)
        self._meta_data['allowed_lazy_attributes'] = [
            Providers
        ]


class Providers(OrganizingCollection):
    def __init__(self, authn):
        super(Providers, self).__init__(authn)
        self._meta_data['allowed_lazy_attributes'] = [
            Tmos_s
        ]


class Tmos_s(Collection):
    def __init__(self, container):
        super(Tmos_s, self).__init__(container)
        if container._meta_data['bigip']._meta_data['tmos_version'] < '13.1.0':
            # Starting from bigip v13.1.0 tmos resources 'kind' was changed
            # from 'mcpremoteproviderstate' to 'authproviderstate'
            # and tmos collection 'kind'
            # from 'mcpremoteprovidercollectionstate' to 'mcpremoteproviderstate"
            self._meta_data['required_json_kind'] = 'cm:system:authn:providers:tmos:mcpremoteprovidercollectionstate'
            self._meta_data['attribute_registry'] = {
                'cm:system:authn:providers:tmos:mcpremoteproviderstate': Tmos
            }
        else:
            self._meta_data['required_json_kind'] = 'cm:system:authn:providers:tmos:authprovidercollectionstate'
            self._meta_data['attribute_registry'] = {
                'cm:system:authn:providers:tmos:authproviderstate': Tmos
            }
        self._meta_data['allowed_lazy_attributes'] = [Tmos]


class Tmos(Resource):
    def __init__(self, container):
        super(Tmos, self).__init__(container)
        if container._meta_data['bigip']._meta_data['tmos_version'] < '13.1.0':
            # Starting from bigip v13.1.0 tmos resource 'kind' was changed
            # from 'mcpremoteproviderstate' to 'authproviderstate'
            self._meta_data['required_json_kind'] = 'cm:system:authn:providers:tmos:mcpremoteproviderstate'
        else:
            self._meta_data['required_json_kind'] = 'ccm:system:authn:providers:tmos:authproviderstate'
            self._meta_data['required_load_parameters'] = set(('id',))

    def create(self, **kwargs):
        raise UnsupportedMethod(
            "Only a single remote mcp auth provider allowed."
        )

    def update(self, **kwargs):
        # You can technically do this, but it will really screw up the system
        raise UnsupportedMethod

    def modify(self, **kwargs):
        # You can technically do this, but it will really screw up the system
        raise UnsupportedMethod

    def delete(self, **kwargs):
        # You can technically do this, but it will really screw up the system
        raise UnsupportedMethod
