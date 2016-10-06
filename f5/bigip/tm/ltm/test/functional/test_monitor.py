# Copyright 2015-2106 F5 Networks Inc.
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

from pprint import pprint as pp

TESTDESCRIPTION = "TESTDESCRIPTION"


def setup_basic_test(request, bigip):
    monitor1 = bigip.ltm.monitor
    return monitor1


def delete_resource(resources):
    for resource in resources.get_collection():
        rn = resource.name
        if rn != 'http' and rn != 'http_head_f5' and rn != 'https'\
                and rn != 'https_443' and rn != 'https_head_f5'\
                and rn != 'diameter' and rn != 'dns' and rn != 'external'\
                and rn != 'firepass' and rn != 'ftp' and rn != 'gateway_icmp'\
                and rn != 'icmp' and rn != 'imap' and rn != 'inband'\
                and rn != 'ldap' and rn != 'module_score' and rn != 'mssql'\
                and rn != 'mysql' and rn != 'nntp' and rn != 'none'\
                and rn != 'oracle' and rn != 'pop3' and rn != 'postgresql'\
                and rn != 'radius' and rn != 'radius_accounting'\
                and rn != 'real_server' and rn != 'rpc' and rn != 'sasp'\
                and rn != 'scripted' and rn != 'sip' and rn != 'smb'\
                and rn != 'smtp' and rn != 'snmp_dca'\
                and rn != 'snmp_dca_base' and rn != 'soap'\
                and rn != 'tcp' and rn != 'tcp_echo'\
                and rn != 'tcp_half_open' and rn != 'udp'\
                and rn != 'virtual_location' and rn != 'wap' and rn != 'wmi':
            pp(resource.__dict__)
            resource.delete()


def setup_http_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.https
    pp(hc1._meta_data)
    http1 = hc1.http.create(name=name, partition=partition)
    return http1, hc1


class TestMonitor(object):
    def test_get_collection(self, request, bigip):
        m1 = setup_basic_test(request, bigip)
        list_of_references = m1.get_collection()
        assert len(list_of_references) == 39


class TestMonitorHTTP(object):
    def test_http_create_refresh_update_delete_load(self, request, bigip):
        http1, hc1 = setup_http_test(request, bigip, 'Common', 'test1')
        assert http1.name == 'test1'
        http1.description = TESTDESCRIPTION
        http1.update()
        assert http1.description == TESTDESCRIPTION
        http1.description = ''
        http1.refresh()
        assert http1.description == TESTDESCRIPTION
        http2 = hc1.http.load(partition='Common', name='test1')
        assert http2.selfLink == http1.selfLink


# End HTTP Tests
# Begin HTTPS Tests

def setup_https_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.https_s
    https1 = hc1.https.create(name=name, partition=partition)
    return https1, hc1


class TestMonitorHTTPS(object):
    def test_https_create_refresh_update_delete_load(self, request, bigip):
        https1, hc1 = setup_https_test(request, bigip, 'Common', 'httpstest')
        assert https1.name == 'httpstest'
        https1.description = TESTDESCRIPTION
        https1.update()
        assert https1.description == TESTDESCRIPTION
        https1.description = ''
        https1.refresh()
        assert https1.description == TESTDESCRIPTION
        https2 = hc1.https.load(partition='Common', name='httpstest')
        assert https2.selfLink == https1.selfLink


# End HTTPS Tests
# Begin Diameter Tests

def setup_diameter_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.diameters
    diameter1 = hc1.diameter.create(name=name, partition=partition)
    return diameter1, hc1


class TestMonitorDiameter(object):
    def test_diameter_create_refresh_update_delete_load(self, request, bigip):
        diameter1, hc1 = setup_diameter_test(request, bigip, 'Common',
                                             'diametertest')
        assert diameter1.name == 'diametertest'
        diameter1.description = TESTDESCRIPTION
        diameter1.update()
        assert diameter1.description == TESTDESCRIPTION
        diameter1.description = ''
        diameter1.refresh()
        assert diameter1.description == TESTDESCRIPTION
        diameter2 = hc1.diameter.load(partition='Common', name='diametertest')
        assert diameter2.selfLink == diameter1.selfLink


# End Diameter Tests
# Begin DNS Tests

def setup_dns_test(request, bigip, partition, name, qname):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.dns_s
    dns1 = hc1.dns.create(name=name, partition=partition, qname=qname)
    return dns1, hc1


