# Copyright 2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#


def setup_radius_test(request, mgmt_root):
    def teardown():
        auth_radobj.delete()
        auth_radius_server1.delete()
        auth_radius_server2.delete()
    request.addfinalizer(teardown)

    auth_radius_server1 = mgmt_root.tm.auth.radius_servers.radius_server.create(
        name='system_auth_name1',
        server='172.16.44.20',
        secret='letmein00'
    )
    auth_radius_server2 = mgmt_root.tm.auth.radius_servers.radius_server.create(
        name='system_auth_name2',
        server='172.16.44.21',
        secret='letmein00'
    )

    auth_radobj = mgmt_root.tm.auth.radius_s.radius.create(
        name='system-auth',
        servers=['system_auth_name1']
        )
    return auth_radobj


class TestRadius(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        rad1 = setup_radius_test(request, mgmt_root)
        rad2 = mgmt_root.tm.auth.radius_s.radius.load(name='system-auth')
        assert rad1.name == rad2.name

        # Update
        rad1.servers = ['system_auth_name1', 'system_auth_name2']
        rad1.update()
        assert len(rad1.servers) != len(rad2.servers)

        # Refresh
        rad2.refresh()
        assert len(rad1.servers) == len(rad2.servers)
