# Copyright 2018 F5 Networks Inc.
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

import os
import pytest
import tempfile

TESTDESCRIPTION = "TESTDESCRIPTION"


def create_refresh_update_delete_load(resource, collection):
    resource.description = TESTDESCRIPTION
    resource.update()
    assert resource.description == TESTDESCRIPTION
    resource.description = ''
    resource.refresh()
    assert resource.description == TESTDESCRIPTION
    r2 = collection.load(
        partition='Common', name=resource.name
    )
    assert r2.selfLink == resource.selfLink


@pytest.fixture
def temp_name():
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    return name


@pytest.fixture
def monitors_oc(mgmt_root):
    monitor1 = mgmt_root.tm.gtm.monitor
    return monitor1


class TestMonitor(object):
    def test_get_collection(self, monitors_oc):
        list_of_references = monitors_oc.get_collection()
        assert len(list_of_references) == 32


# Begin Bigip Tests
@pytest.fixture
def bigip_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.bigips.bigip.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def bigip_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.bigips.bigip
    yield collection


class TestMonitorBigip(object):
    def test_create_refresh_update_delete_load(self, bigip_resource, bigip_collection):
        create_refresh_update_delete_load(bigip_resource, bigip_collection)
# End Bigip Tests


# Begin Bigip Links Tests
@pytest.fixture
def bigip_link_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.bigip_links.bigip_link.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def bigip_link_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.bigip_links.bigip_link
    yield collection


class TestMonitorBigipLink(object):
    def test_create_refresh_update_delete_load(self, bigip_link_resource, bigip_link_collection):
        create_refresh_update_delete_load(bigip_link_resource, bigip_link_collection)
# End BIGIP Tests


# Begin External
@pytest.fixture
def external_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.externals.external.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def external_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.externals.external
    yield collection


class TestMonitorExternal(object):
    def test_create_refresh_update_delete_load(self, external_resource, external_collection):
        create_refresh_update_delete_load(external_resource, external_collection)
# End External Tests


# Begin FirePass
@pytest.fixture
def firepass_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.firepass_s.firepass.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def firepass_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.firepass_s.firepass
    yield collection


class TestMonitorFirepass(object):
    def test_create_refresh_update_delete_load(self, firepass_resource, firepass_collection):
        create_refresh_update_delete_load(firepass_resource, firepass_collection)
# End FirePass Tests


# Begin FTP Tests
@pytest.fixture
def ftp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.ftps.ftp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def ftp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.ftps.ftp
    yield collection


class TestMonitorFtps(object):
    def test_create_refresh_update_delete_load(self, ftp_resource, ftp_collection):
        create_refresh_update_delete_load(ftp_resource, ftp_collection)
# End FTP Tests


# Begin GateWay-ICMP
@pytest.fixture
def gateway_icmp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def gateway_icmp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.gateway_icmps.gateway_icmp
    yield collection


class TestMonitorGatewayIcmp(object):
    def test_create_refresh_update_delete_load(self, gateway_icmp_resource, gateway_icmp_collection):
        create_refresh_update_delete_load(gateway_icmp_resource, gateway_icmp_collection)
# End GateWay-ICMP


# Begin GTP
@pytest.fixture
def gtp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.gtps.gtp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def gtp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.gtps.gtp
    yield collection


class TestMonitorGtp(object):
    def test_create_refresh_update_delete_load(self, gtp_resource, gtp_collection):
        create_refresh_update_delete_load(gtp_resource, gtp_collection)
# End GTP


# Begin HTTP Tests
@pytest.fixture
def http_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.https.http.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def http_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.https.http
    yield collection


class TestMonitorHTTP(object):
    def test_create_refresh_update_delete_load(self, http_resource, http_collection):
        create_refresh_update_delete_load(http_resource, http_collection)
# End HTTP Tests


# Begin HTTPS Tests
@pytest.fixture
def https_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.https_s.https.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def https_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.https_s.https
    yield collection


class TestMonitorHTTPS(object):
    def test_create_refresh_update_delete_load(self, https_resource, https_collection):
        create_refresh_update_delete_load(https_resource, https_collection)
