# Copyright 2014-2017 F5 Networks Inc.
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
from f5.bigip.tm.gtm.rule import Rule
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeRule():
    fake_rule_s = mock.MagicMock()
    fake_rule = Rule(fake_rule_s)
    return fake_rule


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.gtm.rules.rule
        r2 = b.tm.gtm.rules.rule
        assert r1 is not r2

    def test_create_no_args(self, FakeRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRule.create()

    def test_create_partition(self, FakeRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRule.create(partition='Common')

    def test_create_name(self, FakeRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRule.create(name='myname')

    def test_create_api_anon(self, FakeRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRule.create(apiAnonymous='when LB_SELECTED {}')
