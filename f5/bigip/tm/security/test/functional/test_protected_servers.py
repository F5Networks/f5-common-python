# Copyright 2018 F5 Networks Inc.
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

from f5.bigip.tm.security.protected_servers import Netflow_Protected_Server
from f5.bigip.tm.security.protected_servers import Traffic_Matching_Criteria
from requests.exceptions import HTTPError

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def traffic_matching_criteria(mgmt_root):
    tmc1 = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria.create(
        name='fake_tmc', destinationAddressInline='1.1.1.1', sourceAddressInline='2.2.2.2', partition='Common')
    yield tmc1
    tmc1.delete()


@pytest.fixture(scope='function')
def netflow_protected_server(mgmt_root, traffic_matching_criteria):
    tmc = traffic_matching_criteria
    nps1 = mgmt_root.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server.create(
        name='fake_nps', trafficMatchingCriteria=tmc.fullPath, partition='Common')
    yield nps1
    nps1.delete()


class TestTrafficMatchingCriteria(object):
    def test_create_req_args(self, mgmt_root):
        tmc1 = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria.create(
            name='fake_tmc', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/protected-servers/traffic-matching-criteria/~Common~fake_tmc'
        assert tmc1.name == 'fake_tmc'
        assert tmc1.partition == 'Common'
        assert tmc1.selfLink.startswith(URI)
        assert tmc1.kind == 'tm:security:protected-servers:traffic-matching-criteria:traffic-matching-criteriastate'
        assert not hasattr(tmc1, 'description')
        tmc1.delete()

    def test_create_opt_args(self, mgmt_root):
        tmc1 = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s.traffic_matching_criteria.create(
            name='fake_tmc', destinationAddressInline='1.1.1.1', sourceAddressInline='2.2.2.2', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/protected-servers/traffic-matching-criteria/~Common~fake_tmc'
        assert tmc1.name == 'fake_tmc'
        assert tmc1.partition == 'Common'
        assert tmc1.selfLink.startswith(URI)
        tmc1.modify(description=DESC)
        assert hasattr(tmc1, 'description')
        assert tmc1.description == DESC
        tmc1.delete()

    def test_refresh(self, mgmt_root, traffic_matching_criteria):
        tmc = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s
        tmc1 = traffic_matching_criteria
        tmc2 = tmc.traffic_matching_criteria.load(name='fake_tmc', partition='Common')
        assert tmc1.name == tmc2.name
        assert tmc1.kind == tmc2.kind
        assert tmc1.selfLink == tmc2.selfLink
        assert not hasattr(tmc1, 'description')
        assert not hasattr(tmc2, 'description')
        tmc2.modify(description=DESC)
        assert hasattr(tmc2, 'description')
        assert tmc2.description == DESC
        tmc1.refresh()
        assert tmc1.selfLink == tmc2.selfLink
        assert hasattr(tmc1, 'description')
        assert tmc1.description == tmc2.description

    def test_delete(self, mgmt_root):
        tmc = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s
        tmc1 = tmc.traffic_matching_criteria.create(name='fake_tmc', destinationAddressInline='1.1.1.1', sourceAddressInline='2.2.2.2', partition='Common')
        tmc1.delete()
        with pytest.raises(HTTPError) as err:
            tmc.traffic_matching_criteria.load(partition='Common', name='fake_tmc')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        tmc = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s
        with pytest.raises(HTTPError) as err:
            tmc.traffic_matching_criteria.load(partition='Common', name='fake_tmc')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, traffic_matching_criteria):
        tmc1 = traffic_matching_criteria
        URI = 'https://localhost/mgmt/tm/security/protected-servers/traffic-matching-criteria/~Common~fake_tmc'
        assert tmc1.name == 'fake_tmc'
        assert tmc1.partition == 'Common'
        assert tmc1.selfLink.startswith(URI)
        assert not hasattr(tmc1, 'description')
        tmc1.description = DESC
        tmc1.update()
        assert hasattr(tmc1, 'description')
        assert tmc1.description == DESC
        tmc = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s
        tmc2 = tmc.traffic_matching_criteria.load(partition='Common', name='fake_tmc')
        assert tmc1.name == tmc2.name
        assert tmc1.partition == tmc2.partition
        assert tmc1.selfLink == tmc2.selfLink
        assert hasattr(tmc2, 'description')
        assert tmc1.description == tmc2.description

    def test_traffic_matching_criteria_collection(self, mgmt_root, traffic_matching_criteria):
        tmc1 = traffic_matching_criteria
        URI = 'https://localhost/mgmt/tm/security/protected-servers/traffic-matching-criteria/~Common~fake_tmc'
        assert tmc1.name == 'fake_tmc'
        assert tmc1.partition == 'Common'
        assert tmc1.selfLink.startswith(URI)
        tmc = mgmt_root.tm.security.protected_servers.traffic_matching_criteria_s.get_collection()
        assert isinstance(tmc, list)
        assert len(tmc)
        assert isinstance(tmc[0], Traffic_Matching_Criteria)


class TestNetflowProtectedServer(object):
    def test_create_req_args(self, mgmt_root, traffic_matching_criteria):
        tmc = traffic_matching_criteria
        nps1 = mgmt_root.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server.create(
            name='fake_nps', trafficMatchingCriteria=tmc.fullPath, partition='Common')
        URI = 'https://localhost/mgmt/tm/security/protected-servers/netflow-protected-server/~Common~fake_nps'
        assert nps1.name == 'fake_nps'
        assert nps1.partition == 'Common'
        assert nps1.selfLink.startswith(URI)
        assert nps1.kind == 'tm:security:protected-servers:netflow-protected-server:netflow-protected-serverstate'
        assert nps1.trafficMatchingCriteria == tmc.fullPath
        nps1.delete()

    def test_create_opt_args(self, mgmt_root, traffic_matching_criteria):
        tmc = traffic_matching_criteria
        nps1 = mgmt_root.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server.create(
            name='fake_nps', trafficMatchingCriteria=tmc.fullPath, partition='Common', packetCapacity='100')
        URI = 'https://localhost/mgmt/tm/security/protected-servers/netflow-protected-server/~Common~fake_nps'
        assert nps1.name == 'fake_nps'
        assert nps1.partition == 'Common'
        assert nps1.selfLink.startswith(URI)
        nps1.modify(throughputCapacity='100')
        assert nps1.throughputCapacity == '100'
        nps1.delete()

    def test_refresh(self, mgmt_root, netflow_protected_server):
        nps = mgmt_root.tm.security.protected_servers.netflow_protected_server_s
        nps1 = netflow_protected_server
        nps2 = nps.netflow_protected_server.load(name='fake_nps', partition='Common')
        assert nps1.name == nps2.name
        assert nps1.kind == nps2.kind
        assert nps1.selfLink == nps2.selfLink
        nps2.modify(throughputCapacity='100')
        assert nps2.throughputCapacity == '100'
        nps1.refresh()
        assert nps1.selfLink == nps2.selfLink
        assert nps1.throughputCapacity == '100'

    def test_delete(self, mgmt_root, traffic_matching_criteria):
        tmc = traffic_matching_criteria
        nps = mgmt_root.tm.security.protected_servers.netflow_protected_server_s
        nps1 = mgmt_root.tm.security.protected_servers.netflow_protected_server_s.netflow_protected_server.create(
            name='fake_nps', trafficMatchingCriteria=tmc.fullPath, partition='Common')
        nps1.delete()
        with pytest.raises(HTTPError) as err:
            nps.netflow_protected_server.load(partition='Common', name='fake_nps')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        nps = mgmt_root.tm.security.protected_servers.netflow_protected_server_s
        with pytest.raises(HTTPError) as err:
            nps.netflow_protected_server.load(partition='Common', name='fake_nps')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, netflow_protected_server):
        nps1 = netflow_protected_server
        URI = 'https://localhost/mgmt/tm/security/protected-servers/netflow-protected-server/~Common~fake_nps'
        assert nps1.name == 'fake_nps'
        assert nps1.partition == 'Common'
        assert nps1.selfLink.startswith(URI)
        nps1.throughputCapacity = '100'
        nps1.update()
        assert nps1.throughputCapacity == '100'
        nps = mgmt_root.tm.security.protected_servers.netflow_protected_server_s
        nps2 = nps.netflow_protected_server.load(partition='Common', name='fake_nps')
        assert nps1.name == nps2.name
        assert nps1.kind == nps2.kind
        assert nps1.selfLink == nps2.selfLink
        assert nps2.throughputCapacity == '100'

    def test_traffic_matching_criteria_collection(self, mgmt_root, netflow_protected_server):
        nps1 = netflow_protected_server
        URI = 'https://localhost/mgmt/tm/security/protected-servers/netflow-protected-server/~Common~fake_nps'
        assert nps1.name == 'fake_nps'
        assert nps1.partition == 'Common'
        assert nps1.selfLink.startswith(URI)
        nps = mgmt_root.tm.security.protected_servers.netflow_protected_server_s.get_collection()
        assert isinstance(nps, list)
        assert len(nps)
        assert isinstance(nps[0], Netflow_Protected_Server)
