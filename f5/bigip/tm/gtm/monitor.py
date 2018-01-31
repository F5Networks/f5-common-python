# coding=utf-8
#
#  Copyright 2018 F5 Networks Inc.
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

"""BIG-IP® GTM monitor submodule.

REST URI
    ``http://localhost/mgmt/tm/gtm/monitor/``

GUI Path
    ``DNS --> GSLB --> Monitors``

REST Kind
    ``tm:gtm:monitor*``
"""

from f5.bigip.mixins import UpdateMonitorMixin
from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Monitor(OrganizingCollection):
    def __init__(self, gtm):
        super(Monitor, self).__init__(gtm)
        self._meta_data['allowed_lazy_attributes'] = [
            Bigips,
            Bigip_Links,
            Externals,
            Firepass_s,
            Ftps,
            Gateway_Icmps,
            Gtps,
            Https,
            Https_s,
            Imaps,
            Ldaps,
            Mssqls,
            Mysqls,
            Nntps,
            Oracles,
            Pop3s,
            Postgresqls,
            Radius_s,
            Radius_Accountings,
            Real_Servers,
            Scripteds,
            Sips,
            Smtps,
            Snmps,
            Snmp_Links,
            Soaps,
            Tcps,
            Tcp_Half_Opens,
            Udps,
            Waps,
            Wmis
        ]


class Bigips(Collection):
    def __init__(self, monitor):
        super(Bigips, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Bigip]
        self._meta_data['attribute_registry'] = {
            'tm:gtm:monitor:bigip:bigipstate': Bigip
        }


class Bigip(UpdateMonitorMixin, Resource):
    def __init__(self, bigips):
        super(Bigip, self).__init__(bigips)
        self._meta_data['required_json_kind'] = 'tm:gtm:monitor:bigip:bigipstate'


class Bigip_Links(Collection):
    def __init__(self, monitor):
        super(Bigip_Links, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Bigip_Link]
        self._meta_data['attribute_registry'] = {
            'tm:gtm:monitor:bigip-link:bigip-linkstate': Bigip_Link
        }


class Bigip_Link(UpdateMonitorMixin, Resource):
    def __init__(self, bigip_links):
        super(Bigip_Link, self).__init__(bigip_links)
        self._meta_data['required_json_kind'] = 'tm:gtm:monitor:bigip-link:bigip-linkstate'


