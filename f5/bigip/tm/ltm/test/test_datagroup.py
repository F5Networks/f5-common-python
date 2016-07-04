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
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.ltm.data_group import Internal, External


@pytest.fixture
def FakeData_Group_Internal():
    fake_dg = mock.MagicMock()
    fake_dg = Internal(fake_dg)
    return fake_dg

@pytest.fixture
def FakeData_Group_External():
    fake_dg = mock.MagicMock()
    fake_dg = External(fake_dg)
    return fake_dg


class TestCreate(object):
    def test_create_internal_two(self, fakeicontrolsession):
        mgmt = ManagementRoot('172.16.44.15', 'admin', 'admin')
        dg1 = mgmt.tm.ltm.data_group.internals.internal
        dg2 = mgmt.tm.ltm.data_group.internals.internal
        assert dg1 is not dg2

    def test_create_external_two(self, fakeicontrolsession):
        mgmt = ManagementRoot('172.16.44.15', 'admin', 'admin')
        dg1 = mgmt.tm.ltm.data_group.externals.external
        dg2 = mgmt.tm.ltm.data_group.externals.external
        assert dg1 is not dg2

    def test_create_internal_no_args(self, FakeData_Group_Internal):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeData_Group_Internal.create()

    def test_create_external_no_args(self, FakeData_Group_External):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeData_Group_External.create()
