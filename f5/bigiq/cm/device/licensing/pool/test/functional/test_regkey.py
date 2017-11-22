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


@pytest.fixture(scope="function")
def license(mgmt_root):
    """Creates a license pool to put license offerings in

    Note that in BIG-IQ 5.1.0 you are able to delete a regkey pool even if it
    has existing regkeys in it.

    :param mgmt_root:
    :return:
    """
    collection = mgmt_root.cm.device.licensing.pool.regkey.licenses_s
    resource = collection.licenses.create(
        name='foo'
    )
    yield resource
    resource.delete()


@pytest.fixture(scope='function')
def licenses(mgmt_root):
    licensing = mgmt_root.cm.device.licensing
    collection = licensing.pool.regkey.licenses_s.get_collection()
    return collection


def wait_for_status(obj, status):
    for x in range(60):
        obj.refresh()
        if obj.status == status:
            return
        time.sleep(1)


@pytest.fixture(scope='function')
def offering(license):
    resource = license.offerings_s.offerings.create(
        regKey=symbols.biq_license_regkey,
        status="ACTIVATING_AUTOMATIC"
    )
    wait_for_status(resource, 'READY')

    yield resource
    resource.delete()


class TestLicensePoolRegkeyCollection(object):
    def test_get_collection(self, licenses):
        assert len(licenses) == 0


class TestLicensePoolRegkey(object):
    def test_create_v12_license(self, license):
        resource = license.offerings_s.offerings.create(
            regKey=symbols.biq_license_regkey,
            status="ACTIVATING_AUTOMATIC"
        )

        try:
            for x in range(60):
                resource.refresh()
                if resource.status == 'READY':
                    break
                elif resource.status == 'ACTIVATING_AUTOMATIC_NEED_EULA_ACCEPT':
                    resource.modify(
                        status='ACTIVATING_AUTOMATIC_EULA_ACCEPTED',
                        eulaText=resource.eulaText
                    )
                time.sleep(1)
            assert resource.status == 'READY'
            assert resource.regKey == symbols.biq_license_regkey
        finally:
            resource.delete()


class TestDeviceLicensing(object):
    @pytest.mark.skipif(
        not hasattr(symbols, 'biq_bigip_unmanaged_device_v13'),
        reason=SKIPIF_UNMANAGED_DEVICE_MESSAGE
    )
    def test_license_unmanaged_device_v13(self, offering):
        resource = offering.members_s.members.create(
            deviceAddress=symbols.biq_bigip_unmanaged_device_v13,
            username="admin",
            password="admin",
            httpsPort=8443
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
