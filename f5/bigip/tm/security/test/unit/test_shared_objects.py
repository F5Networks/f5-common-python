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
from f5.bigip.tm.security.shared_objects import Address_List
from f5.bigip.tm.security.shared_objects import Port_List
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture()
def FakeAddrLst():
    fake_col = mock.MagicMock()
    fake_col._meta_data['bigip'].tmos_version = '14.0.0'
    fake_addrlst = Address_List(fake_col)
    return fake_addrlst


@pytest.fixture()
def FakePortLst():
    fake_col = mock.MagicMock()
    fake_col._meta_data['bigip'].tmos_version = '14.0.0'
    fake_portlist = Port_List(fake_col)
    return fake_portlist


class TestAddresslist_sharedobjects(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '14.0.0'
        a1 = b.tm.security.shared_objects.address_lists.address_list
        a2 = b.tm.security.shared_objects.address_lists.address_list
        assert a1 is not a2

    def test_create_no_args(self, FakeAddrLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeAddrLst.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1.', 'admin', 'admin')
        b._meta_data['tmos_version'] = '14.0.0'
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.shared_objects.address_lists.address_list.create(
                name='destined_to_fail', partition='Common')


class TestPortList_sharedobjects(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '14.0.0'
        r1 = b.tm.security.shared_objects.port_lists.port_list
        r2 = b.tm.security.shared_objects.port_lists.port_list
        assert r1 is not r2

    def test_create_no_args(self, FakePortLst):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePortLst.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '14.0.0'
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.shared_objects.port_lists.port_list.create(
                name='destined_to_fail', partition='Common')
