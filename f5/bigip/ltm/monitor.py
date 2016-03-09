# Copyright 2014-2016 F5 Networks Inc.
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

"""BigIP LTM monitor submodule.

REST URI
    ``http://localhost/mgmt/tm/ltm/monitors/``

GUI Path
    ``Local Traffic --> Monitors``

REST Kind
    ``tm:ltm:monitors*``
"""

from f5.bigip.resource import Collection
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import Resource


class Monitor(OrganizingCollection):
    def __init__(self, ltm):
        super(Monitor, self).__init__(ltm)
        self._meta_data['allowed_lazy_attributes'] = [
            HTTPs,
            HTTPS_s,
            Diameters,
            DNS_s,
            Externals,
            FirePass_s,
            FTPs,
            GateWay_ICMPs,
            ICMPs,
            IMAPs,
            InBands,
            LDAPs,
            Module_Scores,
            MSSQLs,
            MYSQLs,
            NNTPs,
            NONEs,
            Oracles,
            POP3s,
            PostGRESQLs,
            Radius_s,
            Radius_Accountings,
            Real_Servers,
            RPCs,
            SASPs,
            Scripteds,
            SIPs,
            SMBs,
            SMTPs,
            SNMP_DCAs,
            SNMP_DCA_Bases,
            SOAPs,
            TCPs,
            TCP_Echos,
            TCP_Half_Opens,
            UDPs,
            Virtual_Locations,
            WAPs,
            WMIs]