class Externals(Collection):
    def __init__(self, monitor):
        super(Externals, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [External]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:external:externalstate': External}


class External(UpdateMonitorMixin, Resource):
    def __init__(self, externals):
        super(External, self).__init__(externals)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:external:externalstate'


class Firepass_s(Collection):
    def __init__(self, monitor):
        super(Firepass_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Firepass]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:firepass:firepassstate': Firepass}


class Firepass(UpdateMonitorMixin, Resource):
    def __init__(self, firepass_s):
        super(Firepass, self).__init__(firepass_s)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:firepass:firepassstate'


class Ftps(Collection):
    def __init__(self, monitor):
        super(Ftps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Ftp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:ftp:ftpstate': Ftp}


class Ftp(UpdateMonitorMixin, Resource):
    def __init__(self, ftps):
        super(Ftp, self).__init__(ftps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:ftp:ftpstate'


class Gateway_Icmps(Collection):
    def __init__(self, monitor):
        super(Gateway_Icmps, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Gateway_Icmp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:gateway-icmp:gateway-icmpstate': Gateway_Icmp}


class Gateway_Icmp(UpdateMonitorMixin, Resource):
    def __init__(self, gateway_icmps):
        super(Gateway_Icmp, self).__init__(gateway_icmps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:gateway-icmp:gateway-icmpstate'


class Gtps(Collection):
    def __init__(self, monitor):
        super(Gtps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Gtp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:gtp:gtpstate': Gtp}


class Gtp(UpdateMonitorMixin, Resource):
    def __init__(self, gtps):
        super(Gtp, self).__init__(gtps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:gtp:gtpstate'


class Https(Collection):
    def __init__(self, monitor):
        super(Https, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Http]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:http:httpstate': Http}


class Http(UpdateMonitorMixin, Resource):
    def __init__(self, https):
        super(Http, self).__init__(https)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:http:httpstate'


class Https_s(Collection):
    """BIG-IP® Https monitor collection."""
    def __init__(self, monitor):
        super(Https_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HttpS]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:https:httpsstate': HttpS}


class HttpS(UpdateMonitorMixin, Resource):
    """BIG-IP® Https monitor resource."""
    def __init__(self, https_s):
        super(HttpS, self).__init__(https_s)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:https:httpsstate'


class Imaps(Collection):
    """BIG-IP® Imap monitor collection."""
    def __init__(self, monitor):
        super(Imaps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Imap]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:imap:imapstate': Imap}


class Imap(UpdateMonitorMixin, Resource):
    """BIG-IP® Imap monitor resource."""
    def __init__(self, imaps):
        super(Imap, self).__init__(imaps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:imap:imapstate'


class Ldaps(Collection):
    """BIG-IP® Ldap monitor collection."""
    def __init__(self, monitor):
        super(Ldaps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Ldap]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:ldap:ldapstate': Ldap}


class Ldap(UpdateMonitorMixin, Resource):
    """BIG-IP® Ldap monitor resource."""
    def __init__(self, ldaps):
        super(Ldap, self).__init__(ldaps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:ldap:ldapstate'


class Mssqls(Collection):
    """BIG-IP® Mssql monitor collection."""
    def __init__(self, monitor):
        super(Mssqls, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Mssql]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:mssql:mssqlstate': Mssql}


class Mssql(UpdateMonitorMixin, Resource):
    """BIG-IP® Mssql monitor resource."""
    def __init__(self, mssqls):
        super(Mssql, self).__init__(mssqls)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:mssql:mssqlstate'


class Mysqls(Collection):
    """BIG-IP® MySQL monitor collection."""
    def __init__(self, monitor):
        super(Mysqls, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Mysql]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:mysql:mysqlstate': Mysql}


class Mysql(UpdateMonitorMixin, Resource):
    """BIG-IP® MySQL monitor resource."""
    def __init__(self, mysqls):
        super(Mysql, self).__init__(mysqls)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:mysql:mysqlstate'


class Nntps(Collection):
    """BIG-IP® Nntps monitor collection."""
    def __init__(self, monitor):
        super(Nntps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Nntp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:nntp:nntpstate': Nntp}


class Nntp(UpdateMonitorMixin, Resource):
    """BIG-IP® Nntps monitor resource."""
    def __init__(self, nntps):
        super(Nntp, self).__init__(nntps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:nntp:nntpstate'


class Nones(Collection):
    """BIG-IP® None monitor collection."""
    def __init__(self, monitor):
        super(Nones, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NONE]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:none:nonestate': NONE}


class NONE(UpdateMonitorMixin, Resource):
    """BIG-IP® None monitor resource."""
    def __init__(self, nones):
        super(NONE, self).__init__(nones)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:none:nonestate'


class Oracles(Collection):
    """BIG-IP® Oracle monitor collection."""
    def __init__(self, monitor):
        super(Oracles, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Oracle]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:oracle:oraclestate': Oracle}


class Oracle(UpdateMonitorMixin, Resource):
    """BIG-IP® Oracle monitor resource."""
    def __init__(self, oracles):
        super(Oracle, self).__init__(oracles)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:oracle:oraclestate'


class Pop3s(Collection):
    """BIG-IP® Pop3 monitor collection."""
    def __init__(self, monitor):
        super(Pop3s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Pop3]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:pop3:pop3state': Pop3}


class Pop3(UpdateMonitorMixin, Resource):
    """BIG-IP® Pop3 monitor resource."""
    def __init__(self, pop3s):
        super(Pop3, self).__init__(pop3s)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:pop3:pop3state'


class Postgresqls(Collection):
    """BIG-IP® PostGRES SQL monitor collection."""
    def __init__(self, monitor):
        super(Postgresqls, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Postgresql]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:postgresql:postgresqlstate': Postgresql}


class Postgresql(UpdateMonitorMixin, Resource):
    """BIG-IP® PostGRES SQL monitor resource."""
    def __init__(self, postgresqls):
        super(Postgresql, self).__init__(postgresqls)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:postgresql:postgresqlstate'


class Radius_s(Collection):
    """BIG-IP® radius monitor collection."""
    def __init__(self, monitor):
        super(Radius_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Radius]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:radius:radiusstate': Radius}


class Radius(UpdateMonitorMixin, Resource):
    """BIG-IP® radius monitor resource."""
    def __init__(self, radius_s):
        super(Radius, self).__init__(radius_s)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:radius:radiusstate'


class Radius_Accountings(Collection):
    """BIG-IP® radius accounting monitor collection."""
    def __init__(self, monitor):
        super(Radius_Accountings, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Radius_Accounting]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:radius-accounting:radius-accountingstate':
             Radius_Accounting}


class Radius_Accounting(UpdateMonitorMixin, Resource):
    """BIG-IP® radius accounting monitor resource."""
    def __init__(self, radius_accountings):
        super(Radius_Accounting, self).__init__(radius_accountings)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:radius-accounting:radius-accountingstate'


class Real_Servers(Collection):
    """BIG-IP® real-server monitor collection."""
    def __init__(self, monitor):
        super(Real_Servers, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Real_Server]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:real-server:real-serverstate': Real_Server}


class Real_Server(UpdateMonitorMixin, Resource):
    """BIG-IP® real-server monitor resource."""
    def __init__(self, real_servers):
        super(Real_Server, self).__init__(real_servers)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:real-server:real-serverstate'

    def update(self, **kwargs):
        """Change the configuration of the resource on the device.

        This method uses Http PUT alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * ``tmCommand`` attribute removed prior to PUT
        * ``agent`` attribute removed prior to PUT
        * ``post`` attribute removed prior to PUT


        :param kwargs: keys and associated values to alter on the device

        """
        self.__dict__.pop('tmCommand', '')
        self.__dict__.pop('agent', '')
        self.__dict__.pop('method', '')
        super(Real_Server, self).update(**kwargs)


class Scripteds(Collection):
    """BIG-IP® scripted monitor collection."""
    def __init__(self, monitor):
        super(Scripteds, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Scripted]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:scripted:scriptedstate': Scripted}


class Scripted(UpdateMonitorMixin, Resource):
    """BIG-IP® scripted monitor resource."""
    def __init__(self, scripteds):
        super(Scripted, self).__init__(scripteds)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:scripted:scriptedstate'


class Sips(Collection):
    """BIG-IP® Sip monitor collection."""
    def __init__(self, monitor):
        super(Sips, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Sip]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:sip:sipstate': Sip}


class Sip(UpdateMonitorMixin, Resource):
    """BIG-IP® Sip monitor resource."""
    def __init__(self, sips):
        super(Sip, self).__init__(sips)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:sip:sipstate'


class Smtps(Collection):
    """BIG-IP® Smtp monitor collection."""
    def __init__(self, monitor):
        super(Smtps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Smtp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:smtp:smtpstate': Smtp}


class Smtp(UpdateMonitorMixin, Resource):
    """BIG-IP® Smtp monitor resource."""
    def __init__(self, smtps):
        super(Smtp, self).__init__(smtps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:smtp:smtpstate'


class Snmps(Collection):
    """BIG-IP® Smtp monitor collection."""
    def __init__(self, monitor):
        super(Snmps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Snmp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:snmp:snmpstate': Snmp}


class Snmp(UpdateMonitorMixin, Resource):
    """BIG-IP® Smtp monitor resource."""
    def __init__(self, snmps):
        super(Snmp, self).__init__(snmps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:snmp:snmpstate'


class Snmp_Links(Collection):
    def __init__(self, monitor):
        super(Snmp_Links, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Snmp_Link]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:snmp-link:snmp-linkstate': Snmp_Link}


class Snmp_Link(UpdateMonitorMixin, Resource):
    def __init__(self, snmp_links):
        super(Snmp_Link, self).__init__(snmp_links)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:snmp-link:snmp-linkstate'


class Soaps(Collection):
    def __init__(self, monitor):
        super(Soaps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Soap]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:soap:soapstate': Soap}


class Soap(UpdateMonitorMixin, Resource):
    def __init__(self, soaps):
        super(Soap, self).__init__(soaps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:soap:soapstate'


class Tcps(Collection):
    def __init__(self, monitor):
        super(Tcps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Tcp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:tcp:tcpstate': Tcp}


class Tcp(UpdateMonitorMixin, Resource):
    def __init__(self, tcps):
        super(Tcp, self).__init__(tcps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:tcp:tcpstate'


class Tcp_Half_Opens(Collection):
    def __init__(self, monitor):
        super(Tcp_Half_Opens, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Tcp_Half_Open]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:tcp-half-open:tcp-half-openstate': Tcp_Half_Open}


class Tcp_Half_Open(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_half_opens):
        super(Tcp_Half_Open, self).__init__(tcp_half_opens)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:tcp-half-open:tcp-half-openstate'


class Udps(Collection):
    def __init__(self, monitor):
        super(Udps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Udp]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:udp:udpstate': Udp}


class Udp(UpdateMonitorMixin, Resource):
    def __init__(self, udps):
        super(Udp, self).__init__(udps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:udp:udpstate'


class Waps(Collection):
    def __init__(self, monitor):
        super(Waps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Wap]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:wap:wapstate': Wap}


class Wap(UpdateMonitorMixin, Resource):
    def __init__(self, waps):
        super(Wap, self).__init__(waps)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:wap:wapstate'


class Wmis(Collection):
    def __init__(self, monitor):
        super(Wmis, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Wmi]
        self._meta_data['attribute_registry'] =\
            {'tm:gtm:monitor:wmi:wmistate': Wmi}


class Wmi(UpdateMonitorMixin, Resource):
    def __init__(self, wmis):
        super(Wmi, self).__init__(wmis)
        self._meta_data['required_json_kind'] =\
            'tm:gtm:monitor:wmi:wmistate'
        self._meta_data['read_only_attributes'] =\
            ['agent', 'post', 'method']

    def update(self, **kwargs):
        """Change the configuration of the resource on the device.

        This method uses Http PUT alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * ``agent`` attribute removed prior to PUT
        * ``post`` attribute removed prior to PUT
        * ``method`` attribute removed prior to PUT

        :param kwargs: keys and associated values to alter on the device

        """
        self.__dict__.pop('agent', '')
        self.__dict__.pop('post', '')
        self.__dict__.pop('method', '')
        super(Wmi, self).update(**kwargs)
