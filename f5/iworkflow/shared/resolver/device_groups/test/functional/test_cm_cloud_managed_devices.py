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

from pytest import symbols
from requests.exceptions import HTTPError

MISSING_SYMBOLS_BIGIP = True
if hasattr(symbols, 'run_iwf_cloud_managed_devices_tests'):
    if symbols.run_iwf_cloud_managed_devices_tests is True:
        MISSING_SYMBOLS_BIGIP = False


def delete_resource(mgmt_root, uuid):
    try:
        dg = mgmt_root.shared.resolver.device_groups
        device = dg.cm_cloud_managed_devices.devices_s.device.load(
            uuid=uuid
        )
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    device.delete()


def setup_create_test(**kwargs):
    dg = kwargs['mr'].shared.resolver.device_groups
    device = dg.cm_cloud_managed_devices.devices_s.device.create(
        address=kwargs['address'],
        password=kwargs['password'],
        rootPassword=kwargs['root_password'],
        userName=kwargs['username']
    )
    uuid = device.uuid

    def teardown():
        delete_resource(kwargs['mr'], uuid)
    kwargs['request'].addfinalizer(teardown)
    return device, dg


class TestDevice(object):
    @pytest.mark.skipif(
        MISSING_SYMBOLS_BIGIP,
        reason="You must opt-in to run iWorkflow cloud-managed-devices tests."
               "To run them, set the symbols variable "
               "'run_iwf_cloud_managed_devices_tests: True'"
    )
    def test_curdle(self, request, mgmt_root):
        device, dg = setup_create_test(
            request=request, mr=mgmt_root, address='10.2.2.2',
            password='admin', root_password='default', username='admin'
        )
        assert device.address == '10.2.2.2'
        assert device.state == 'PENDING'

    def test_load(self, request, mgmt_root):
        rp = dict(
            params="$filter=address+eq+'10.0.2.15'"
        )
        dg = mgmt_root.shared.resolver.device_groups
        devices = dg.cm_cloud_managed_devices.devices_s.get_collection(
            requests_params=rp
        )
        assert len(devices) == 1

        device = devices.pop()
        assert device.address == '10.0.2.15'
        assert device.product == 'iWorkflow'
        assert device.state == 'ACTIVE'
        assert device.mcpDeviceName == '/Common/localhost'
        assert device.kind == \
            'shared:resolver:device-groups:restdeviceresolverdevicestate'
