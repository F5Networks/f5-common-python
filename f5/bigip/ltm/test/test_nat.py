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

from f5.bigip.ltm.nat import NAT
from f5.bigip.resource import MissingRequiredCreationParameter


@pytest.fixture
def FakeNat():
    fake_nat_collection = mock.MagicMock()
    fake_nat = NAT(fake_nat_collection)
    return fake_nat


class TestCreate(object):
    def test_create_no_args(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create()

    def test_create_name(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create(name='myname')

    def test_create_partition(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create(name='myname', partition='Common')

    def test_create_translation(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create(name='myname', partition='Common',
                           translationAddress='192.168.1.1')

    def test_create_originating(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create(name='myname', partition='Common',
                           originatingAddress='192.168.2.1')

    def test_create_inheritedtrafficgroup_false_no_tg(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create(name='mynat', partition='Common',
                           translationAddress='192.168.1.1',
                           originatingAddress='192.168.2.1',
                           inheritedTrafficGroup='false')

    def test_create_inheritedtrafficgroup_false_empty_tg(self, FakeNat):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNat.create(name='mynat', partition='Common',
                           translationAddress='192.168.1.1',
                           originatingAddress='192.168.2.1',
                           inheritedTrafficGroup='false',
                           trafficGroup='')
