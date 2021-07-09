# Copyright 2021 F5 Networks Inc.
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
from f5.bigip.tm.ltm.cipher import Group
from f5.bigip.tm.ltm.cipher import Rule
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeCipherRule():
    fake_rule_s = mock.MagicMock()
    fake_rule = Rule(fake_rule_s)
    return fake_rule


@pytest.fixture
def FakeCipherGroup():
    fake_group_s = mock.MagicMock()
    fake_group = Group(fake_group_s)
    return fake_group


class TestCipherRuleCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.ltm.cipher.rules.rule
        r2 = b.tm.ltm.cipher.rules.rule
        assert r1 is not r2

    def test_create_no_args(self, FakeCipherRule):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeCipherRule.create()


class TestCipherGroupCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        g1 = b.tm.ltm.cipher.groups.group
        g2 = b.tm.ltm.cipher.groups.group
        assert g1 is not g2

    def test_create_no_args(self, FakeCipherGroup):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeCipherGroup.create()
