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

import os
import pytest
import tempfile
import time

from pytest import symbols


SKIPIF_MANAGED_DEVICE_MESSAGE = """
You must opt-in to run BIG-IQ license tests. To run them, set the symbols variable
'run_biq_license_tests' to 'True' and the 'biq_bigip_managed_device' variable to
the IP address of the BIG-IP to license.
"""


SKIPIF_UNMANAGED_DEVICE_MESSAGE = """
You must opt-in to run BIG-IQ license tests. To run them, set the symbols variable
'run_biq_license_tests' to 'True' and the 'biq_bigip_unmanaged_device' variable to
the IP address of the BIG-IP to license.
"""


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


@pytest.fixture(scope='function')
def licenses(mgmt_root):
    licensing = mgmt_root.cm.device.licensing
    collection = licensing.pool.utility.licenses_s.get_collection()
    return collection


def wait_for_status(obj, status):
    for x in range(60):
        obj.refresh()
        if obj.status == status:
            return
        time.sleep(5)


@pytest.fixture(scope='function')
def license(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)

    resource = mgmt_root.cm.device.licensing.pool.utility.licenses_s.licenses.create(
        regKey=symbols.biq_license_utility,
        status="ACTIVATING_AUTOMATIC",
        name=name
    )
    for x in range(60):
        resource.refresh()
        if resource.status == 'READY':
            break
        elif resource.status == 'ACTIVATING_AUTOMATIC_NEED_EULA_ACCEPT':
            resource.modify(
                status='ACTIVATING_AUTOMATIC_EULA_ACCEPTED',
                eulaText=resource.eulaText
            )
        elif resource.status == 'ACTIVATION_FAILED_OFFERING':
            raise Exception(resource.message)
        time.sleep(5)

    yield resource
    resource.delete()


class TestLicensePoolUtilityCollection(object):
    def test_get_collection(self, licenses):
        assert len(licenses) == 0


class TestLicensePoolUtility(object):
    def test_create_v12_license(self, license):
        assert license.status == 'READY'
        assert license.regKey == symbols.biq_license_utility


class TestDeviceLicensing(object):
    @pytest.mark.skipif(
        not hasattr(symbols, 'biq_bigip_unmanaged_device_v13'),
        reason=SKIPIF_UNMANAGED_DEVICE_MESSAGE
    )
    def test_license_unmanaged_device_v13(self, license):
        offerings = license.offerings_s.get_collection()
        offering = next((o for o in offerings if o.name == 'F5-BIG-MSP-BT-200M-LIC-DEV'), None)
        if offering is None:
            raise Exception("No offering named 'F5-BIG-MSP-BT-200M-LIC-DEV' was found")
        resource = offering.members_s.members.create(
            deviceAddress=symbols.biq_bigip_unmanaged_device_v13,
            username="admin",
            password="admin",
            httpsPort=8443,
            unitOfMeasure="hourly"
        )
        wait_for_status(resource, 'LICENSED')

        try:
            assert resource.status == 'LICENSED'
            assert resource.deviceAddress == symbols.biq_bigip_unmanaged_device_v13
        finally:
            resource.delete(
                id=resource.id,
                username='admin',
                password='admin'
            )

# TODO(Add managed licensing once we have added the /mgmt/cm/global/tasks/device-trust API)
#    @pytest.mark.skipif(
#        not hasattr(symbols, 'biq_bigip_managed_device'),
#        reason=SKIPIF_MANAGED_DEVICE_MESSAGE
#    )
#    def test_license_managed_device(self, offering):
#        resource = offering.members_s.members.create(
#            deviceAddress=symbols.biq_bigip_unmanaged_device,
#            username="admin",
#            password="admin",
#        )
#        wait_for_status(resource, 'LICENSED')
#
#        try:
#            assert resource.status == 'LICENSED'
#            assert resource.deviceAddress == symbols.biq_bigip_unmanaged_device
#        finally:
#            resource.delete(
#                id=resource.id,
#                username='admin',
#                password='admin'
#            )
