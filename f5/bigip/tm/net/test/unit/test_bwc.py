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
from f5.bigip.tm.net.bwc import Policy
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakePolicy():
    fake_policy_s = mock.MagicMock()
    fake_policy = Policy(fake_policy_s)
    return fake_policy


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.net.bwc.policys.policy
        p2 = b.tm.net.bwc.policys.policy
        assert p1 is not p2

    def test_create_no_args(self, FakePolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePolicy.create()
