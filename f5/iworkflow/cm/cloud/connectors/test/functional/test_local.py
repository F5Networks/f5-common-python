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

import netaddr
import pytest
import time

from pytest import symbols


CONNECTOR_NAME = 'local10'


MISSING_SYMBOLS_BIGIP = True
if hasattr(symbols, 'run_iwf_cloud_managed_devices_tests'):
    if symbols.run_iwf_cloud_managed_devices_tests is True:
        MISSING_SYMBOLS_BIGIP = False


def wait_for_state(obj, state):
    for x in range(60):
        obj.refresh()
        if obj.state == state:
            return
        time.sleep(1)


@pytest.fixture(scope='module')
def connector(mgmt_root):
    locals = mgmt_root.cm.cloud.connectors.locals
    local = locals.local.create(name=CONNECTOR_NAME)
    yield local
    local.delete()


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


@pytest.fixture(scope="module")
def connector_device(connector, managed_device):
    connector.modify(
        deviceReference=dict(
            link=managed_device.selfLink
        )
    )


class TestLocal(object):
    def test_local_curdl(self, connector):
        assert connector.name == CONNECTOR_NAME
        assert connector.kind == 'cm:cloud:connectors:cloudconnectorstate'
        assert connector.selfLink.startswith(
            'https://localhost/mgmt/cm/cloud/connectors/local/'
        )

    def test_create_node(self, connector, connector_device):
        params = {
            "state": "RUNNING",
            "cloudNodeID": "vm-id-1234",
            "properties": [
                {
                    "id": "ToBeConfiguredByiWorkflow",
                    "provider": "true"
                },
                {
                    "id": "BIG-IP",
                    "provider": "true"
                },
                {
                    "id": "DeviceCreatedWithDefaultCredentials",
                    "provider": "true"
                },
                {
                    "id": "DeviceLeaveRootLoginEnabled",
                    "provider": "true"
                },
                {
                    "id": "DeviceHostname",
                    "provider": "hostname.example.com"
                },
                {
                    "id": "DeviceMgmtUser",
                    "provider": "admin"
                },
                {
                    "id": "DeviceMgmtPassword",
                    "provider": "admin"
                }
            ],
            "ipAddress": "<<replace>>",
            "networkInterfaces": [
                {
                    "localAddress": "<<replace>>",
                    "subnetAddress": "<<replace>>"
                },
                {
                    "localAddress": "10.2.2.3",
                    "subnetAddress": "10.2.2.0/24",
                    "name": "internal"
                }
            ]
        }
        ip = netaddr.IPNetwork(symbols.iwf_bigip_managed_device)
        params['ipAddress'] = symbols.iwf_bigip_managed_device
        params['networkInterfaces'][0]['localAddress'] = \
            symbols.iwf_bigip_managed_device
        params['networkInterfaces'][0]['subnetAddress'] = str(ip.cidr)
        node = connector.nodes_s.node.create(**params)

        for x in range(60):
            node.refresh(
                requests_params=dict(
                    params='$expand=currentConfigDeviceTaskReference'
                )
            )
            if not hasattr(node, 'currentConfigDeviceTaskReference'):
                pass
            elif 'currentStep' not in node.currentConfigDeviceTaskReference:
                pass
            elif node.currentConfigDeviceTaskReference['currentStep'] == 'SUCCESS':  # NOQA
                return True
            elif node.currentConfigDeviceTaskReference['currentStep'] == 'FAILURE':  # NOQA
                break
            time.sleep(10)

        # If success was never returned, fail this test
        assert False
