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


class HTTPs(Collection):
    """BigIP HTTP monitor collection."""
    def __init__(self, monitor):
        super(HTTPs, self).__init__(monitor)
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


class HTTP(UpdateMonitorMixin, Resource):
    """BigIP HTTP monitor resource."""
    def __init__(self, https):
        super(HTTP, self).__init__(https)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:http:httpstate'


class HTTPS_s(Collection):
    """BigIP HTTPS monitor collection."""
    def __init__(self, monitor):
        super(HTTPS_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HTTPS]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:https:httpsstate': HTTPS}


class HTTPS(UpdateMonitorMixin, Resource):
    """BigIP HTTPS monitor resource."""
    def __init__(self, https_s):
        super(HTTPS, self).__init__(https_s)
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


class DNS_s(Collection):
    """BigIP DNS monitor collection."""
    def __init__(self, monitor):
        super(DNS_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [DNS]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:dns:dnsstate': DNS}


class DNS(UpdateMonitorMixin, Resource):
    """BigIP DNS monitor resource."""
    def __init__(self, dns_s):
        super(DNS, self).__init__(dns_s)
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


class FirePass_s(Collection):
    """BigIP Fire Pass monitor collection."""
    def __init__(self, monitor):
        super(FirePass_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FirePass]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:firepass:firepassstate': FirePass}


class FirePass(UpdateMonitorMixin, Resource):
    """BigIP external monitor resource."""
    def __init__(self, firepass_s):
        super(FirePass, self).__init__(firepass_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:firepass:firepassstate'


class FTPs(Collection):
    """BigIP FTP monitor collection."""
    def __init__(self, monitor):
        super(FTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:ftp:ftpstate': FTP}


class FTP(UpdateMonitorMixin, Resource):
    """BigIP FTP monitor resource."""
    def __init__(self, ftps):
        super(FTP, self).__init__(ftps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ftp:ftpstate'


class GateWay_ICMPs(Collection):
    """BigIP Gateway ICMP monitor collection."""
    def __init__(self, monitor):
        super(GateWay_ICMPs, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [GateWay_ICMP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:gateway-icmp:gateway-icmpstate': GateWay_ICMP}


class GateWay_ICMP(UpdateMonitorMixin, Resource):
    """BigIP Gateway ICMP monitor resource."""
    def __init__(self, gateway_icmps):
        super(GateWay_ICMP, self).__init__(gateway_icmps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:gateway-icmp:gateway-icmpstate'


class ICMPs(Collection):
    """BigIP ICMP monitor collection."""
    def __init__(self, monitor):
        super(ICMPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [ICMP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:icmp:icmpstate': ICMP}


class ICMP(UpdateMonitorMixin, Resource):
    """BigIP ICMP monitor resource."""
    def __init__(self, icmps):
        super(ICMP, self).__init__(icmps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:icmp:icmpstate'


class IMAPs(Collection):
    """BigIP IMAP monitor collection."""
    def __init__(self, monitor):
        super(IMAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [IMAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:imap:imapstate': IMAP}


class IMAP(UpdateMonitorMixin, Resource):
    """BigIP IMAP monitor resource."""
    def __init__(self, imaps):
        super(IMAP, self).__init__(imaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:imap:imapstate'


class InBands(Collection):
    """BigIP in band monitor collection."""
    def __init__(self, monitor):
        super(InBands, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [InBand]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:inband:inbandstate': InBand}


class InBand(UpdateMonitorMixin, Resource):
    """BigIP in band monitor resource."""
    def __init__(self, inbands):
        super(InBand, self).__init__(inbands)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:inband:inbandstate'


class LDAPs(Collection):
    """BigIP LDAP monitor collection."""
    def __init__(self, monitor):
        super(LDAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [LDAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:ldap:ldapstate': LDAP}


class LDAP(UpdateMonitorMixin, Resource):
    """BigIP LDAP monitor resource."""
    def __init__(self, ldaps):
        super(LDAP, self).__init__(ldaps)
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


class MYSQLs(Collection):
    """BigIP MySQL monitor collection."""
    def __init__(self, monitor):
        super(MYSQLs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MYSQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:mysql:mysqlstate': MYSQL}


class MYSQL(UpdateMonitorMixin, Resource):
    """BigIP MySQL monitor resource."""
    def __init__(self, mysqls):
        super(MYSQL, self).__init__(mysqls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mysql:mysqlstate'


class MSSQLs(Collection):
    """BigIP MSSQL monitor collection."""
    def __init__(self, monitor):
        super(MSSQLs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MSSQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:mssql:mssqlstate': MSSQL}


class MSSQL(UpdateMonitorMixin, Resource):
    """BigIP MSSQL monitor resource."""
    def __init__(self, mssqls):
        super(MSSQL, self).__init__(mssqls)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mssql:mssqlstate'


class NNTPs(Collection):
    """BigIP NNTPs monitor collection."""
    def __init__(self, monitor):
        super(NNTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NNTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:nntp:nntpstate': NNTP}


class NNTP(UpdateMonitorMixin, Resource):
    """BigIP NNTPs monitor resource."""
    def __init__(self, nntps):
        super(NNTP, self).__init__(nntps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:nntp:nntpstate'


class NONEs(Collection):
    """BigIP None monitor collection."""
    def __init__(self, monitor):
        super(NONEs, self).__init__(monitor)
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


class POP3s(Collection):
    """BigIP POP3 monitor collection."""
    def __init__(self, monitor):
        super(POP3s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [POP3]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:pop3:pop3state': POP3}


class POP3(UpdateMonitorMixin, Resource):
    """BigIP POP3 monitor resource."""
    def __init__(self, pop3s):
        super(POP3, self).__init__(pop3s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:pop3:pop3state'


class PostGRESQLs(Collection):
    """BigIP PostGRES SQL monitor collection."""
    def __init__(self, monitor):
        super(PostGRESQLs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [PostGRESQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:postgresql:postgresqlstate': PostGRESQL}


class PostGRESQL(UpdateMonitorMixin, Resource):
    """BigIP PostGRES SQL monitor resource."""
    def __init__(self, postgresqls):
        super(PostGRESQL, self).__init__(postgresqls)
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

        This method uses HTTP PUT alter the service state on the device.

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


class RPCs(Collection):
    """BigIP RPC monitor collection."""
    def __init__(self, monitor):
        super(RPCs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [RPC]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:rpc:rpcstate': RPC}


class RPC(UpdateMonitorMixin, Resource):
    """BigIP RPC monitor resource."""
    def __init__(self, rpcs):
        super(RPC, self).__init__(rpcs)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:rpc:rpcstate'


class SASPs(Collection):
    """BigIP SASP monitor collection."""
    def __init__(self, monitor):
        super(SASPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SASP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:sasp:saspstate': SASP}


class SASP(UpdateMonitorMixin, Resource):
    """BigIP SASP monitor resource."""
    def __init__(self, sasps):
        super(SASP, self).__init__(sasps)
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


class SIPs(Collection):
    """BigIP SIP monitor collection."""
    def __init__(self, monitor):
        super(SIPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SIP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:sip:sipstate': SIP}


class SIP(UpdateMonitorMixin, Resource):
    """BigIP SIP monitor resource."""
    def __init__(self, sips):
        super(SIP, self).__init__(sips)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sip:sipstate'


class SMBs(Collection):
    """BigIP SMB monitor collection."""
    def __init__(self, monitor):
        super(SMBs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMB]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:smb:smbstate': SMB}


class SMB(UpdateMonitorMixin, Resource):
    """BigIP SMB monitor resource."""
    def __init__(self, smbs):
        super(SMB, self).__init__(smbs)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smb:smbstate'


class SMTPs(Collection):
    """BigIP SMTP monitor collection."""
    def __init__(self, monitor):
        super(SMTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:smtp:smtpstate': SMTP}


class SMTP(UpdateMonitorMixin, Resource):
    """BigIP SMTP monitor resource."""
    def __init__(self, smtps):
        super(SMTP, self).__init__(smtps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smtp:smtpstate'


class SNMP_DCAs(Collection):
    """BigIP SNMP DCA monitor collection."""
    def __init__(self, monitor):
        super(SNMP_DCAs, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:snmp-dca:snmp-dcastate': SNMP_DCA}


class SNMP_DCA(UpdateMonitorMixin, Resource):
    """BigIP SNMP DCA monitor resource."""
    def __init__(self, snmp_dcas):
        super(SNMP_DCA, self).__init__(snmp_dcas)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca:snmp-dcastate'


class SNMP_DCA_Bases(Collection):
    """BigIP SNMP DCA bases monitor collection."""
    def __init__(self, monitor):
        super(SNMP_DCA_Bases, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA_Base]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate': SNMP_DCA_Base}


class SNMP_DCA_Base(UpdateMonitorMixin, Resource):
    """BigIP SNMP DCA monitor resource."""
    def __init__(self, snmp_dca_bases):
        super(SNMP_DCA_Base, self).__init__(snmp_dca_bases)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate'


class SOAPs(Collection):
    """BigIP SOAP monitor collection."""
    def __init__(self, monitor):
        super(SOAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SOAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:soap:soapstate': SOAP}


class SOAP(UpdateMonitorMixin, Resource):
    """BigIP SOAP monitor resource."""
    def __init__(self, soaps):
        super(SOAP, self).__init__(soaps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:soap:soapstate'


class TCPs(Collection):
    """BigIP TCP monitor collection."""
    def __init__(self, monitor):
        super(TCPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [TCP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp:tcpstate': TCP}


class TCP(UpdateMonitorMixin, Resource):
    """BigIP TCP monitor resource."""
    def __init__(self, tcps):
        super(TCP, self).__init__(tcps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp:tcpstate'


class TCP_Echos(Collection):
    """BigIP TCP echo monitor collection."""
    def __init__(self, monitor):
        super(TCP_Echos, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [TCP_Echo]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp-echo:tcp-echostate': TCP_Echo}


class TCP_Echo(UpdateMonitorMixin, Resource):
    """BigIP TCP echo monitor resource."""
    def __init__(self, tcp_echos):
        super(TCP_Echo, self).__init__(tcp_echos)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-echo:tcp-echostate'


class TCP_Half_Opens(Collection):
    """BigIP TCP half open monitor collection."""
    def __init__(self, monitor):
        super(TCP_Half_Opens, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [TCP_Half_Open]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp-half-open:tcp-half-openstate': TCP_Half_Open}


class TCP_Half_Open(UpdateMonitorMixin, Resource):
    """BigIP TCP half open monitor resource."""
    def __init__(self, tcp_half_opens):
        super(TCP_Half_Open, self).__init__(tcp_half_opens)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-half-open:tcp-half-openstate'


class UDPs(Collection):
    """BigIP UDP monitor collection."""
    def __init__(self, monitor):
        super(UDPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [UDP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:udp:udpstate': UDP}


class UDP(UpdateMonitorMixin, Resource):
    """BigIP UDP monitor resource."""
    def __init__(self, udps):
        super(UDP, self).__init__(udps)
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


class WAPs(Collection):
    """BigIP WAP monitor collection."""
    def __init__(self, monitor):
        super(WAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:wap:wapstate': WAP}


class WAP(UpdateMonitorMixin, Resource):
    """BigIP WAP monitor resource."""
    def __init__(self, waps):
        super(WAP, self).__init__(waps)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wap:wapstate'


class WMIs(Collection):
    """BigIP WMI monitor collection."""
    def __init__(self, monitor):
        super(WMIs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WMI]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:wmi:wmistate': WMI}


class WMI(UpdateMonitorMixin, Resource):
    """BigIP WMI monitor resource."""
    def __init__(self, wmis):
        super(WMI, self).__init__(wmis)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wmi:wmistate'
        self._meta_data['read_only_attributes'] =\
            ['agent', 'post', 'method']

    def update(self, **kwargs):
        """Change the configuration of the resource on the device.

        This method uses HTTP PUT alter the service state on the device.

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
        super(WMI, self).update(**kwargs)
