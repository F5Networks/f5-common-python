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
from f5.bigip.tm.security.blacklist_publisher import Category
from f5.bigip.tm.security.blacklist_publisher import Profile
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeBlProfile():
    fake_col = mock.MagicMock()
    fake_profile = Profile(fake_col)
    return fake_profile


@pytest.fixture
def FakeBlCategory():
    fake_col = mock.MagicMock()
    fake_profile = Category(fake_col)
    return fake_profile


class TestBlProfile(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        bl_p1 = b.tm.security.blacklist_publisher.profile_s.profile
        bl_p2 = b.tm.security.blacklist_publisher.profile_s.profile
        assert bl_p1 is not bl_p2

    def test_create_no_args(self, FakeBlProfile):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeBlProfile.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.blacklist_publisher.profile_s.profile.create(
                name='Fake')


class TestBlCategory(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        bl_p1 = b.tm.security.blacklist_publisher.category_s.category
        bl_p2 = b.tm.security.blacklist_publisher.category_s.category
        assert bl_p1 is not bl_p2

    def test_create_no_args(self, FakeBlCategory):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeBlCategory.create()

    def test_create_mandatory_args_missing(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        with pytest.raises(MissingRequiredCreationParameter):
            b.tm.security.blacklist_publisher.category_s.category.create(
                name='Fake')
