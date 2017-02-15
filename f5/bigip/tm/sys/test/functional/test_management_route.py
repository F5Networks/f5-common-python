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

from f5.bigip.resource import MissingRequiredCreationParameter


def setup_management_route_test(request, mgmt_root, name, network, gateway):
    def teardown():
        if mgmt_root.tm.sys.management_routes.management_route.exists(
                name=name):
            mroute = mgmt_root.tm.sys.management_routes.management_route.load(
                name=name)
            mroute.delete()
    request.addfinalizer(teardown)

    mroute1 = mgmt_root.tm.sys.management_routes.management_route.create(
        name=name,
        network=network,
        gateway=gateway)

    return mroute1


class TestMgmtRoute(object):
    def test_missing_required_params(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter) as err:
            mgmt_root.tm.sys.management_routes.management_route.create()
        assert 'Missing required params:' in str(err)

    def test_CDU(self, request, mgmt_root):
        mr1 = setup_management_route_test(request,
                                          mgmt_root,
                                          'testroute',
                                          '192.168.15.0/24',
                                          '10.0.2.1')

        assert mr1.name == 'testroute'
        assert mr1.network == '192.168.15.0/24'
        assert mr1.gateway == '10.0.2.1'

        # Change Gateway
        mr1.gateway = '10.0.2.2'
        mr1.update()
        assert mr1.gateway == '10.0.2.2'

        # Add Description
        assert hasattr(mr1, 'description') is False
        mr1.description = 'my test route'
        mr1.update()
        assert mr1.description == 'my test route'

        # Delete Route
        mr1.delete()
        assert mgmt_root.tm.sys.management_routes.management_route.exists(
            name='testroute') is False
