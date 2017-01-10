# coding=utf-8
#
# Copyright 2016 F5 Networks Inc.
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

"""BIG-IP Local Traffic Manager (LTM) SNAT Translation module.

REST URI
    ``https://localhost/mgmt/tm/ltm/snat-translation?ver=11.6.0``

GUI Path
    ``Local Traffic --> Address Translation --> Address Translation List``

REST Kind
    ``tm:ltm:snat-translation:*``
"""

from f5.bigip.mixins import ExclusiveAttributesMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import Resource


class Snat_Translations(Collection):
    """BIG-IP® SNAT Translation collection."""
    def __init__(self, ltm):
        super(Snat_Translations, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Snat_Translation]
        self._meta_data['attribute_registry'] = {
            'tm:ltm:snat-translation:snat-translationstate': Snat_Translation
        }


class Snat_Translation(ExclusiveAttributesMixin, Resource):
    """BIG-IP® SNAT Translation"""
    def __init__(self, Snat_Translations):
        super(Snat_Translation, self).__init__(Snat_Translations)
        self._meta_data['required_json_kind'] =\
            "tm:ltm:snat-translation:snat-translationstate"
        self._meta_data['read_only_attributes'].append('address')
        self._meta_data['exclusive_attributes'].append(('enabled', 'disabled'))
