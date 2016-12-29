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

from pytest import symbols
from requests.exceptions import HTTPError


MISSING_SYMBOLS_LICENSE = True
if hasattr(symbols, 'run_iwf_license_tests'):
    if symbols.run_iwf_license_tests is True:
        MISSING_SYMBOLS_LICENSE = False


pytestmark = pytest.mark.skipif(
    MISSING_SYMBOLS_LICENSE,
    reason="You must opt-in to run iWorkflow license tests."
           "To run them, set the symbols variable "
           "'run_iwf_license_tests: True'"
)


def delete_pool(mgmt_root, uuid):
    try:
        p = mgmt_root.cm.shared.licensing.pools_s.pool.load(uuid=uuid)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_basic_test(request, mgmt_root, key):
    def teardown():
        delete_pool(mgmt_root, uuid)

    pool1 = mgmt_root.cm.shared.licensing.pools_s.pool.create(baseRegKey=key)
    uuid = pool1.uuid

    request.addfinalizer(teardown)
    return pool1


class TestLicensePoolCollection(object):
    def test_get_collection(self, request, mgmt_root, opt_release):
        setup_basic_test(request, mgmt_root, symbols.iwf_license_pool)
