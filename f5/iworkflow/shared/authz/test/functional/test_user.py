# Copyright 2015-2106 F5 Networks Inc.
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


@pytest.fixture(scope="module")
def user(mgmt_root):
    user = mgmt_root.shared.authz.users_s.user.create(
        name="foo1",
        password="default",
        displayName="Foo user",
        shell="/usr/bin/tmsh"
    )
    yield user
    user.delete()


@pytest.fixture
def users(mgmt_root):
    users = mgmt_root.shared.authz.users_s.get_collection()
    return users


class TestUser(object):
    def test_users_collection(self, users):
        # There may be 2 users (like when running in vagrant)
        # or only 1 user (like if running in openstack)
        assert len(users) >= 1

    def test_create_user(self, user):
        assert user.name == 'foo1'
        assert user.displayName == "Foo user"
        assert user.shell == "/usr/bin/tmsh"
