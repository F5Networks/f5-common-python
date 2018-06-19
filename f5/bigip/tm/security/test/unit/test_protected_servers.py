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
from f5.bigip.tm.security.protected_servers import Netflow_Protected_Server
from f5.bigip.tm.security.protected_servers import Traffic_Matching_Criteria
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeTrafficMatchingCriteria():
    fake_col = mock.MagicMock()
    fake_tmc = Traffic_Matching_Criteria(fake_col)
    return fake_tmc


@pytest.fixture
def FakeNetflowProtectedServer():
    fake_col = mock.MagicMock()
    fake_nps = Netflow_Protected_Server(fake_col)
    return fake_nps


class TestTrafficMatchingCriteria(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        tmc1 = b.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria
        tmc2 = b.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria
        assert tmc1 is not tmc2

    def test_create_no_args(self, FakeTrafficMatchingCriteria):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeTrafficMatchingCriteria.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria.create(
                name='Fake')


class TestNetflowProtectedServer(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        nps1 = b.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server
        nps2 = b.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server
        assert nps1 is not nps2

    def test_create_no_args(self, FakeNetflowProtectedServer):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeNetflowProtectedServer.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server.create(
                name='Fake')
