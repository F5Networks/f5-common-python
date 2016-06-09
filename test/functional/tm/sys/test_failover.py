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

from f5.bigip.tm.sys.failover import InvalidParameterValue
from pprint import pprint as pp

import time
import pytest


class TestFailover(object):
    def test_failover_LR(self, bigip):
        """Test failover refresh and load.

        Test that the failover object can be refreshed and loaded. The object
        also supports update, but this will force a failover on the
        device and this may have negative consequences to the device we
        are using to test if it is not setup properly so I am not testing
        it here.
        """

        f = bigip.sys.failover.load()
        assert 'Failover active' in f.apiRawValues['apiAnonymous']
        f.refresh()
        assert 'Failover active' in f.apiRawValues['apiAnonymous']

    def test_toggle_standby(self, bigip):
        f = bigip.sys.failover
        f.toggle_standby(trafficgroup="traffic-group-1", state=None)
        assert f.standby is None
        assert f.command == u"run"
        pp(f.raw)
        f.toggle_standby(trafficgroup="traffic-group-1", state=True)
        assert f.standby is True
        assert f.command == u"run"
        pp('************')
        f.refresh()
        pp(f.raw)
        assert 'Failover active' in f.apiRawValues['apiAnonymous']

    def test_attribute_values(self, bigip):
        fl = bigip.sys.failover
        # Testing both conditions
        with pytest.raises(InvalidParameterValue):
            fl.exec_cmd('run', online=True, offline=True)
        with pytest.raises(InvalidParameterValue):
            fl.exec_cmd('run', online=False, offline=False)

    def test_exec_cmd(self, bigip):
        f = bigip.sys.failover
        f.exec_cmd('run', offline=True)
        fl = bigip.sys.failover.load()
        assert 'Failover forced_offline' in fl.apiRawValues['apiAnonymous']
        f.exec_cmd('run', offline=False, online=True)
        fl.refresh()
        assert 'Failover active' in fl.apiRawValues['apiAnonymous']

    def test_exec_cmd_cmdargs(self, bigip):
        f = bigip.sys.failover
        f.exec_cmd('run', utilCmdArgs='offline')
        fl = bigip.sys.failover.load()
        assert 'Failover forced_offline' in fl.apiRawValues['apiAnonymous']
        f.exec_cmd('run', utilCmdArgs='online')
        # We need this 1 sec delay as sometimes the status does not change
        # straight away, causing the assertion to fail.
        time.sleep(1)
        fl.refresh()
        assert 'Failover active' in fl.apiRawValues['apiAnonymous']
