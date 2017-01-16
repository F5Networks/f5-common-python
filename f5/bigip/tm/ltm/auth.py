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
"""BIG-IP® LTM auth submodule.

REST URI
    ``http://localhost/mgmt/tm/ltm/auth/``

GUI Path
    ``Local Traffic --> Profiles --> Authentication``

REST Kind
    ``tm:ltm:auth:*``
"""
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.sdk_exception import UnsupportedMethod


class Auth(OrganizingCollection):
    """BIG-IP® LTM Authentication organizing collection."""
    def __init__(self, ltm):
        super(Auth, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Crldp_Servers,
            Kerberos_Delegations,
            Ldaps,
            Ocsp_Responders,
            Profiles,
            Radius_s,
            Radius_Servers,
            Ssl_Cc_Ldaps,
            Ssl_Crldps,
            Ssl_Ocsps,
            Tacacs_s
        ]


class Crldp_Servers(Collection):
    """BIG-IP® LTM Auth Crldp Server collection"""
    def __init__(self, ltm):
        super(Crldp_Servers, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Crldp_Server]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:crldp-server:crldp-serverstate': Crldp_Server}


class Crldp_Server(Resource):
    def __init__(self, crldp_servers):
        """BIG-IP® LTM Auth Crldp Server resource"""
        super(Crldp_Server, self).__init__(crldp_servers)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:crldp-server:crldp-serverstate'
        self._meta_data['required_creation_parameters'].update(('host',))


class Kerberos_Delegations(Collection):
    """BIG-IP® LTM Auth Kerberos Delegation collection"""
    def __init__(self, ltm):
        super(Kerberos_Delegations, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Kerberos_Delegation]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:kerberos-delegation:kerberos-delegationstate':
                Kerberos_Delegation}


class Kerberos_Delegation(Resource):
    """BIG-IP® LTM Auth Kerberos Delegation resource"""
    def __init__(self, kerberos_delegations):
        super(Kerberos_Delegation, self).__init__(kerberos_delegations)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:kerberos-delegation:kerberos-delegationstate'
        self._meta_data['required_creation_parameters'].update(
            ('serverPrincipal', 'clientPrincipal',))


class Ldaps(Collection):
    """BIG-IP® LTM Auth Ldap collection"""
    def __init__(self, ltm):
        super(Ldaps, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Ldap]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:ldap:ldapstate': Ldap}


class Ldap(Resource):
    """BIG-IP® LTM Auth Ldap resource"""
    def __init__(self, ldaps):
        super(Ldap, self).__init__(ldaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:ldap:ldapstate'
        self._meta_data['required_creation_parameters'].update(('servers',))


class Ocsp_Responders(Collection):
    """BIG-IP® LTM Auth Ocsp Responder collection"""
    def __init__(self, ltm):
        super(Ocsp_Responders, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Ocsp_Responder]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:ocsp-responder:ocsp-responderstate': Ocsp_Responder}


class Ocsp_Responder(Resource):
    """BIG-IP® LTM Auth Ocsp Responder resource"""
    def __init__(self, ocsp_responders):
        super(Ocsp_Responder, self).__init__(ocsp_responders)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:ocsp-responder:ocsp-responderstate'


class Profiles(Collection):
    """BIG-IP® LTM Auth Profile collection"""
    def __init__(self, ltm):
        super(Profiles, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Profile]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:profile:profilestate': Profile}


class Profile(Resource):
    """BIG-IP® LTM Auth Profile resource"""
    def __init__(self, profiles):
        super(Profile, self).__init__(profiles)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:profile:profilestate'
        self._meta_data['required_creation_parameters'].update(
            ('defaultsFrom', 'configuration',))

    def update(self, **kwargs):
        '''Update is not supported for LTM Auth Profiles

        :raises: UnsupportedOperation
        '''
        raise UnsupportedMethod(
            "%s does not support the modify method" % self.__class__.__name__
        )


class Radius_s(Collection):
    """BIG-IP® LTM Auth Radius collection"""
    def __init__(self, ltm):
        super(Radius_s, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Radius]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:radius:radiusstate': Radius}


class Radius(Resource):
    """BIG-IP® LTM Auth Radius resource"""
    def __init__(self, radius_s):
        super(Radius, self).__init__(radius_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:radius:radiusstate'


class Radius_Servers(Collection):
    """BIG-IP® LTM Auth Radius Server collection"""
    def __init__(self, ltm):
        super(Radius_Servers, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Radius_Server]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:radius-server:radius-serverstate': Radius_Server}


class Radius_Server(Resource):
    """BIG-IP® LTM Auth Radius Server resource"""
    def __init__(self, radius_server_s):
        super(Radius_Server, self).__init__(radius_server_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:radius-server:radius-serverstate'
        self._meta_data['required_creation_parameters'].update(
            ('secret', 'server',))


class Ssl_Cc_Ldaps(Collection):
    """BIG-IP® LTM Auth SSL CC LDAP collection"""
    def __init__(self, ltm):
        super(Ssl_Cc_Ldaps, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Cc_Ldap]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:ssl-cc-ldap:ssl-cc-ldapstate': Ssl_Cc_Ldap}


class Ssl_Cc_Ldap(Resource):
    """BIG-IP® LTM Auth SSL CC LDAP resource"""
    def __init__(self, ssl_cc_ldaps):
        super(Ssl_Cc_Ldap, self).__init__(ssl_cc_ldaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:ssl-cc-ldap:ssl-cc-ldapstate'
        self._meta_data['required_creation_parameters'].update(
            ('servers', 'userKey',))


class Ssl_Crldps(Collection):
    """BIG-IP® LTM Auth SSL CLRDP collection"""
    def __init__(self, ltm):
        super(Ssl_Crldps, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Crldp]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:ssl-crldp:ssl-crldpstate': Ssl_Crldp}


class Ssl_Crldp(Resource):
    """BIG-IP® LTM Auth SSL CLRDP resource"""
    def __init__(self, ssl_crldps):
        super(Ssl_Crldp, self).__init__(ssl_crldps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:ssl-crldp:ssl-crldpstate'


class Ssl_Ocsps(Collection):
    """BIG-IP® LTM Auth SSL OCSP collection"""
    def __init__(self, ltm):
        super(Ssl_Ocsps, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Ssl_Ocsp]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:ssl-ocsp:ssl-ocspstate': Ssl_Ocsp}


class Ssl_Ocsp(Resource):
    """BIG-IP® LTM Auth SSL OCSP resource"""
    def __init__(self, ssl_ocsps):
        super(Ssl_Ocsp, self).__init__(ssl_ocsps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:ssl-ocsp:ssl-ocspstate'


class Tacacs_s(Collection):
    """BIG-IP® LTM Auth TACACS+ Server collection"""
    def __init__(self, ltm):
        super(Tacacs_s, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [Tacacs]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:auth:tacacs:tacacsstate': Tacacs}


class Tacacs(Resource):
    """BIG-IP® LTM Auth TACACS+ Server resource"""
    def __init__(self, tacacs_s):
        super(Tacacs, self).__init__(tacacs_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:auth:tacacs:tacacsstate'
        self._meta_data['required_creation_parameters'].update(
            ('secret', 'servers', 'service'))