# End HTTPS Tests


# Begin IMAP
@pytest.fixture
def imap_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.imaps.imap.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def imap_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.imaps.imap
    yield collection


class TestMonitorImap(object):
    def test_create_refresh_update_delete_load(self, imap_resource, imap_collection):
        create_refresh_update_delete_load(imap_resource, imap_collection)
# End IMAP


# Begin LDAP
@pytest.fixture
def ldap_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.ldaps.ldap.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def ldap_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.ldaps.ldap
    yield collection


class TestMonitorLdap(object):
    def test_create_refresh_update_delete_load(self, ldap_resource, ldap_collection):
        create_refresh_update_delete_load(ldap_resource, ldap_collection)
# End LDAP Tests


# Begin MSSQL
@pytest.fixture
def mssql_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.mssqls.mssql.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def mssql_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.mssqls.mssql
    yield collection


class TestMonitorMssql(object):
    def test_create_refresh_update_delete_load(self, mssql_resource, mssql_collection):
        create_refresh_update_delete_load(mssql_resource, mssql_collection)
# End MSSQL


# Begin MYSQL
@pytest.fixture
def mysql_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.mysqls.mysql.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def mysql_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.mysqls.mysql
    yield collection


class TestMonitorMysql(object):
    def test_create_refresh_update_delete_load(self, mysql_resource, mysql_collection):
        create_refresh_update_delete_load(mysql_resource, mysql_collection)
# End MYSQL


# Begin NNTP
@pytest.fixture
def nntp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.nntps.nntp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def nntp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.nntps.nntp
    yield collection


class TestMonitorNntp(object):
    def test_create_refresh_update_delete_load(self, nntp_resource, nntp_collection):
        create_refresh_update_delete_load(nntp_resource, nntp_collection)
# End NNTP


# Begin Oracle
@pytest.fixture
def oracle_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.oracles.oracle.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def oracle_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.oracles.oracle
    yield collection


class TestMonitorOracle(object):
    def test_create_refresh_update_delete_load(self, oracle_resource, oracle_collection):
        create_refresh_update_delete_load(oracle_resource, oracle_collection)
# End Oracle


# Begin POP3
@pytest.fixture
def pop3_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.pop3s.pop3.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def pop3_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.pop3s.pop3
    yield collection


class TestMonitorPop3(object):
    def test_create_refresh_update_delete_load(self, pop3_resource, pop3_collection):
        create_refresh_update_delete_load(pop3_resource, pop3_collection)
# End POP3


# Begin PostgreSQL
@pytest.fixture
def postgresql_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.postgresqls.postgresql.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def postgresql_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.postgresqls.postgresql
    yield collection


class TestMonitorPostgreSQL(object):
    def test_create_refresh_update_delete_load(self, postgresql_resource, postgresql_collection):
        create_refresh_update_delete_load(postgresql_resource, postgresql_collection)
# End PostGRESQL


# Begin Radius
@pytest.fixture
def radius_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.radius_s.radius.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def radius_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.radius_s.radius
    yield collection


class TestMonitorRadius(object):
    def test_create_refresh_update_delete_load(self, radius_resource, radius_collection):
        create_refresh_update_delete_load(radius_resource, radius_collection)
# End Radius


# Begin Radius_Accounting
@pytest.fixture
def radius_accounting_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.radius_accountings.radius_accounting.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def radius_accounting_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.radius_accountings.radius_accounting
    yield collection


class TestMonitorRadiusAccounting(object):
    def test_create_refresh_update_delete_load(self, radius_accounting_resource, radius_accounting_collection):
        create_refresh_update_delete_load(radius_accounting_resource, radius_accounting_collection)
# End Radius_Accounting


# Begin Real_Server
@pytest.fixture
def real_server_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.real_servers.real_server.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def real_server_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.real_servers.real_server
    yield collection


class TestMonitorRealServer(object):
    def test_create_refresh_update_delete_load(self, real_server_resource, real_server_collection):
        create_refresh_update_delete_load(real_server_resource, real_server_collection)
