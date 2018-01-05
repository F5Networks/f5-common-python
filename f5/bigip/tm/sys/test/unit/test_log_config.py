# Copyright 2016 F5 Networks Inc.
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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.sys.log_config import Alertd
from f5.bigip.tm.sys.log_config import Arcsight
from f5.bigip.tm.sys.log_config import Filter
from f5.bigip.tm.sys.log_config import Ipfix
from f5.bigip.tm.sys.log_config import Local_Database
from f5.bigip.tm.sys.log_config import Local_Syslog
from f5.bigip.tm.sys.log_config import Management_Port
from f5.bigip.tm.sys.log_config import Publisher
from f5.bigip.tm.sys.log_config import Remote_High_Speed_Log
from f5.bigip.tm.sys.log_config import Remote_Syslog
from f5.bigip.tm.sys.log_config import Splunk
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeAlertd():
    fake_alertd_s = mock.MagicMock()
    fake_alertd = Alertd(fake_alertd_s)
    return fake_alertd


def test_alertd_create(FakeAlertd):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeAlertd.create(name='myalertd')
    assert str(EIO.value) == 'Alertd does not support the create method'


def test_alertd_delete(FakeAlertd):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeAlertd.delete()
    assert str(EIO.value) == 'Alertd does not support the delete method'


@pytest.fixture
def FakeArcsight():
    fake_as_s = mock.MagicMock()
    fake_as = Arcsight(fake_as_s)
    return fake_as


def test_arcsight_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    as1 = b.tm.sys.log_config.destination.arcsights.arcsight
    as2 = b.tm.sys.log_config.destination.arcsights.arcsight
    assert as1 is not as2


def test_arcsight_create_no_args(FakeArcsight):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeArcsight.create()
    assert 'name' in str(EIO.value)


def test_arcsight_create_missing_args(FakeArcsight):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeArcsight.create(name='myarcsightlc')
    assert 'forwardTo' in str(EIO.value)


@pytest.fixture
def FakeIpfix():
    fake_ipf_s = mock.MagicMock()
    fake_ipf = Ipfix(fake_ipf_s)
    return fake_ipf


def test_ipfix_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    ipf1 = b.tm.sys.log_config.destination.ipfixs.ipfix
    ipf2 = b.tm.sys.log_config.destination.ipfixs.ipfix
    assert ipf1 is not ipf2


def test_ipfix_create_no_args(FakeIpfix):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeIpfix.create()
    assert 'name' in str(EIO.value)


def test_ipfix_create_missing_args(FakeIpfix):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeIpfix.create(name='myipfixlc')
    assert 'poolName' in str(EIO.value)


@pytest.fixture
def FakeFilter():
    fake_filter_s = mock.MagicMock()
    fake_filter = Filter(fake_filter_s)
    return fake_filter


def test_filter_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    f1 = b.tm.sys.log_config.filters.filter
    f2 = b.tm.sys.log_config.filters.filter
    assert f1 is not f2


def test_filter_create_no_args(FakeFilter):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeFilter.create()
    assert 'name' in str(EIO.value)


def test_filter_create_missing_args(FakeFilter):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeFilter.create(name='logfilt')
    assert 'publisher' in str(EIO.value)


@pytest.fixture
def FakeLocalDB():
    fake_ldb_s = mock.MagicMock()
    fake_ldb = Local_Database(fake_ldb_s)
    return fake_ldb


def test_ldb_create(FakeLocalDB):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeLocalDB.create(name='myldb')
    assert str(EIO.value) == 'Local_Database does not support the create method'


def test_ldb_delete(FakeLocalDB):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeLocalDB.delete()
    assert str(EIO.value) == 'Local_Database does not support the delete method'


@pytest.fixture
def FakeLocalSL():
    fake_lsl_s = mock.MagicMock()
    fake_lsl = Local_Syslog(fake_lsl_s)
    return fake_lsl


def test_lsl_create(FakeLocalSL):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeLocalSL.create(name='myldb')
    assert str(EIO.value) == 'Local_Syslog does not support the create method'


def test_lsl_delete(FakeLocalSL):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeLocalSL.delete()
    assert str(EIO.value) == 'Local_Syslog does not support the delete method'


@pytest.fixture
def FakeMgmtPort():
    fake_mp_s = mock.MagicMock()
    fake_mp = Management_Port(fake_mp_s)
    return fake_mp


def test_mgmtport_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    mp1 = b.tm.sys.log_config.destination.management_ports.management_port
    mp2 = b.tm.sys.log_config.destination.management_ports.management_port
    assert mp1 is not mp2


def test_mgmtport_create_no_args(FakeMgmtPort):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeMgmtPort.create()
    assert 'name' in str(EIO.value)


def test_mgmtport_create_missing_args(FakeMgmtPort):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeMgmtPort.create(name='mymplc')
    assert 'ipAddress' in str(EIO.value)


@pytest.fixture
def FakePublisher():
    fake_publisher_s = mock.MagicMock()
    fake_publisher = Publisher(fake_publisher_s)
    return fake_publisher


def test_publisher_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p1 = b.tm.sys.log_config.publishers.publisher
    p2 = b.tm.sys.log_config.publishers.publisher
    assert p1 is not p2


def test_publisher_create_no_args(FakePublisher):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakePublisher.create()
    assert 'name' in str(EIO.value)


@pytest.fixture
def FakeRHSL():
    fake_hsl_s = mock.MagicMock()
    fake_hsl = Remote_High_Speed_Log(fake_hsl_s)
    return fake_hsl


def test_rhsl_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    hsl1 = b.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log
    hsl2 = b.tm.sys.log_config.destination.remote_high_speed_logs.remote_high_speed_log
    assert hsl1 is not hsl2


def test_rhsl_create_no_args(FakeRHSL):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeRHSL.create()
    assert 'name' in str(EIO.value)


def test_rhsl_create_missing_args(FakeRHSL):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeRHSL.create(name='myhsllc')
    assert 'poolName' in str(EIO.value)


@pytest.fixture
def FakeRSyslog():
    fake_rsyslog_s = mock.MagicMock()
    fake_rsyslog = Remote_Syslog(fake_rsyslog_s)
    return fake_rsyslog


def test_rsyslog_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    rsys1 = b.tm.sys.log_config.destination.remote_syslogs.remote_syslog
    rsys2 = b.tm.sys.log_config.destination.remote_syslogs.remote_syslog
    assert rsys1 is not rsys2


def test_rsyslog_create_no_args(FakeRSyslog):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeRSyslog.create()
    assert 'name' in str(EIO.value)


def test_rsyslog_create_missing_args(FakeRSyslog):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeRSyslog.create(name='myrsysloglc')
    assert 'remoteHighSpeedLog' in str(EIO.value)


@pytest.fixture
def FakeSplunk():
    fake_splunk_s = mock.MagicMock()
    fake_splunk = Splunk(fake_splunk_s)
    return fake_splunk


def test_splunk_create_two(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    splunk1 = b.tm.sys.log_config.destination.splunks.splunk
    splunk2 = b.tm.sys.log_config.destination.splunks.splunk
    assert splunk1 is not splunk2


def test_splunk_create_no_args(FakeSplunk):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeSplunk.create()
    assert 'name' in str(EIO.value)


def test_splunk_create_missing_args(FakeSplunk):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeSplunk.create(name='mysplunklc')
    assert 'forwardTo' in str(EIO.value)
