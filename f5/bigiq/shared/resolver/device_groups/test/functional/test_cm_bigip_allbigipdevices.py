# Copyright 2015-2016 F5 Networks Inc.
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

import pytest
import time

from pytest import symbols

MISSING_SYMBOLS_BIGIP = True
if hasattr(symbols, 'run_biq_cloud_managed_devices_tests'):
    if symbols.run_biq_cloud_managed_devices_tests is True:
        MISSING_SYMBOLS_BIGIP = False


def wait_for_state(obj, state):
    for x in range(60):
        obj.refresh()
        if obj.state == state:
            return
        time.sleep(1)


@pytest.fixture(scope='function')
def managed_device(mgmt_root):
    dg = mgmt_root.shared.resolver.device_groups
    device = dg.cm_bigip_allbigipdevices.devices_s.device.create(
        address=symbols.biq_bigip_managed_device,
        password='admin',
        rootPassword='default',
        userName='admin'
    )
    wait_for_state(device, 'ACTIVE')
    yield device
    device.delete()


@pytest.mark.skipif(
    MISSING_SYMBOLS_BIGIP,
    reason="You must opt-in to run BIG-IQ managed-devices tests."
           "To run them, set the symbols variable "
           "'run_biq_cloud_managed_devices_tests: True'"
)
class TestDevice(object):
    def test_curdl(self, managed_device):
        assert managed_device.address == symbols.biq_bigip_managed_device
        assert managed_device.state == 'ACTIVE'

    def test_load(self, managed_device, mgmt_root):
        rp = dict(
            params="$filter=address+eq+'{0}'".format(
                symbols.biq_bigip_managed_device
            )
        )
        dg = mgmt_root.shared.resolver.device_groups
        devices = dg.cm_bigip_allbigipdevices.devices_s.get_collection(
            requests_params=rp
        )
        assert len(devices) == 1

        device = devices.pop()
        assert device.address == symbols.biq_bigip_managed_device
        assert device.product == 'BIG-IP'
        assert device.state == 'ACTIVE'
        assert device.mcpDeviceName == '/Common/bigip1'
        assert device.kind == \
            'shared:resolver:device-groups:restdeviceresolverdevicestate'
