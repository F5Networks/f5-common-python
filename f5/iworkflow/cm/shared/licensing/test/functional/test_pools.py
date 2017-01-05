# Copyright 2015-2106 F5 Networks Inc.
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


MISSING_SYMBOLS_LICENSE = True
if hasattr(symbols, 'run_iwf_license_tests'):
    if symbols.run_iwf_license_tests is True:
        MISSING_SYMBOLS_LICENSE = False


pytestmark = pytest.mark.skipif(
    MISSING_SYMBOLS_LICENSE,
    reason="You must opt-in to run iWorkflow license tests."
           "To run them, set the symbols variable "
           "'run_iwf_license_tests: True'"
)


def wait_for_state(obj, state):
    for x in range(60):
        obj.refresh()
        if obj.state == state:
            return
        time.sleep(1)


@pytest.fixture(scope="module")
def pool(mgmt_root):
    pool = mgmt_root.cm.shared.licensing.pools_s.pool.create(
        baseRegKey=symbols.iwf_license_pool
    )
    wait_for_state(pool, 'LICENSED')
    yield pool
    pool.delete()


@pytest.fixture(scope="module")
def managed_device(mgmt_root):
    dg = mgmt_root.shared.resolver.device_groups
    device = dg.cm_cloud_managed_devices.devices_s.device.create(
        address="10.2.2.2",
        userName="admin",
        password="admin",
        automaticallyUpdateFramework=False
    )
    wait_for_state(device, 'ACTIVE')
    yield device
    device.delete()


@pytest.fixture
def pools(mgmt_root):
    pools = mgmt_root.cm.shared.licensing.pools_s.get_collection()
    return pools


class TestLicensePoolCollection(object):
    def test_get_collection(self, pools):
        assert len(pools) == 0


class TestDeviceLicensing(object):
    def test_license_managed_device(self, pool, managed_device):
        """Test licensing a managed device

        A managed device is one that iWorkflow has already discovered. To
        license a managed device you need to supply the device's
        deviceReference to the member's collection.

        As part of adding the reference, iWorkflow should generate a uuid
        for the entry in the member's collection.

        :param pool:
        :param managed_device:
        :return:
        """
        member = pool.members_s.member.create(
            deviceReference=dict(
                link=managed_device.selfLink
            )
        )
        wait_for_state(member, 'LICENSED')

        try:
            assert member.state == 'LICENSED'
            assert managed_device.product == "BIG-IP"
            assert managed_device.state == "ACTIVE"
        finally:
            member.delete()
