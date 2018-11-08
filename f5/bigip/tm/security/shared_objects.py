# coding=utf-8
#
# Copyright 2015-2017 F5 Networks Inc.
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

"""BIG-IP® Advanced Firewall Manager™ (AFM®) module.

REST URI
    ``http://localhost/mgmt/tm/security/shared-objects``

GUI Path
    ``Security --> Network Address Translation``

REST Kind
    ``tm:security:shared-objects:*``
"""
from distutils.version import LooseVersion
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Shared_Objects(OrganizingCollection):
    """BIG-IP® AFM® Nat organizing collection."""

    def __init__(self, security):
        super(Shared_Objects, self).__init__(security)
        self._meta_data['minimum_version'] = '14.0.0'
        self._meta_data['allowed_lazy_attributes'] = [
            Address_Lists,
            Port_Lists]


class Address_Lists(Collection):
    """BIG-IP® AFM® Address List collection"""
    def __init__(self, shared_objects):
        super(Address_Lists, self).__init__(shared_objects)
        self._meta_data['allowed_lazy_attributes'] = [Address_List]
        self._meta_data['attribute_registry'] = \
            {'tm:security:shared-objects:address-list:address-liststate':
                Address_List}


class Address_List(Resource):
    """BIG-IP® Address List resource"""
    def __init__(self, address_lists):
        super(Address_List, self).__init__(address_lists)
        self._meta_data['required_json_kind'] = \
            'tm:security:shared-objects:address-list:address-liststate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self.tmos_ver = self._meta_data['bigip'].tmos_version
        if LooseVersion(self.tmos_ver) < LooseVersion('12.0.0'):
            self._meta_data['minimum_additional_parameters'] = {
                'addressLists', 'addresses', 'geo'}
        else:
            self._meta_data['minimum_additional_parameters'] = {
                'addressLists', 'addresses', 'geo', 'fqdns'}


class Port_Lists(Collection):
    """BIG-IP® AFM® Port List collection"""
    def __init__(self, shared_objects):
        super(Port_Lists, self).__init__(shared_objects)
        self._meta_data['allowed_lazy_attributes'] = [Port_List]
        self._meta_data['attribute_registry'] = \
            {'tm:security:shared-objects:port-list:port-liststate':
                Port_List}


class Port_List(Resource):
    """BIG-IP® Port List resource"""
    def __init__(self, port_lists):
        super(Port_List, self).__init__(port_lists)
        self._meta_data['required_json_kind'] = \
            'tm:security:shared-objects:port-list:port-liststate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['minimum_additional_parameters'] = {'ports',
                                                            'portLists'}