class TestMonitorDNS(object):
    def test_dns_create_refresh_update_delete_load(self, request, bigip):
        dns1, hc1 = setup_dns_test(request, bigip, 'Common', 'dnstest', 'aqna')
        assert dns1.name == 'dnstest'
        dns1.description = TESTDESCRIPTION
        dns1.update()
        assert dns1.description == TESTDESCRIPTION
        dns1.description = ''
        dns1.refresh()
        assert dns1.description == TESTDESCRIPTION
        dns2 = hc1.dns.load(partition='Common', name='dnstest')
        assert dns2.selfLink == dns1.selfLink


# End DNS Tests
# Begin External

def setup_external_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.externals
    external1 = hc1.external.create(name=name, partition=partition)
    return external1, hc1


class TestMonitorExternal(object):
    def test_external_create_refresh_update_delete_load(self, request, bigip):
        external1, hc1 = setup_external_test(request, bigip, 'Common',
                                             'externaltest')
        assert external1.name == 'externaltest'
        external1.description = TESTDESCRIPTION
        external1.update()
        assert external1.description == TESTDESCRIPTION
        external1.description = ''
        external1.refresh()
        assert external1.description == TESTDESCRIPTION
        external2 = hc1.external.load(partition='Common', name='externaltest')
        assert external2.selfLink == external1.selfLink


# End External Tests
# Begin FirePass

def setup_firepass_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.firepass_s
    firepass1 = hc1.firepass.create(name=name, partition=partition)
    return firepass1, hc1


class TestMonitorFirePass(object):
    def test_firepass_create_refresh_update_delete_load(self, request, bigip):
        firepass1, hc1 = setup_firepass_test(request, bigip, 'Common',
                                             'firepasstest')
        assert firepass1.name == 'firepasstest'
        firepass1.description = TESTDESCRIPTION
        firepass1.update()
        assert firepass1.description == TESTDESCRIPTION
        firepass1.description = ''
        firepass1.refresh()
        assert firepass1.description == TESTDESCRIPTION
        firepass2 = hc1.firepass.load(partition='Common', name='firepasstest')
        assert firepass2.selfLink == firepass1.selfLink


# End FirePass Tests
# Begin FTP Tests

def setup_ftp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.ftps
    ftp1 = hc1.ftp.create(name=name, partition=partition)
    return ftp1, hc1


class TestMonitorFTP(object):
    def test_ftp_create_refresh_update_delete_load(self, request, bigip):
        ftp1, hc1 = setup_ftp_test(request, bigip, 'Common', 'ftptest')
        assert ftp1.name == 'ftptest'
        ftp1.description = TESTDESCRIPTION
        ftp1.update()
        assert ftp1.description == TESTDESCRIPTION
        ftp1.description = ''
        ftp1.refresh()
        assert ftp1.description == TESTDESCRIPTION
        ftp2 = hc1.ftp.load(partition='Common', name='ftptest')
        assert ftp2.selfLink == ftp1.selfLink


# End FTP Tests
# Begin GateWay-ICMP

def setup_gateway_icmp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.gateway_icmps
    gateway_icmp1 = hc1.gateway_icmp.create(name=name, partition=partition)
    return gateway_icmp1, hc1


class TestMonitorGateWay_ICMP(object):
    def test_gateway_icmp_create_refresh_update_delete_load(self,
                                                            request,
                                                            bigip):
        gateway_icmp1, hc1 =\
            setup_gateway_icmp_test(request,
                                    bigip,
                                    'Common',
                                    'gateway_icmptest')
        assert gateway_icmp1.name == 'gateway_icmptest'
        gateway_icmp1.description = TESTDESCRIPTION
        gateway_icmp1.update()
        assert gateway_icmp1.description == TESTDESCRIPTION
        gateway_icmp1.description = ''
        gateway_icmp1.refresh()
        assert gateway_icmp1.description == TESTDESCRIPTION
        gateway_icmp2 = hc1.gateway_icmp.load(
            partition='Common', name='gateway_icmptest')
        assert gateway_icmp2.selfLink == gateway_icmp1.selfLink


# End GateWay-ICMP
# Begin ICMP

def setup_icmp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.icmps
    icmp1 = hc1.icmp.create(name=name, partition=partition)
    return icmp1, hc1


class TestMonitorICMP(object):
    def test_icmp_create_refresh_update_delete_load(self, request, bigip):
        icmp1, hc1 = setup_icmp_test(request, bigip, 'Common', 'icmptest')
        assert icmp1.name == 'icmptest'
        icmp1.description = TESTDESCRIPTION
        icmp1.update()
        assert icmp1.description == TESTDESCRIPTION
        icmp1.description = ''
        icmp1.refresh()
        assert icmp1.description == TESTDESCRIPTION
        icmp2 = hc1.icmp.load(partition='Common', name='icmptest')
        assert icmp2.selfLink == icmp1.selfLink


