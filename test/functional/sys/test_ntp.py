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


def setup_ntp_test(request, bigip):
    def teardown():
        n.servers = servers
        n.update()
    request.addfinalizer(teardown)
    n = bigip.sys.ntp.load()
    servers = n.servers
    return n, servers


class TestGlobal_Setting(object):
    def test_RUL(self, request, bigip):
        # Load
        ip = '192.168.1.1'
        ntp1, orig_servers = setup_ntp_test(request, bigip)
        ntp2 = bigip.sys.ntp.load()
        assert len(ntp1.servers) == len(ntp2.servers)

        # Update
        ntp1.servers = [ip]
        ntp1.update()
        assert ip in ntp1.servers
        assert ip not in ntp2.servers

        # Refresh
        ntp2.refresh()
        assert ip in ntp2.servers
