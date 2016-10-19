# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from distutils.version import LooseVersion
import pytest


def setup_syslog_test(request, mgmt_root):
    def teardown():
        d.authPrivFrom = "notice"
        d.authPrivTo = "emerg"
        d.consoleLog = "enabled"
        d.cronFrom = "warning"
        d.cronTo = "emerg"
        d.daemonFrom = "notice"
        d.daemonTo = "emerg"
        d.isoDate = "disabled"
        d.kernFrom = "debug"
        d.kernTo = "emerg"
        d.local6From = "notice"
        d.local6To = "emerg"
        d.mailFrom = "notice"
        d.mailTo = "emerg"
        d.messagesFrom = "notice"
        d.messagesTo = "warning"
        d.userLogFrom = "notice"
        d.userLogTo = "emerg"
        d.remoteServers = []
        d.update()
    request.addfinalizer(teardown)
    d = mgmt_root.tm.sys.syslog.load()
    return d


def setup_syslog_test_clustered_host(request, mgmt_root):
    def teardown():
        d.clusteredHostSlot = "enabled"
        d.clusteredMessageSlot = "disabled"
        d.update()
    request.addfinalizer(teardown)
    d = mgmt_root.tm.sys.syslog.load()
    return d


class TestSyslogCommon(object):
    def test_load(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        assert s1.authPrivFrom == s2.authPrivFrom
        assert s1.authPrivTo == s2.authPrivTo
        assert s1.consoleLog == s2.consoleLog
        assert s1.cronFrom == s2.cronFrom
        assert s1.cronTo == s2.cronTo
        assert s1.daemonFrom == s2.daemonFrom
        assert s1.daemonTo == s2.daemonTo
        assert s1.isoDate == s2.isoDate
        assert s1.kernFrom == s2.kernFrom
        assert s1.kernTo == s2.kernTo
        assert s1.local6From == s2.local6From
        assert s1.local6To == s2.local6To
        assert s1.mailFrom == s2.mailFrom
        assert s1.mailTo == s2.mailTo
        assert s1.messagesFrom == s2.messagesFrom
        assert s1.messagesTo == s2.messagesTo
        assert s1.userLogFrom == s2.userLogFrom
        assert s1.userLogTo == s2.userLogTo

    def test_update_auth_priv_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.authPrivFrom = "emerg"
        s1.update()
        assert "emerg" == s1.authPrivFrom
        assert "emerg" != s2.authPrivFrom

        # Refresh
        s2.refresh()
        assert "emerg" == s2.authPrivFrom

    def test_update_auth_priv_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.authPrivTo = "notice"
        s1.update()
        assert "notice" == s1.authPrivTo
        assert "notice" != s2.authPrivTo

        # Refresh
        s2.refresh()
        assert "notice" == s2.authPrivTo

    def test_update_console_log(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.consoleLog = "disabled"
        s1.update()
        assert "disabled" == s1.consoleLog
        assert "disabled" != s2.consoleLog

        # Refresh
        s2.refresh()
        assert "disabled" == s2.consoleLog

    def test_update_cron_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.cronFrom = "notice"
        s1.update()
        assert "notice" == s1.cronFrom
        assert "notice" != s2.cronFrom

        # Refresh
        s2.refresh()
        assert "notice" == s2.cronFrom

    def test_update_cron_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.cronTo = "notice"
        s1.update()
        assert "notice" == s1.cronTo
        assert "notice" != s2.cronTo

        # Refresh
        s2.refresh()
        assert "notice" == s2.cronTo

    def test_update_daemon_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.daemonFrom = "emerg"
        s1.update()
        assert "emerg" == s1.daemonFrom
        assert "emerg" != s2.daemonFrom

        # Refresh
        s2.refresh()
        assert "emerg" == s2.daemonFrom

    def test_update_daemon_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.daemonTo = "notice"
        s1.update()
        assert "notice" == s1.daemonTo
        assert "notice" != s2.daemonTo

        # Refresh
        s2.refresh()
        assert "notice" == s2.daemonTo

    def test_update_iso_date(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.isoDate = "enabled"
        s1.update()
        assert "enabled" == s1.isoDate
        assert "enabled" != s2.isoDate

        # Refresh
        s2.refresh()
        assert "enabled" == s2.isoDate

    def test_update_kern_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.kernFrom = "notice"
        s1.update()
        assert "notice" == s1.kernFrom
        assert "notice" != s2.kernFrom

        # Refresh
        s2.refresh()
        assert "notice" == s2.kernFrom

    def test_update_kern_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.kernTo = "notice"
        s1.update()
        assert "notice" == s1.kernTo
        assert "notice" != s2.kernTo

        # Refresh
        s2.refresh()
        assert "notice" == s2.kernTo

    def test_update_local_6_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.local6From = "emerg"
        s1.update()
        assert "emerg" == s1.local6From
        assert "emerg" != s2.local6From

        # Refresh
        s2.refresh()
        assert "emerg" == s2.local6From

    def test_update_local_6_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.local6To = "notice"
        s1.update()
        assert "notice" == s1.local6To
        assert "notice" != s2.local6To

        # Refresh
        s2.refresh()
        assert "notice" == s2.local6To

    def test_update_mail_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.mailFrom = "emerg"
        s1.update()
        assert "emerg" == s1.mailFrom
        assert "emerg" != s2.mailFrom

        # Refresh
        s2.refresh()
        assert "emerg" == s2.mailFrom

    def test_update_mail_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.mailTo = "notice"
        s1.update()
        assert "notice" == s1.mailTo
        assert "notice" != s2.mailTo

        # Refresh
        s2.refresh()
        assert "notice" == s2.mailTo

    def test_update_messages_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.messagesFrom = "emerg"
        s1.update()
        assert "emerg" == s1.messagesFrom
        assert "emerg" != s2.messagesFrom

        # Refresh
        s2.refresh()
        assert "emerg" == s2.messagesFrom

    def test_update_messages_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.messagesTo = "emerg"
        s1.update()
        assert "emerg" == s1.messagesTo
        assert "emerg" != s2.messagesTo

        # Refresh
        s2.refresh()
        assert "emerg" == s2.messagesTo

    def test_update_user_log_from(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.userLogFrom = "emerg"
        s1.update()
        assert "emerg" == s1.userLogFrom
        assert "emerg" != s2.userLogFrom

        # Refresh
        s2.refresh()
        assert "emerg" == s2.userLogFrom

    def test_update_user_log_to(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        s1.userLogTo = "notice"
        s1.update()
        assert "notice" == s1.userLogTo
        assert "notice" != s2.userLogTo

        # Refresh
        s2.refresh()
        assert "notice" == s2.userLogTo


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.0.0'),
    reason='Clustered slots are only supported in 12.0.0 or greater.'
)
class TestSyslogClusteredHostOptions(object):
    def test_load(self, request, mgmt_root):
        s1 = setup_syslog_test_clustered_host(request, mgmt_root)
        s2 = setup_syslog_test_clustered_host(request, mgmt_root)

        assert s1.clusteredHostSlot == s2.clusteredHostSlot
        assert s1.clusteredMessageSlot == s2.clusteredMessageSlot

    def test_update_clustered_host_slot(self, request, mgmt_root):
        s1 = setup_syslog_test_clustered_host(request, mgmt_root)
        s2 = setup_syslog_test_clustered_host(request, mgmt_root)

        s1.clusteredHostSlot = "disabled"
        s1.update()
        assert "disabled" == s1.clusteredHostSlot
        assert "disabled" != s2.clusteredHostSlot

        # Refresh
        s2.refresh()
        assert "disabled" == s2.clusteredHostSlot

    def test_update_clustered_message_slot(self, request, mgmt_root):
        s1 = setup_syslog_test_clustered_host(request, mgmt_root)
        s2 = setup_syslog_test_clustered_host(request, mgmt_root)

        s1.clusteredMessageSlot = "enabled"
        s1.update()
        assert "enabled" == s1.clusteredMessageSlot
        assert "enabled" != s2.clusteredMessageSlot

        # Refresh
        s2.refresh()
        assert "enabled" == s2.clusteredMessageSlot


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) >= LooseVersion('11.6.1'),
    reason='Remote options changed in version 11.6.1 or greater.'
)
class TestSyslogLegacyRemoteServersOptions(object):
    def test_update_remote_servers(self, request, mgmt_root):
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        remote_servers = dict(
            name="remotesyslog1",
            host="10.10.10.10",
            remotePort=514
        )

        s1.remoteServers = [remote_servers]
        s1.update()
        assert hasattr(s1, 'remoteServers')
        assert not hasattr(s2, 'remoteServers')

        s1_remote = s1.remoteServers.pop()
        assert remote_servers['name'] == s1_remote['name']
        assert remote_servers['host'] == s1_remote['host']
        assert remote_servers['remotePort'] == s1_remote['remotePort']

        # Refresh
        s2.refresh()
        assert hasattr(s2, 'remoteServers')

        s2_remote = s2.remoteServers.pop()
        assert remote_servers['name'] == s2_remote['name']
        assert remote_servers['host'] == s2_remote['host']
        assert remote_servers['remotePort'] == s2_remote['remotePort']


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('11.6.1'),
    reason='Remote options changed in version 11.6.1 or greater.'
)
class TestSyslogChangedRemoteServersOptions(object):
    def test_update_remote_servers(self, request, mgmt_root):
        """Test updating of the remote server list

        Prior to version 11.6.0, the `name` field and the `partition`
        field were separate values. At the release of 11.6.0, this was
        changed so that the `name` field contained teh full path to the
        object, and the `partition` field was dropped entirely from the
        returned value.

        :param request:
        :param mgmt_root:
        :return:
        """
        s1 = setup_syslog_test(request, mgmt_root)
        s2 = setup_syslog_test(request, mgmt_root)

        remote_servers = dict(
            name="/Common/remotesyslog1",
            host="10.10.10.10",
            remotePort=514
        )

        s1.remoteServers = [remote_servers]
        s1.update()
        assert hasattr(s1, 'remoteServers')
        assert not hasattr(s2, 'remoteServers')

        s1_remote = s1.remoteServers.pop()
        assert remote_servers['name'] == s1_remote['name']
        assert remote_servers['host'] == s1_remote['host']
        assert remote_servers['remotePort'] == s1_remote['remotePort']

        # Refresh
        s2.refresh()
        assert hasattr(s2, 'remoteServers')

        s2_remote = s2.remoteServers.pop()
        assert remote_servers['name'] == s2_remote['name']
        assert remote_servers['host'] == s2_remote['host']
        assert remote_servers['remotePort'] == s2_remote['remotePort']