# End ICMP
# Begin IMAP

def setup_imap_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.imaps
    imap1 = hc1.imap.create(name=name, partition=partition)
    return imap1, hc1


class TestMonitorIMAP(object):
    def test_imap_create_refresh_update_delete_load(self, request, bigip):
        imap1, hc1 = setup_imap_test(request, bigip, 'Common', 'imaptest')
        assert imap1.name == 'imaptest'
        imap1.description = TESTDESCRIPTION
        imap1.update()
        assert imap1.description == TESTDESCRIPTION
        imap1.description = ''
        imap1.refresh()
        assert imap1.description == TESTDESCRIPTION
        imap2 = hc1.imap.load(partition='Common', name='imaptest')
        assert imap2.selfLink == imap1.selfLink


# End IMAP
# Begin InBand

def setup_inband_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.inbands
    inband1 = hc1.inband.create(name=name, partition=partition)
    return inband1, hc1


class TestMonitorInBand(object):
    def test_inband_create_refresh_update_delete_load(self, request, bigip):
        inband1, hc1 =\
            setup_inband_test(request, bigip, 'Common', 'inbandtest')
        assert inband1.name == 'inbandtest'
        inband1.description = TESTDESCRIPTION
        inband1.update()
        assert inband1.description == TESTDESCRIPTION
        inband1.description = ''
        inband1.refresh()
        assert inband1.description == TESTDESCRIPTION
        inband2 = hc1.inband.load(partition='Common', name='inbandtest')
        assert inband2.selfLink == inband1.selfLink


# End InBand
# Begin LDAP

def setup_ldap_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.ldaps
    ldap1 = hc1.ldap.create(name=name, partition=partition)
    return ldap1, hc1


class TestMonitorLDAP(object):
    def test_ldap_create_refresh_update_delete_load(self, request, bigip):
        ldap1, hc1 = setup_ldap_test(request, bigip, 'Common', 'ldaptest')
        assert ldap1.name == 'ldaptest'
        ldap1.description = TESTDESCRIPTION
        ldap1.update()
        assert ldap1.description == TESTDESCRIPTION
        ldap1.description = ''
        ldap1.refresh()
        assert ldap1.description == TESTDESCRIPTION
        ldap2 = hc1.ldap.load(partition='Common', name='ldaptest')
        assert ldap2.selfLink == ldap1.selfLink

# End LDAP Tests
# Begin Module-Score


def setup_module_score_test(request, bigip, partition, name, snmpaddr):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.module_scores
    creation_params = {'name': name,
                       'partition': partition,
                       'snmp-ip-address': snmpaddr}
    module_score1 = hc1.module_score.create(**creation_params)
    return module_score1, hc1


class TestMonitorModule_Score(object):
    def test_module_score_create_refresh_update_delete_load(self, request,
                                                            bigip):
        module_score1, hc1 =\
            setup_module_score_test(request,
                                    bigip,
                                    'Common',
                                    'module_scoretest',
                                    '9.9.9.9')
        assert module_score1.name == 'module_scoretest'
        module_score1.description = TESTDESCRIPTION
        module_score1.update()
        assert module_score1.description == TESTDESCRIPTION
        module_score1.description = ''
        module_score1.refresh()
        assert module_score1.description == TESTDESCRIPTION
        module_score2 = hc1.module_score.load(
            partition='Common', name='module_scoretest')
        assert module_score2.selfLink == module_score1.selfLink


# End Module-Score
# Begin MSSQL

def setup_mssql_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.mssqls
    creation_params = {'name': name,
                       'partition': partition}
    mssql1 = hc1.mssql.create(**creation_params)
    return mssql1, hc1


class TestMonitorMSSQL(object):
    def test_mssql_create_refresh_update_delete_load(self, request, bigip):
        mssql1, hc1 = setup_mssql_test(request, bigip, 'Common', 'mssqltest')
        assert mssql1.name == 'mssqltest'
        mssql1.description = TESTDESCRIPTION
        mssql1.update()
        assert mssql1.description == TESTDESCRIPTION
        mssql1.description = ''
        mssql1.refresh()
        assert mssql1.description == TESTDESCRIPTION
        mssql2 = hc1.mssql.load(partition='Common', name='mssqltest')
        assert mssql2.selfLink == mssql1.selfLink


# End MSSQL
# Begin MYSQL

def setup_mysql_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.mysqls
    creation_params = {'name': name,
                       'partition': partition}
    mysql1 = hc1.mysql.create(**creation_params)
    return mysql1, hc1


