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

"""BIG-IQ® license pool regkeys.

REST URI
    ``http://localhost/mgmt/cm/device/licensing/pool/regkey/licenses``

REST Kind
    ``cm:device:licensing:pool:regkey:licenses:*``
"""

from f5.bigiq.resource import Collection
from f5.bigiq.resource import Resource


class Licenses_s(Collection):
    def __init__(self, regkey):
        super(Licenses_s, self).__init__(regkey)
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:regkeypoollicensecollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [License]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:regkeypoollicensestate': License  # NOQA
        }


class License(Resource):
    def __init__(self, licenses_s):
        super(License, self).__init__(licenses_s)
        self._meta_data['required_creation_parameters'] = set(('name',))
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:regkeypoollicensestate'
        self._meta_data['allowed_lazy_attributes'] = [
            Offerings_s
        ]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingcollectionstate': Offerings_s  # NOQA
        }


class Offerings_s(Collection):
    def __init__(self, license):
        super(Offerings_s, self).__init__(license)
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingcollectionstate'  # NOQA
        self._meta_data['allowed_lazy_attributes'] = [Offering]
        self._meta_data['attribute_registry'] = {
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingstate': Offering  # NOQA
        }


class Offering(Resource):
    def __init__(self, offerings_s):
        super(Offering, self).__init__(offerings_s)
        self._meta_data['required_creation_parameters'] = set(('regKey',))
        self._meta_data['required_json_kind'] = \
            'cm:device:licensing:pool:regkey:licenses:item:offerings:regkeypoollicenseofferingstate'  # NOQA
