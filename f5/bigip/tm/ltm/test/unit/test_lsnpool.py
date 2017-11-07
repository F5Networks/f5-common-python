# Copyright 2015 F5 Networks Inc.
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

import mock
import pytest


from f5.bigip import ManagementRoot
from f5.bigip.tm.ltm.lsnpool import LSNLogProfile
from f5.bigip.tm.ltm.lsnpool import LSNLogProfiles
from f5.bigip.tm.ltm.lsnpool import LSNPool
from f5.bigip.tm.ltm.lsnpool import LSNPools
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeLSNpool():
    fake_pool = mock.MagicMock()
    fake_pool = LSNPool(fake_pool)
    return fake_pool


@pytest.fixture
def FakeLSNpools():
    fake_pools = mock.MagicMock()
    fake_pools = LSNPools(fake_pools)
    return fake_pools


@pytest.fixture
def FakeLSNpoolLogProfile():
    fake_lp = mock.MagicMock()
    fake_lp = LSNLogProfile(fake_lp)
    return fake_lp


@pytest.fixture
def FakeLSNpoolLogProfiles():
    fake_lps = mock.MagicMock()
    fake_lps = LSNLogProfiles(fake_lps)
    return fake_lps


class TestLSNPoolCreate(object):
    def test_create_lsnpool_two(self, fakeicontrolsession):
        mgmt = ManagementRoot('localhost', 'admin', 'admin')
        dg1 = mgmt.tm.ltm.lsnpools.lsnpool.create
        dg2 = mgmt.tm.ltm.lsnpools.lsnpool.create
        assert dg1 is not dg2

    def test_create_lsnpool_no_args(self, FakeLSNpool):
        # name parameter is mandatory
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLSNpool.create()

    def test_overloaded_resource_name_lsnpools(self, FakeLSNpools):
        assert FakeLSNpools._format_resource_name() == "lsn-pools"


class TestLSNPoolLogProfileCreate(object):
    def test_create_logProfile_two(self, fakeicontrolsession):
        mgmt = ManagementRoot('localhost', 'admin', 'admin')
        dg1 = mgmt.tm.ltm.lsnlogprofiles.lsnlogprofile.create
        dg2 = mgmt.tm.ltm.lsnlogprofiles.lsnlogprofile.create
        assert dg1 is not dg2

    def test_create_logProfile_no_args(self, FakeLSNpoolLogProfile):
        # name parameter is mandatory
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLSNpoolLogProfile.create()

    def test_overloaded_resource_name_logProfile(self, FakeLSNpoolLogProfiles):
        resource_nm = "lsn-log-profiles"
        assert FakeLSNpoolLogProfiles._format_resource_name() == resource_nm