class TestMonitorMYSQL(object):
    def test_mysql_create_refresh_update_delete_load(self, request, bigip):
        mysql1, hc1 = setup_mysql_test(request, bigip, 'Common', 'mysqltest')
        assert mysql1.name == 'mysqltest'
        mysql1.description = TESTDESCRIPTION
        mysql1.update()
        assert mysql1.description == TESTDESCRIPTION
        mysql1.description = ''
        mysql1.refresh()
        assert mysql1.description == TESTDESCRIPTION
        mysql2 = hc1.mysql.load(partition='Common', name='mysqltest')
        assert mysql2.selfLink == mysql1.selfLink

# End MYSQL
# Begin NNTP


def setup_nntp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.nntps
    creation_params = {'name': name,
                       'partition': partition}
    nntp1 = hc1.nntp.create(**creation_params)
    return nntp1, hc1


class TestMonitorNNTP(object):
    def test_nntp_create_refresh_update_delete_load(self, request, bigip):
        nntp1, hc1 = setup_nntp_test(request, bigip, 'Common', 'nntptest')
        assert nntp1.name == 'nntptest'
        nntp1.description = TESTDESCRIPTION
        nntp1.update()
        assert nntp1.description == TESTDESCRIPTION
        nntp1.description = ''
        nntp1.refresh()
        assert nntp1.description == TESTDESCRIPTION
        nntp2 = hc1.nntp.load(partition='Common', name='nntptest')
        assert nntp2.selfLink == nntp1.selfLink


# End NNTP
# Begin NONE
'''
def setup_none_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.nones
    none1 = hc1.none
    creation_params = {'name': name,
                       'partition': partition}
    none1.create(**creation_params)
    return none1, hc1


class TestMonitorNONE(object):
    def test_none_create_refresh_update_delete_load(self, request,
                                                            bigip):
        none1, hc1 = setup_none_test(request, bigip, 'Common', 'nonetest')
        assert none1.name == 'nonetest'
        none1.description = TESTDESCRIPTION
        none1.update()
        assert none1.description == TESTDESCRIPTION
        none1.description = ''
        none1.refresh()
        assert none1.description == TESTDESCRIPTION
        none2 = hc1.none
        none2.load(partition='Common', name='nonetest')
        assert none2.selfLink == none1.selfLink

'''
# End NONE
# Begin Oracle


def setup_oracle_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.oracles
    creation_params = {'name': name,
                       'partition': partition}
    oracle1 = hc1.oracle.create(**creation_params)
    return oracle1, hc1


class TestMonitorOracle(object):
    def test_oracle_create_refresh_update_delete_load(self, request, bigip):
        oracle1, hc1 =\
            setup_oracle_test(request, bigip, 'Common', 'oracletest')
        assert oracle1.name == 'oracletest'
        oracle1.description = TESTDESCRIPTION
        oracle1.update()
        assert oracle1.description == TESTDESCRIPTION
        oracle1.description = ''
        oracle1.refresh()
        assert oracle1.description == TESTDESCRIPTION
        oracle2 = hc1.oracle.load(partition='Common', name='oracletest')
        assert oracle2.selfLink == oracle1.selfLink


# End Oracle
# Begin POP3

def setup_pop3_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.pop3s
    creation_params = {'name': name,
                       'partition': partition}
    pop31 = hc1.pop3.create(**creation_params)
    return pop31, hc1


class TestMonitorPOP3(object):
    def test_pop3_create_refresh_update_delete_load(self, request, bigip):
        pop31, hc1 = setup_pop3_test(request, bigip, 'Common', 'pop3test')
        assert pop31.name == 'pop3test'
        pop31.description = TESTDESCRIPTION
        pop31.update()
        assert pop31.description == TESTDESCRIPTION
        pop31.description = ''
        pop31.refresh()
        assert pop31.description == TESTDESCRIPTION
        pop32 = hc1.pop3.load(partition='Common', name='pop3test')
        assert pop32.selfLink == pop31.selfLink


# End POP3
# Begin PostGRESQL

def setup_postgresql_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.postgresqls
    creation_params = {'name': name,
                       'partition': partition}
    postgresql1 = hc1.postgresql.create(**creation_params)
    return postgresql1, hc1


