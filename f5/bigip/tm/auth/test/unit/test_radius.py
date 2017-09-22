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

from f5.bigip import ManagementRoot
from f5.bigip.tm.auth.radius import Radius
from f5.sdk_exception import InvalidName
from f5.sdk_exception import MissingRequiredCreationParameter

import mock
import pytest


@pytest.fixture
def FakeRadius():
    fake_radius = mock.MagicMock()
    fake_radobj = Radius(fake_radius)
    return fake_radobj


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('localhost', 'admin', 'admin')
        r1 = b.tm.auth.radius_s.radius
        r2 = b.tm.auth.radius_s.radius
        assert r1 is not r2

    def test_create_no_args(self, FakeRadius):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRadius.create()

    def test_create_bad_name(self, FakeRadius):
        with pytest.raises(InvalidName):
            FakeRadius.create(name='testauth')