# End Real_Server


# Begin Scripted
@pytest.fixture
def scripted_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.scripteds.scripted.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def scripted_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.scripteds.scripted
    yield collection


class TestMonitorScripted(object):
    def test_create_refresh_update_delete_load(self, scripted_resource, scripted_collection):
        create_refresh_update_delete_load(scripted_resource, scripted_collection)
# End Scripted


# Begin SIP
@pytest.fixture
def sip_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.sips.sip.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def sip_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.sips.sip
    yield collection


class TestMonitorSip(object):
    def test_create_refresh_update_delete_load(self, sip_resource, sip_collection):
        create_refresh_update_delete_load(sip_resource, sip_collection)
# End SIP


# Begin SMTP
@pytest.fixture
def smtp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.smtps.smtp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def smtp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.smtps.smtp
    yield collection


class TestMonitorSmtp(object):
    def test_create_refresh_update_delete_load(self, smtp_resource, smtp_collection):
        create_refresh_update_delete_load(smtp_resource, smtp_collection)
# End SMTP


# Begin SNMP
@pytest.fixture
def snmp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.snmps.snmp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def snmp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.snmps.snmp
    yield collection


class TestMonitorSnmp(object):
    def test_create_refresh_update_delete_load(self, snmp_resource, snmp_collection):
        create_refresh_update_delete_load(snmp_resource, snmp_collection)
# End SNMP


# Begin SNMP Link
@pytest.fixture
def snmp_link_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.snmp_links.snmp_link.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def snmp_link_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.snmp_links.snmp_link
    yield collection


class TestMonitorSnmpLink(object):
    def test_create_refresh_update_delete_load(self, snmp_link_resource, snmp_link_collection):
        create_refresh_update_delete_load(snmp_link_resource, snmp_link_collection)
# End SNMP


# Begin SOAP
@pytest.fixture
def soap_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.soaps.soap.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def soap_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.soaps.soap
    yield collection


class TestMonitorSoap(object):
    def test_create_refresh_update_delete_load(self, soap_resource, soap_collection):
        create_refresh_update_delete_load(soap_resource, soap_collection)
# End SOAP


# Begin TCP
@pytest.fixture
def tcp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.tcps.tcp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def tcp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.tcps.tcp
    yield collection


class TestMonitorTcp(object):
    def test_create_refresh_update_delete_load(self, tcp_resource, tcp_collection):
        create_refresh_update_delete_load(tcp_resource, tcp_collection)
# End TCP


# Begin TCP_Half_Open
@pytest.fixture
def tcp_half_open_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.tcp_half_opens.tcp_half_open.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def tcp_half_open_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.tcp_half_opens.tcp_half_open
    yield collection


class TestMonitorTcpHalfOpen(object):
    def test_create_refresh_update_delete_load(self, tcp_half_open_resource, tcp_half_open_collection):
        create_refresh_update_delete_load(tcp_half_open_resource, tcp_half_open_collection)
# End TCP_Half_Open


# Begin UDP
@pytest.fixture
def udp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.udps.udp.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def udp_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.udps.udp
    yield collection


class TestMonitorUdp(object):
    def test_create_refresh_update_delete_load(self, udp_resource, udp_collection):
        create_refresh_update_delete_load(udp_resource, udp_collection)
# End UDP


# Begin WAP
@pytest.fixture
def wap_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.waps.wap.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def wap_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.waps.wap
    yield collection


class TestMonitorWap(object):
    def test_create_refresh_update_delete_load(self, wap_resource, wap_collection):
        create_refresh_update_delete_load(wap_resource, wap_collection)
# End WAP


# Begin WMI
@pytest.fixture
def wmi_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.gtm.monitor.wmis.wmi.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def wmi_collection(mgmt_root):
    collection = mgmt_root.tm.gtm.monitor.wmis.wmi
    yield collection


class TestMonitorWmi(object):
    def test_create_refresh_update_delete_load(self, wmi_resource, wmi_collection):
        create_refresh_update_delete_load(wmi_resource, wmi_collection)
# End WMI
