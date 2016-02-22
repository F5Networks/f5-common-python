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


class TestFailover(object):
    def test_failover_LR(self, bigip):
        '''Test failover refresh and load.

        Test that the failover object can be refreshed and loaded. The object
        also supports update, but this will force a failover on the
        device and this may have negative consequences to the device we
        are using to test if it is not setup properly so I am not testing
        it here.
        '''
        f = bigip.sys.failover.load()
        assert f.apiRawValues['apiAnonymous'].startswith('Failover active')
        f.refresh()
        assert f.apiRawValues['apiAnonymous'].startswith('Failover active')
