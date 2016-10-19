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


def setup_test(request, bigip, name):
    def teardown():
        if dns1.exists(name=name):
            dns1.delete()

    request.addfinalizer(teardown)
    dc1 = bigip.net.dns_resolvers
    dr1 = dc1.dns_resolver
    dns1 = dr1.create(name=name)
    return dc1, dns1


class TestDnsResolver(object):
    def test_CURDL(self, request, bigip):

        # Test create
        dc1, dns1 = setup_test(request, bigip, name='test_dns_resolver')
        assert dns1.name == 'test_dns_resolver'

        # Test update
        dns1.useTcp = 'no'
        dns1.update()
        assert dns1.useTcp == 'no'

        # Test refresh
        dns1.useTcp = 'yes'
        dns1.refresh()
        assert dns1.useTcp == 'no'

        # Test Load
        dns2 = dc1.dns_resolver.load(name='test_dns_resolver')
        assert dns2.useTcp == dns1.useTcp
