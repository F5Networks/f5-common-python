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
if hasattr(symbols, 'run_biq_license_tests'):
    if symbols.run_biq_license_tests is True:
        MISSING_SYMBOLS_LICENSE = False


pytestmark = pytest.mark.skipif(
    MISSING_SYMBOLS_LICENSE,
    reason="You must opt-in to run BIG-IQ license tests."
           "To run them, set the symbols variable "
           "'run_biq_license_tests: True'"
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
        baseRegKey=symbols.biq_license_pool
    )
    wait_for_state(pool, 'LICENSED')
    yield pool
    pool.delete()


@pytest.fixture
def pools(mgmt_root):
    pools = mgmt_root.cm.shared.licensing.pools_s.get_collection()
    return pools


class TestLicensePoolCollection(object):
    def test_get_collection(self, pools):
        assert len(pools) == 0


class TestDeviceLicensing(object):
    def test_license_unmanaged_device(self, pool):
        """Test licensing a managed device

        A managed device is one that BIG-IQ has already discovered. To
        license a managed device you need to supply the device's
        deviceReference to the member's collection.

        As part of adding the reference, BIG-IQ should generate a uuid
        for the entry in the member's collection.

        :param pool:
        :return:
        """
        member = pool.members_s.member.create(
            deviceAddress="10.2.2.3",
            username="admin",
            password="admin",
        )
        wait_for_state(member, 'LICENSED')

        try:
            assert member.state == 'LICENSED'
            assert member.deviceAddress == "10.2.2.3"
        finally:
            member.delete(
                username='admin',
                password='admin'
            )
