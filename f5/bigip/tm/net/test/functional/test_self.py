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
from requests import HTTPError

from f5.sdk_exception import MissingRequiredCreationParameter
TESTDESCRIPTION = "TESTDESCRIPTION"


def delete_selfip(mgmt_root, name, partition):
    try:
        s = mgmt_root.tm.net.selfips.selfip.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    s.delete()


def delete_vlan(mgmt_root, name, partition):
    try:
        s = mgmt_root.tm.net.vlans.vlan.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    s.delete()


def setup_self_test(request, mgmt_root, partition, name,
                    vlan='v1', vlan_partition='Common'):
    def teardown():
        delete_selfip(mgmt_root, name, partition)
        delete_vlan(mgmt_root, 'v1', 'Common')
    request.addfinalizer(teardown)

    sc1 = mgmt_root.tm.net.selfips
    vc1 = mgmt_root.tm.net.vlans
    vc1.vlan.create(name=vlan, partition=vlan_partition)
    s1 = sc1.selfip.create(
        name=name, partition=partition, address='192.168.101.1/32', vlan='v1')
    return s1, sc1


class TestSelfIP(object):
    def test_create_missing_args(self, request, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.net.selfips.selfip.create(name="s1", partition='Common')

    def test_CURDL(self, request, mgmt_root):
        # We will assume that the setup/teardown will test create/delete
        s1, sc1 = setup_self_test(request, mgmt_root, 'Common', 'self1')
        s2 = mgmt_root.tm.net.selfips.selfip.load(
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
    def test_get_collection(self, request, mgmt_root):
        setup_self_test(request, mgmt_root, 'Common', 'self1')
        sc = mgmt_root.tm.net.selfips
        self_ips = sc.get_collection()
        assert len(self_ips) >= 1
        assert self_ips[0].name == 'self1'
