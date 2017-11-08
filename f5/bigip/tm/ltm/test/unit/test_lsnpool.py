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
from f5.bigip.tm.ltm.lsn_pools import LSN_Log_Profile
from f5.bigip.tm.ltm.lsn_pools import LSN_Log_Profiles
from f5.bigip.tm.ltm.lsn_pools import LSN_Pool
from f5.bigip.tm.ltm.lsn_pools import LSN_Pools
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeLSNpool():
    fake_pool = mock.MagicMock()
    fake_pool = LSN_Pool(fake_pool)
    return fake_pool


@pytest.fixture
def FakeLSNpools():
    fake_pools = mock.MagicMock()
    fake_pools = LSN_Pools(fake_pools)
    return fake_pools


@pytest.fixture
def FakeLSNpoolLogProfile():
    fake_lp = mock.MagicMock()
    fake_lp = LSN_Log_Profile(fake_lp)
    return fake_lp


@pytest.fixture
def FakeLSNpoolLogProfiles():
    fake_lps = mock.MagicMock()
    fake_lps = LSN_Log_Profiles(fake_lps)
    return fake_lps


class TestLSNPoolCreate(object):
    def test_create_lsnpool_two(self, fakeicontrolsession):
        mgmt = ManagementRoot('localhost', 'admin', 'admin')
        dg1 = mgmt.tm.ltm.lsn_pools.lsn_pool.create
        dg2 = mgmt.tm.ltm.lsn_pools.lsn_pool.create
        assert dg1 is not dg2

    def test_create_lsnpool_no_args(self, FakeLSNpool):
        # name parameter is mandatory
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLSNpool.create()


class TestLSNPoolLogProfileCreate(object):
    def test_create_logProfile_two(self, fakeicontrolsession):
        mgmt = ManagementRoot('localhost', 'admin', 'admin')
        dg1 = mgmt.tm.ltm.lsn_log_profiles.lsn_log_profile.create
        dg2 = mgmt.tm.ltm.lsn_log_profiles.lsn_log_profile.create
        assert dg1 is not dg2

    def test_create_logProfile_no_args(self, FakeLSNpoolLogProfile):
        # name parameter is mandatory
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLSNpoolLogProfile.create()
