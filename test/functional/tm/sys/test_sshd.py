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

from pprint import pprint as pp


def setup_sshd_test(request, bigip):
    def teardown():
        d.allow = ['ALL']
        d.banner = 'disabled'
        d.bannerText = ''
        d.inactivityTimeout = 0
        d.logLevel = 'info'
        d.login = 'enabled'
        d.port = 22

        d.update()
    request.addfinalizer(teardown)
    d = bigip.sys.sshd.load()
    return d


class TestSshd(object):
    def test_load(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        assert ssh1.allow == ssh2.allow
        assert ssh1.banner == ssh2.banner
        assert ssh1.inactivityTimeout == ssh2.inactivityTimeout
        assert ssh1.logLevel == ssh2.logLevel
        assert ssh1.login == ssh2.login
        assert ssh1.port == ssh2.port

        pp(ssh1.raw)
        pp(ssh2.raw)

    def test_update_allow(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        ssh1.allow = ['192.168.1.1']
        pp(ssh2.raw)
        ssh1.update()
        assert ['192.168.1.1'] == ssh1.allow
        assert ['192.168.1.1'] != ssh2.allow

        # Refresh
        ssh2.refresh()
        assert ['192.168.1.1'] == ssh2.allow

    def test_update_banner(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        banners = ['enabled', 'disabled']

        for banner in banners:
            ssh1.banner = banner
            pp(ssh2.raw)
            ssh1.update()
            assert banner == ssh1.banner
            assert banner != ssh2.banner

            # Refresh
            ssh2.refresh()
            assert banner == ssh2.banner

    def test_update_bannerText(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        ssh1.bannerText = 'foo banner'
        pp(ssh2.raw)
        ssh1.update()
        assert 'foo banner' == ssh1.bannerText
        assert not hasattr(ssh2, 'bannerText')

        # Refresh
        ssh2.refresh()
        assert 'foo banner' == ssh2.bannerText

    def test_update_inactivityTimeout(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        ssh1.inactivityTimeout = 10
        pp(ssh2.raw)
        ssh1.update()
        assert 10 == ssh1.inactivityTimeout
        assert 10 != ssh2.inactivityTimeout

        # Refresh
        ssh2.refresh()
        assert 10 == ssh2.inactivityTimeout

    def test_update_logLevel(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        levels = ['debug', 'debug1', 'debug2', 'debug3', 'error', 'fatal',
                  'info', 'quiet', 'verbose']

        for level in levels:
            ssh1.logLevel = level
            pp(ssh2.raw)
            ssh1.update()
            assert level == ssh1.logLevel
            assert level != ssh2.logLevel

            # Refresh
            ssh2.refresh()
            assert level == ssh2.logLevel

    def test_update_login(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        logins = ['disabled', 'enabled']

        for login in logins:
            ssh1.login = login
            pp(ssh2.raw)
            ssh1.update()
            assert login == ssh1.login
            assert login != ssh2.login

            # Refresh
            ssh2.refresh()
            assert login == ssh2.login

    def test_update_port(self, request, bigip):
        ssh1 = setup_sshd_test(request, bigip)
        ssh2 = bigip.sys.sshd.load()

        ssh1.port = 1234
        pp(ssh2.raw)
        ssh1.update()
        assert 1234 == ssh1.port
        assert 1234 != ssh2.port

        # Refresh
        ssh2.refresh()
        assert 1234 == ssh2.port