class TestMonitorPostGRESQL(object):
    def test_postgresql_create_refresh_update_delete_load(self, request,
                                                          bigip):
        postgresql1, hc1 =\
            setup_postgresql_test(request, bigip, 'Common', 'postgresqltest')
        assert postgresql1.name == 'postgresqltest'
        postgresql1.description = TESTDESCRIPTION
        postgresql1.update()
        assert postgresql1.description == TESTDESCRIPTION
        postgresql1.description = ''
        postgresql1.refresh()
        assert postgresql1.description == TESTDESCRIPTION
        postgresql2 = hc1.postgresql.load(
            partition='Common', name='postgresqltest')
        assert postgresql2.selfLink == postgresql1.selfLink


# End PostGRESQL
# Begin Radius

def setup_radius_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.radius_s
    creation_params = {'name': name,
                       'partition': partition}
    radius1 = hc1.radius.create(**creation_params)
    return radius1, hc1


class TestMonitorRadius(object):
    def test_radius_create_refresh_update_delete_load(self, request, bigip):
        radius1, hc1 =\
            setup_radius_test(request, bigip, 'Common', 'radiustest')
        assert radius1.name == 'radiustest'
        radius1.description = TESTDESCRIPTION
        radius1.update()
        assert radius1.description == TESTDESCRIPTION
        radius1.description = ''
        radius1.refresh()
        assert radius1.description == TESTDESCRIPTION
        radius2 = hc1.radius.load(partition='Common', name='radiustest')
        assert radius2.selfLink == radius1.selfLink


# End Radius
# Begin Radius_Accounting

def setup_radius_accounting_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.radius_accountings
    creation_params = {'name': name,
                       'partition': partition}
    radius_accounting1 = hc1.radius_accounting.create(**creation_params)
    return radius_accounting1, hc1


class TestMonitorRadius_Accounting(object):
    def test_radius_accounting_create_refresh_update_delete_load(self, request,
                                                                 bigip):
        radius_accounting1, hc1 =\
            setup_radius_accounting_test(request,
                                         bigip,
                                         'Common',
                                         'radius_accountingtest')
        assert radius_accounting1.name == 'radius_accountingtest'
        radius_accounting1.description = TESTDESCRIPTION
        radius_accounting1.update()
        assert radius_accounting1.description == TESTDESCRIPTION
        radius_accounting1.description = ''
        radius_accounting1.refresh()
        assert radius_accounting1.description == TESTDESCRIPTION
        radius_accounting2 = hc1.radius_accounting.load(
            partition='Common',
            name='radius_accountingtest')
        assert radius_accounting2.selfLink == radius_accounting1.selfLink


# End Radius_Accounting
# Begin Real_Server

def setup_real_server_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.real_servers
    creation_params = {'name': name,
                       'partition': partition}
    real_server1 = hc1.real_server.create(**creation_params)
    return real_server1, hc1


class TestMonitorReal_Server(object):
    def test_real_server_create_refresh_update_delete_load(self, request,
                                                           bigip):
        real_server1, hc1 =\
            setup_real_server_test(request, bigip, 'Common', 'real_servertest')
        assert real_server1.name == 'real_servertest'
        real_server1.description = TESTDESCRIPTION
        real_server1.update()
        assert real_server1.description == TESTDESCRIPTION
        real_server1.description = ''
        real_server1.refresh()
        assert real_server1.description == TESTDESCRIPTION
        real_server2 = hc1.real_server.load(
            partition='Common', name='real_servertest')
        assert real_server2.selfLink == real_server1.selfLink


# End Real_Server
# Begin RPC

def setup_rpc_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.rpcs
    creation_params = {'name': name,
                       'partition': partition}
    rpc1 = hc1.rpc.create(**creation_params)
    return rpc1, hc1


class TestMonitorRPC(object):
    def test_rpc_create_refresh_update_delete_load(self, request, bigip):
        rpc1, hc1 = setup_rpc_test(request, bigip, 'Common', 'rpctest')
        assert rpc1.name == 'rpctest'
        rpc1.description = TESTDESCRIPTION
        rpc1.update()
        assert rpc1.description == TESTDESCRIPTION
        rpc1.description = ''
        rpc1.refresh()
        assert rpc1.description == TESTDESCRIPTION
        rpc2 = hc1.rpc.load(partition='Common', name='rpctest')
        assert rpc2.selfLink == rpc1.selfLink


# End RPC
# Begin SASP

def setup_sasp_test(request, bigip, partition, name, primaryAddress='1.1.1.1'):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.sasps
    creation_params = {'name': name,
                       'partition': partition,
                       'primaryAddress': primaryAddress}
    sasp1 = hc1.sasp.create(**creation_params)
    return sasp1, hc1


