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

import json
import os
import pytest
import time

from pytest import symbols


MISSING_SYMBOLS_BIGIP = True
if hasattr(symbols, 'run_iwf_cloud_managed_devices_tests'):
    if symbols.run_iwf_cloud_managed_devices_tests is True:
        MISSING_SYMBOLS_BIGIP = False


pytestmark = pytest.mark.skipif(
    MISSING_SYMBOLS_BIGIP,
    reason="You must opt-in to run iWorkflow cloud-managed-devices tests."
           "To run them, set the symbols variable "
           "'run_iwf_cloud_managed_devices_tests: True'"
)


fixture_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'fixtures'
)
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


def wait_for_state(obj, state):
    for x in range(60):
        obj.refresh()
        if obj.state == state:
            return
        time.sleep(1)


@pytest.fixture(scope="module")
def managed_device(mgmt_root):
    dg = mgmt_root.shared.resolver.device_groups
    device = dg.cm_cloud_managed_devices.devices_s.device.create(
        address=symbols.iwf_bigip_managed_device,
        userName="admin",
        password="admin",
        automaticallyUpdateFramework=True
    )
    wait_for_state(device, 'ACTIVE')
    yield device
    device.delete()


@pytest.fixture(scope="function")
def template(mgmt_root, managed_device):
    iapp = mgmt_root.cm.cloud.templates.iapps.iapp.create(
        name='f5.http.v1.2.0rc4',
        deviceForJSONTransformation=dict(
            link=str(managed_device.selfLink)
        ),
        templateContent=load_fixture('f5.http.v1.2.0rc4.tmpl')
    )
    yield iapp
    iapp.delete()


class TestBigIpCommonTemplates(object):
    def test_count_collection(self, template, mgmt_root):
        iapps = mgmt_root.cm.cloud.templates.iapps.get_collection()
        assert len(iapps) == 1

    def test_load_example(self, template, mgmt_root):
        iapp = mgmt_root.cm.cloud.templates.iapps.iapp.load(
            name='f5.http.v1.2.0rc4'
        )
        assert iapp.name == 'f5.http.v1.2.0rc4'
