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
"""BIG-IP® LTM profile submodule.

REST URI
    ``http://localhost/mgmt/tm/ltm/profile/``

GUI Path
    ``Local Traffic --> Profiles``

REST Kind
    ``tm:ltm:profile*``
"""


from f5.bigip.resource import Collection
from f5.bigip.resource import MissingUpdateParameter
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource
from f5.bigip.resource import UnsupportedOperation


class Profile(OrganizingCollection):
    def __init__(self, ltm):
        super(Profile, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            Analytics_s,
            Certificate_Authoritys,
            Classifications,
            Client_Ldaps,
            Client_Ssls,
            Dhcpv4s,
            Dhcpv6s,
            Diameters,
            Dns_s,
            Dns_Loggings,
            Fasthttps,
            Fastl4s,
            Fixs,
            Ftps,
            Gtps,
            Htmls,
            Https,
            Http_Compressions,
            Http2s,
            Icaps,
            Iiops,
            Ipothers,
            Mblbs,
            Mssqls,
            Ntlms,
            Ocsp_Stapling_Params_s,
            One_Connects,
            Pcps,
            Pptps,
            Qoes,
            Radius_s,
            Ramcaches,
            Request_Adapts,
            Request_Logs,
            Response_Adapts,
            Rewrites,
            Rtsps,
            Sctps,
            Server_Ldaps,
            Server_Ssls,
            Sips,
            Smtps,
            Smtps_s,
            Socks_s,
            Spdys,
            Statistics_s,
            Streams,
            Tcps,
            Tftps,
            Udps,
            Wa_Caches,
            Web_Accelerations,
            Web_Securitys,
            Xmls]


class Client_Ssls(Collection):
    """BIG-IP® Client SSL profile collection."""
    def __init__(self, profile):
        super(Client_Ssls, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Client_Ssl]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:client-ssl:client-sslstate': Client_Ssl}


class Client_Ssl(Resource):
    def __init__(self, client_ssls):
        super(Client_Ssl, self).__init__(client_ssls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:profile:client-ssl:client-sslstate'


class Analytics_s(Collection):
    """BIG-IP® Analytics profile collection.

    .. note::
         Profile and sub-collections
         require AVR provisioned.
    """
    def __init__(self, profile):
        super(Analytics_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Analytics]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:profile:analytics:analyticsstate': Analytics}


class Analytics(Resource):
    """BIG-IP® Analytics profile resource."""
    def __init__(self, Analytics_s):
        super(Analytics, self).__init__(Analytics_s)
        self._meta_data['allowed_lazy_attributes'] = [Alerts_s,
                                                      Traffic_Captures]
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:analytics:analyticsstate'
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:analytics:alerts:alertscollectionstate': Alerts_s,
             'tm:ltm:profile:analytics:traffic-capture:\
             traffic-capturecollectionstate':
                 Traffic_Captures}


class Alerts_s(Collection):
    """BIG-IP® Alerts sub-collection."""
    def __init__(self, Analytics):
        super(Alerts_s, self).__init__(Analytics)
        self._meta_data['allowed_lazy_attributes'] = [Alerts]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:analytics:alerts:alertsstate': Alerts}


class Traffic_Captures(Collection):
    """BIG-IP® Traffic Capture sub-collection."""
    def __init__(self, Analytics):
        super(Traffic_Captures, self).__init__(Analytics)
        self._meta_data['allowed_lazy_attributes'] = [Traffic_Capture]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:analytics:traffic-capture:\
            traffic-capturestate': Traffic_Capture}