class TestMonitorSASP(object):
    def test_sasp_create_refresh_update_delete_load(self, request, bigip):
        sasp1, hc1 = setup_sasp_test(request, bigip, 'Common', 'sasptest')
        assert sasp1.name == 'sasptest'
        sasp1.description = TESTDESCRIPTION
        pp(sasp1.__dict__)
        sasp1.update()
        assert sasp1.description == TESTDESCRIPTION
        sasp1.description = ''
        sasp1.refresh()
        assert sasp1.description == TESTDESCRIPTION
        sasp2 = hc1.sasp.load(partition='Common', name='sasptest')
        assert sasp2.selfLink == sasp1.selfLink


# End SASP
# Begin Scripted

def setup_scripted_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.scripteds
    creation_params = {'name': name,
                       'partition': partition}
    scripted1 = hc1.scripted.create(**creation_params)
    return scripted1, hc1


class TestMonitorScripted(object):
    def test_scripted_create_refresh_update_delete_load(self, request, bigip):
        scripted1, hc1 =\
            setup_scripted_test(request, bigip, 'Common', 'scriptedtest')
        assert scripted1.name == 'scriptedtest'
        scripted1.description = TESTDESCRIPTION
        scripted1.update()
        assert scripted1.description == TESTDESCRIPTION
        scripted1.description = ''
        scripted1.refresh()
        assert scripted1.description == TESTDESCRIPTION
        scripted2 = hc1.scripted.load(
            partition='Common', name='scriptedtest')
        assert scripted2.selfLink == scripted1.selfLink


# End Scripted
# Begin SIP

def setup_sip_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.sips
    creation_params = {'name': name,
                       'partition': partition}
    sip1 = hc1.sip.create(**creation_params)
    return sip1, hc1


class TestMonitorSIP(object):
    def test_sip_create_refresh_update_delete_load(self, request, bigip):
        sip1, hc1 = setup_sip_test(request, bigip, 'Common', 'siptest')
        assert sip1.name == 'siptest'
        sip1.description = TESTDESCRIPTION
        sip1.update()
        assert sip1.description == TESTDESCRIPTION
        sip1.description = ''
        sip1.refresh()
        assert sip1.description == TESTDESCRIPTION
        sip2 = hc1.sip.load(partition='Common', name='siptest')
        assert sip2.selfLink == sip1.selfLink


# End SIP
# Begin SMB

def setup_smb_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.smbs
    creation_params = {'name': name,
                       'partition': partition}
    smb1 = hc1.smb.create(**creation_params)
    return smb1, hc1


class TestMonitorSMB(object):
    def test_smb_create_refresh_update_delete_load(self, request, bigip):
        smb1, hc1 = setup_smb_test(request, bigip, 'Common', 'smbtest')
        assert smb1.name == 'smbtest'
        smb1.description = TESTDESCRIPTION
        smb1.update()
        assert smb1.description == TESTDESCRIPTION
        smb1.description = ''
        smb1.refresh()
        assert smb1.description == TESTDESCRIPTION
        smb2 = hc1.smb.load(partition='Common', name='smbtest')
        assert smb2.selfLink == smb1.selfLink


# End SMB
# Begin SMTP

def setup_smtp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.smtps
    creation_params = {'name': name,
                       'partition': partition}
    smtp1 = hc1.smtp.create(**creation_params)
    return smtp1, hc1


class TestMonitorSMTP(object):
    def test_smtp_create_refresh_update_delete_load(self, request, bigip):
        smtp1, hc1 = setup_smtp_test(request, bigip, 'Common', 'smtptest')
        assert smtp1.name == 'smtptest'
        smtp1.description = TESTDESCRIPTION
        smtp1.update()
        assert smtp1.description == TESTDESCRIPTION
        smtp1.description = ''
        smtp1.refresh()
        assert smtp1.description == TESTDESCRIPTION
        smtp2 = hc1.smtp.load(partition='Common', name='smtptest')
        assert smtp2.selfLink == smtp1.selfLink


# End SMTP
# Begin SNMP_DCA

def setup_snmp_dca_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.snmp_dcas
    creation_params = {'name': name,
                       'partition': partition}
    snmp_dca1 = hc1.snmp_dca.create(**creation_params)
    return snmp_dca1, hc1


class TestMonitorSNMP_DCA(object):
    def test_snmp_dca_create_refresh_update_delete_load(self, request, bigip):
        snmp_dca1, hc1 =\
            setup_snmp_dca_test(request, bigip, 'Common', 'snmp_dcatest')
        assert snmp_dca1.name == 'snmp_dcatest'
        snmp_dca1.description = TESTDESCRIPTION
        snmp_dca1.update()
        assert snmp_dca1.description == TESTDESCRIPTION
        snmp_dca1.description = ''
        snmp_dca1.refresh()
        assert snmp_dca1.description == TESTDESCRIPTION
        snmp_dca2 = hc1.snmp_dca.load(partition='Common', name='snmp_dcatest')
        assert snmp_dca2.selfLink == snmp_dca1.selfLink


