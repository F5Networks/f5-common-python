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
from f5.bigip.tm.ltm.traffic_class import Traffic_Class


@pytest.fixture
def FakeTraffic():
    fake_traffic_class_s = mock.MagicMock()
    fake_traffic = Traffic_Class(fake_traffic_class_s)
    return fake_traffic


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = mr.tm.ltm.traffic_class_s.traffic_class
        t2 = mr.tm.ltm.traffic_class_s.traffic_class
        assert t1 is not t2

    def test_create_no_args(self, FakeTraffic):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeTraffic.create()

    def test_create_name(self, FakeTraffic):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeTraffic.create(name='myname')
