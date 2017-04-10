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
    ``http://localhost/mgmt/tm/security/firewall``

GUI Path
    ``Security --> Network Firewall``

REST Kind
    ``tm:security:firewall:*``
"""
from f5.bigip.mixins import CheckExistenceMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import NonExtantFirewallRule

from distutils.version import LooseVersion


class Firewall(OrganizingCollection):
    """BIG-IP® AFM® Firewall organizing collection."""

    def __init__(self, security):
        super(Firewall, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Address_Lists,
            Port_Lists,
            Rule_Lists]


class Address_Lists(Collection):
    """BIG-IP® AFM® Address List collection"""
    def __init__(self, firewall):
        super(Address_Lists, self).__init__(firewall)
        self._meta_data['allowed_lazy_attributes'] = [Address_List]
        self._meta_data['attribute_registry'] = \
            {'tm:security:firewall:address-list:address-liststate':
                Address_List}


class Address_List(Resource):
    """BIG-IP® Address List resource"""
    def __init__(self, address_lists):
        super(Address_List, self).__init__(address_lists)
        self._meta_data['required_json_kind'] = \
            'tm:security:firewall:address-list:address-liststate'
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
    def __init__(self, firewall):
        super(Port_Lists, self).__init__(firewall)
        self._meta_data['allowed_lazy_attributes'] = [Port_List]
        self._meta_data['attribute_registry'] = \
            {'tm:security:firewall:port-list:port-liststate':
                Port_List}


class Port_List(Resource):
    """BIG-IP® Port List resource"""
    def __init__(self, port_lists):
        super(Port_List, self).__init__(port_lists)
        self._meta_data['required_json_kind'] = \
            'tm:security:firewall:port-list:port-liststate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['minimum_additional_parameters'] = {'ports',
                                                            'portLists'}


class Rule_Lists(Collection):
    """BIG-IP® AFM® Rule List collection"""
    def __init__(self, firewall):
        super(Rule_Lists, self).__init__(firewall)
        self._meta_data['allowed_lazy_attributes'] = [Rule_List]
        self._meta_data['attribute_registry'] = \
            {'tm:security:firewall:rule-list:rule-liststate':
                Rule_List}


class Rule_List(Resource):
    """BIG-IP® Rule List resource"""
    def __init__(self, rule_lists):
        super(Rule_List, self).__init__(rule_lists)
        self._meta_data['required_json_kind'] = \
            'tm:security:firewall:rule-list:rule-liststate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['allowed_lazy_attributes'] = [Rules_s]
        self._meta_data['attribute_registry'] = \
            {'tm:security:firewall:rule-list:rules:rulescollectionstate':
                Rules_s}


class Rules_s(Collection):
    """BIG-IP® AFM® Rules sub-collection."""
    def __init__(self, rule_list):
        super(Rules_s, self).__init__(rule_list)
        self._meta_data['required_json_kind'] = \
            'tm:security:firewall:rule-list:rules:rulescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Rule]
        self._meta_data['attribute_registry'] = \
            {'tm:security:firewall:rule-list:rules:rulesstate':
                Rule}


class Rule(Resource, CheckExistenceMixin):
    """BIG-IP® AFM® Rule resource.


    NOTE:: The 'place-before' and 'place-after' attribute are
        mandatory but cannot be present with one another. Those attributes
        will not be visible when the class is created, they exist for the
        sole purpose of rule ordering in the BIGIP. The ordering of the
        rules corresponds to the index in the 'items' of the Rules_s
        sub-collection.
    """
    def __init__(self, rules_s):
        super(Rule, self).__init__(rules_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:firewall:rule-list:rules:rulesstate'
        self._meta_data['required_creation_parameters'].update(('action',))
        self._meta_data['exclusive_attributes'].append(
            ('place-after', 'place-before'))
        self._meta_data['minimum_additional_parameters'] = {'place-before',
                                                            'place-after'}
        self.tmos_ver = self._meta_data['bigip'].tmos_version

    def update(self, **kwargs):
        """We need to implement the custom exclusive parameter check."""
        self._check_exclusive_parameters(**kwargs)
        return super(Rule, self)._update(**kwargs)

    def modify(self, **kwargs):
        """We need to implement the custom exclusive parameter check."""
        self._check_exclusive_parameters(**kwargs)
        return super(Rule, self)._modify(**kwargs)

    def load(self, **kwargs):
        """Custom load method to address issue in 11.6.0 Final,

        where non existing objects would be True.
        """
        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._load_11_6(**kwargs)
        else:
            return super(Rule, self)._load(**kwargs)

    def _load_11_6(self, **kwargs):
        """Must check if rule actually exists before proceeding with load."""
        if self._check_existence_by_collection(self._meta_data['container'],
                                               kwargs['name']):
            return super(Rule, self)._load(**kwargs)
        msg = 'The application resource named, {}, does not exist on the ' \
              'device.'.format(kwargs['name'])
        raise NonExtantFirewallRule(msg)

    def exists(self, **kwargs):
        """Some objects when deleted still return when called by their

        direct URI, this is a known issue in 11.6.0.
        """

        if LooseVersion(self.tmos_ver) == LooseVersion('11.6.0'):
            return self._exists_11_6(**kwargs)
        else:
            return super(Rule, self)._load(**kwargs)

    def _exists_11_6(self, **kwargs):
        """Check rule existence on device."""

        return self._check_existence_by_collection(
            self._meta_data['container'], kwargs['name'])
