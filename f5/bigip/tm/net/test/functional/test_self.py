# Copyright 2014-2016 F5 Networks Inc.
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
TESTDESCRIPTION = "TESTDESCRIPTION"


def delete_resource(resources):
    for resource in resources.get_collection():
        resource.delete()


def setup_self_test(request, bigip, partition, name,
                    vlan='v1', vlan_partition='Common'):
    def teardown():
        delete_resource(sc1)
        delete_resource(vc1)
    request.addfinalizer(teardown)

    sc1 = bigip.net.selfips
    vc1 = bigip.net.vlans
    vc1.vlan.create(name=vlan, partition=vlan_partition)
    s1 = sc1.selfip.create(
        name=name, partition=partition, address='192.168.101.1/32', vlan='v1')
    return s1, sc1


class TestSelfIP(object):
    def test_create_missing_args(self, request, bigip):
        with pytest.raises(MissingRequiredCreationParameter):
            bigip.net.selfips.selfip.create(name="s1", partition='Common')

    def test_CURDL(self, request, bigip):
        # We will assume that the setup/teardown will test create/delete
        s1, sc1 = setup_self_test(request, bigip, 'Common', 'self1')
        s2 = bigip.net.selfips.selfip.load(
            name=s1.name, partition=s1.partition)
        assert s1.name == 'self1'
        assert s2.name == s1.name
        assert s1.generation == s2.generation

        s1.allowService = ['tcp:0', 'udp:0']
        s1.update()
        assert s1.generation > s2.generation
        assert len(s1.allowService) == 2
        assert 'tcp:0' in s1.allowService
        assert 'udp:0' in s1.allowService
        assert not hasattr(s2, 'allowService')

        s2.refresh()
        assert s1.generation == s2.generation
        assert len(s2.allowService) == 2
        assert 'tcp:0' in s2.allowService
        assert 'udp:0' in s2.allowService


class TestSelfIPCollection(object):
    def test_get_collection(self, request, bigip):
        setup_self_test(request, bigip, 'Common', 'self1')
        sc = bigip.net.selfips
        self_ips = sc.get_collection()
        assert len(self_ips) == 1
        assert self_ips[0].name == 'self1'
