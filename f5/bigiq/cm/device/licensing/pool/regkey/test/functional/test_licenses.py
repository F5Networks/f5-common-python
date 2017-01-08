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


@pytest.fixture(scope="module")
def license(mgmt_root):
    """Creates a license pool to put license offerings in

    Note that in BIG-IQ 5.1.0 you are able to delete a regkey pool even if it
    has existing regkeys in it.

    :param mgmt_root:
    :return:
    """
    licenses = mgmt_root.cm.device.licensing.pool.regkey.licenses_s
    license = licenses.license.create(
        name='foo'
    )
    yield license
    license.delete()


@pytest.fixture
def licenses(mgmt_root):
    licensing = mgmt_root.cm.device.licensing
    lics = licensing.pool.regkey.licenses_s.get_collection()
    return lics


class TestLicensePoolRegkeyCollection(object):
    def test_get_collection(self, licenses):
        assert len(licenses) == 0


class TestLicensePoolRegkey(object):
    def test_create_v12_license(self, license):
        offering = license.offerings_s.offering.create(
            regKey=symbols.bigip_v12_license,
            status="ACTIVATING_AUTOMATIC"
        )

        try:
            for x in range(60):
                offering.refresh()
                if offering.status == 'READY':
                    break
                time.sleep(1)
            assert offering.status == 'READY'
            assert offering.regKey == symbols.bigip_v12_license
        finally:
            pass
            offering.delete()
