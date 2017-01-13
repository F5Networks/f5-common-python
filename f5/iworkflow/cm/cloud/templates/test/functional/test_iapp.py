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


@pytest.mark.parametrize("template", [
    ('f5.bea_weblogic'),
    ('f5.cifs'),
    ('f5.citrix_presentation_server'),
    ('f5.citrix_xen_app'),
    ('f5.diameter'),
    ('f5.dns'),
    ('f5.ftp'),
    ('f5.http'),
    ('f5.ip_forwarding'),
    ('f5.ldap'),
    ('f5.microsoft_exchange_2010'),
    ('f5.microsoft_exchange_owa_2007'),
    ('f5.microsoft_iis'),
    ('f5.microsoft_lync_server_2010'),
    ('f5.microsoft_ocs_2007_r2'),
    ('f5.microsoft_sharepoint_2007'),
    ('f5.microsoft_sharepoint_2010'),
    ('f5.npath'),
    ('f5.oracle_as_10g'),
    ('f5.oracle_ebs'),
    ('f5.peoplesoft_9'),
    ('f5.radius'),
    ('f5.replication'),
    ('f5.sap_enterprise_portal'),
    ('f5.sap_erp'),
    ('f5.vmware_view'),
    ('f5.vmware_vmotion')
])
class TestBigIpCommonTemplates(object):
    def test_count_collection(self, template, mgmt_root):
        iapps = mgmt_root.cm.cloud.templates.iapps.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(template)
            )
        )
        assert len(iapps) == 1

    def test_load_example(self, template, mgmt_root):
        iapps = mgmt_root.cm.cloud.templates.iapps.get_collection(
            requests_params=dict(
                params="$filter=name+eq+'{0}'".format(template)
            )
        )
        iapp = iapps.pop()
        example = iapp.providers_s.providers.load(name='example')
        assert example.templateName == template + '-example'
