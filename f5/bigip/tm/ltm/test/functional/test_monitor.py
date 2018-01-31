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

import os
import pytest
import tempfile

from distutils.version import LooseVersion

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


@pytest.fixture(
    scope="module",
    params=[
        ('https', 'http'),
        ('diameters', 'diameter'),
        ('externals', 'external'),
        ('firepass_s', 'firepass'),
        ('ftps', 'ftp'),
        ('gateway_icmps', 'gateway_icmp'),
        ('icmps', 'icmp'),
        ('imaps', 'imap'),
        ('inbands', 'inband'),
        ('ldaps', 'ldap'),
        pytest.param(
            ('mqtts', 'mqtt'),
            marks=pytest.mark.skipif(
                LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
                reason='This class only works on version 13.1.0 or newer'
            )
        ),
        ('mssqls', 'mssql'),
        ('mysqls', 'mysql'),
        ('nntps', 'nntp'),
        ('oracles', 'oracle'),
        ('pop3s', 'pop3'),
        ('postgresqls', 'postgresql'),
        ('radius_s', 'radius'),
        ('radius_accountings', 'radius_accounting'),
        ('real_servers', 'real_server'),
        ('rpcs', 'rpc'),
        ('scripteds', 'scripted'),
        ('sips', 'sip'),
        ('smbs', 'smb'),
        ('smtps', 'smtp'),
        ('snmp_dcas', 'snmp_dca'),
        ('snmp_dca_bases', 'snmp_dca_base'),
        ('soaps', 'soap'),
        ('tcps', 'tcp'),
        ('tcp_echos', 'tcp_echo'),
        ('tcp_half_opens', 'tcp_half_open'),
        ('udps', 'udp'),
        ('waps', 'wap'),
        ('wmis', 'wmi')
    ],
    ids=[
        'HTTP',
        'Diameter',
        'External',
        'Firepass',
        'FTP',
        'Gateway ICMP',
        'ICMP',
        'IMAP',
        'Inband',
        'LDAP',
        'MQTT',
        'MSSQL',
        'MySQL',
        'NNTP',
        'Oracle',
        'POP3',
        'PostgreSQL',
        'RADIUS',
        'RADIUS Accounting',
        'Real Server',
        'RPC',
        'Scripted',
        'SIP',
        'SMB',
        'SMTP',
        'SNMP DCA',
        'SNMP DCA Base',
        'SOAP',
        'TCP',
        'TCP Echo',
        'TCP Half Open',
        'UDP',
        'WAP',
        'WMI'
    ]
)
def crud_operations(request, mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)

    organizing = getattr(mgmt_root.tm.ltm.monitor, request.param[0])
    collection = getattr(organizing, request.param[1])
    resource = collection.create(
        name=name, partition='Common'
    )
    yield resource, collection
    resource.delete()


def test_create_refresh_update_delete_load(crud_operations):
    create_refresh_update_delete_load(crud_operations[0], crud_operations[1])


# Begin general collection tests
@pytest.fixture
def monitors_oc(mgmt_root):
    monitor1 = mgmt_root.tm.ltm.monitor
    return monitor1


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.1.0'),
    reason='This class only works on version 13.1.0 or older'
)
class TestMonitor(object):
    def test_get_collection(self, monitors_oc):
        list_of_references = monitors_oc.get_collection()
        assert len(list_of_references) == 39


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='This class only works on version 13.1.0 or newer'
)
class TestMonitorPostV13_1_0(object):
    def test_get_collection(self, monitors_oc):
        """Tests the number of endpoints in the monitor OrganizingClass

        In 13.1.0 the MQTT endpoint was added, bringing the total to 40
        """
        list_of_references = monitors_oc.get_collection()
        assert len(list_of_references) == 40
# End general collection tests


# Begin Pre 13.1.0 HTTPS Tests
@pytest.fixture
def https_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.ltm.monitor.https_s.https.create(
        name=temp_name, partition='Common'
    )
    yield resource
    resource.delete()


@pytest.fixture
def https_collection(mgmt_root):
    collection = mgmt_root.tm.ltm.monitor.https_s.https
    yield collection


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.1.0'),
    reason='This class only works on version 13.1.0 or older'
)
class TestMonitorHttps(object):
    def test_create_refresh_update_delete_load(self, https_resource, https_collection):
        create_refresh_update_delete_load(https_resource, https_collection)
# End Pre 13.1.0 HTTPS Tests


# Begin Post 13.1.0HTTPS Tests
@pytest.fixture
def https_resource2(mgmt_root, temp_name):
    resource = mgmt_root.tm.ltm.monitor.https_s.https.create(
        name=temp_name, partition='Common', compatibility='disabled'
    )
    yield resource
    resource.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='This class only works on version 13.1.0 or newer'
)
class TestMonitorHttps2(object):
    def test_create_refresh_update_delete_load(self, https_resource2, https_collection):
        create_refresh_update_delete_load(https_resource2, https_collection)
# End HTTPS Tests


# Begin DNS Tests
@pytest.fixture
def dns_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.ltm.monitor.dns_s.dns.create(
        name=temp_name, partition='Common', qname='aqna'
    )
    yield resource
    resource.delete()


@pytest.fixture
def dns_collection(mgmt_root):
    collection = mgmt_root.tm.ltm.monitor.dns_s.dns
    yield collection


class TestMonitorDns(object):
    def test_create_refresh_update_delete_load(self, dns_resource, dns_collection):
        create_refresh_update_delete_load(dns_resource, dns_collection)
# End DNS Tests


# Begin Module-Score
@pytest.fixture
def module_score_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.ltm.monitor.module_scores.module_score.create(
        name=temp_name, partition='Common', snmpIpAddress='9.9.9.9'
    )
    yield resource
    resource.delete()


@pytest.fixture
def module_score_collection(mgmt_root):
    collection = mgmt_root.tm.ltm.monitor.module_scores.module_score
    yield collection


class TestMonitorModuleScore(object):
    def test_create_refresh_update_delete_load(self, module_score_resource, module_score_collection):
        create_refresh_update_delete_load(module_score_resource, module_score_collection)
# End Module-Score


# Begin SASP
@pytest.fixture
def sasp_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.ltm.monitor.sasps.sasp.create(
        name=temp_name, partition='Common', primaryAddress='10.10.10.10'
    )
    yield resource
    resource.delete()


@pytest.fixture
def sasp_collection(mgmt_root):
    collection = mgmt_root.tm.ltm.monitor.sasps.sasp
    yield collection


class TestMonitorSasp(object):
    def test_create_refresh_update_delete_load(self, sasp_resource, sasp_collection):
        create_refresh_update_delete_load(sasp_resource, sasp_collection)
# End Virtual_Location


# Begin Virtual_Location
@pytest.fixture
def virtual_location_resource(mgmt_root, temp_name):
    resource = mgmt_root.tm.ltm.monitor.virtual_locations.virtual_location.create(
        name=temp_name, partition='Common', pool='tp1'
    )
    yield resource
    resource.delete()


@pytest.fixture
def virtual_location_collection(mgmt_root):
    collection = mgmt_root.tm.ltm.monitor.virtual_locations.virtual_location
    yield collection


class TestMonitorVirtualLocation(object):
    def test_create_refresh_update_delete_load(self, virtual_location_resource, virtual_location_collection):
        create_refresh_update_delete_load(virtual_location_resource, virtual_location_collection)
# End Virtual_Location
