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

from icontrol.exceptions import iControlUnexpectedHTTPError
from pytest import symbols


def wait_for_state(obj, state):
    for x in range(60):
        obj.refresh()
        if obj.state == state:
            return
        time.sleep(1)


@pytest.fixture(scope="module")
def managed_device(mgmt_root):
    try:
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
    except iControlUnexpectedHTTPError:
        yield False


@pytest.fixture(scope="module")
def http_template_example(mgmt_root, managed_device):
    assert managed_device.address == symbols.iwf_bigip_managed_device

    iapps = mgmt_root.cm.cloud.templates.iapps.get_collection(
        requests_params=dict(
            params="$filter=name+eq+'f5.http'"
        )
    )
    iapp = iapps.pop()
    example = iapp.providers_s.providers.load(name='example')
    yield example


@pytest.fixture(scope='module')
def connector(mgmt_root):
    locals = mgmt_root.cm.cloud.connectors.locals
    local = locals.local.create(name='local1')
    yield local
    local.delete()


class TestIapp(object):
    def test_create(self, http_template_example, connector, mgmt_root):
        template = http_template_example.raw
        template.pop('_meta_data', None)
        template['isF5Example'] = False
        template['templateName'] = 'app_http'
        template['properties'] = [
            dict(
                id='cloudConnectorReference',
                isRequired=True,
                provider=connector.selfLink
            )
        ]

        iapp = mgmt_root.cm.cloud.provider.templates.iapps.iapp.create(
            **template
        )
        assert iapp.templateName == 'app_http'
        assert iapp.isF5Example is False

    def test_delete(self, mgmt_root):
        iapps = mgmt_root.cm.cloud.provider.templates.iapps

        collection = iapps.get_collection(
            requests_params=dict(
                params="$filter=templateName+eq+'app_http'"
            )
        )
        assert len(collection) == 1
        iapp = collection.pop()
        iapp.delete()

        collection = iapps.get_collection(
            requests_params=dict(
                params="$filter=templateName+eq+'app_http'"
            )
        )
        iapps.refresh()
        assert len(collection) == 0
