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


@pytest.mark.skipif(
    pytest.config.getoption('--release') < '13.0.0',
    reason='This test will fail below 13.0.0'
    )
class TestServiceTmm(object):
    def test_restart_service_tmm(self, mgmt_root):
        # restart
        tmm = mgmt_root.tm.sys.service.tmm.load()
        tmm_restart = tmm.exec_cmd('restart')
        assert tmm_restart.command == 'restart'
        get_activation_state(mgmt_root)
        # Use the pollster to check for expected state. The pollster uses
        # a method which checks for any exception. If one is found, it keeps
        # trying.
        # Check if forced to offline
        pollster(check_device_state_as_expected)(mgmt_root, 'offline')
        # Check if device is active
        pollster(check_device_state_as_expected)(mgmt_root, 'active')

    def test_load_service_tmm(self, mgmt_root):
        # Load
        tmm = mgmt_root.tm.sys.service.tmm.load()
        URI = 'https://localhost/mgmt/tm/sys/service/tmm'
        assert tmm.name == 'tmm'
        assert tmm.selfLink.startswith(URI)
