# Copyright 2017 F5 Networks Inc.
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

import pytest

# from distutils.version import LooseVersion
from f5.sdk_exception import MissingRequiredCreationParameter
from requests import HTTPError


def delete_filter(mgmt_root, name, partition):
    try:
        f = mgmt_root.tm.sys.log_config.filters.filter.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    f.delete()


def setup_create_filter_test(request, mgmt_root, name, partition):
    def teardown():
        delete_filter(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_filter_test(request, mgmt_root, name, partition):
    def teardown():
        delete_filter(mgmt_root, name, partition)

    filter1 = mgmt_root.tm.sys.log_config.filters.filter.create(
        name=name, partition=partition, publisher='local-db-publisher')
    request.addfinalizer(teardown)
    return filter1


class TestFilters(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.filters.filter.create()

    def test_create_no_publisher(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.filters.filter.create(name='logfilt1')

    def test_create_filter(self, request, mgmt_root):
        setup_create_filter_test(request, mgmt_root, 'filter1', 'Common')
        # Test create
        filter1 = mgmt_root.tm.sys.log_config.filters.filter.create(name='filter1', partition='Common', publisher='local-db-publisher')
        assert filter1.name == 'filter1'
        assert filter1.partition == 'Common'
        assert 'local-db-publisher' in filter1.publisher

        filter2 = mgmt_root.tm.sys.log_config.filters.filter.load(name='filter1')
        assert filter1.publisher == filter2.publisher

        # Test update
        filter1.publisher = 'sys-db-access-publisher'
        filter1.update()
        assert filter1.publisher != filter2.publisher

        # Test refresh
        filter2.refresh()
        assert filter1.publisher == filter2.publisher

        # Test delete
        filter1.delete()
        assert mgmt_root.tm.sys.log_config.filters.filter.exists(name='filter1') is False


def delete_publisher(mgmt_root, name, partition):
    try:
        p = mgmt_root.tm.sys.log_config.publishers.publisher.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_create_publisher_test(request, mgmt_root, name, partition):
    def teardown():
        delete_publisher(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_publisher_test(request, mgmt_root, name, partition):
    def teardown():
        delete_publisher(mgmt_root, name, partition)

    pub1 = mgmt_root.tm.sys.log_config.publishers.publisher.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return pub1


class TestPublishers(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.publishers.publisher.create()

    def test_create_publisher(self, request, mgmt_root):
        setup_create_filter_test(request, mgmt_root, 'pub1', 'Common')
        # Test create
        pub1 = mgmt_root.tm.sys.log_config.publishers.publisher.create(name='pub1', partition='Common')
        assert pub1.name == 'pub1'
        assert pub1.partition == 'Common'

        pub2 = mgmt_root.tm.sys.log_config.publishers.publisher.load(name='pub1')
        assert pub1.name == pub2.name

        # Test update
        pub1.destinations = [{'name': 'local-syslog'}]
        pub1.update()
        assert pub1.destinations == [{'name': 'local-syslog', 'partition': 'Common'}]
        assert hasattr(pub1, 'destinations') is True
        assert hasattr(pub2, 'destinations') is False

        # Test refresh
        pub2.refresh()
        assert hasattr(pub2, 'destinations') is True
        assert pub1.destinations == pub2.destinations

        # Test delete
        pub1.delete()
        assert mgmt_root.tm.sys.log_config.publishers.publisher.exists(name='pub1') is False


def setup_alertd_test(request, mgmt_root):
    def teardown():
        a.description = ''
        a.update()
    request.addfinalizer(teardown)
    a = mgmt_root.tm.sys.log_config.destination.alertds.alertd.load(name='alertd')
    return a


class TestDestinationAlertd(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        dest2 = mgmt_root.tm.sys.log_config.destination.alertds.alertd.load(name='alertd')
        dest1 = setup_alertd_test(request, mgmt_root)

        # Update
        dest1.description = "desc"
        dest1.update()

        assert 'desc' in dest1.description
        assert hasattr(dest2, 'description') is False

        # Refresh
        dest2.refresh()
        assert 'desc' in dest2.description
        assert dest1.description == dest2.description


def setup_localdb_test(request, mgmt_root):
    def teardown():
        a.description = ''
        a.update()
    request.addfinalizer(teardown)
    a = mgmt_root.tm.sys.log_config.destination.local_databases.local_database.load(name='local-db')
    return a


class TestDestinationLocalDb(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        dest2 = mgmt_root.tm.sys.log_config.destination.local_databases.local_database.load(name='local-db')
        dest1 = setup_localdb_test(request, mgmt_root)

        # Update
        dest1.description = "desc"
        dest1.update()

        assert 'desc' in dest1.description
        assert hasattr(dest2, 'description') is False

        # Refresh
        dest2.refresh()
        assert 'desc' in dest2.description
        assert dest1.description == dest2.description


def setup_localsyslog_test(request, mgmt_root):
    def teardown():
        a.description = ''
        a.update()
    request.addfinalizer(teardown)
    a = mgmt_root.tm.sys.log_config.destination.local_syslogs.local_syslog.load(name='local-syslog')
    return a


class TestDestinationLocalSyslog(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        dest2 = mgmt_root.tm.sys.log_config.destination.local_syslogs.local_syslog.load(name='local-syslog')
        dest1 = setup_localsyslog_test(request, mgmt_root)

        # Update
        dest1.description = "desc"
        dest1.update()

        assert 'desc' in dest1.description
        assert hasattr(dest2, 'description') is False

        # Refresh
        dest2.refresh()
        assert 'desc' in dest2.description
        assert dest1.description == dest2.description


def delete_arcsight(mgmt_root, name, partition):
    try:
        a = mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    a.delete()


def setup_create_arcsight_test(request, mgmt_root, name, partition):
    def teardown():
        delete_arcsight(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_arcsight_test(request, mgmt_root, name, partition):
    def teardown():
        delete_arcsight(mgmt_root, name, partition)

    dest1 = mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.create(
        name=name, partition=partition, forwardTo='alertd')
    request.addfinalizer(teardown)
    return dest1


class TestDestinationArcsight(object):
    def test_create_arcsight_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.create()

    def test_create_arcsight_no_forwardto(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.create(name='logdest-arcsight')

    def test_create_arcsight(self, request, mgmt_root):
        setup_create_arcsight_test(request, mgmt_root, 'logdest-arcsight', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.create(name='logdest-arcsight', partition='Common', forwardTo='alertd')
        assert dest1.name == 'logdest-arcsight'
        assert 'alertd' in dest1.forwardTo

    def test_load_update_refresh_arcsight(self, request, mgmt_root):
        setup_basic_arcsight_test(request, mgmt_root, 'logdest-arcsight', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.load(name='logdest-arcsight')
        dest2 = mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.load(name='logdest-arcsight')
        assert dest1.forwardTo == dest2.forwardTo

        dest1.forwardTo = 'local-db'
        dest1.update()
        assert dest1.forwardTo != dest2.forwardTo

        dest2.refresh()
        assert dest1.forwardTo == dest2.forwardTo

    def test_delete_arcsight(self, request, mgmt_root):
        setup_basic_arcsight_test(request, mgmt_root, 'logdest-arcsight', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.load(name='logdest-arcsight')
        dest1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.sys.log_config.destination.arcsights.arcsight.load(name='logdest-arcsight')
        assert err.value.response.status_code == 404


def delete_mgmtport(mgmt_root, name, partition):
    try:
        a = mgmt_root.tm.sys.log_config.destination.management_ports.management_port.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    a.delete()


def setup_create_mgmtport_test(request, mgmt_root, name, partition):
    def teardown():
        delete_mgmtport(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_mgmtport_test(request, mgmt_root, name, partition, address, port):
    def teardown():
        delete_mgmtport(mgmt_root, name, partition)

    dest1 = mgmt_root.tm.sys.log_config.destination.management_ports.management_port.create(
        name=name, partition=partition, ipAddress=address, port=port)
    request.addfinalizer(teardown)
    return dest1


class TestDestinationMgmtPort(object):
    def test_create_mgmtport_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.management_ports.management_port.create()

    def test_create_mgmtport_no_ipaddress(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.management_ports.management_port.create(name='logdest-mgmtport', port=80)

    def test_create_mgmtport_no_port(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.management_ports.management_port.create(name='logdest-mgmtport', ipAddress='192.168.1.100')

    def test_create_mgmtport(self, request, mgmt_root):
        setup_create_mgmtport_test(request, mgmt_root, 'logdest-mgmtport', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.management_ports.management_port.create(name='logdest-mgmtport', ipAddress='192.168.1.100', port=80)
        assert dest1.name == 'logdest-mgmtport'
        assert '192.168.1.100' in dest1.ipAddress
        assert dest1.port is 80

    def test_load_update_refresh_mgmtport(self, request, mgmt_root):
        setup_basic_mgmtport_test(request, mgmt_root, 'logdest-mgmtport', 'Common', '192.168.1.100', 80)
        dest1 = mgmt_root.tm.sys.log_config.destination.management_ports.management_port.load(name='logdest-mgmtport')
        dest2 = mgmt_root.tm.sys.log_config.destination.management_ports.management_port.load(name='logdest-mgmtport')
        assert dest1.port == dest2.port

        dest1.port = 8080
        dest1.update()
        assert dest1.port != dest2.port

        dest2.refresh()
        assert dest1.port == dest2.port

    def test_delete_mgmtport(self, request, mgmt_root):
        setup_basic_mgmtport_test(request, mgmt_root, 'logdest-mgmtport', 'Common', '192.168.1.100', 80)
        dest1 = mgmt_root.tm.sys.log_config.destination.management_ports.management_port.load(name='logdest-mgmtport')
        dest1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.sys.log_config.destination.management_ports.management_port.load(name='logdest-mgmtport')
        assert err.value.response.status_code == 404


def delete_splunk(mgmt_root, name, partition):
    try:
        a = mgmt_root.tm.sys.log_config.destination.splunks.splunk.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    a.delete()


def setup_create_splunk_test(request, mgmt_root, name, partition):
    def teardown():
        delete_splunk(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_splunk_test(request, mgmt_root, name, partition):
    def teardown():
        delete_splunk(mgmt_root, name, partition)

    dest1 = mgmt_root.tm.sys.log_config.destination.splunks.splunk.create(
        name=name, partition=partition, forwardTo='alertd')
    request.addfinalizer(teardown)
    return dest1


class TestDestinationSplunk(object):
    def test_create_splunk_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.splunks.splunk.create()

    def test_create_splunk_no_forwardto(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.splunks.splunk.create(name='logdest-splunk')

    def test_create_splunk(self, request, mgmt_root):
        setup_create_splunk_test(request, mgmt_root, 'logdest-splunk', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.splunks.splunk.create(name='logdest-splunk', partition='Common', forwardTo='alertd')
        assert dest1.name == 'logdest-splunk'
        assert 'alertd' in dest1.forwardTo

    def test_load_update_refresh_splunk(self, request, mgmt_root):
        setup_basic_splunk_test(request, mgmt_root, 'logdest-splunk', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.splunks.splunk.load(name='logdest-splunk')
        dest2 = mgmt_root.tm.sys.log_config.destination.splunks.splunk.load(name='logdest-splunk')
        assert dest1.forwardTo == dest2.forwardTo

        dest1.forwardTo = 'local-db'
        dest1.update()
        assert dest1.forwardTo != dest2.forwardTo

        dest2.refresh()
        assert dest1.forwardTo == dest2.forwardTo

    def test_delete_splunk(self, request, mgmt_root):
        setup_basic_splunk_test(request, mgmt_root, 'logdest-splunk', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.splunks.splunk.load(name='logdest-splunk')
        dest1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.sys.log_config.destination.splunks.splunk.load(name='logdest-splunk')
        assert err.value.response.status_code == 404


@pytest.fixture
def basic_pool(mgmt_root):
    pool1 = mgmt_root.tm.ltm.pools.pool.create(name='logdest-pool', partition='Common')
    yield pool1
    pool1.delete()


def delete_ipfix(mgmt_root, name, partition):
    try:
        a = mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    a.delete()


def setup_create_ipfix_test(request, mgmt_root, name, partition):
    def teardown():
        delete_ipfix(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_ipfix_test(request, mgmt_root, name, partition, pool):
    def teardown():
        delete_ipfix(mgmt_root, name, partition)

    dest1 = mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.create(
        name=name, partition=partition, poolName=pool)
    request.addfinalizer(teardown)
    return dest1


class TestDestinationIpfix(object):
    def test_create_ipfix_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.create()

    def test_create_ipfix_no_poolname(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.create(name='logdest-ipfix')

    def test_create_ipfix(self, request, mgmt_root, basic_pool):
        setup_create_ipfix_test(request, mgmt_root, 'logdest-ipfix', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.create(name='logdest-ipfix', partition='Common', poolName=basic_pool.name)
        assert dest1.name == 'logdest-ipfix'
        assert 'logdest-pool' in dest1.poolName

    def test_load_update_refresh_ipfix(self, request, mgmt_root, basic_pool):
        setup_basic_ipfix_test(request, mgmt_root, 'logdest-ipfix', 'Common', basic_pool.name)
        dest1 = mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.load(name='logdest-ipfix')
        dest2 = mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.load(name='logdest-ipfix')
        assert dest1.poolName == dest2.poolName
        assert 'udp' in dest1.transportProfile

        dest1.transportProfile = 'tcp'
        dest1.update()
        assert dest1.transportProfile != dest2.transportProfile

        dest2.refresh()
        assert dest1.transportProfile == dest2.transportProfile

    def test_delete_ipfix(self, request, mgmt_root, basic_pool):
        setup_basic_ipfix_test(request, mgmt_root, 'logdest-ipfix', 'Common', basic_pool.name)
        dest1 = mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.load(name='logdest-ipfix')
        dest1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.sys.log_config.destination.ipfixs.ipfix.load(name='logdest-ipfix')
        assert err.value.response.status_code == 404


def delete_remote_high_speed_log(mgmt_root, name, partition):
    try:
        a = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    a.delete()


def setup_create_remote_high_speed_log_test(request, mgmt_root, name, partition):
    def teardown():
        delete_remote_high_speed_log(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_remote_high_speed_log_test(request, mgmt_root, name, partition, pool):
    def teardown():
        delete_remote_high_speed_log(mgmt_root, name, partition)

    dest1 = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.create(
        name=name, partition=partition, poolName=pool)
    request.addfinalizer(teardown)
    return dest1


class TestDestinationRemoteHighSpeedLog(object):
    def test_create_remote_high_speed_log_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.create()

    def test_create_remote_high_speed_log_no_poolname(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.create(name='logdest-remote_high_speed_log')

    def test_create_remote_high_speed_log(self, request, mgmt_root, basic_pool):
        setup_create_remote_high_speed_log_test(request, mgmt_root, 'logdest-remote_high_speed_log', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.create(name='logdest-remote_high_speed_log',
                                                                                                            partition='Common', poolName=basic_pool.name)
        assert dest1.name == 'logdest-remote_high_speed_log'
        assert 'logdest-pool' in dest1.poolName

    def test_load_update_refresh_remote_high_speed_log(self, request, mgmt_root, basic_pool):
        setup_basic_remote_high_speed_log_test(request, mgmt_root, 'logdest-remote_high_speed_log', 'Common', basic_pool.name)
        dest1 = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.load(name='logdest-remote_high_speed_log')
        dest2 = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.load(name='logdest-remote_high_speed_log')
        assert dest1.poolName == dest2.poolName
        assert 'tcp' in dest1.protocol

        dest1.protocol = 'udp'
        dest1.update()
        assert dest1.protocol != dest2.protocol

        dest2.refresh()
        assert dest1.protocol == dest2.protocol

    def test_delete_remote_high_speed_log(self, request, mgmt_root, basic_pool):
        setup_basic_remote_high_speed_log_test(request, mgmt_root, 'logdest-remote_high_speed_log', 'Common', basic_pool.name)
        dest1 = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.load(name='logdest-remote_high_speed_log')
        dest1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.load(name='logdest-remote_high_speed_log')
        assert err.value.response.status_code == 404


@pytest.fixture
def basic_dest(mgmt_root, basic_pool):
    ld1 = mgmt_root.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log.create(name='logdest-empty', partition='Common',
                                                                                                      poolName=basic_pool.name)
    yield ld1
    ld1.delete()


def delete_remote_syslog(mgmt_root, name, partition):
    try:
        a = mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    a.delete()


def setup_create_remote_syslog_test(request, mgmt_root, name, partition):
    def teardown():
        delete_remote_syslog(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_remote_syslog_test(request, mgmt_root, name, partition, dest):
    def teardown():
        delete_remote_syslog(mgmt_root, name, partition)

    dest1 = mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.create(
        name=name, partition=partition, remoteHighSpeedLog=dest)
    request.addfinalizer(teardown)
    return dest1


class TestDestinationRemoteSyslog(object):
    def test_create_remote_syslog_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.create()

    def test_create_remote_syslog_no_poolname(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.create(name='logdest-remote_syslog')

    def test_create_remote_syslog(self, request, mgmt_root, basic_dest):
        setup_create_remote_syslog_test(request, mgmt_root, 'logdest-remote_syslog', 'Common')
        dest1 = mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.create(name='logdest-remote_syslog', partition='Common',
                                                                                            remoteHighSpeedLog=basic_dest.name)
        assert dest1.name == 'logdest-remote_syslog'
        assert 'logdest-empty' in dest1.remoteHighSpeedLog

    def test_load_update_refresh_remote_syslog(self, request, mgmt_root, basic_dest):
        setup_basic_remote_syslog_test(request, mgmt_root, 'logdest-remote_syslog', 'Common', basic_dest.name)
        dest1 = mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.load(name='logdest-remote_syslog')
        dest2 = mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.load(name='logdest-remote_syslog')
        assert dest1.remoteHighSpeedLog == dest2.remoteHighSpeedLog
        assert 'rfc3164' in dest1.format

        dest1.format = 'rfc5424'
        dest1.update()
        assert dest1.format != dest2.format

        dest2.refresh()
        assert dest1.format == dest2.format

    def test_delete_remote_syslog(self, request, mgmt_root, basic_dest):
        setup_basic_remote_syslog_test(request, mgmt_root, 'logdest-remote_syslog', 'Common', basic_dest.name)
        dest1 = mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.load(name='logdest-remote_syslog')
        dest1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.sys.log_config.destination.remote_syslogs.remote_syslog.load(name='logdest-remote_syslog')
        assert err.value.response.status_code == 404
