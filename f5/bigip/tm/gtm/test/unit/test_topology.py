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

import pytest

from f5.bigip import ManagementRoot
from f5.bigip.resource import InvalidName
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm import Gtm
from f5.bigip.tm.gtm.topology import Topology


@pytest.fixture
def FakeTopology(fakeicontrolsession):
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    fake_gtm = Gtm(mr.tm)
    fake_top = Topology(fake_gtm)
    return fake_top


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.gtm.topology_s.topology
        r2 = b.tm.gtm.topology_s.topology
        assert r1 is not r2

    def test_create_no_args(self, FakeTopology):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeTopology.create()

    def test_invalid_name_no_keywords(self, FakeTopology):
        with pytest.raises(InvalidName):
            FakeTopology.create(name='fake_stuff')

    def test_invalid_name_no_ldns(self, FakeTopology):
        with pytest.raises(InvalidName):
            FakeTopology.create(name='server: fake_stuff')

    def test_invalid_name_no_server(self, FakeTopology):
        with pytest.raises(InvalidName):
            FakeTopology.create(name='ldns: fake_stuff')


class Test_Refresh_Modify_Update(object):
    def test_refresh_raises(self, FakeTopology):
        with pytest.raises(UnsupportedOperation):
            FakeTopology.refresh()

    def test_modify_raises(self, FakeTopology):
        with pytest.raises(UnsupportedOperation):
            FakeTopology.modify()

    def test_update_raises(self, FakeTopology):
        with pytest.raises(UnsupportedOperation):
            FakeTopology.update()
