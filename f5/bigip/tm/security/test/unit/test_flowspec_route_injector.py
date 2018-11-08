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
from f5.bigip.tm.security.flowspec_route_injector import Neighbor
from f5.bigip.tm.security.flowspec_route_injector import Neighbor_s
from f5.bigip.tm.security.flowspec_route_injector import Profile
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeProfile():
    fake_col = mock.MagicMock()
    fake_profile = Profile(fake_col)
    return fake_profile


def MakeFlowspecProfile(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.flowspec_route_injector.profile_s.profile
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/flowspec-route-injector/profile/' \
        '~Common~fakeprofile/'
    return p


class TestProfile(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.security.flowspec_route_injector.profile_s.profile
        p2 = b.tm.security.flowspec_route_injector.profile_s.profile
        assert p1 is not p2

    def test_create_no_arguments(self, FakeProfile):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeProfile.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.flowspec_route_injector.profile_s.profile.create(
                name='Fake')


class TestProfileNeighborSubCollection(object):
    def test_profile_neighbor_subcollection(self, fakeicontrolsession):
        pc = Neighbor_s(MakeFlowspecProfile(fakeicontrolsession))
        kind = 'tm:security:flowspec-route-injector:profile:neighbor:neighborstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Neighbor_s)
        assert kind in list(iterkeys(test_meta))
        assert Neighbor in test_meta2
