# Copyright 2017 F5 Networks Inc.
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
from f5.bigip.tm.security.dos import Profile
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeProfile():
    fake_profiles = mock.MagicMock()
    fake_profile = Profile(fake_profiles)
    return fake_profile


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        n1 = b.tm.security.dos.profiles.profile
        n2 = b.tm.security.dos.profiles.profile
        assert n1 is not n2

    def test_create_no_args(self, FakeProfile):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeProfile.create()
