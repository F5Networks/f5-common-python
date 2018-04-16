# Copyright 2018 F5 Networks Inc.
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
from f5.bigip.tm.security.log import Profile
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeProfile():
    fake_col = mock.MagicMock()
    fake_profile = Profile(fake_col)
    return fake_profile


class TestProfile(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.log.profiles.profile
        r2 = b.tm.security.log.profiles.profile
        assert r1 is not r2

    def test_create_no_args(self, FakeProfile):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeProfile.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.log.profiles.profile.create(name='destined_to_fail')
