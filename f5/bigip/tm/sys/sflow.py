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
"""BIG-IP® system sflow module

REST URI
    ``http://localhost/mgmt/tm/sys/sflow``

GUI Path
   ``System->sFlow``

REST Kind
    ``tm:sys:sflow:*``
"""

# from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnnamedResource
# from f5.sdk_exception import UnsupportedMethod


class Sflow(OrganizingCollection):
    def __init__(self, sys):
        super(Sflow, self).__init__(sys)
        self._meta_data['allowed_lazy_attributes'] = [
            Global_Settings,
            Receivers]


class Global_Settings(OrganizingCollection):
    def __init__(self, sflow):
        super(Global_Settings, self).__init__(sflow)
        self._meta_data['allowed_lazy_attributes'] = [
            Http,
            Interface,
            System,
            Vlan]


class Http(UnnamedResource):
    def __init__(self, global_settings):
        super(Http, self).__init__(global_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:sflow:global-settings:http:httpstate'


class Interface(UnnamedResource):
    def __init__(self, global_settings):
        super(Interface, self).__init__(global_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:sflow:global-settings:interface:interfacestate'


class System(UnnamedResource):
    def __init__(self, global_settings):
        super(System, self).__init__(global_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:sflow:global-settings:system:systemstate'


class Vlan(UnnamedResource):
    def __init__(self, global_settings):
        super(Vlan, self).__init__(global_settings)
        self._meta_data['required_load_parameters'] = set()
        self._meta_data['required_json_kind'] =\
            'tm:sys:sflow:global-settings:vlan:vlanstate'


class Receivers(Collection):
    def __init__(self, sflow):
        super(Receivers, self).__init__(sflow)
        self._meta_data['allowed_lazy_attributes'] = [Receiver]
        self._meta_data['attribute_registry'] =\
            {'tm:sys:sflow:receiver:receiverstate': Receiver}


class Receiver(Resource):
    def __init__(self, receivers):
        super(Receiver, self).__init__(receivers)
        self._meta_data['required_creation_parameters'].update(
            ('name', 'address'))
        self._meta_data['required_json_kind'] =\
            'tm:sys:sflow:receiver:receiverstate'
