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
from f5.bigip.tm.gtm.datacenter import Datacenter


@pytest.fixture
def FakeDatacenter():
    fake_dc_s = mock.MagicMock()
    fake_dc = Datacenter(fake_dc_s)
    return fake_dc


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.gtm.datacenters.datacenter
        r2 = b.tm.gtm.datacenters.datacenter
        assert r1 is not r2

    def test_create_no_args(self, FakeDatacenter):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeDatacenter.create()

    def test_create_partition(self, FakeDatacenter):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeDatacenter.create(partition='Common')