class Https(Collection):
    """BigIP HTTP monitor collection."""
    def __init__(self, monitor):
        super(Https, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HTTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:http:httpstate': HTTP}


class UpdateMonitorMixin(object):
    def update(self, **kwargs):
        """Change the configuration of the resource on the device.

        This method uses HTTP PUT alter the service state on the device.

        The attributes of the instance will be packaged as a dictionary.  That
        dictionary will be updated with kwargs.  It is then submitted as JSON
        to the device.  Various edge cases are handled:

        * read-only attributes that are unchangeable are removed
        * ``defaultsFrom`` attribute is removed from JSON before the PUT

        :param kwargs: keys and associated values to alter on the device

        """
        self.__dict__.pop(u'defaultsFrom', '')
        self._update(**kwargs)


class Http(UpdateMonitorMixin, Resource):
    """BigIP Http monitor resource."""
    def __init__(self, https):
        super(Http, self).__init__(https)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:http:httpstate'


class Https_s(Collection):
    """BigIP Https monitor collection."""
    def __init__(self, monitor):
        super(Https_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Https]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:https:httpsstate': Https}


class Https(UpdateMonitorMixin, Resource):
    """BigIP Https monitor resource."""
    def __init__(self, https_s):
        super(Https, self).__init__(https_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:https:httpsstate'


class Diameters(Collection):
    """BigIP diameter monitor collection."""
    def __init__(self, monitor):
        super(Diameters, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Diameter]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:diameter:diameterstate': Diameter}


class Diameter(UpdateMonitorMixin, Resource):
    """BigIP diameter monitor resource."""
    def __init__(self, diameters):
        super(Diameter, self).__init__(diameters)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:diameter:diameterstate'


class Dns_s(Collection):
    """BigIP DNS monitor collection."""
    def __init__(self, monitor):
        super(Dns_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [DNS]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:dns:dnsstate': DNS}


class Dns(UpdateMonitorMixin, Resource):
    """BigIP Dns monitor resource."""
    def __init__(self, dns_s):
        super(Dns, self).__init__(dns_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:dns:dnsstate'
        self._meta_data['required_creation_parameters'].update(('qname',))


class Externals(Collection):
    """BigIP external monitor collection."""
    def __init__(self, monitor):
        super(Externals, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [External]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:external:externalstate': External}


class External(UpdateMonitorMixin, Resource):
    """BigIP external monitor resrouce."""
    def __init__(self, externals):
        super(External, self).__init__(externals)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:external:externalstate'


class Firepass_s(Collection):
    """BigIP Fire Pass monitor collection."""
    def __init__(self, monitor):
        super(Firepass_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FirePass]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:firepass:firepassstate': FirePass}


class Firepass(UpdateMonitorMixin, Resource):
    """BigIP external monitor resource."""
    def __init__(self, firepass_s):
        super(Firepass, self).__init__(firepass_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:firepass:firepassstate'


class Ftps(Collection):
    """BigIP FTP monitor collection."""
    def __init__(self, monitor):
        super(Ftps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:ftp:ftpstate': FTP}


class Ftp(UpdateMonitorMixin, Resource):
    """BigIP Ftp monitor resource."""
    def __init__(self, ftps):
        super(Ftp, self).__init__(ftps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ftp:ftpstate'


class Gateway_Icmps(Collection):
    """BigIP Gateway ICMP monitor collection."""
    def __init__(self, monitor):
        super(Gateway_Icmps, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [GateWay_ICMP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:gateway-icmp:gateway-icmpstate': GateWay_ICMP}


class Gateway_Icmp(UpdateMonitorMixin, Resource):
    """BigIP Gateway ICMP monitor resource."""
    def __init__(self, gateway_icmps):
        super(Gateway_Icmp, self).__init__(gateway_icmps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:gateway-icmp:gateway-icmpstate'


class Icmps(Collection):
    """BigIP ICMP monitor collection."""
    def __init__(self, monitor):
        super(Icmps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [ICMP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:icmp:icmpstate': ICMP}


class Icmp(UpdateMonitorMixin, Resource):
    """BigIP Icmp monitor resource."""
    def __init__(self, icmps):
        super(Icmp, self).__init__(icmps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:icmp:icmpstate'


class Imaps(Collection):
    """BigIP IMAP monitor collection."""
    def __init__(self, monitor):
        super(Imaps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [IMAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:imap:imapstate': IMAP}


class Imap(UpdateMonitorMixin, Resource):
    """BigIP Imap monitor resource."""
    def __init__(self, imaps):
        super(Imap, self).__init__(imaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:imap:imapstate'


class Inbands(Collection):
    """BigIP in band monitor collection."""
    def __init__(self, monitor):
        super(Inbands, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [InBand]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:inband:inbandstate': InBand}


class Inband(UpdateMonitorMixin, Resource):
    """BigIP in band monitor resource."""
    def __init__(self, inbands):
        super(Inband, self).__init__(inbands)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:inband:inbandstate'


class Ldaps(Collection):
    """BigIP LDAP monitor collection."""
    def __init__(self, monitor):
        super(Ldaps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [LDAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:ldap:ldapstate': LDAP}


class Ldap(UpdateMonitorMixin, Resource):
    """BigIP Ldap monitor resource."""
    def __init__(self, ldaps):
        super(Ldap, self).__init__(ldaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ldap:ldapstate'


class Module_Scores(Collection):
    """BigIP module scores monitor collection."""
    def __init__(self, monitor):
        super(Module_Scores, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Module_Score]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:module-score:module-scorestate': Module_Score}


class Module_Score(UpdateMonitorMixin, Resource):
    """BigIP module scores monitor resource."""
    def __init__(self, gateway_icmps):
        super(Module_Score, self).__init__(gateway_icmps)
        self._meta_data['required_creation_parameters'].update(
            ('snmp-ip-address',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:module-score:module-scorestate'


class Mysqls(Collection):
    """BigIP MySQL monitor collection."""
    def __init__(self, monitor):
        super(Mysqls, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MYSQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:mysql:mysqlstate': MYSQL}


class Mysql(UpdateMonitorMixin, Resource):
    """BigIP MySQL monitor resource."""
    def __init__(self, mysqls):
        super(Mysql, self).__init__(mysqls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mysql:mysqlstate'


class Mssqls(Collection):
    """BigIP MSSQL monitor collection."""
    def __init__(self, monitor):
        super(Mssqls, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MSSQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:mssql:mssqlstate': MSSQL}


class Mssql(UpdateMonitorMixin, Resource):
    """BigIP Mssql monitor resource."""
    def __init__(self, mssqls):
        super(Mssql, self).__init__(mssqls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mssql:mssqlstate'


class Nntps(Collection):
    """BigIP Nntps monitor collection."""
    def __init__(self, monitor):
        super(Nntps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NNTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:nntp:nntpstate': NNTP}


class Nntp(UpdateMonitorMixin, Resource):
    """BigIP Nntps monitor resource."""
    def __init__(self, nntps):
        super(Nntp, self).__init__(nntps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:nntp:nntpstate'


class Nones(Collection):
    """BigIP None monitor collection."""
    def __init__(self, monitor):
        super(Nones, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NONE]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:none:nonestate': NONE}


class NONE(UpdateMonitorMixin, Resource):
    """BigIP None monitor resource."""
    def __init__(self, nones):
        super(NONE, self).__init__(nones)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:none:nonestate'


class Oracles(Collection):
    """BigIP Oracle monitor collection."""
    def __init__(self, monitor):
        super(Oracles, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Oracle]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:oracle:oraclestate': Oracle}


class Oracle(UpdateMonitorMixin, Resource):
    """BigIP Oracle monitor resource."""
    def __init__(self, oracles):
        super(Oracle, self).__init__(oracles)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:oracle:oraclestate'


class Pop3s(Collection):
    """BigIP POP3 monitor collection."""
    def __init__(self, monitor):
        super(Pop3s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [POP3]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:pop3:pop3state': POP3}


class Pop3(UpdateMonitorMixin, Resource):
    """BigIP Pop3 monitor resource."""
    def __init__(self, pop3s):
        super(Pop3, self).__init__(pop3s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:pop3:pop3state'


class Postgresqls(Collection):
    """BigIP PostGRES SQL monitor collection."""
    def __init__(self, monitor):
        super(Postgresqls, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [PostGRESQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:postgresql:postgresqlstate': PostGRESQL}


class Postgresql(UpdateMonitorMixin, Resource):
    """BigIP PostGRES SQL monitor resource."""
    def __init__(self, postgresqls):
        super(Postgresql, self).__init__(postgresqls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:postgresql:postgresqlstate'


class Radius_s(Collection):
    """BigIP radius monitor collection."""
    def __init__(self, monitor):
        super(Radius_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Radius]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:radius:radiusstate': Radius}


class Radius(UpdateMonitorMixin, Resource):
    """BigIP radius monitor resource."""
    def __init__(self, radius_s):
        super(Radius, self).__init__(radius_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:radius:radiusstate'


class Radius_Accountings(Collection):
    """BigIP radius accounting monitor collection."""
    def __init__(self, monitor):
        super(Radius_Accountings, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Radius_Accounting]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:radius-accounting:radius-accountingstate':
             Radius_Accounting}


class Radius_Accounting(UpdateMonitorMixin, Resource):
    """BigIP radius accounting monitor resource."""
    def __init__(self, radius_accountings):
        super(Radius_Accounting, self).__init__(radius_accountings)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:radius-accounting:radius-accountingstate'


class Real_Servers(Collection):
    """BigIP real-server monitor collection."""
    def __init__(self, monitor):
        super(Real_Servers, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Real_Server]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:real-server:real-serverstate': Real_Server}


class Real_Server(UpdateMonitorMixin, Resource):
    """BigIP real-server monitor resource."""
    def __init__(self, real_servers):
        super(Real_Server, self).__init__(real_servers)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:real-server:real-serverstate'

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


class Rpcs(Collection):
    """BigIP RPC monitor collection."""
    def __init__(self, monitor):
        super(Rpcs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [RPC]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:rpc:rpcstate': RPC}


class Rpc(UpdateMonitorMixin, Resource):
    """BigIP Rpc monitor resource."""
    def __init__(self, rpcs):
        super(Rpc, self).__init__(rpcs)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:rpc:rpcstate'


class Sasps(Collection):
    """BigIP SASP monitor collection."""
    def __init__(self, monitor):
        super(Sasps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SASP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:sasp:saspstate': SASP}


class Sasp(UpdateMonitorMixin, Resource):
    """BigIP Sasp monitor resource."""
    def __init__(self, sasps):
        super(Sasp, self).__init__(sasps)
        self._meta_data['required_creation_parameters'].update(
            ('primaryAddress',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sasp:saspstate'


class Scripteds(Collection):
    """BigIP scripted monitor collection."""
    def __init__(self, monitor):
        super(Scripteds, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Scripted]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:scripted:scriptedstate': Scripted}


class Scripted(UpdateMonitorMixin, Resource):
    """BigIP scripted monitor resource."""
    def __init__(self, scripteds):
        super(Scripted, self).__init__(scripteds)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:scripted:scriptedstate'


class Sips(Collection):
    """BigIP SIP monitor collection."""
    def __init__(self, monitor):
        super(Sips, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SIP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:sip:sipstate': SIP}


class Sip(UpdateMonitorMixin, Resource):
    """BigIP Sip monitor resource."""
    def __init__(self, sips):
        super(Sip, self).__init__(sips)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sip:sipstate'


class Smbs(Collection):
    """BigIP SMB monitor collection."""
    def __init__(self, monitor):
        super(Smbs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMB]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:smb:smbstate': SMB}


class Smb(UpdateMonitorMixin, Resource):
    """BigIP Smb monitor resource."""
    def __init__(self, smbs):
        super(Smb, self).__init__(smbs)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smb:smbstate'


class Smtps(Collection):
    """BigIP SMTP monitor collection."""
    def __init__(self, monitor):
        super(Smtps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:smtp:smtpstate': SMTP}


class Smtp(UpdateMonitorMixin, Resource):
    """BigIP Smtp monitor resource."""
    def __init__(self, smtps):
        super(Smtp, self).__init__(smtps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smtp:smtpstate'


class Snmp_Dcas(Collection):
    """BigIP SNMP DCA monitor collection."""
    def __init__(self, monitor):
        super(Snmp_Dcas, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:snmp-dca:snmp-dcastate': SNMP_DCA}


class Snmp_Dca(UpdateMonitorMixin, Resource):
    """BigIP SNMP DCA monitor resource."""
    def __init__(self, snmp_dcas):
        super(Snmp_Dca, self).__init__(snmp_dcas)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca:snmp-dcastate'


class Snmp_Dca_Bases(Collection):
    """BigIP SNMP DCA bases monitor collection."""
    def __init__(self, monitor):
        super(Snmp_Dca_Bases, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Snmp_Dca_Base]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate': Snmp_Dca_Base}


class Snmp_Dca_Base(UpdateMonitorMixin, Resource):
    """BigIP SNMP DCA monitor resource."""
    def __init__(self, snmp_dca_bases):
        super(Snmp_Dca_Base, self).__init__(snmp_dca_bases)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate'


class Soaps(Collection):
    """BigIP SOAP monitor collection."""
    def __init__(self, monitor):
        super(Soaps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SOAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:soap:soapstate': SOAP}


class Soap(UpdateMonitorMixin, Resource):
    """BigIP Soap monitor resource."""
    def __init__(self, soaps):
        super(Soap, self).__init__(soaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:soap:soapstate'


class Tcps(Collection):
    """BigIP TCP monitor collection."""
    def __init__(self, monitor):
        super(Tcps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [TCP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp:tcpstate': TCP}


class Tcp(UpdateMonitorMixin, Resource):
    """BigIP Tcp monitor resource."""
    def __init__(self, tcps):
        super(Tcp, self).__init__(tcps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp:tcpstate'


class Tcp_Echos(Collection):
    """BigIP Tcp echo monitor collection."""
    def __init__(self, monitor):
        super(Tcp_Echos, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Tcp_Echo]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp-echo:tcp-echostate': Tcp_Echo}


class Tcp_Echo(UpdateMonitorMixin, Resource):
    """BigIP Tcp echo monitor resource."""
    def __init__(self, tcp_echos):
        super(Tcp_Echo, self).__init__(tcp_echos)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-echo:tcp-echostate'


class Tcp_Half_Opens(Collection):
    """BigIP Tcp half open monitor collection."""
    def __init__(self, monitor):
        super(Tcp_Half_Opens, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Tcp_Half_Open]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp-half-open:tcp-half-openstate': Tcp_Half_Open}


class Tcp_Half_Open(UpdateMonitorMixin, Resource):
    """BigIP Tcp half open monitor resource."""
    def __init__(self, tcp_half_opens):
        super(Tcp_Half_Open, self).__init__(tcp_half_opens)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-half-open:tcp-half-openstate'


class Udps(Collection):
    """BigIP UDP monitor collection."""
    def __init__(self, monitor):
        super(Udps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [UDP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:udp:udpstate': UDP}


class Udp(UpdateMonitorMixin, Resource):
    """BigIP Udp monitor resource."""
    def __init__(self, udps):
        super(Udp, self).__init__(udps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:udp:udpstate'


class Virtual_Locations(Collection):
    """BigIP virtual-locations monitor collection."""
    def __init__(self, monitor):
        super(Virtual_Locations, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Virtual_Location]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:virtual-location:virtual-locationstate':
             Virtual_Location}


class Virtual_Location(UpdateMonitorMixin, Resource):
    """BigIP virtual-locations monitor resource."""
    def __init__(self, virtual_locations):
        super(Virtual_Location, self).__init__(virtual_locations)
        self._meta_data['required_creation_parameters'].update(
            ('pool',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:virtual-location:virtual-locationstate'


class Waps(Collection):
    """BigIP WAP monitor collection."""
    def __init__(self, monitor):
        super(Waps, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:wap:wapstate': WAP}


class Wap(UpdateMonitorMixin, Resource):
    """BigIP Wap monitor resource."""
    def __init__(self, waps):
        super(Wap, self).__init__(waps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wap:wapstate'


class Wmis(Collection):
    """BigIP WMI monitor collection."""
    def __init__(self, monitor):
        super(Wmis, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WMI]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:wmi:wmistate': WMI}


class Wmi(UpdateMonitorMixin, Resource):
    """BigIP Wmi monitor resource."""
    def __init__(self, wmis):
        super(Wmi, self).__init__(wmis)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wmi:wmistate'
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
