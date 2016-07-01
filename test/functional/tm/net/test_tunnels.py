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

from requests.exceptions import HTTPError


TEST_DESCR = "TEST DESCRIPTION"


def delete_resource(resource):
    try:
        resource.delete()
    except HTTPError as err:
        if err.response.status_code != 404:
            raise


def setup_tunnel_test(request, bigip, name, partition, ip, profile):
    def teardown():
        delete_resource(tunnel)
    request.addfinalizer(teardown)

    tunnel = bigip.net.tunnels_s.tunnels.tunnel.create(
        name=name, partition=partition, localAddress=ip, profile=profile)
    return tunnel


def setup_gre_test(request, bigip, name, partition):
    def teardown():
        delete_resource(gre)
    request.addfinalizer(teardown)

    gre = bigip.net.tunnels_s.gres.gre.create(
        name=name, partition=partition)
    return gre


def setup_vxlan_test(request, bigip, name, partition):
    def teardown():
        delete_resource(vxlan)
    request.addfinalizer(teardown)

    vxlan = bigip.net.tunnels_s.vxlans.vxlan.create(
        name=name, partition=partition)
    return vxlan


class TestTunnels(object):
    def test_tunnel_list(self, bigip):
        tunnels = bigip.net.tunnels_s.tunnels.get_collection()
        assert len(tunnels)
        for tunnel in tunnels:
            assert tunnel.generation


class TestTunnel(object):
    def test_tunnel_CURDL(self, request, bigip):
        # Create and Delete are tested by the setup/teardown
        t1 = setup_tunnel_test(
            request, bigip, 'tunnel-test', 'Common',
            '192.168.1.1', '/Common/gre'
        )

        # Load
        t2 = bigip.net.tunnels_s.tunnels.tunnel.load(
            name='tunnel-test', partition='Common')
        assert t1.name == 'tunnel-test'
        assert t1.name == t2.name
        assert t1.generation == t2.generation

        # Update
        t1.description = TEST_DESCR
        t1.update()
        assert t1.description == TEST_DESCR
        assert t1.generation > t2.generation

        # Refresh
        t2.refresh()
        assert t2.description == TEST_DESCR
        assert t1.generation == t2.generation


class TestGre(object):
    def test_gre_CURDL(self, request, bigip):
        # Create and Delete are tested by the setup/teardown
        g1 = setup_gre_test(request, bigip, 'gre-test', 'Common')
        assert g1.name == 'gre-test'

        # Load
        g2 = bigip.net.tunnels_s.gres.gre.load(
            name='gre-test', partition='Common')
        assert g1.name == g2.name
        assert g1.generation == g2.generation

        # Update
        g1.description = TEST_DESCR
        g1.update()
        assert g1.description == TEST_DESCR
        assert g1.generation > g2.generation

        # Refresh
        g2.refresh()
        assert g2.description == g1.description
        assert g2.generation == g1.generation


class TestVxlan(object):
    def test_vxlan_CURDL(self, request, bigip):
        # Create and Delete are tested by the setup/teardown
        vx1 = setup_vxlan_test(request, bigip, 'vxlan-test', 'Common')
        assert vx1.name == 'vxlan-test'

        # Load
        vx2 = bigip.net.tunnels_s.vxlans.vxlan.load(
            name='vxlan-test', partition='Common')
        assert vx1.name == vx2.name
        assert vx1.generation == vx2.generation

        # Update
        vx1.description = TEST_DESCR
        vx1.update()
        assert vx1.description == TEST_DESCR
        assert vx1.generation > vx2.generation

        # Refresh
        vx2.refresh()
        assert vx2.description == vx1.description
        assert vx2.generation == vx1.generation