# End SNMP_DCA
# Begin SNMP_DCA_Base

def setup_snmp_dca_base_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.snmp_dca_bases
    creation_params = {'name': name,
                       'partition': partition}
    snmp_dca_base1 = hc1.snmp_dca_base.create(**creation_params)
    return snmp_dca_base1, hc1


class TestMonitorSNMP_DCA_Base(object):
    def test_snmp_dca_base_create_refresh_update_delete_load(self, request,
                                                             bigip):
        snmp_dca_base1, hc1 =\
            setup_snmp_dca_base_test(request,
                                     bigip,
                                     'Common',
                                     'snmp_dca_basetest')
        assert snmp_dca_base1.name == 'snmp_dca_basetest'
        snmp_dca_base1.description = TESTDESCRIPTION
        snmp_dca_base1.update()
        assert snmp_dca_base1.description == TESTDESCRIPTION
        snmp_dca_base1.description = ''
        snmp_dca_base1.refresh()
        assert snmp_dca_base1.description == TESTDESCRIPTION
        snmp_dca_base2 = hc1.snmp_dca_base.load(
            partition='Common', name='snmp_dca_basetest'
        )
        assert snmp_dca_base2.selfLink == snmp_dca_base1.selfLink


# End SNMP_DCA_Base
# Begin SOAP

def setup_soap_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.soaps
    creation_params = {'name': name,
                       'partition': partition}
    soap1 = hc1.soap.create(**creation_params)
    return soap1, hc1


class TestMonitorSOAP(object):
    def test_soap_create_refresh_update_delete_load(self, request, bigip):
        soap1, hc1 = setup_soap_test(request, bigip, 'Common', 'soaptest')
        assert soap1.name == 'soaptest'
        soap1.description = TESTDESCRIPTION
        soap1.update()
        assert soap1.description == TESTDESCRIPTION
        soap1.description = ''
        soap1.refresh()
        assert soap1.description == TESTDESCRIPTION
        soap2 = hc1.soap.load(partition='Common', name='soaptest')
        assert soap2.selfLink == soap1.selfLink


# End SOAP
# Begin TCP

def setup_tcp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.tcps
    creation_params = {'name': name,
                       'partition': partition}
    tcp1 = hc1.tcp.create(**creation_params)
    return tcp1, hc1


class TestMonitorTCP(object):
    def test_tcp_create_refresh_update_delete_load(self, request, bigip):
        tcp1, hc1 = setup_tcp_test(request, bigip, 'Common', 'tcptest')
        assert tcp1.name == 'tcptest'
        tcp1.description = TESTDESCRIPTION
        tcp1.update()
        assert tcp1.description == TESTDESCRIPTION
        tcp1.description = ''
        tcp1.refresh()
        assert tcp1.description == TESTDESCRIPTION
        tcp2 = hc1.tcp.load(partition='Common', name='tcptest')
        assert tcp2.selfLink == tcp1.selfLink


# End TCP
# Begin TCP_Echo

def setup_tcp_echo_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.tcp_echos
    creation_params = {'name': name,
                       'partition': partition}
    tcp_echo1 = hc1.tcp_echo.create(**creation_params)
    return tcp_echo1, hc1


class TestMonitorTCP_Echo(object):
    def test_tcp_echo_create_refresh_update_delete_load(self, request, bigip):
        tcp_echo1, hc1 =\
            setup_tcp_echo_test(request, bigip, 'Common', 'tcp_echotest')
        assert tcp_echo1.name == 'tcp_echotest'
        tcp_echo1.description = TESTDESCRIPTION
        tcp_echo1.update()
        assert tcp_echo1.description == TESTDESCRIPTION
        tcp_echo1.description = ''
        tcp_echo1.refresh()
        assert tcp_echo1.description == TESTDESCRIPTION
        tcp_echo2 = hc1.tcp_echo.load(partition='Common', name='tcp_echotest')
        assert tcp_echo2.selfLink == tcp_echo1.selfLink


# End TCP_Echo
# Begin TCP_Half_Open

def setup_tcp_half_open_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.tcp_half_opens
    creation_params = {'name': name,
                       'partition': partition}
    tcp_half_open1 = hc1.tcp_half_open.create(**creation_params)
    return tcp_half_open1, hc1