class Alerts(Resource):
    """BIG-IP® Alerts resource."""
    def __init__(self, Alerts_s):
        super(Alerts, self).__init__(Alerts_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:analytics:alerts:alertsstate'


class Traffic_Capture(Resource):
    """BIG-IP® Traffic Capture resource."""
    def __init__(self, Traffic_Captures):
        super(Traffic_Capture, self).__init__(Traffic_Captures)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:analytics:traffic-capture:traffic-capturestate'


class Certificate_Authoritys(Collection):
    """BIG-IP® Certificate Authority profile collection."""
    def __init__(self, profile):
        super(Certificate_Authoritys, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Certificate_Authority]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:certificate-authority:\
            certificate-authoritystate': Certificate_Authority}


class Certificate_Authority(Resource):
    """BIG-IP® Certificate Authority resource."""
    def __init__(self, Certificate_Authoritys):
        super(Certificate_Authority, self).__init__(Certificate_Authoritys)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:certificate-authority:certificate-authoritystate'


class Classifications(Collection):
    """BIG-IP® Classification profile collection."""
    def __init__(self, profile):
        super(Classifications, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Classification]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:classification:\
            classificationstate': Classification}


class Classification(Resource):
    """BIG-IP® Classification resource."""
    def __init__(self, Classifications):
        super(Classification, self).__init__(Classifications)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:classification:classificationstate'

    def create(self, **kwargs):
        """Create is not supported for Classification

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Classification

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Client_Ldaps(Collection):
    """BIG-IP® Client Ldap profile collection."""
    def __init__(self, profile):
        super(Client_Ldaps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Client_Ldap]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:client-ldap:client-ldapstate': Client_Ldap}
        self._meta_data['minimum_version'] = '11.6.0'


class Client_Ldap(Resource):
    """BIG-IP® Client Ldap resource."""
    def __init__(self, Client_Ldaps):
        super(Client_Ldap, self).__init__(Client_Ldaps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:client-ldap:client-ldapstate'


class Dhcpv4s(Collection):
    """BIG-IP® Dhcpv4 profile collection."""
    def __init__(self, profile):
        super(Dhcpv4s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Dhcpv4]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:dhcpv4:dhcpv4state': Dhcpv4}
        self._meta_data['minimum_version'] = '11.6.0'


class Dhcpv4(Resource):
    """BIG-IP® Dhcpv4 resource."""
    def __init__(self, Dhcpv4s):
        super(Dhcpv4, self).__init__(Dhcpv4s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:dhcpv4:dhcpv4state'


class Dhcpv6s(Collection):
    """BIG-IP® Dhcpv6 profile collection."""
    def __init__(self, profile):
        super(Dhcpv6s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Dhcpv6]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:dhcpv6:dhcpv6state': Dhcpv6}
        self._meta_data['minimum_version'] = '11.6.0'


class Dhcpv6(Resource):
    """BIG-IP® Dhcpv6 resource."""
    def __init__(self, Dhcpv6s):
        super(Dhcpv6, self).__init__(Dhcpv6s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:dhcpv6:dhcpv6state'


class Diameters(Collection):
    """BIG-IP® Diameter profile collection."""
    def __init__(self, profile):
        super(Diameters, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Diameter]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:diameter:diameterstate': Diameter}


class Diameter(Resource):
    """BIG-IP® Diameter resource."""
    def __init__(self, Diameters):
        super(Diameter, self).__init__(Diameters)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:diameter:diameterstate'


class Dns_s(Collection):
    """BIG-IP® DNS profile collection."""
    def __init__(self, profile):
        super(Dns_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Dns]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:dns:dnsstate': Dns}


class Dns(Resource):
    """BIG-IP® DNS resource."""
    def __init__(self, Dns_s):
        super(Dns, self).__init__(Dns_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:dns:dnsstate'


class Dns_Loggings(Collection):
    """BIG-IP® DNS Logging profile collection."""
    def __init__(self, profile):
        super(Dns_Loggings, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Dns_Logging]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:dns-logging:dns-loggingstate': Dns_Logging}


class Dns_Logging(Resource):
    """BIG-IP® DNS Logging resource."""
    def __init__(self, Dns_Loggings):
        super(Dns_Logging, self).__init__(Dns_Loggings)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:dns-logging:dns-loggingstate'
        self._meta_data['required_creation_parameters'].update(
            ('logPublisher',))


class Fasthttps(Collection):
    """BIG-IP® Fasthttp profile collection."""
    def __init__(self, profile):
        super(Fasthttps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Fasthttp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:fasthttp:fasthttpstate': Fasthttp}


class Fasthttp(Resource):
    """BIG-IP® Fasthttp resource."""
    def __init__(self, Fasthttps):
        super(Fasthttp, self).__init__(Fasthttps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:fasthttp:fasthttpstate'


class Fastl4s(Collection):
    """BIG-IP® Fastl4 profile collection."""
    def __init__(self, profile):
        super(Fastl4s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Fastl4]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:fastl4:fastl4state': Fastl4}


class Fastl4(Resource):
    """BIG-IP® Fastl4 resource."""
    def __init__(self, Fastl4s):
        super(Fastl4, self).__init__(Fastl4s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:fastl4:fastl4state'


class Fixs(Collection):
    """BIG-IP® Fix profile collection."""
    def __init__(self, profile):
        super(Fixs, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Fix]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:fix:fixstate': Fix}


class Fix(Resource):
    """BIG-IP® Fix resource."""
    def __init__(self, Fixs):
        super(Fix, self).__init__(Fixs)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:fix:fixstate'


class Ftps(Collection):
    """BIG-IP® Ftp profile collection."""
    def __init__(self, profile):
        super(Ftps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Ftp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:ftp:ftpstate': Ftp}


class Ftp(Resource):
    """BIG-IP® Ftp resource."""
    def __init__(self, Ftps):
        super(Ftp, self).__init__(Ftps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:ftp:ftpstate'


class Gtps(Collection):
    """BIG-IP® Gtp profile collection."""
    def __init__(self, profile):
        super(Gtps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Gtp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:gtp:gtpstate': Gtp}
        self._meta_data['minimum_version'] = '11.6.0'


class Gtp(Resource):
    """BIG-IP® Gtp resource."""
    def __init__(self, Gtps):
        super(Gtp, self).__init__(Gtps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:gtp:gtpstate'


class Htmls(Collection):
    """BIG-IP® Html profile collection."""
    def __init__(self, profile):
        super(Htmls, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Html]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:html:htmlstate': Html}


class Html(Resource):
    """BIG-IP® Html resource."""
    def __init__(self, Htmls):
        super(Html, self).__init__(Htmls)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:html:htmlstate'


class Https(Collection):
    """BIG-IP® Http profile collection."""
    def __init__(self, profile):
        super(Https, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Http]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:http:httpstate': Http}


class Http(Resource):
    """BIG-IP® Http resource."""
    def __init__(self, Https):
        super(Http, self).__init__(Https)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:http:httpstate'


class Http_Compressions(Collection):
    """BIG-IP® Http_Compression profile collection."""
    def __init__(self, profile):
        super(Http_Compressions, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Http_Compression]
        temp = \
            {'tm:ltm:profile:http-compression:http-compressionstate':
                Http_Compression}
        self._meta_data['attribute_registry'] = temp


class Http_Compression(Resource):
    """BIG-IP® Http_Compression resource."""
    def __init__(self, Http_Compressions):
        super(Http_Compression, self).__init__(Http_Compressions)
        temp = \
            'tm:ltm:profile:http-compression:http-compressionstate'
        self._meta_data['required_json_kind'] = temp


class Http2s(Collection):
    """BIG-IP® Http2 profile collection."""
    def __init__(self, profile):
        super(Http2s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Http2]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:http2:http2state': Http2}
        self._meta_data['minimum_version'] = '11.6.0'


class Http2(Resource):
    """BIG-IP® Http2 resource."""
    def __init__(self, Http2s):
        super(Http2, self).__init__(Http2s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:http2:http2state'


class Icaps(Collection):
    """BIG-IP® Icap profile collection."""
    def __init__(self, profile):
        super(Icaps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Icap]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:icap:icapstate': Icap}


class Icap(Resource):
    """BIG-IP® Icap resource."""
    def __init__(self, Icaps):
        super(Icap, self).__init__(Icaps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:icap:icapstate'


class Iiops(Collection):
    """BIG-IP® Iiop profile collection."""
    def __init__(self, profile):
        super(Iiops, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Iiop]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:iiop:iiopstate': Iiop}
        self._meta_data['minimum_version'] = '12.0.0'


class Iiop(Resource):
    """BIG-IP® Iiop resource."""
    def __init__(self, Iiops):
        super(Iiop, self).__init__(Iiops)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:iiop:iiopstate'


class Ipothers(Collection):
    """BIG-IP® Ipother profile collection."""
    def __init__(self, profile):
        super(Ipothers, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Ipother]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:ipother:ipotherstate': Ipother}


class Ipother(Resource):
    """BIG-IP® Ipother resource."""
    def __init__(self, Ipothers):
        super(Ipother, self).__init__(Ipothers)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:ipother:ipotherstate'


class Mblbs(Collection):
    """BIG-IP® Mblb profile collection."""
    def __init__(self, profile):
        super(Mblbs, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Mblb]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:mblb:mblbstate': Mblb}


class Mblb(Resource):
    """BIG-IP® Mblb resource."""
    def __init__(self, Mblbs):
        super(Mblb, self).__init__(Mblbs)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:mblb:mblbstate'


class Mssqls(Collection):
    """BIG-IP® Mssql profile collection."""
    def __init__(self, profile):
        super(Mssqls, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Mssql]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:mssql:mssqlstate': Mssql}


class Mssql(Resource):
    """BIG-IP® Mssql resource."""
    def __init__(self, Mssqls):
        super(Mssql, self).__init__(Mssqls)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:mssql:mssqlstate'


class Ntlms(Collection):
    """BIG-IP® Ntlm profile collection."""
    def __init__(self, profile):
        super(Ntlms, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Ntlm]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:ntlm:ntlmstate': Ntlm}


class Ntlm(Resource):
    """BIG-IP® Ntlm resource."""
    def __init__(self, Ntlms):
        super(Ntlm, self).__init__(Ntlms)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:ntlm:ntlmstate'


class Ocsp_Stapling_Params_s(Collection):
    """BIG-IP® Ocsp_Stapling_Params profile collection."""
    def __init__(self, profile):
        super(Ocsp_Stapling_Params_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Ocsp_Stapling_Params]
        temp = \
            {'tm:ltm:profile:ocsp-stapling-params:ocsp-stapling-paramsstate':
                Ocsp_Stapling_Params}
        self._meta_data['attribute_registry'] = temp
        self._meta_data['minimum_version'] = '11.6.0'


class Ocsp_Stapling_Params(Resource):
    """BIG-IP® Ocsp_Stapling_Params resource."""

    def __init__(self, Ocsp_Stapling_Params_s):
        super(Ocsp_Stapling_Params, self).__init__(Ocsp_Stapling_Params_s)
        self._meta_data['exclusive_attributes'].append(
            ('proxyServerPool', 'dnsResolver'))
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:ocsp-stapling-params:ocsp-stapling-paramsstate'

    def create(self, **kwargs):
        """Create the resource on the BIG-IP®.

        Uses HTTP POST to the `collection` URI to create a resource associated
        with a new unique URI on the device.

        As proxyServerPool parameter will be required
        only if useProxyServer is set to 'enabled'
        we have to use conditional to capture this logic during create.

        """
        if kwargs['useProxyServer'] == 'enabled':
            tup_par = ('proxyServerPool', 'trustedCa', 'useProxyServer')
        else:
            tup_par = ('dnsResolver', 'trustedCa', 'useProxyServer')

        self._meta_data['required_creation_parameters'].update(tup_par)
        return self._create(**kwargs)

    def update(self, **kwargs):
        """When setting useProxyServer to enable we need to supply

            proxyServerPool value as well
        """
        if 'useProxyServer' in kwargs and \
                kwargs['useProxyServer'] == 'enabled':
            if 'proxyServerPool' not in kwargs:
                error = 'Missing proxyServerPool parameter value.'
                raise MissingUpdateParameter(error)
        if hasattr(self, 'useProxyServer'):
            if getattr(self, 'useProxyServer') == 'enabled' and \
                    not hasattr(self, 'proxyServerPool'):
                error = 'Missing proxyServerPool parameter value.'
                raise MissingUpdateParameter(error)

        self._update(**kwargs)

        return self


class One_Connects(Collection):
    """BIG-IP® One_Connect profile collection."""
    def __init__(self, profile):
        super(One_Connects, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [One_Connect]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:one-connect:one-connectstate': One_Connect}


class One_Connect(Resource):
    """BIG-IP® One_Connect resource."""
    def __init__(self, One_Connects):
        super(One_Connect, self).__init__(One_Connects)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:one-connect:one-connectstate'


class Pcps(Collection):
    """BIG-IP® Pcp profile collection."""
    def __init__(self, profile):
        super(Pcps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Pcp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:pcp:pcpstate': Pcp}


class Pcp(Resource):
    """BIG-IP® Pcp resource."""
    def __init__(self, Pcps):
        super(Pcp, self).__init__(Pcps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:pcp:pcpstate'


class Pptps(Collection):
    """BIG-IP® Pptp profile collection."""
    def __init__(self, profile):
        super(Pptps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Pptp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:pptp:pptpstate': Pptp}


class Pptp(Resource):
    """BIG-IP® Pptp resource."""
    def __init__(self, Pptps):
        super(Pptp, self).__init__(Pptps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:pptp:pptpstate'


class Qoes(Collection):
    """BIG-IP® Qoe profile collection."""
    def __init__(self, profile):
        super(Qoes, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Qoe]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:qoe:qoestate': Qoe}


class Qoe(Resource):
    """BIG-IP® Qoe resource."""
    def __init__(self, Qoes):
        super(Qoe, self).__init__(Qoes)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:qoe:qoestate'


class Radius_s(Collection):
    """BIG-IP® Radius profile collection."""
    def __init__(self, profile):
        super(Radius_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Radius]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:radius:radiusstate': Radius}


class Radius(Resource):
    """BIG-IP® Radius resource."""
    def __init__(self, Radius_s):
        super(Radius, self).__init__(Radius_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:radius:radiusstate'


class Ramcaches(Collection):
    """BIG-IP® Ramcache profile collection."""
    pass


class Ramcache(Resource):
    """BIG-IP® Ramcache resource."""
    pass


class Request_Adapts(Collection):
    """BIG-IP® Request_Adapt profile collection."""
    def __init__(self, profile):
        super(Request_Adapts, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Request_Adapt]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:request-adapt:request-adaptstate': Request_Adapt}


class Request_Adapt(Resource):
    """BIG-IP® Request_Adapt resource."""
    def __init__(self, Request_Adapts):
        super(Request_Adapt, self).__init__(Request_Adapts)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:request-adapt:request-adaptstate'


class Request_Logs(Collection):
    """BIG-IP® Request_Log profile collection."""
    def __init__(self, profile):
        super(Request_Logs, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Request_Log]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:request-log:request-logstate': Request_Log}


class Request_Log(Resource):
    """BIG-IP® Request_Log resource."""
    def __init__(self, Request_Logs):
        super(Request_Log, self).__init__(Request_Logs)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:request-log:request-logstate'


class Response_Adapts(Collection):
    """BIG-IP® Response_Adapt profile collection."""
    def __init__(self, profile):
        super(Response_Adapts, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Response_Adapt]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:response-adapt:\
            response-adaptstate': Response_Adapt}


class Response_Adapt(Resource):
    """BIG-IP® Response_Adapt resource."""
    def __init__(self, Response_Adapts):
        super(Response_Adapt, self).__init__(Response_Adapts)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:response-adapt:response-adaptstate'


class Rewrites(Collection):
    """BIG-IP® Rewrite profile collection."""
    def __init__(self, profile):
        super(Rewrites, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Rewrite]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:rewrite:rewritestate': Rewrite}


class Rewrite(Resource):
    """BIG-IP® Rewrite resource."""
    def __init__(self, Rewrites):
        super(Rewrite, self).__init__(Rewrites)
        self._meta_data['allowed_lazy_attributes'] = []
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:rewrite:rewritestate'
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:rewrite:uri-rules:uri-rulescollectionstate':
             Uri_Rules_s}


class Uri_Rules_s(Collection):
    """BIG-IP® Rewrite sub-collection."""
    def __init__(self, Rewrite):
        super(Uri_Rules_s, self).__init__(Rewrite)
        self._meta_data['allowed_lazy_attributes'] = [Uri_Rules]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:rewrite:uri-rules:uri-rulesstate': Uri_Rules}


class Uri_Rules(Resource):
    """BIG-IP® URI Rules resource"""
    def __init__(self, Uri_Rules_s):
        super(Uri_Rules, self).__init__(Uri_Rules_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:rewrite:uri-rules:uri-rulesstate'


class Rtsps(Collection):
    """BIG-IP® Rtsp profile collection."""
    def __init__(self, profile):
        super(Rtsps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Rtsp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:rtsp:rtspstate': Rtsp}


class Rtsp(Resource):
    """BIG-IP® Rtsp resource."""
    def __init__(self, Rtsps):
        super(Rtsp, self).__init__(Rtsps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:rtsp:rtspstate'


class Sctps(Collection):
    """BIG-IP® Sctp profile collection."""
    def __init__(self, profile):
        super(Sctps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Sctp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:sctp:sctpstate': Sctp}


class Sctp(Resource):
    """BIG-IP® Sctp resource."""
    def __init__(self, Sctps):
        super(Sctp, self).__init__(Sctps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:sctp:sctpstate'


class Server_Ldaps(Collection):
    """BIG-IP® Server_Ldap profile collection."""
    def __init__(self, profile):
        super(Server_Ldaps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Server_Ldap]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:server-ldap:server-ldapstate': Server_Ldap}
        self._meta_data['minimum_version'] = '11.6.0'


class Server_Ldap(Resource):
    """BIG-IP® Server_Ldap resource."""
    def __init__(self, Server_Ldaps):
        super(Server_Ldap, self).__init__(Server_Ldaps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:server-ldap:server-ldapstate'


class Server_Ssls(Collection):
    """BIG-IP® Server_Ssl profile collection."""
    def __init__(self, profile):
        super(Server_Ssls, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Server_Ssl]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:server-ssl:server-sslstate': Server_Ssl}


class Server_Ssl(Resource):
    """BIG-IP® Server_Ssl resource."""
    def __init__(self, Server_Ssls):
        super(Server_Ssl, self).__init__(Server_Ssls)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:server-ssl:server-sslstate'


class Sips(Collection):
    """BIG-IP® Sip profile collection."""
    def __init__(self, profile):
        super(Sips, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Sip]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:sip:sipstate': Sip}


class Sip(Resource):
    """BIG-IP® Sip resource."""
    def __init__(self, Sips):
        super(Sip, self).__init__(Sips)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:sip:sipstate'


class Smtps(Collection):
    """BIG-IP® Smtp profile collection.

    .. note::
         Profile requires ASM provisioned.
    """
    def __init__(self, profile):
        super(Smtps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Smtp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:smtp:smtpstate': Smtp}
        self._meta_data['minimum_version'] = '11.6.0'


class Smtp(Resource):
    """BIG-IP® Smtp resource."""
    def __init__(self, Smtps):
        super(Smtp, self).__init__(Smtps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:smtp:smtpstate'


class Smtps_s(Collection):
    """BIG-IP® Smtps profile collection."""
    def __init__(self, profile):
        super(Smtps_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [SmtpS]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:smtps:smtpsstate': SmtpS}


class SmtpS(Resource):
    """BIG-IP® Smtps resource."""
    def __init__(self, Smtps_s):
        super(SmtpS, self).__init__(Smtps_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:smtps:smtpsstate'


class Socks_s(Collection):
    """BIG-IP® Socks profile collection."""
    def __init__(self, profile):
        super(Socks_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Socks]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:socks:socksstate': Socks}


class Socks(Resource):
    """BIG-IP® Socks resource."""
    def __init__(self, Socks_s):
        super(Socks, self).__init__(Socks_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:socks:socksstate'
        self._meta_data['required_creation_parameters'].update(
            ('dnsResolver',))


class Spdys(Collection):
    """BIG-IP® Spdy profile collection."""
    def __init__(self, profile):
        super(Spdys, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Spdy]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:spdy:spdystate': Spdy}


class Spdy(Resource):
    """BIG-IP® Spdy resource."""
    def __init__(self, Spdys):
        super(Spdy, self).__init__(Spdys)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:spdy:spdystate'


class Statistics_s(Collection):
    """BIG-IP® Statistics profile collection."""
    def __init__(self, profile):
        super(Statistics_s, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Statistics]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:statistics:statisticsstate': Statistics}


class Statistics(Resource):
    """BIG-IP® Statistics resource."""
    def __init__(self, Statistics_s):
        super(Statistics, self).__init__(Statistics_s)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:statistics:statisticsstate'


class Streams(Collection):
    """BIG-IP® Stream profile collection."""
    def __init__(self, profile):
        super(Streams, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Stream]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:stream:streamstate': Stream}


class Stream(Resource):
    """BIG-IP® Stream resource."""
    def __init__(self, Streams):
        super(Stream, self).__init__(Streams)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:stream:streamstate'


class Tcps(Collection):
    """BIG-IP® Tcp profile collection."""
    def __init__(self, profile):
        super(Tcps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Tcp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:tcp:tcpstate': Tcp}


class Tcp(Resource):
    """BIG-IP® Tcp resource."""
    def __init__(self, Tcps):
        super(Tcp, self).__init__(Tcps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:tcp:tcpstate'


class Tftps(Collection):
    """BIG-IP® Tftp profile collection."""
    def __init__(self, profile):
        super(Tftps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Tftp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:tftp:tftpstate': Tftp}
        self._meta_data['minimum_version'] = '12.0.0'


class Tftp(Resource):
    """BIG-IP® Tftp resource."""
    def __init__(self, Tftps):
        super(Tftp, self).__init__(Tftps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:tftp:tftpstate'


class Udps(Collection):
    """BIG-IP® Udp profile collection."""
    def __init__(self, profile):
        super(Udps, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Udp]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:udp:udpstate': Udp}


class Udp(Resource):
    """BIG-IP® Udp resource."""
    def __init__(self, Udps):
        super(Udp, self).__init__(Udps)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:udp:udpstate'


class Wa_Caches(Collection):
    """BIG-IP® Wa_Cache profile collection."""
    pass


class Wa_Cache(Resource):
    """BIG-IP® Wa_Cache resource."""
    pass


class Web_Accelerations(Collection):
    """BIG-IP® Web_Acceleration profile collection."""
    def __init__(self, profile):
        super(Web_Accelerations, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Web_Acceleration]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:web-acceleration:\
            web-accelerationstate': Web_Acceleration}


class Web_Acceleration(Resource):
    """BIG-IP® Web_Acceleration resource."""
    def __init__(self, Web_Accelerations):
        super(Web_Acceleration, self).__init__(Web_Accelerations)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:web-acceleration:web-accelerationstate'


class Web_Securitys(Collection):
    """BIG-IP® Web_Security profile collection."""
    def __init__(self, profile):
        super(Web_Securitys, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Websecurity]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:websecurity:websecuritystate': Websecurity}


class Websecurity(Resource):
    """BIG-IP® Web_Security resource."""
    def __init__(self, Web_Securitys):
        super(Websecurity, self).__init__(Web_Securitys)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:web-security:web-securitystate'

    def create(self, **kwargs):
        """Create is not supported for Web Security

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the create method" % self.__class__.__name__
        )

    def update(self, **kwargs):
        """Update is not supported for Web Security

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the update method" % self.__class__.__name__
        )

    def refresh(self, **kwargs):
        """Refresh is not supported for Web Security

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the refresh method" % self.__class__.__name__
        )

    def delete(self, **kwargs):
        """Delete is not supported for Web Security

        :raises: UnsupportedOperation
        """
        raise UnsupportedOperation(
            "%s does not support the delete method" % self.__class__.__name__
        )


class Xmls(Collection):
    """BIG-IP® Xml profile collection."""
    def __init__(self, profile):
        super(Xmls, self).__init__(profile)
        self._meta_data['allowed_lazy_attributes'] = [Xml]
        self._meta_data['attribute_registry'] = \
            {'tm:ltm:profile:xml:xmlstate': Xml}


class Xml(Resource):
    """BIG-IP® Xml resource."""
    def __init__(self, Xmls):
        super(Xml, self).__init__(Xmls)
        self._meta_data['required_json_kind'] = \
            'tm:ltm:profile:xml:xmlstate'
