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


TESTDESCRIPTION = "TESTDESCRIPTION"


def setup_node_test(request, bigip, partition, name, addr):
    def teardown():
        node1.delete()
    request.addfinalizer(teardown)

    nodes = bigip.ltm.nodes
    node1 = bigip.ltm.nodes.node.create(
        name=name, partition=partition, address=addr)
    return node1, nodes


class TestNode(object):
    def test_create_missing_args(self, bigip):
        n1 = bigip.ltm.nodes.node
        with pytest.raises(MissingRequiredCreationParameter):
            n1.create(name="n1", partition='Common')

    def test_CURDLE(self, request, bigip):
        # We will assume that the setup/teardown will test create/delete
        n1, nc1 = setup_node_test(
            request, bigip, 'Common', 'node1', '192.168.100.1')
        n2 = bigip.ltm.nodes.node.load(name=n1.name, partition=n1.partition)
        assert n1.name == 'node1'
        assert n2.name == n1.name
        assert n1.generation == n2.generation

        n1.description = TESTDESCRIPTION
        n1.update()
        assert n1.generation > n2.generation
        assert n1.description == TESTDESCRIPTION
        assert not hasattr(n2, 'description')

        n2.refresh()
        assert n1.generation == n2.generation
        assert n2.description == n1.description

        # Exists
        assert bigip.ltm.nodes.node.exists(name='node1', partition='Common')
        assert not bigip.ltm.nodes.node.exists(name='node2',
                                               partition='Common')


class TestNodes(object):
    def test_get_collection(self, request, bigip):
        setup_node_test(request, bigip, 'Common', 'node1', '192.168.100.1')
        sc = bigip.ltm.nodes
        nodes = sc.get_collection()
        assert len(nodes) >= 1
        assert [n for n in nodes if n.name == 'node1']
