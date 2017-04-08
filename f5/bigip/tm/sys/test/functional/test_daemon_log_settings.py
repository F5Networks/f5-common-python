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


def setup_daemon_log_settings_clusterd_test(request, mgmt_root):
    def teardown():
        clusterd.logLevel = 'notice'
        clusterd.update()
    request.addfinalizer(teardown)
    clusterd = mgmt_root.tm.sys.daemon_log_settings.clusterd.load()
    return clusterd


def setup_daemon_log_settings_csyncd_test(request, mgmt_root):
    def teardown():
        csyncd.logLevel = 'notice'
        csyncd.update()
    request.addfinalizer(teardown)
    csyncd = mgmt_root.tm.sys.daemon_log_settings.csyncd.load()
    return csyncd


def setup_daemon_log_settings_icrd_test(request, mgmt_root):
    def teardown():
        icrd.audit = 'modifications'
        icrd.update()
    request.addfinalizer(teardown)
    icrd = mgmt_root.tm.sys.daemon_log_settings.icrd.load()
    return icrd


def setup_daemon_log_settings_lind_test(request, mgmt_root):
    def teardown():
        lind.logLevel = 'notice'
        lind.update()
    request.addfinalizer(teardown)
    lind = mgmt_root.tm.sys.daemon_log_settings.lind.load()
    return lind


def setup_daemon_log_settings_mcpd_test(request, mgmt_root):
    def teardown():
        mcpd.logLevel = 'notice'
        mcpd.update()
    request.addfinalizer(teardown)
    mcpd = mgmt_root.tm.sys.daemon_log_settings.mcpd.load()
    return mcpd


def setup_daemon_log_settings_tmm_test(request, mgmt_root):
    def teardown():
        tmm.httpLogLevel = 'error'
        tmm.update()
    request.addfinalizer(teardown)
    tmm = mgmt_root.tm.sys.daemon_log_settings.tmm.load()
    return tmm


class TestDaemon_Log_Settings(object):
    def test_clusterd_RUL(self, request, mgmt_root):
        # Load
        daemon1 = setup_daemon_log_settings_clusterd_test(request, mgmt_root)
        daemon2 = mgmt_root.tm.sys.daemon_log_settings.clusterd.load()
        assert daemon1.logLevel == 'notice'
        assert daemon1.logLevel == daemon2.logLevel

        # Update
        daemon1.logLevel = 'error'
        daemon1.update()
        assert daemon1.logLevel == 'error'
        assert daemon2.logLevel == 'notice'

        # Refresh
        daemon2.refresh()
        assert daemon1.logLevel == daemon2.logLevel

    def test_csyncd_RUL(self, request, mgmt_root):
        # Load
        daemon1 = setup_daemon_log_settings_csyncd_test(request, mgmt_root)
        daemon2 = mgmt_root.tm.sys.daemon_log_settings.csyncd.load()
        assert daemon1.logLevel == 'notice'
        assert daemon1.logLevel == daemon2.logLevel

        # Update
        daemon1.logLevel = 'error'
        daemon1.update()
        assert daemon1.logLevel == 'error'
        assert daemon2.logLevel == 'notice'

        # Refresh
        daemon2.refresh()
        assert daemon1.logLevel == daemon2.logLevel

    def test_icrd_RUL(self, request, mgmt_root):
        # Load
        daemon1 = setup_daemon_log_settings_icrd_test(request, mgmt_root)
        daemon2 = mgmt_root.tm.sys.daemon_log_settings.icrd.load()
        assert daemon1.audit == 'modifications'
        assert daemon1.audit == daemon2.audit

        # Update
        daemon1.audit = 'all'
        daemon1.update()
        assert daemon1.audit == 'all'
        assert daemon2.audit == 'modifications'

        # Refresh
        daemon2.refresh()
        assert daemon1.audit == daemon2.audit

    def test_lind_RUL(self, request, mgmt_root):
        # Load
        daemon1 = setup_daemon_log_settings_lind_test(request, mgmt_root)
        daemon2 = mgmt_root.tm.sys.daemon_log_settings.lind.load()
        assert daemon1.logLevel == 'notice'
        assert daemon1.logLevel == daemon2.logLevel

        # Update
        daemon1.logLevel = 'error'
        daemon1.update()
        assert daemon1.logLevel == 'error'
        assert daemon2.logLevel == 'notice'

        # Refresh
        daemon2.refresh()
        assert daemon1.logLevel == daemon2.logLevel

    def test_mcpd_RUL(self, request, mgmt_root):
        # Load
        daemon1 = setup_daemon_log_settings_mcpd_test(request, mgmt_root)
        daemon2 = mgmt_root.tm.sys.daemon_log_settings.mcpd.load()
        assert daemon1.logLevel == 'notice'
        assert daemon1.logLevel == daemon2.logLevel

        # Update
        daemon1.logLevel = 'error'
        daemon1.update()
        assert daemon1.logLevel == 'error'
        assert daemon2.logLevel == 'notice'

        # Refresh
        daemon2.refresh()
        assert daemon1.logLevel == daemon2.logLevel

    def test_tmm_RUL(self, request, mgmt_root):
        # Load
        daemon1 = setup_daemon_log_settings_tmm_test(request, mgmt_root)
        daemon2 = mgmt_root.tm.sys.daemon_log_settings.tmm.load()
        assert daemon1.httpLogLevel == 'error'
        assert daemon1.httpLogLevel == daemon2.httpLogLevel

        # Update
        daemon1.httpLogLevel = 'warning'
        daemon1.update()
        assert daemon1.httpLogLevel == 'warning'
        assert daemon2.httpLogLevel == 'error'

        # Refresh
        daemon2.refresh()
        assert daemon1.httpLogLevel == daemon2.httpLogLevel
