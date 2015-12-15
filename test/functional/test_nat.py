# Copyright 2015 F5 Networks Inc.
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

from f5.bigip import exceptions
import pytest
from requests.exceptions import HTTPError

# Test assumptions:
#
# NAT#_IP_ADDR needs to be on a valid cidr assigned to the "external"
#   (client-facing) interface on your BIGIP
# NAT#_ORIG_IP_ADDR needs to be on a valid cidr assigned to the "internal"
#   (server-facing) interface on your BIGIP
#
# The following tests work when creating a VE via HEAT in the Boulder lab using
# ve_openstack_test.yaml.

nat1 = {
    'name': 'foo',
    'vlan_name': 'external',
    'ip_address': '10.2.2.100',
    'orig_ip_address': '10.2.3.100'
}

nat2 = {
    'name': 'bar',
    'vlan_name': 'external',
    'ip_address': '10.2.2.101',
    'orig_ip_address': '10.2.3.101'
}

# TBD: set to True once we figure out how to create a new partition
multi_partition = False

nat_default_folder = 'Common'
nat_other_folder = 'Uncommon' if multi_partition else nat_default_folder


def setup_standard_test(request, bigip):
    def teardown():
        bigip.ltm.nat.delete(nat1['name'])
        assert not bigip.ltm.nat.exists(nat1['name'])
        bigip.ltm.nat.delete(nat2['name'])
        assert not bigip.ltm.nat.exists(nat2['name'])
        if multi_partition:
            bigip.ltm.nat.delete(nat2['name'], nat_other_folder)
            assert not bigip.ltm.nat.exists(nat2['name'], nat_other_folder)
    request.addfinalizer(teardown)

    bigip.ltm.nat.create(nat1['name'], nat1['ip_address'],
                         nat1['orig_ip_address'])
    assert bigip.ltm.nat.exists(nat1['name'])


def setup_multi_nat_test(request, bigip):
    setup_standard_test(request, bigip)

    # create with all parameters, same name but in different folders
    bigip.ltm.nat.create(nat2['name'],
                         nat2['ip_address'],
                         nat2['orig_ip_address'],
                         "traffic-group-1",
                         nat2['vlan_name'],
                         nat_default_folder)
    assert bigip.ltm.nat.exists(nat2['name'])
    if multi_partition:
        bigip.ltm.nat.create(nat2['name'],
                             nat2['ip_address'],
                             nat2['orig_ip_address'],
                             "traffic-group-1",
                             nat2['vlan_name'],
                             nat_other_folder)
        assert bigip.ltm.nat.exists(nat2['name'], nat_other_folder)


def test_nat_create_and_delete_one(request, bigip):
    assert bigip.ltm.nat.create(nat1['name'],
                                nat1['ip_address'],
                                nat1['orig_ip_address'])
    assert bigip.ltm.nat.exists(nat1['name'])

    assert bigip.ltm.nat.delete(nat1['name'])
    assert not bigip.ltm.nat.exists(nat1['name'])


def test_nat_create_and_delete_two(request, bigip):
    setup_multi_nat_test(request, bigip)

    bigip.ltm.nat.delete_all()
    assert not bigip.ltm.nat.exists(nat1['name'])
    assert not bigip.ltm.nat.exists(nat2['name'])


def test_nat_getters(request, bigip):
    setup_multi_nat_test(request, bigip)

    # test that a single ip_addr can be fetched
    assert bigip.ltm.nat.get_addr(nat1['name']) == nat1['ip_address']

    # test that a single orig_ip_addr can be fetched
    assert(bigip.ltm.nat.get_original_addr(nat1['name']) ==
           nat1['orig_ip_address'])

    # test that a single vlan can be fetched
    exp_vlan_name = '/%s/%s' % (nat_default_folder, nat2['vlan_name'])
    assert bigip.ltm.nat.get_vlan(nat2['name'])[0] == exp_vlan_name


def test_nat_gat_nats(request, bigip):
    setup_multi_nat_test(request, bigip)

    # test that all nats can be fetched
    nats = bigip.ltm.nat.get_nats()
    if len(nats) != 2 or nat1['name'] not in nats or nat2['name'] not in nats:
        raise exceptions.NATCreationException
    if multi_partition:
        nats = bigip.ltm.nat.get_nats(folder=nat_other_folder)
        if len(nats) != 1 or nat2['name'] not in nats:
            raise exceptions.NATCreationException


def test_nat_get_addrs(request, bigip):
    setup_multi_nat_test(request, bigip)

    # test that all ip_addrs can be fetched
    addrs = bigip.ltm.nat.get_addrs()
    if len(addrs) != 2:
        raise exceptions.NATCreationException
    if multi_partition:
        addrs = bigip.ltm.nat.get_addrs(nat_other_folder)
        if len(addrs) != 1:
            raise exceptions.NATCreationException


def test_nat_get_original_addrs(request, bigip):
    setup_multi_nat_test(request, bigip)

    # test that all orig_ip_addrs can be fetched
    addrs = bigip.ltm.nat.get_original_addrs()
    if len(addrs) != 2:
        raise exceptions.NATCreationException
    if multi_partition:
        addrs = bigip.ltm.nat.get_original_addrs(nat_other_folder)
        if len(addrs) != 1:
            raise exceptions.NATCreationException


def test_nat_create_duplicate_name(request, bigip):
    setup_standard_test(request, bigip)
    # create duplicate by name
    with pytest.raises(HTTPError):
        bigip.ltm.nat.create(name=nat1['name'],
                             ip_address=nat2['ip_address'],
                             orig_ip_address=nat2['orig_ip_address'])
    assert bigip.ltm.nat.exists(name=nat1['name'])


def test_nat_create_duplicate_ip_addr(request, bigip):
    setup_standard_test(request, bigip)
    # create duplicate by ip_address
    with pytest.raises(HTTPError):
        bigip.ltm.nat.create(name=nat2['name'],
                             ip_address=nat1['ip_address'],
                             orig_ip_address=nat2['orig_ip_address'])
    assert not bigip.ltm.nat.exists(name=nat2['name'])


def test_nat_create_duplicate_orig_addr(request, bigip):
    setup_standard_test(request, bigip)
    # create duplicate by orig_ip_address
    with pytest.raises(HTTPError):
        bigip.ltm.nat.create(name=nat2['name'],
                             ip_address=nat2['ip_address'],
                             orig_ip_address=nat1['orig_ip_address'])
    assert not bigip.ltm.nat.exists(name=nat2['name'])
