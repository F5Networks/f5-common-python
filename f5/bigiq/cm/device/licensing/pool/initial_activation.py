# coding=utf-8
#
# Copyright 2017 F5 Networks Inc.
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

"""BIG-IQ® license pool regkeys.

REST URI
    ``http://localhost/mgmt/cm/device/licensing/pool/initial-activation``

REST Kind
    ``cm:device:licensing:pool:initial-activation:*``
"""

from f5.bigiq.resource import Collection
from f5.bigiq.resource import Resource


class Initial_Activations(Collection):
    def __init__(self, pool):
        super(Initial_Activations, self).__init__(pool)
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:initial-activation:initialactivationworkercollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Initial_Activation]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:initial-activation:initialactivationworkeritemstate': Initial_Activation  # NOQA
        }


class Initial_Activation(Resource):
    def __init__(self, initial_activations):
        super(Initial_Activation, self).__init__(initial_activations)
        self._meta_data['required_creation_parameters'] = {'name', 'regKey'}
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:initial-activation:initialactivationworkeritemstate'
