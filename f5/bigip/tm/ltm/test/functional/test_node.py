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

from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import NodeStateModifyUnsupported


TESTDESCRIPTION = "TESTDESCRIPTION"


def setup_node_test(request, mgmt_root, partition, name, addr):
    def teardown():
        if mgmt_root.tm.ltm.nodes.node.exists(name=name, partition=partition):
            loaded_node = mgmt_root.tm.ltm.nodes.node.load(
                name=name, partition=partition)
            loaded_node.delete()
    teardown()
    request.addfinalizer(teardown)

    nodes = mgmt_root.tm.ltm.nodes
    node1 = mgmt_root.tm.ltm.nodes.node.create(
        name=name, partition=partition, address=addr)
    return node1, nodes


class TestNode(object):
    def test_create_missing_args(self, mgmt_root):
        n1 = mgmt_root.tm.ltm.nodes.node
        with pytest.raises(MissingRequiredCreationParameter):
            n1.create(name="n1", partition='Common')

    def test_CURDLE(self, request, mgmt_root):
        # We will assume that the setup/teardown will test create/delete
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name=n1.name, partition=n1.partition)
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
        assert mgmt_root.tm.ltm.nodes.node.exists(
            name='node1', partition='Common')
        assert not mgmt_root.tm.ltm.nodes.node.exists(name='node2',
                                                      partition='Common')

    def test_state_update(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.state == 'unchecked'
        n1.state = 'user-down'
        n1.update()
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name='node1', partition='Common')
        assert n2.state == 'user-down'
        assert n2.state == n1.state

    def test_state_update_with_kwargs(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.state == 'unchecked'
        n1.update(state='user-down')
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name='node1', partition='Common')
        assert n2.state == 'user-down'
        assert n2.state == n1.state

    def test_state_update_invalid_value_with_kwargs(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.state == 'unchecked'
        n1.update(state='down')
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name='node1', partition='Common')
        assert n2.state == 'unchecked'
        assert n2.state == n1.state

    def test_state_update_invalid_value(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.state == 'unchecked'
        n1.state = 'down'
        n1.update()
        n2 = mgmt_root.tm.ltm.nodes.node.load(name='node1', partition='Common')
        assert n2.state == 'unchecked'
        assert n2.state == n1.state

    def test_session_update_with_kwargs(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.session == 'user-enabled'
        n1.update(session='user-disabled')
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name='node1', partition='Common')
        assert n2.session == 'user-disabled'
        assert n2.session == n1.session

    def test_session_update_invalid_value_with_kwargs(self, request,
                                                      mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.session == 'user-enabled'
        n1.update(session='monitor-enabled')
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name='node1', partition='Common')
        assert n2.session == 'user-enabled'
        assert n2.session == n1.session

    def test_session_update_invalid_value(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.session == 'user-enabled'
        n1.session = 'monitor-enabled'
        n1.update()
        n2 = mgmt_root.tm.ltm.nodes.node.load(name='node1', partition='Common')
        assert n2.session == 'user-enabled'
        assert n2.session == n1.session

    def test_update_session_state(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.session == 'user-enabled'
        assert n1.state == 'unchecked'
        n1.session = 'user-disabled'
        n1.state = 'user-down'
        n1.update()
        n2 = mgmt_root.tm.ltm.nodes.node.load(name='node1', partition='Common')
        n2.session = 'user-disabled'
        n2.state = 'user-down'
        n2.session = n1.session
        n2.state = n1.state

    def test_update_session_state_kwargs(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        assert n1.session == 'user-enabled'
        assert n1.state == 'unchecked'
        n1.update(session='user-disabled', state='user-down')
        n2 = mgmt_root.tm.ltm.nodes.node.load(name='node1', partition='Common')
        n2.session = 'user-disabled'
        n2.state = 'user-down'
        n2.session = n1.session
        n2.state = n1.state

    def test_update_session_without_state(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '192.168.100.2')
        assert n1.session == 'user-enabled'
        assert n1.state == 'unchecked'
        n1.update(session='user-disabled')
        n2 = mgmt_root.tm.ltm.nodes.node.load(name='node1', partition='Common')
        n2.session = 'user-disabled'
        n2.session = n1.session
        n2.state = n1.state

    def test_state_modify(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '10.10.10.1')
        assert n1.state == 'unchecked'
        n1.modify(state='user-down')
        n2 = mgmt_root.tm.ltm.nodes.node.load(
            name='node1', partition='Common')
        assert n2.state == 'user-down'
        assert n1.state == n2.state

    def test_state_modify_error(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '10.10.10.1')
        with pytest.raises(NodeStateModifyUnsupported) as ex:
            n1.modify(state='down')
        assert "The node resource does not support a" in str(ex.value)

    def test_session_modify_error(self, request, mgmt_root):
        n1, nc1 = setup_node_test(
            request, mgmt_root, 'Common', 'node1', '10.10.10.1')
        with pytest.raises(NodeStateModifyUnsupported) as ex:
            n1.modify(session='monitor-enabled')
        assert "The node resource does not support a" in str(ex.value)


class TestNodes(object):
    def test_get_collection(self, request, mgmt_root):
        setup_node_test(request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        sc = mgmt_root.tm.ltm.nodes
        nodes = sc.get_collection()
        assert len(nodes) >= 1
        assert [n for n in nodes if n.name == 'node1']

    def test_stats(self, request, mgmt_root, opt_release):
        setup_node_test(request, mgmt_root, 'Common', 'node1', '192.168.100.1')
        nodes_stats = mgmt_root.tm.ltm.nodes.stats.load()
        stats_link = 'https://localhost/mgmt/tm/ltm/node/' +\
            '~Common~node1/stats'
        assert stats_link in nodes_stats.entries
        node_nested_stats = nodes_stats.entries[stats_link]['nestedStats']
        assert node_nested_stats['selfLink'] == stats_link+'?ver='+opt_release
        entries = node_nested_stats['entries']
        assert entries['tmName']['description'] == '/Common/node1'
        assert entries['status.enabledState']['description'] == 'enabled'
