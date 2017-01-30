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
def role(mgmt_root):
    role = mgmt_root.shared.authz.roles_s.role.create(
        name="foo-role",
        description="Foo role"
    )
    yield role
    role.delete()


@pytest.fixture
def roles(mgmt_root):
    roles = mgmt_root.shared.authz.roles_s.get_collection()
    return roles


class TestRole(object):
    def test_roles_collection(self, roles):
        assert len(roles) >= 1

    def test_create_role(self, role):
        assert role.name == 'foo-role'
        assert role.description == "Foo role"
