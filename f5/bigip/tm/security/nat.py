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
    ``http://localhost/mgmt/tm/security/nat``

GUI Path
    ``Security --> Nat``

REST Kind
    ``tm:security:nat:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Nat(OrganizingCollection):
    """BIG-IP® AFM® Nat organizing collection."""

    def __init__(self, security):
        super(Nat, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Destination_Translations,
            Policys,
            Source_Translations]
        self._meta_data['minimum_version'] = '12.1.0'


class Destination_Translations(Collection):
    """BIG-IP® AFM® Nat Destination Translation collection"""
    def __init__(self, nat):
        super(Destination_Translations, self).__init__(nat)
        self._meta_data['allowed_lazy_attributes'] = \
            [Destination_Translation]
        self._meta_data['attribute_registry'] = \
            {'tm:security:nat:destination-translation:'
             'destination-translationstate': Destination_Translation}


class Destination_Translation(Resource):
    """BIG-IP® AFM® Nat Destination Translation resource"""
    def __init__(self, destination_translations):
        super(Destination_Translation, self).__init__(destination_translations)
        self._meta_data['required_json_kind'] = \
            'tm:security:nat:destination-translation:' \
            'destination-translationstate'
        self._meta_data['required_creation_parameters'].update(
            ('partition',), ('type',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['allowed_lazy_attributes'] = []


class Rules_s(Collection):
    """BIG-IP® AFM® Nat Policy Rules sub-collection."""
    def __init__(self, rule_list):
        super(Rules_s, self).__init__(rule_list)
        self._meta_data['required_json_kind'] = \
            'tm:security:nat:policy:rules:rulescollectionstate'
        self._meta_data['allowed_lazy_attributes'] = [Rules]
        self._meta_data['attribute_registry'] = \
            {'tm:security:nat:policy:rules:rulesstate': Rules}


class Rules(Resource):
    """BIG-IP® AFM® Nat Policy Rules resource.

    NOTE:: The 'place-before' and 'place-after' attribute are
        mandatory but cannot be present with one another. Those attributes
        will not be visible when the class is created, they exist for the
        sole purpose of rule ordering in the BIGIP. The ordering of the
        rules corresponds to the index in the 'items' of the Rules_s
        sub-collection.
    """
    def __init__(self, rules_s):
        super(Rules, self).__init__(rules_s)
        self._meta_data['required_json_kind'] = \
            'tm:security:nat:policy:rules:rulesstate'
        self._meta_data['exclusive_attributes'].append(
            ('place-after', 'place-before'))
        self._meta_data['minimum_additional_parameters'] = {'place-before',
                                                            'place-after'}

    def update(self, **kwargs):
        """We need to implement the custom exclusive parameter check."""
        self._check_exclusive_parameters(**kwargs)
        return super(Rules, self)._update(**kwargs)

    def modify(self, **kwargs):
        """We need to implement the custom exclusive parameter check."""
        self._check_exclusive_parameters(**kwargs)
        return super(Rules, self)._modify(**kwargs)


class Policys(Collection):
    """BIG-IP® AFM® Nat Policy collection"""
    def __init__(self, nat):
        super(Policys, self).__init__(nat)
        self._meta_data['allowed_lazy_attributes'] = [Policy]
        self._meta_data['attribute_registry'] = \
            {'tm:security:nat:policy:policystate': Policy}


class Policy(Resource):
    """BIG-IP® AFM® Nat Policy resource"""
    def __init__(self, policys):
        super(Policy, self).__init__(policys)
        self._meta_data['required_json_kind'] = \
            'tm:security:nat:policy:policystate'
        self._meta_data['required_creation_parameters'].update(('partition',))
        self._meta_data['required_load_parameters'].update(('partition',))
        self._meta_data['allowed_lazy_attributes'] = [Rules_s]
        self._meta_data['attribute_registry'] = \
            {'tm:security:nat:policy:rules:rulescollectionstate': Rules_s}


class Source_Translations(Collection):
    """BIG-IP® AFM® Nat Source Translation collection"""
    def __init__(self, nat):
        super(Source_Translations, self).__init__(nat)
        self._meta_data['allowed_lazy_attributes'] = [Source_Translation]
        self._meta_data['attribute_registry'] = \
            {'tm:security:nat:source-translation:source-translationstate':
                Source_Translation}


class Source_Translation(Resource):
    """BIG-IP® AFM® Nat Source Translation resource"""
    def __init__(self, source_translations):
        super(Source_Translation, self).__init__(source_translations)
        self._meta_data['required_json_kind'] = \
            'tm:security:nat:source-translation:source-translationstate'
        self._meta_data['required_creation_parameters'].update(('partition',),
                                                               ('type',))
        self._meta_data['required_load_parameters'].update(('partition',))
