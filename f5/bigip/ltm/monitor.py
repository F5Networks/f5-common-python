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
    def __init__(self, monitor):
        super(HTTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HTTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:http:httpstate': HTTP}


class UpdateMonitorMixin(object):
    def update(self, **kwargs):
        self.__dict__.pop(u'defaultsFrom', '')
        self._update(**kwargs)


class HTTP(UpdateMonitorMixin, Resource):
    def __init__(self, http_s):
        super(HTTP, self).__init__(http_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:http:httpstate'


class HTTPS_s(Collection):
    def __init__(self, monitor):
        super(HTTPS_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HTTPS]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:https:httpsstate': HTTPS}


class HTTPS(UpdateMonitorMixin, Resource):
    def __init__(self, https_s):
        super(HTTPS, self).__init__(https_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:https:httpsstate'


class Diameters(Collection):
    def __init__(self, monitor):
        super(Diameters, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Diameter]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:diameter:diameterstate': Diameter}


class Diameter(UpdateMonitorMixin, Resource):
    def __init__(self, diameter_s):
        super(Diameter, self).__init__(diameter_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:diameter:diameterstate'


class DNS_s(Collection):
    def __init__(self, monitor):
        super(DNS_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [DNS]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:dns:dnsstate': DNS}


class DNS(UpdateMonitorMixin, Resource):
    def __init__(self, dns_s):
        super(DNS, self).__init__(dns_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:dns:dnsstate'
        self._meta_data['required_creation_parameters'].update(('qname',))


class Externals(Collection):
    def __init__(self, monitor):
        super(Externals, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [External]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:external:externalstate': External}


class External(UpdateMonitorMixin, Resource):
    def __init__(self, external_s):
        super(External, self).__init__(external_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:external:externalstate'


class FirePass_s(Collection):
    def __init__(self, monitor):
        super(FirePass_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FirePass]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:firepass:firepassstate': FirePass}


class FirePass(UpdateMonitorMixin, Resource):
    def __init__(self, firepass_s):
        super(FirePass, self).__init__(firepass_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:firepass:firepassstate'


class FTPs(Collection):
    def __init__(self, monitor):
        super(FTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:ftp:ftpstate': FTP}


class FTP(UpdateMonitorMixin, Resource):
    def __init__(self, ftp_s):
        super(FTP, self).__init__(ftp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ftp:ftpstate'


class GateWay_ICMPs(Collection):
    def __init__(self, monitor):
        super(GateWay_ICMPs, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [GateWay_ICMP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:gateway-icmp:gateway-icmpstate': GateWay_ICMP}


class GateWay_ICMP(UpdateMonitorMixin, Resource):
    def __init__(self, gateway_icmp_s):
        super(GateWay_ICMP, self).__init__(gateway_icmp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:gateway-icmp:gateway-icmpstate'


class ICMPs(Collection):
    def __init__(self, monitor):
        super(ICMPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [ICMP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:icmp:icmpstate': ICMP}


class ICMP(UpdateMonitorMixin, Resource):
    def __init__(self, icmp_s):
        super(ICMP, self).__init__(icmp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:icmp:icmpstate'


class IMAPs(Collection):
    def __init__(self, monitor):
        super(IMAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [IMAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:imap:imapstate': IMAP}


class IMAP(UpdateMonitorMixin, Resource):
    def __init__(self, imap_s):
        super(IMAP, self).__init__(imap_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:imap:imapstate'


class InBands(Collection):
    def __init__(self, monitor):
        super(InBands, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [InBand]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:inband:inbandstate': InBand}


class InBand(UpdateMonitorMixin, Resource):
    def __init__(self, inband_s):
        super(InBand, self).__init__(inband_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:inband:inbandstate'


class LDAPs(Collection):
    def __init__(self, monitor):
        super(LDAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [LDAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:ldap:ldapstate': LDAP}


class LDAP(UpdateMonitorMixin, Resource):
    def __init__(self, ldap_s):
        super(LDAP, self).__init__(ldap_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ldap:ldapstate'


class Module_Scores(Collection):
    def __init__(self, monitor):
        super(Module_Scores, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Module_Score]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:module-score:module-scorestate': Module_Score}


class Module_Score(UpdateMonitorMixin, Resource):
    def __init__(self, gateway_icmp_s):
        super(Module_Score, self).__init__(gateway_icmp_s)
        self._meta_data['required_creation_parameters'].update(
            ('snmp-ip-address',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:module-score:module-scorestate'


class MYSQLs(Collection):
    def __init__(self, monitor):
        super(MYSQLs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MYSQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:mysql:mysqlstate': MYSQL}


class MYSQL(UpdateMonitorMixin, Resource):
    def __init__(self, mysql_s):
        super(MYSQL, self).__init__(mysql_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mysql:mysqlstate'


class MSSQLs(Collection):
    def __init__(self, monitor):
        super(MSSQLs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MSSQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:mssql:mssqlstate': MSSQL}


class MSSQL(UpdateMonitorMixin, Resource):
    def __init__(self, mssql_s):
        super(MSSQL, self).__init__(mssql_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mssql:mssqlstate'


class NNTPs(Collection):
    def __init__(self, monitor):
        super(NNTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NNTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:nntp:nntpstate': NNTP}


class NNTP(UpdateMonitorMixin, Resource):
    def __init__(self, nntp_s):
        super(NNTP, self).__init__(nntp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:nntp:nntpstate'


class NONEs(Collection):
    def __init__(self, monitor):
        super(NONEs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NONE]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:none:nonestate': NONE}


class NONE(UpdateMonitorMixin, Resource):
    def __init__(self, none_s):
        super(NONE, self).__init__(none_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:none:nonestate'


class Oracles(Collection):
    def __init__(self, monitor):
        super(Oracles, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Oracle]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:oracle:oraclestate': Oracle}


class Oracle(UpdateMonitorMixin, Resource):
    def __init__(self, oracle_s):
        super(Oracle, self).__init__(oracle_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:oracle:oraclestate'


class POP3s(Collection):
    def __init__(self, monitor):
        super(POP3s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [POP3]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:pop3:pop3state': POP3}


class POP3(UpdateMonitorMixin, Resource):
    def __init__(self, pop3_s):
        super(POP3, self).__init__(pop3_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:pop3:pop3state'


class PostGRESQLs(Collection):
    def __init__(self, monitor):
        super(PostGRESQLs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [PostGRESQL]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:postgresql:postgresqlstate': PostGRESQL}


class PostGRESQL(UpdateMonitorMixin, Resource):
    def __init__(self, postgresql_s):
        super(PostGRESQL, self).__init__(postgresql_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:postgresql:postgresqlstate'


class Radius_s(Collection):
    def __init__(self, monitor):
        super(Radius_s, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Radius]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:radius:radiusstate': Radius}


class Radius(UpdateMonitorMixin, Resource):
    def __init__(self, radius_s):
        super(Radius, self).__init__(radius_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:radius:radiusstate'


class Radius_Accountings(Collection):
    def __init__(self, monitor):
        super(Radius_Accountings, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Radius_Accounting]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:radius-accounting:radius-accountingstate':
             Radius_Accounting}


class Radius_Accounting(UpdateMonitorMixin, Resource):
    def __init__(self, radius_accountings):
        super(Radius_Accounting, self).__init__(radius_accountings)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:radius-accounting:radius-accountingstate'


class Real_Servers(Collection):
    def __init__(self, monitor):
        super(Real_Servers, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Real_Server]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:real-server:real-serverstate': Real_Server}


class Real_Server(UpdateMonitorMixin, Resource):
    def __init__(self, real_server_s):
        super(Real_Server, self).__init__(real_server_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:real-server:real-serverstate'

    def update(self, **kwargs):
        self.__dict__.pop('tmCommand', '')
        self.__dict__.pop('agent', '')
        self.__dict__.pop('method', '')
        super(Real_Server, self).update(**kwargs)


class RPCs(Collection):
    def __init__(self, monitor):
        super(RPCs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [RPC]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:rpc:rpcstate': RPC}


class RPC(UpdateMonitorMixin, Resource):
    def __init__(self, rpc_s):
        super(RPC, self).__init__(rpc_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:rpc:rpcstate'


class SASPs(Collection):
    def __init__(self, monitor):
        super(SASPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SASP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:sasp:saspstate': SASP}


class SASP(UpdateMonitorMixin, Resource):
    def __init__(self, sasp_s):
        super(SASP, self).__init__(sasp_s)
        self._meta_data['required_creation_parameters'].update(
            ('primaryAddress',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sasp:saspstate'


class Scripteds(Collection):
    def __init__(self, monitor):
        super(Scripteds, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Scripted]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:scripted:scriptedstate': Scripted}


class Scripted(UpdateMonitorMixin, Resource):
    def __init__(self, scripted_s):
        super(Scripted, self).__init__(scripted_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:scripted:scriptedstate'


class SIPs(Collection):
    def __init__(self, monitor):
        super(SIPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SIP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:sip:sipstate': SIP}


class SIP(UpdateMonitorMixin, Resource):
    def __init__(self, sip_s):
        super(SIP, self).__init__(sip_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sip:sipstate'


class SMBs(Collection):
    def __init__(self, monitor):
        super(SMBs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMB]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:smb:smbstate': SMB}


class SMB(UpdateMonitorMixin, Resource):
    def __init__(self, smb_s):
        super(SMB, self).__init__(smb_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smb:smbstate'


class SMTPs(Collection):
    def __init__(self, monitor):
        super(SMTPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMTP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:smtp:smtpstate': SMTP}


class SMTP(UpdateMonitorMixin, Resource):
    def __init__(self, smtp_s):
        super(SMTP, self).__init__(smtp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smtp:smtpstate'


class SNMP_DCAs(Collection):
    def __init__(self, monitor):
        super(SNMP_DCAs, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:snmp-dca:snmp-dcastate': SNMP_DCA}


class SNMP_DCA(UpdateMonitorMixin, Resource):
    def __init__(self, snmp_dca_s):
        super(SNMP_DCA, self).__init__(snmp_dca_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca:snmp-dcastate'


class SNMP_DCA_Bases(Collection):
    def __init__(self, monitor):
        super(SNMP_DCA_Bases, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA_Base]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate': SNMP_DCA_Base}


class SNMP_DCA_Base(UpdateMonitorMixin, Resource):
    def __init__(self, snmp_dca_base_s):
        super(SNMP_DCA_Base, self).__init__(snmp_dca_base_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate'


class SOAPs(Collection):
    def __init__(self, monitor):
        super(SOAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SOAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:soap:soapstate': SOAP}


class SOAP(UpdateMonitorMixin, Resource):
    def __init__(self, soap_s):
        super(SOAP, self).__init__(soap_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:soap:soapstate'


class TCPs(Collection):
    def __init__(self, monitor):
        super(TCPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [TCP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp:tcpstate': TCP}


class TCP(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_s):
        super(TCP, self).__init__(tcp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp:tcpstate'


class TCP_Echos(Collection):
    def __init__(self, monitor):
        super(TCP_Echos, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [TCP_Echo]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp-echo:tcp-echostate': TCP_Echo}


class TCP_Echo(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_echo_s):
        super(TCP_Echo, self).__init__(tcp_echo_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-echo:tcp-echostate'


class TCP_Half_Opens(Collection):
    def __init__(self, monitor):
        super(TCP_Half_Opens, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [TCP_Half_Open]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:tcp-half-open:tcp-half-openstate': TCP_Half_Open}


class TCP_Half_Open(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_half_open_s):
        super(TCP_Half_Open, self).__init__(tcp_half_open_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-half-open:tcp-half-openstate'


class UDPs(Collection):
    def __init__(self, monitor):
        super(UDPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [UDP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:udp:udpstate': UDP}


class UDP(UpdateMonitorMixin, Resource):
    def __init__(self, udp_s):
        super(UDP, self).__init__(udp_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:udp:udpstate'


class Virtual_Locations(Collection):
    def __init__(self, monitor):
        super(Virtual_Locations, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Virtual_Location]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:virtual-location:virtual-locationstate':
             Virtual_Location}


class Virtual_Location(UpdateMonitorMixin, Resource):
    def __init__(self, virtual_location_s):
        super(Virtual_Location, self).__init__(virtual_location_s)
        self._meta_data['required_creation_parameters'].update(
            ('pool',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:virtual-location:virtual-locationstate'


class WAPs(Collection):
    def __init__(self, monitor):
        super(WAPs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WAP]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:wap:wapstate': WAP}


class WAP(UpdateMonitorMixin, Resource):
    def __init__(self, wap_s):
        super(WAP, self).__init__(wap_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wap:wapstate'


class WMIs(Collection):
    def __init__(self, monitor):
        super(WMIs, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WMI]
        self._meta_data['attribute_registry'] =\
            {'tm:ltm:monitor:wmi:wmistate': WMI}


class WMI(UpdateMonitorMixin, Resource):
    def __init__(self, wmi_s):
        super(WMI, self).__init__(wmi_s)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wmi:wmistate'
        self._meta_data['read_only_attributes'] =\
            ['agent', 'post', 'method']

    def update(self, **kwargs):
        self.__dict__.pop('agent', '')
        self.__dict__.pop('post', '')
        self.__dict__.pop('method', '')
        super(WMI, self).update(**kwargs)
