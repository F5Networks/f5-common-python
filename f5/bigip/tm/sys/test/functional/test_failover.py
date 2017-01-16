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

from f5.multi_device.utils import get_device_info
from f5.multi_device.utils import pollster
from f5.sdk_exception import BooleansToReduceHaveSameValue

import pytest


def get_activation_state(device):
    '''Get the activation state for a device.'''

    device_name = get_device_info(device).name
    act = device.tm.cm.devices.device.load(
        name=device_name,
        partition='Common'
    )
    return act.failoverState


def check_device_state_as_expected(device, expected_state):
    assert get_activation_state(device).lower() == expected_state.lower()


@pytest.fixture
def teardown_device_failover_state(request, mgmt_root):
    def teardown():
        if get_activation_state(mgmt_root).lower() != 'active':
            f = mgmt_root.tm.sys.failover
            f.exec_cmd('run', utilCmdArgs='online')
    request.addfinalizer(teardown)


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
        fl = f.toggle_standby(trafficgroup="traffic-group-1", state=None)
        assert fl.standby is None
        assert fl.command == "run"
        fl = f.toggle_standby(trafficgroup="traffic-group-1", state=True)
        assert fl.standby is True
        assert fl.command == "run"
        fl.refresh()
        assert 'Failover active' in fl.apiRawValues['apiAnonymous']

    def test_toggle_bad_kwargs_standby(self, mgmt_root):
        with pytest.raises(TypeError) as ex:
            f = mgmt_root.tm.sys.failover
            f.toggle_standby(trafficgroup="traffic-group-1",
                             state=None, foo="bar")
        assert "Unexpected **kwargs" in str(ex.value)

    def test_attribute_values(self, bigip):
        fl = bigip.sys.failover
        # Testing both conditions
        with pytest.raises(BooleansToReduceHaveSameValue) as ex1:
            fl.exec_cmd('run', online=True, offline=True)
        assert 'online and offline, have same value: True' \
            in str(ex1.value)
        with pytest.raises(BooleansToReduceHaveSameValue) as ex2:
            fl.exec_cmd('run', online=False, offline=False)
        assert 'online and offline, have same value: False' \
            in str(ex2.value)

    def test_exec_cmd(self, mgmt_root, teardown_device_failover_state):
        fl = mgmt_root.tm.sys.failover.load()
        f = mgmt_root.tm.sys.failover
        f.exec_cmd('run', offline=True)
        get_activation_state(mgmt_root)
        # Use the pollster to check for expected state. The pollster uses
        # a method which checks for any exception. If one is found, it keeps
        # trying.
        pollster(check_device_state_as_expected)(mgmt_root, 'forced-offline')
        fl.refresh()
        assert 'Failover forced_offline' in fl.apiRawValues['apiAnonymous']
        f.exec_cmd('run', offline=False, online=True)
        pollster(check_device_state_as_expected)(mgmt_root, 'active')
        fl.refresh()
        assert 'Failover active' in fl.apiRawValues['apiAnonymous']

    def test_exec_cmd_cmdargs(self, mgmt_root, teardown_device_failover_state):
        fl = mgmt_root.tm.sys.failover.load()
        f = mgmt_root.tm.sys.failover
        f.exec_cmd('run', utilCmdArgs='offline')
        pollster(check_device_state_as_expected)(mgmt_root, 'forced-offline')
        fl.refresh()
        assert 'Failover forced_offline' in fl.apiRawValues['apiAnonymous']
        f.exec_cmd('run', utilCmdArgs='online')
        pollster(check_device_state_as_expected)(mgmt_root, 'active')
        fl.refresh()
        assert 'Failover active' in fl.apiRawValues['apiAnonymous']
