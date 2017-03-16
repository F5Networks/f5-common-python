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
from f5.bigip.tm.security.dos import Application
from f5.bigip.tm.security.dos import Applications
from f5.bigip.tm.security.dos import Dos_Network
from f5.bigip.tm.security.dos import Dos_Networks
from f5.bigip.tm.security.dos import Profile
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeProfile():
    fake_profiles = mock.MagicMock()
    fake_profile = Profile(fake_profiles)
    return fake_profile


def Makeprofile(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.dos.profiles.profile
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/dos/profile/~Common' \
        '~testprofile/'
    return p


class TestDosProfile(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.security.dos.profiles.profile
        r2 = b.tm.security.dos.profiles.profile
        assert r1 is not r2

    def test_create_no_args(self, FakeProfile):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeProfile.create()


class TestApplicationSubcollection(object):
    def test_app_subcollection(self, fakeicontrolsession):
        pc = Applications(Makeprofile(fakeicontrolsession))
        kind = 'tm:security:dos:profile:application:applicationstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Applications)
        assert kind in list(iterkeys(test_meta))
        assert Application in test_meta2

    def test_app_create(self, fakeicontrolsession):
        pc = Applications(Makeprofile(fakeicontrolsession))
        pc2 = Applications(Makeprofile(fakeicontrolsession))
        r1 = pc.application
        r2 = pc2.application
        assert r1 is not r2

    def test_app_create_no_args_v11(self, fakeicontrolsession):
        pc = Applications(Makeprofile(fakeicontrolsession))
        with pytest.raises(MissingRequiredCreationParameter):
            pc.application.create()


class TestDosNetworksSubcollection(object):
    def test_dosnet_subcollection(self, fakeicontrolsession):
        pc = Dos_Networks(Makeprofile(fakeicontrolsession))
        kind = 'tm:security:dos:profile:dos-network:dos-networkstate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Dos_Networks)
        assert kind in list(iterkeys(test_meta))
        assert Dos_Network in test_meta2

    def test_dosnet_create(self, fakeicontrolsession):
        pc = Dos_Networks(Makeprofile(fakeicontrolsession))
        pc2 = Dos_Networks(Makeprofile(fakeicontrolsession))
        r1 = pc.dos_network
        r2 = pc2.dos_network
        assert r1 is not r2

    def test_dosnet_create_no_args_v11(self, fakeicontrolsession):
        pc = Dos_Networks(Makeprofile(fakeicontrolsession))
        with pytest.raises(MissingRequiredCreationParameter):
            pc.dos_network.create()