class TestMonitorTCP_Half_Open(object):
    def test_tcp_half_open_create_refresh_update_delete_load(self, request,
                                                             bigip):
        tcp_half_open1, hc1 =\
            setup_tcp_half_open_test(request,
                                     bigip,
                                     'Common',
                                     'tcp_half_opentest')
        assert tcp_half_open1.name == 'tcp_half_opentest'
        tcp_half_open1.description = TESTDESCRIPTION
        tcp_half_open1.update()
        assert tcp_half_open1.description == TESTDESCRIPTION
        tcp_half_open1.description = ''
        tcp_half_open1.refresh()
        assert tcp_half_open1.description == TESTDESCRIPTION
        tcp_half_open2 = hc1.tcp_half_open.load(
            partition='Common', name='tcp_half_opentest')
        assert tcp_half_open2.selfLink == tcp_half_open1.selfLink


# End TCP_Half_Open
# Begin UDP

def setup_udp_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.udps
    creation_params = {'name': name,
                       'partition': partition}
    udp1 = hc1.udp.create(**creation_params)
    return udp1, hc1


class TestMonitorUDP(object):
    def test_udp_create_refresh_update_delete_load(self, request, bigip):
        udp1, hc1 = setup_udp_test(request, bigip, 'Common', 'udptest')
        assert udp1.name == 'udptest'
        udp1.description = TESTDESCRIPTION
        udp1.update()
        assert udp1.description == TESTDESCRIPTION
        udp1.description = ''
        udp1.refresh()
        assert udp1.description == TESTDESCRIPTION
        udp2 = hc1.udp.load(partition='Common', name='udptest')
        assert udp2.selfLink == udp1.selfLink


# End UDP
# Begin Virtual_Location

def setup_virtual_location_test(request, bigip, partition, name, pool='tp1'):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.virtual_locations
    creation_params = {'name': name,
                       'partition': partition,
                       'pool': pool}
    virtual_location1 = hc1.virtual_location.create(**creation_params)
    return virtual_location1, hc1


class TestMonitorVirtual_Location(object):
    def test_virtual_location_create_refresh_update_delete_load(self, request,
                                                                bigip):
        virtual_location1, hc1 =\
            setup_virtual_location_test(request,
                                        bigip,
                                        'Common',
                                        'virtual_locationtest')
        assert virtual_location1.name == 'virtual_locationtest'
        virtual_location1.description = TESTDESCRIPTION
        virtual_location1.update()
        assert virtual_location1.description == TESTDESCRIPTION
        virtual_location1.description = ''
        virtual_location1.refresh()
        assert virtual_location1.description == TESTDESCRIPTION
        virtual_location2 = hc1.virtual_location.load(
            partition='Common', name='virtual_locationtest'
        )
        assert virtual_location2.selfLink == virtual_location1.selfLink


# End Virtual_Location
# Begin WAP

def setup_wap_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.waps
    creation_params = {'name': name,
                       'partition': partition}
    wap1 = hc1.wap.create(**creation_params)
    return wap1, hc1


class TestMonitorWAP(object):
    def test_wap_create_refresh_update_delete_load(self, request, bigip):
        wap1, hc1 = setup_wap_test(request, bigip, 'Common', 'waptest')
        assert wap1.name == 'waptest'
        wap1.description = TESTDESCRIPTION
        wap1.update()
        assert wap1.description == TESTDESCRIPTION
        wap1.description = ''
        wap1.refresh()
        assert wap1.description == TESTDESCRIPTION
        wap2 = hc1.wap.load(partition='Common', name='waptest')
        assert wap2.selfLink == wap1.selfLink


# End WAP
# Begin WMI

def setup_wmi_test(request, bigip, partition, name):
    def teardown():
        delete_resource(hc1)
    request.addfinalizer(teardown)
    hc1 = bigip.ltm.monitor.wmis
    creation_params = {'name': name,
                       'partition': partition}
    wmi1 = hc1.wmi.create(**creation_params)
    return wmi1, hc1


class TestMonitorWMI(object):
    def test_wmi_create_refresh_update_delete_load(self, request, bigip):
        wmi1, hc1 = setup_wmi_test(request, bigip, 'Common', 'wmitest')
        assert wmi1.name == 'wmitest'
        wmi1.description = TESTDESCRIPTION
        wmi1.update()
        assert wmi1.description == TESTDESCRIPTION
        wmi1.description = ''
        wmi1.refresh()
        assert wmi1.description == TESTDESCRIPTION
        wmi2 = hc1.wmi.load(partition='Common', name='wmitest')
        assert wmi2.selfLink == wmi1.selfLink
