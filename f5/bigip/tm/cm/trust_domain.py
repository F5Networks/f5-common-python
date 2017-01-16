# coding=utf-8
#
#  Copyright 2016 F5 Networks Inc.
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

"""BIG-IP® cluster trust-domain submodule

REST URI
    ``http://localhost/mgmt/tm/cm/trust-domain``

GUI Path
    ``Device Management --> Device Trust``

REST Kind
    ``tm:cm:device-group:*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedOperation


class Trust_Domains(Collection):
    """BIG-IP® cluster trust-domain collection."""

    def __init__(self, cm):
        super(Trust_Domains, self).__init__(cm)
        self._meta_data['allowed_lazy_attributes'] = [Trust_Domain]
        self._meta_data['attribute_registry'] = \
            {'tm:cm:trust-domain:trust-domainstate': Trust_Domain}


class Trust_Domain(Resource):
    """BIG-IP® cluster trust-domain resource"""
    def __init__(self, trust_domains):
        super(Trust_Domain, self).__init__(trust_domains)
        self._meta_data['required_json_kind'] =\
            'tm:cm:trust-domain:trust-domainstate'
        self._meta_data['required_creation_parameters'].update(('partition',))

    def create(self, **kwargs):
        """Create is not supported for trust domains.

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedOperation`
        """
        raise UnsupportedOperation(
            "BIG-IP trust domains cannot be created by users")

    def delete(self):
        """Delete is not supported for trust domains.

        :raises: :exc:`~f5.BIG-IP.resource.UnsupportedOperation`
        """
        raise UnsupportedOperation(
            "BIG-IP trust domains cannot be deleted by users")
