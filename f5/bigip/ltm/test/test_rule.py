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

from f5.bigip import BigIP
from f5.bigip.ltm.nat import NAT
from f5.bigip.resource import MissingRequiredCreationParameter


@pytest.fixture
def FakeRule():
    fake_rule_collection = mock.MagicMock()
    fake_rule = NAT(fake_rule_collection)
    return fake_rule


class TestCreate(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        r1 = b.ltm.rulecollection.rule
        r2 = b.ltm.rulecollection.rule
        assert r1 is not r2

    def test_create_no_args(self, FakeRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRule.create()

    def test_create_partition(self, FakeRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRule.create(name='myname', partition='Common')
