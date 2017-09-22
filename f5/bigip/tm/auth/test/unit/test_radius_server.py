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
from f5.bigip.tm.auth.radius_server import Radius_Server
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeRadiusServer():
    fake_radius_server = mock.MagicMock()
    fake_radsrvobj = Radius_Server(fake_radius_server)
    return fake_radsrvobj


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('localhost', 'admin', 'admin')
        rs1 = b.tm.auth.radius_servers.radius_server
        rs2 = b.tm.auth.radius_servers.radius_server
        assert rs1 is not rs2

    def test_create_no_args(self, FakeRadiusServer):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeRadiusServer.create()
