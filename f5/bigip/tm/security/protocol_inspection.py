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

"""BIG-IP® Advanced Firewall Manager™ (AFM®) module.

REST URI
    ``http://localhost/mgmt/tm/security/protocol-inspection``

GUI Path
    ``Security --> Protocol Security --> Inspection_Profiles
      Security --> Protocol Security --> Inspection_List
    ``

REST Kind
    ``tm:security:protocol-inspection*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedMethod


class Protocol_Inspection(OrganizingCollection):
    """BIG-IP® Protocol Inspection Organizing collection"""
    def __init__(self, security):
        super(Protocol_Inspection, self).__init__(security)
        self._meta_data['allowed_lazy_attributes'] = [
            Profiles,
            Compliances,
            Signatures,
        ]


class Profiles(Collection):
    """"BIG-IP® Protocol Inspection Profile collection"""
    def __init__(self, protocol_inspection):
        super(Profiles, self).__init__(protocol_inspection)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] = \
            {'tm:security:protocol-inspection:profile:profilestate':
                Profile}


class Profile(Resource):
    """BIG-IP® Protocol Inspection Profile resource"""
    def __init__(self, profiles):
        super(Profile, self).__init__(profiles)
        self._meta_data['required_json_kind'] = \
            'tm:security:protocol-inspection:profile:profilestate'
        self._meta_data['required_creation_parameters'].update(('partition',))


class Compliances(Collection):
    def __init__(self, protocol_inspection):
        super(Compliances, self).__init__(protocol_inspection)
        self._meta_data['allowed_lazy_attributes'] = [Compliance]
        self._meta_data['attribute_registry'] = \
            {'tm:security:protocol-inspection:compliance:compliancestate':
                Compliance}


class Compliance(Resource):
    """BIG-IP® Protocol Inspection Compliance resource"""
    def __init__(self, compliances):
        super(Compliance, self).__init__(compliances)
        self._meta_data['required_json_kind'] = \
            'tm:security:protocol-inspection:compliance:compliancestate'
        self._meta_data['required_load_parameters'] = set()

    def create(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support the create method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__
        )

    def modify(self, **kwargs):
        raise UnsupportedMethod(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Signatures(Collection):
    """BIG-IP® Protocol Inspection Signature collection"""
    def __init__(self, protocol_inspection):
        super(Signatures, self).__init__(protocol_inspection)
        self._meta_data['allowed_lazy_attributes'] = [Signature]
        self._meta_data['attribute_registry'] = \
            {'tm:security:protocol-inspection:signature:signaturestate':
                Signature}


class Signature(Resource):
    """BIG-IP® Protocol Inspection Signature resource"""
    def __init__(self, signatures):
        super(Signature, self).__init__(signatures)
        self._meta_data['required_json_kind'] = \
            'tm:security:protocol-inspection:signature:signaturestate'
        self._meta_data['required_creation_parameters'].update((
            'partition', 'sig', 'description'))
