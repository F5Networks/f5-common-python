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

import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.security.flowspec_route_injector import Neighbor
from f5.bigip.tm.security.flowspec_route_injector import Profile
from requests.exceptions import HTTPError

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def profile(mgmt_root):
    n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
    p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
        name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
    yield p1
    p1.delete()


@pytest.fixture(scope='function')
def neighbor(mgmt_root):
    n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
    p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
        name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
    neighbor_lst = p1.neighbor_s
    param_set = {'name': '4.4.4.4', 'local-address': '5.5.5.5', 'local-as': '40', 'remote-as': '50'}
    n1 = neighbor_lst.neighbor.create(**param_set)
    yield n1
    n1.delete()
    p1.delete()


class TestProfile(object):
    def test_create_req_args(self, mgmt_root):
        n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
            name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
        URI = 'https://localhost/mgmt/tm/security/' \
              'flowspec-route-injector/profile/~Common~fake_profile'
        assert p1.name == 'fake_profile'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        p1.delete()

    def test_refresh(self, mgmt_root, profile):
        p1 = profile
        p2 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.load(
            name='fake_profile', partition='Common')
        assert p1.name == p2.name
        assert p1.kind == p2.kind
        assert p1.selfLink == p2.selfLink
        assert not hasattr(p1, 'description')
        assert not hasattr(p2, 'description')
        p2.modify(description=DESC)
        p1.modify(description=DESC)
        assert hasattr(p2, 'description')
        assert p2.description == DESC
        p1.refresh()
        assert p1.selfLink == p2.selfLink
        assert hasattr(p1, 'description')
        assert p1.description == p2.description

    def test_delete(self, mgmt_root):
        p = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile
        n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
        p1 = p.create(name='delete_me', partition='Common', routeDomain='/Common/0', neighbor=[n])
        p1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.load(
                name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile
        with pytest.raises(HTTPError) as err:
            p.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, profile):
        p1 = profile
        URI = 'https://localhost/mgmt/tm/security/' \
              'flowspec-route-injector/profile/~Common~fake_profile'
        assert p1.name == 'fake_profile'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.description = DESC
        p1.update()
        assert hasattr(p1, 'description')
        assert p1.description == DESC
        p = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile
        p2 = p.load(name='fake_profile', partition='Common')
        assert p1.name == p2.name
        assert p1.partition == p2.partition
        assert p1.selfLink == p2.selfLink
        assert hasattr(p2, 'description')
        assert p1.description == p2.description

    def test_policies_collection(self, mgmt_root, profile):
        pc = mgmt_root.tm.security.flowspec_route_injector.profile_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Profile)


class TestNeighbor(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
            name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
        neighbor_lst = p1.neighbor_s
        ERR = "Missing required params"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            neighbor_lst.neighbor.create(name='4.4.4.4', local_address='5.5.5.5', local_as='50')
        assert str(err.value).startswith(ERR)
        p1.delete()

    def test_create_req_arg(self, neighbor):
        n1 = neighbor
        URI = 'https://localhost/mgmt/tm/security/' \
              'flowspec-route-injector/profile/~Common~fake_profile/neighbor/4.4.4.4'
        assert n1.name == '4.4.4.4'
        assert n1.selfLink.startswith(URI)
        assert not hasattr(n1, 'description')

    def test_create_optional_args(self, mgmt_root):
        n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
            name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
        neighbor_lst = p1.neighbor_s
        param_set = {'name': '4.4.4.4', 'local-address': '5.5.5.5', 'local-as': '40', 'remote-as': '50', 'holdTime': '100'}
        n1 = neighbor_lst.neighbor.create(**param_set)
        URI = 'https://localhost/mgmt/tm/security/' \
            'flowspec-route-injector/profile/~Common~fake_profile/neighbor/4.4.4.4'
        assert n1.name == '4.4.4.4'
        assert n1.selfLink.startswith(URI)
        assert n1.kind == 'tm:security:flowspec-route-injector:profile:neighbor:neighborstate'
        assert n1.holdTime == 100
        n1.delete()
        p1.delete()

    def test_refresh(self, neighbor, mgmt_root):
        n1 = neighbor
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.load(
            name='fake_profile', partition='Common')
        neighbor_lst = p1.neighbor_s
        n2 = neighbor_lst.neighbor.load(name='4.4.4.4')
        assert n1.name == n2.name
        assert n1.selfLink == n2.selfLink
        assert n1.kind == n2.kind
        n2.modify(holdTime='50')
        assert n2.holdTime == 50
        n1.refresh()
        assert n1.holdTime == 50

    def test_delete(self, mgmt_root):
        n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
            name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
        neighbor_lst = p1.neighbor_s
        param_set = {'name': '4.4.4.4', 'local-address': '5.5.5.5', 'local-as': '40', 'remote-as': '50', 'holdTime': '100'}
        n1 = neighbor_lst.neighbor.create(**param_set)
        n1.delete()
        with pytest.raises(HTTPError) as err:
            neighbor_lst.neighbor.load(name='4.4.4.4')
        assert err.value.response.status_code == 404
        p1.delete()

    def test_load_no_object(self, mgmt_root):
        n = {'name': '1.1.1.1', 'local-address': '2.2.2.2', 'local-as': '20', 'remote-as': '30'}
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.create(
            name='fake_profile', partition='Common', routeDomain='/Common/0', neighbor=[n])
        neighbor_lst = p1.neighbor_s
        with pytest.raises(HTTPError) as err:
            neighbor_lst.neighbor.load(name='4.4.4.4')
        assert err.value.response.status_code == 404
        p1.delete()

    def test_load_and_update(self, neighbor, mgmt_root):
        n1 = neighbor
        URI = 'https://localhost/mgmt/tm/security/' \
            'flowspec-route-injector/profile/~Common~fake_profile/neighbor/4.4.4.4'
        assert n1.name == '4.4.4.4'
        assert n1.selfLink.startswith(URI)
        n1.holdTime = 100
        n1.update()
        assert n1.holdTime == 100
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.load(
            name='fake_profile', partition='Common')
        neighbor_lst = p1.neighbor_s
        n2 = neighbor_lst.neighbor.load(name='4.4.4.4')
        assert n1.name == n2.name
        assert n1.selfLink == n2.selfLink
        assert n1.kind == n2.kind
        assert n1.holdTime == n2.holdTime

    def test_neighbors_subcollection(self, neighbor, mgmt_root):
        n1 = neighbor
        URI = 'https://localhost/mgmt/tm/security/' \
            'flowspec-route-injector/profile/~Common~fake_profile/neighbor/4.4.4.4'
        assert n1.name == '4.4.4.4'
        assert n1.selfLink.startswith(URI)
        p1 = mgmt_root.tm.security.flowspec_route_injector.profile_s.profile.load(
            name='fake_profile', partition='Common')
        neighbor_lst = p1.neighbor_s
        nc = neighbor_lst.get_collection()
        assert isinstance(nc, list)
        assert len(nc)
        assert isinstance(nc[0], Neighbor)
