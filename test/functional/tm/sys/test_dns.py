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


def setup_dns_test(request, bigip):
    def teardown():
        d.nameServers = servers
        d.update()
    request.addfinalizer(teardown)
    d = bigip.sys.dns.load()
    servers = d.nameServers
    return d, servers


class TestDns(object):
    def test_RUL(self, request, bigip):
        # Load
        ip = '192.168.100.85'
        dns1, orig_servers = setup_dns_test(request, bigip)
        dns2 = bigip.sys.dns.load()
        assert len(dns1.nameServers) == len(dns2.nameServers)

        pp(dns1.raw)
        pp(dns2.raw)
        # Update
        dns1.nameServers = [ip]
        pp(dns2.raw)
        dns1.update()
        assert ip in dns1.nameServers
        assert ip not in dns2.nameServers

        # Refresh
        dns2.refresh()
        assert ip in dns2.nameServers
