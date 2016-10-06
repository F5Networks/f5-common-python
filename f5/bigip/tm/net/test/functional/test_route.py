# Copyright 2016 F5 Networks Inc.
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

POOL_NAME = "route-pool"
VLAN_NAME = "route-vlan"
SELF_NAME = "route-self"
SELF_IP = "192.168.100.1/24"
GW_IP = "192.168.100.254"


def delete_resource(resources):
    for resource in resources.get_collection():
        resource.delete()


def setup_route_test(request, bigip, partition, name, network):
    def teardown():
        delete_resource(routes)
        delete_resource(pools)
        delete_resource(selfips)
        delete_resource(vlans)
    request.addfinalizer(teardown)

    # Need to create a VLAN interface, Pool and SelfIP for testing gateways
    pools = bigip.ltm.pools
    pools.pool.create(partition='Common', name=POOL_NAME)

    vlans = bigip.net.vlans
    vlans.vlan.create(partition=partition, name=VLAN_NAME)

    selfips = bigip.net.selfips
    selfips.selfip.create(partition=partition, name=name,
                          address=SELF_IP, vlan=VLAN_NAME)

    routes = bigip.net.routes
    route = routes.route.create(partition=partition, name=name,
                                network=network, blackhole=True)
    return route, routes


class TestRoute(object):
    def test_missing_create_param(self, bigip):
        # Test that the gw types raise an error
        with pytest.raises(MissingRequiredCreationParameter):
            bigip.net.routes.route.create(
                partition='Common', name='test-route',
                network='192.168.1.1/32'
            )
        # Test that the other required args raise an error
        with pytest.raises(MissingRequiredCreationParameter):
            bigip.net.routes.route.create(
                name='test-route', network='192.168.1.1/32', gw='192.168.1.1')

    def test_CURDL(self, request, bigip):
        partition = 'Common'
        name = 'test-route'
        network = '192.168.90.0/24'

        # We assume that setup and teardown will create/delete
        r1, rc1 = setup_route_test(request, bigip, partition, name, network)
        r2 = rc1.route.load(partition=partition, name=name)
        assert r1.name == name
        assert r1.partition == partition
        assert r1.network == network
        assert r1.blackhole is True
        assert r2.name == r1.name
        assert r2.generation == r1.generation

        r1.pool = '/%s/%s' % (partition, POOL_NAME)
        r1.update()
        assert r1.generation > r2.generation

        r2.refresh()
        assert r1.generation == r2.generation
        assert r1.pool == r2.pool

        # Test the other gw types
        r1.tmInterface = "/%s/%s" % (partition, VLAN_NAME)
        r1.update()
        r1.gw = GW_IP
        r1.update()
