# Copyright 2014 F5 Networks Inc.
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
            HTTPCollection,
            HTTPSCollection,
            DiameterCollection,
            DNSCollection,
            ExternalCollection,
            FirePassCollection,
            FTPCollection,
            GateWay_ICMPCollection,
            ICMPCollection,
            IMAPCollection,
            InBandCollection,
            LDAPCollection,
            Module_ScoreCollection,
            MSSQLCollection,
            MYSQLCollection,
            NNTPCollection,
            NONECollection,
            OracleCollection,
            POP3Collection,
            PostGRESQLCollection,
            RadiusCollection,
            Radius_AccountingCollection,
            Real_ServerCollection,
            RPCCollection,
            SASPCollection,
            ScriptedCollection,
            SIPCollection,
            SMBCollection,
            SMTPCollection,
            SNMP_DCACollection,
            SNMP_DCA_BaseCollection,
            SOAPCollection,
            TCPCollection,
            TCP_EchoCollection,
            TCP_Half_OpenCollection,
            UDPCollection,
            Virtual_LocationCollection,
            WAPCollection,
            WMICollection]


class HTTPCollection(Collection):
    def __init__(self, monitor):
        super(HTTPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HTTP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:http:httpstate': HTTP}


class UpdateMonitorMixin(object):
    def update(self, **kwargs):
        self.__dict__.pop(u'defaultsFrom', '')
        self._update(**kwargs)


class HTTP(UpdateMonitorMixin, Resource):
    def __init__(self, http_collection):
        super(HTTP, self).__init__(http_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:http:httpstate'


class HTTPSCollection(Collection):
    def __init__(self, monitor):
        super(HTTPSCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [HTTPS]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:https:httpsstate': HTTPS}


class HTTPS(UpdateMonitorMixin, Resource):
    def __init__(self, https_collection):
        super(HTTPS, self).__init__(https_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:https:httpsstate'


class DiameterCollection(Collection):
    def __init__(self, monitor):
        super(DiameterCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Diameter]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:diameter:diameterstate': Diameter}


class Diameter(UpdateMonitorMixin, Resource):
    def __init__(self, diameter_collection):
        super(Diameter, self).__init__(diameter_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:diameter:diameterstate'


class DNSCollection(Collection):
    def __init__(self, monitor):
        super(DNSCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [DNS]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:dns:dnsstate': DNS}


class DNS(UpdateMonitorMixin, Resource):
    def __init__(self, dns_collection):
        super(DNS, self).__init__(dns_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:dns:dnsstate'
        self._meta_data['required_creation_parameters'].update(('qname',))


class ExternalCollection(Collection):
    def __init__(self, monitor):
        super(ExternalCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [External]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:external:externalstate': External}


class External(UpdateMonitorMixin, Resource):
    def __init__(self, external_collection):
        super(External, self).__init__(external_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:external:externalstate'


class FirePassCollection(Collection):
    def __init__(self, monitor):
        super(FirePassCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FirePass]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:firepass:firepassstate': FirePass}


class FirePass(UpdateMonitorMixin, Resource):
    def __init__(self, firepass_collection):
        super(FirePass, self).__init__(firepass_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:firepass:firepassstate'


class FTPCollection(Collection):
    def __init__(self, monitor):
        super(FTPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [FTP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:ftp:ftpstate': FTP}


class FTP(UpdateMonitorMixin, Resource):
    def __init__(self, ftp_collection):
        super(FTP, self).__init__(ftp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ftp:ftpstate'


class GateWay_ICMPCollection(Collection):
    def __init__(self, monitor):
        super(GateWay_ICMPCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [GateWay_ICMP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:gateway-icmp:gateway-icmpstate': GateWay_ICMP}


class GateWay_ICMP(UpdateMonitorMixin, Resource):
    def __init__(self, gateway_icmp_collection):
        super(GateWay_ICMP, self).__init__(gateway_icmp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:gateway-icmp:gateway-icmpstate'


class ICMPCollection(Collection):
    def __init__(self, monitor):
        super(ICMPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [ICMP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:icmp:icmpstate': ICMP}


class ICMP(UpdateMonitorMixin, Resource):
    def __init__(self, icmp_collection):
        super(ICMP, self).__init__(icmp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:icmp:icmpstate'


class IMAPCollection(Collection):
    def __init__(self, monitor):
        super(IMAPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [IMAP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:imap:imapstate': IMAP}


class IMAP(UpdateMonitorMixin, Resource):
    def __init__(self, imap_collection):
        super(IMAP, self).__init__(imap_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:imap:imapstate'


class InBandCollection(Collection):
    def __init__(self, monitor):
        super(InBandCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [InBand]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:inband:inbandstate': InBand}


class InBand(UpdateMonitorMixin, Resource):
    def __init__(self, inband_collection):
        super(InBand, self).__init__(inband_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:inband:inbandstate'


class LDAPCollection(Collection):
    def __init__(self, monitor):
        super(LDAPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [LDAP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:ldap:ldapstate': LDAP}


class LDAP(UpdateMonitorMixin, Resource):
    def __init__(self, ldap_collection):
        super(LDAP, self).__init__(ldap_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:ldap:ldapstate'


class Module_ScoreCollection(Collection):
    def __init__(self, monitor):
        super(Module_ScoreCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Module_Score]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:module-score:module-scorestate': Module_Score}


class Module_Score(UpdateMonitorMixin, Resource):
    def __init__(self, gateway_icmp_collection):
        super(Module_Score, self).__init__(gateway_icmp_collection)
        self._meta_data['required_creation_parameters'].update(
            ('snmp-ip-address',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:module-score:module-scorestate'


class MYSQLCollection(Collection):
    def __init__(self, monitor):
        super(MYSQLCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MYSQL]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:mysql:mysqlstate': MYSQL}


class MYSQL(UpdateMonitorMixin, Resource):
    def __init__(self, mysql_collection):
        super(MYSQL, self).__init__(mysql_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mysql:mysqlstate'


class MSSQLCollection(Collection):
    def __init__(self, monitor):
        super(MSSQLCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [MSSQL]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:mssql:mssqlstate': MSSQL}


class MSSQL(UpdateMonitorMixin, Resource):
    def __init__(self, mssql_collection):
        super(MSSQL, self).__init__(mssql_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:mssql:mssqlstate'


class NNTPCollection(Collection):
    def __init__(self, monitor):
        super(NNTPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NNTP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:nntp:nntpstate': NNTP}


class NNTP(UpdateMonitorMixin, Resource):
    def __init__(self, nntp_collection):
        super(NNTP, self).__init__(nntp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:nntp:nntpstate'


class NONECollection(Collection):
    def __init__(self, monitor):
        super(NONECollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [NONE]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:none:nonestate': NONE}


class NONE(UpdateMonitorMixin, Resource):
    def __init__(self, none_collection):
        super(NONE, self).__init__(none_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:none:nonestate'


class OracleCollection(Collection):
    def __init__(self, monitor):
        super(OracleCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Oracle]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:oracle:oraclestate': Oracle}


class Oracle(UpdateMonitorMixin, Resource):
    def __init__(self, oracle_collection):
        super(Oracle, self).__init__(oracle_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:oracle:oraclestate'


class POP3Collection(Collection):
    def __init__(self, monitor):
        super(POP3Collection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [POP3]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:pop3:pop3state': POP3}


class POP3(UpdateMonitorMixin, Resource):
    def __init__(self, pop3_collection):
        super(POP3, self).__init__(pop3_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:pop3:pop3state'


class PostGRESQLCollection(Collection):
    def __init__(self, monitor):
        super(PostGRESQLCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [PostGRESQL]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:postgresql:postgresqlstate': PostGRESQL}


class PostGRESQL(UpdateMonitorMixin, Resource):
    def __init__(self, postgresql_collection):
        super(PostGRESQL, self).__init__(postgresql_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:postgresql:postgresqlstate'


class RadiusCollection(Collection):
    def __init__(self, monitor):
        super(RadiusCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Radius]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:radius:radiusstate': Radius}


class Radius(UpdateMonitorMixin, Resource):
    def __init__(self, radius_collection):
        super(Radius, self).__init__(radius_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:radius:radiusstate'


class Radius_AccountingCollection(Collection):
    def __init__(self, monitor):
        super(Radius_AccountingCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Radius_Accounting]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:radius-accounting:radius-accountingstate':
             Radius_Accounting}


class Radius_Accounting(UpdateMonitorMixin, Resource):
    def __init__(self, radius_accounting_collection):
        super(Radius_Accounting, self).__init__(radius_accounting_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:radius-accounting:radius-accountingstate'


class Real_ServerCollection(Collection):
    def __init__(self, monitor):
        super(Real_ServerCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Real_Server]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:real-server:real-serverstate': Real_Server}


class Real_Server(UpdateMonitorMixin, Resource):
    def __init__(self, real_server_collection):
        super(Real_Server, self).__init__(real_server_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:real-server:real-serverstate'

    def update(self, **kwargs):
        self.__dict__.pop('tmCommand', '')
        self.__dict__.pop('agent', '')
        self.__dict__.pop('method', '')
        super(Real_Server, self).update(**kwargs)


class RPCCollection(Collection):
    def __init__(self, monitor):
        super(RPCCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [RPC]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:rpc:rpcstate': RPC}


class RPC(UpdateMonitorMixin, Resource):
    def __init__(self, rpc_collection):
        super(RPC, self).__init__(rpc_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:rpc:rpcstate'


class SASPCollection(Collection):
    def __init__(self, monitor):
        super(SASPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SASP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:sasp:saspstate': SASP}


class SASP(UpdateMonitorMixin, Resource):
    def __init__(self, sasp_collection):
        super(SASP, self).__init__(sasp_collection)
        self._meta_data['required_creation_parameters'].update(
            ('primaryAddress',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sasp:saspstate'


class ScriptedCollection(Collection):
    def __init__(self, monitor):
        super(ScriptedCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [Scripted]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:scripted:scriptedstate': Scripted}


class Scripted(UpdateMonitorMixin, Resource):
    def __init__(self, scripted_collection):
        super(Scripted, self).__init__(scripted_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:scripted:scriptedstate'


class SIPCollection(Collection):
    def __init__(self, monitor):
        super(SIPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SIP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:sip:sipstate': SIP}


class SIP(UpdateMonitorMixin, Resource):
    def __init__(self, sip_collection):
        super(SIP, self).__init__(sip_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:sip:sipstate'


class SMBCollection(Collection):
    def __init__(self, monitor):
        super(SMBCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMB]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:smb:smbstate': SMB}


class SMB(UpdateMonitorMixin, Resource):
    def __init__(self, smb_collection):
        super(SMB, self).__init__(smb_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smb:smbstate'


class SMTPCollection(Collection):
    def __init__(self, monitor):
        super(SMTPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SMTP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:smtp:smtpstate': SMTP}


class SMTP(UpdateMonitorMixin, Resource):
    def __init__(self, smtp_collection):
        super(SMTP, self).__init__(smtp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:smtp:smtpstate'


class SNMP_DCACollection(Collection):
    def __init__(self, monitor):
        super(SNMP_DCACollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:snmp-dca:snmp-dcastate': SNMP_DCA}


class SNMP_DCA(UpdateMonitorMixin, Resource):
    def __init__(self, snmp_dca_collection):
        super(SNMP_DCA, self).__init__(snmp_dca_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca:snmp-dcastate'


class SNMP_DCA_BaseCollection(Collection):
    def __init__(self, monitor):
        super(SNMP_DCA_BaseCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [SNMP_DCA_Base]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate': SNMP_DCA_Base}


class SNMP_DCA_Base(UpdateMonitorMixin, Resource):
    def __init__(self, snmp_dca_base_collection):
        super(SNMP_DCA_Base, self).__init__(snmp_dca_base_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:snmp-dca-base:snmp-dca-basestate'


class SOAPCollection(Collection):
    def __init__(self, monitor):
        super(SOAPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [SOAP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:soap:soapstate': SOAP}


class SOAP(UpdateMonitorMixin, Resource):
    def __init__(self, soap_collection):
        super(SOAP, self).__init__(soap_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:soap:soapstate'


class TCPCollection(Collection):
    def __init__(self, monitor):
        super(TCPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [TCP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:tcp:tcpstate': TCP}


class TCP(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_collection):
        super(TCP, self).__init__(tcp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp:tcpstate'


class TCP_EchoCollection(Collection):
    def __init__(self, monitor):
        super(TCP_EchoCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [TCP_Echo]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:tcp-echo:tcp-echostate': TCP_Echo}


class TCP_Echo(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_echo_collection):
        super(TCP_Echo, self).__init__(tcp_echo_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-echo:tcp-echostate'


class TCP_Half_OpenCollection(Collection):
    def __init__(self, monitor):
        super(TCP_Half_OpenCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [TCP_Half_Open]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:tcp-half-open:tcp-half-openstate': TCP_Half_Open}


class TCP_Half_Open(UpdateMonitorMixin, Resource):
    def __init__(self, tcp_half_open_collection):
        super(TCP_Half_Open, self).__init__(tcp_half_open_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:tcp-half-open:tcp-half-openstate'


class UDPCollection(Collection):
    def __init__(self, monitor):
        super(UDPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [UDP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:udp:udpstate': UDP}


class UDP(UpdateMonitorMixin, Resource):
    def __init__(self, udp_collection):
        super(UDP, self).__init__(udp_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:udp:udpstate'


class Virtual_LocationCollection(Collection):
    def __init__(self, monitor):
        super(Virtual_LocationCollection, self).__init__(monitor)
        fixed = self._meta_data['uri'].replace('_', '-')
        self._meta_data['uri'] = fixed
        self._meta_data['allowed_lazy_attributes'] = [Virtual_Location]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:virtual-location:virtual-locationstate':
             Virtual_Location}


class Virtual_Location(UpdateMonitorMixin, Resource):
    def __init__(self, virtual_location_collection):
        super(Virtual_Location, self).__init__(virtual_location_collection)
        self._meta_data['required_creation_parameters'].update(
            ('pool',))
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:virtual-location:virtual-locationstate'


class WAPCollection(Collection):
    def __init__(self, monitor):
        super(WAPCollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WAP]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:wap:wapstate': WAP}


class WAP(UpdateMonitorMixin, Resource):
    def __init__(self, wap_collection):
        super(WAP, self).__init__(wap_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wap:wapstate'


class WMICollection(Collection):
    def __init__(self, monitor):
        super(WMICollection, self).__init__(monitor)
        self._meta_data['allowed_lazy_attributes'] = [WMI]
        self._meta_data['collection_registry'] =\
            {'tm:ltm:monitor:wmi:wmistate': WMI}


class WMI(UpdateMonitorMixin, Resource):
    def __init__(self, wmi_collection):
        super(WMI, self).__init__(wmi_collection)
        self._meta_data['required_json_kind'] =\
            'tm:ltm:monitor:wmi:wmistate'

    def update(self, **kwargs):
        self.__dict__.pop('agent', '')
        self.__dict__.pop('post', '')
        self.__dict__.pop('method', '')
        super(WMI, self).update(**kwargs)
