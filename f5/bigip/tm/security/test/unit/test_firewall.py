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
from f5.bigip.tm.security.firewall import Address_List
from f5.bigip.tm.security.firewall import Port_List
from f5.bigip.tm.security.firewall import Rule_List

from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeAddrLst():
    fake_col = mock.MagicMock()
    fake_addrlst = Address_List(fake_col)
    return fake_addrlst


@pytest.fixture
def FakePortLst():
    fake_col = mock.MagicMock()
    fake_portlst = Port_List(fake_col)
    return fake_portlst


@pytest.fixture
def FakeRuleLst():
    fake_col = mock.MagicMock()
    fake_rulelst = Rule_List(fake_col)
    return fake_rulelst


class TestAddressList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.address_lists.address_list
        r2 = b.tm.security.firewall.address_lists.address_list
        assert r1 is not r2

    def test_create_no_args(self, FakeAddrLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeAddrLst.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.firewall.address_lists.address_list.create(
                name='destined_to_fail', partition='Fake')


class TestPortList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.port_lists.port_list
        r2 = b.tm.security.firewall.port_lists.port_list
        assert r1 is not r2

    def test_create_no_args(self, FakePortLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePortLst.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.firewall.port_lists.port_list.create(
                name='destined_to_fail', partition='Fake')


class TestRuleList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.firewall.rule_lists.rule_list
        r2 = b.tm.security.firewall.rule_lists.rule_list
        assert r1 is not r2

    def test_create_no_args(self, FakeRuleLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRuleLst.create()
