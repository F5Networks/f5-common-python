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
from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.gtm.listener import Listener
from f5.bigip.tm.gtm.listener import Profile


@pytest.fixture
def FakeListener():
    fake_list_s = mock.MagicMock()
    fake_list = Listener(fake_list_s)
    return fake_list


@pytest.fixture
def FakeProfile():
    fake_prof_s = mock.MagicMock()
    fake_prof = Profile(fake_prof_s)
    return fake_prof


class TestListener(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        r1 = b.tm.gtm.listeners.listener
        r2 = b.tm.gtm.listeners.listener
        assert r1 is not r2

    def test_create_no_args(self, FakeListener):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeListener.create()

    def test_create_partition(self, FakeListener):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeListener.create(name='fake_listener')


class TestProfile(object):
    def test_create_raises(self, FakeProfile):
        with pytest.raises(UnsupportedOperation):
            FakeProfile.create()

    def test_delete_raises(self, FakeProfile):
        with pytest.raises(UnsupportedOperation):
            FakeProfile.delete()

    def test_modify_raises(self, FakeProfile):
        with pytest.raises(UnsupportedOperation):
            FakeProfile.modify()

    def test_update_raises(self, FakeProfile):
        with pytest.raises(UnsupportedOperation):
            FakeProfile.update()
