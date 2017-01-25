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


@pytest.fixture(scope='module')
def device_uuid(mgmt_root):
    dg = mgmt_root.shared.resolver.device_groups
    devices = dg.cm_cloud_managed_devices.devices_s.get_collection(
        requests_params=dict(
            params="$filter=product+eq+'BIG-IP'"
        )
    )
    return devices.pop()


@pytest.fixture(scope="module")
def device_reset(mgmt_root, device_uuid):
    user = mgmt_root.cm.cloud.tasks.reset_devices.reset_device.create(
        deviceUUID=device_uuid
    )
    yield user
    user.delete()


@pytest.fixture
def reset_tasks(mgmt_root):
    devices = mgmt_root.cm.cloud.tasks.reset_devices.get_collection()
    return devices


class TestDeviceReset(object):
    def test_reset_collect(self, reset_tasks):
        assert len(reset_tasks) == 0

    def test_reset_device(self, device_reset, device_uuid):
        assert device_reset.deviceUUID == device_uuid
        assert device_reset.selfLink.startswith(
            'https://localhost/mgmt/cm/cloud/tasks/reset-device/'
        )
