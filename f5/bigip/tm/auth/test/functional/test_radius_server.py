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

from distutils.version import LooseVersion
import pytest


def setup_radius_server_test(request, mgmt_root):
    def teardown():
        auth_radius_server1.delete()
    request.addfinalizer(teardown)

    auth_radius_server1 = mgmt_root.tm.auth.radius_servers.radius_server.create(
        name='system_auth_name1',
        server='172.16.44.20',
        secret='letmein00'
    )
    return auth_radius_server1


class TestRadiusServer(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        radsrv1 = setup_radius_server_test(request, mgmt_root)
        radsrv2 = mgmt_root.tm.auth.radius_servers.radius_server.load(
            name='system_auth_name1'
        )
        assert radsrv1.name == radsrv2.name

        if not LooseVersion(
            pytest.config.getoption('--release')
        ) <= LooseVersion('12.0.0'):
            # Update
            radsrv1.server = '172.16.44.21'
            radsrv1.update()
            assert radsrv1.server != radsrv2.server

            # Refresh
            radsrv2.refresh()
            assert radsrv1.server == radsrv2.server
