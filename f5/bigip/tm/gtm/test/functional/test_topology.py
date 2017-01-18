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


import pytest

from distutils.version import LooseVersion
from f5.bigip.tm.gtm.topology import Topology
from f5.sdk_exception import InvalidName
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation
from f5.sdk_exception import UnsupportedTmosVersion
from pytest import symbols
from requests.exceptions import HTTPError

pytestmark = pytest.mark.skipif(
    symbols
    and hasattr(symbols, 'modules')
    and not symbols.modules['gtm'],
    reason='The modules symbol for GTM is set to False.'
)

MSG = "Topology record name should contain both 'ldns', 'server' keywords " \
      "with their proper arguments"
NAME = 'ldns: subnet 192.168.100.0/24 server: subnet 192.168.200.0/24'
NAME_SPACES = ' ldns: subnet 192.168.100.0/24  server: subnet 192.168.200.0/24'


def delete_topology(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.topology_s.topology.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_create_test(request, mgmt_root, name):
    def teardown():
        delete_topology(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name):
    def teardown():
        delete_topology(mgmt_root, name)

    top1 = mgmt_root.tm.gtm.topology_s.topology.create(
        name=name)
    request.addfinalizer(teardown)
    return top1


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) <
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs > v12.1.0 TMOS to pass')
class TestCreate(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.gtm.topology_s.topology.create()

    def test_invalid_name_raises(self, mgmt_root):
        with pytest.raises(InvalidName) as err:
            mgmt_root.tm.gtm.topology_s.topology.create(name='fake_wrong')
        assert err.value.message == MSG

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, NAME)
        top1 = mgmt_root.tm.gtm.topology_s.topology.create(
            name=NAME)
        assert top1.name == NAME
        assert top1.score and isinstance(top1.score, int)
        assert top1.kind == 'tm:gtm:topology:topologystate'
        assert top1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/topology/'
            'ldns:%20subnet%20192.168.100.0~24%20'
            'server:%20subnet%20192.168.200.0~24')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, NAME)
        reg1 = mgmt_root.tm.gtm.topology_s.topology.create(
            name=NAME, description='NewFakeTopology')
        assert hasattr(reg1, 'description')
        assert reg1.description == 'NewFakeTopology'

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, NAME)
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.topology_s.topology.create(
                name=NAME)
        assert err.value.response.status_code == 409


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) >=
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs < v12.1.0 TMOS to pass')
class TestCreate_pre_12_1_0(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.gtm.topology_s.topology.create()

    def test_invalid_name_raises(self, mgmt_root):
        with pytest.raises(InvalidName) as err:
            mgmt_root.tm.gtm.topology_s.topology.create(name='fake_wrong')
        assert err.value.message == MSG

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, NAME_SPACES)
        top1 = mgmt_root.tm.gtm.topology_s.topology.create(
            name=NAME_SPACES)
        assert top1.name == NAME_SPACES
        assert top1.score and isinstance(top1.score, int)
        assert top1.kind == 'tm:gtm:topology:topologystate'
        assert top1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/topology/'
            '%20ldns:%20subnet%20192.168.100.0~24%20%20'
            'server:%20subnet%20192.168.200.0~24')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, NAME_SPACES)
        reg1 = mgmt_root.tm.gtm.topology_s.topology.create(
            name=NAME_SPACES, description='NewFakeTopology')
        assert hasattr(reg1, 'description')
        assert reg1.description == 'NewFakeTopology'

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, NAME_SPACES)
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.topology_s.topology.create(
                name=NAME_SPACES)
        assert err.value.response.status_code == 409


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Resource disabled for TMOS 12.0.0')
class TestRefresh(object):
    def test_refresh_raises(self, mgmt_root):
        with pytest.raises(UnsupportedOperation):
            mgmt_root.tm.gtm.topology_s.topology.refresh()


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) <
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs > v12.1.0 TMOS to pass')
class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.topology_s.topology.load(name=NAME)
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, NAME)
        t1 = mgmt_root.tm.gtm.topology_s.topology.load(name=NAME)
        assert t1.name == NAME
        assert t1.kind == 'tm:gtm:topology:topologystate'
        t2 = mgmt_root.tm.gtm.topology_s.topology.load(name=NAME)
        assert t1.kind == t2.kind
        assert t1.selfLink == t2.selfLink


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) >=
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs < v12.1.0 TMOS to pass')
class TestLoad_pre_12_1_0(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.topology_s.topology.load(name=NAME_SPACES)
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, NAME_SPACES)
        t1 = mgmt_root.tm.gtm.topology_s.topology.load(name=NAME_SPACES)
        assert t1.name == NAME_SPACES
        assert t1.kind == 'tm:gtm:topology:topologystate'
        t2 = mgmt_root.tm.gtm.topology_s.topology.load(name=NAME_SPACES)
        assert t1.kind == t2.kind
        assert t1.selfLink == t2.selfLink


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Resource disabled for TMOS 12.0.0')
class TestUpdate(object):
    def test_update_raises(self, mgmt_root):
        with pytest.raises(UnsupportedOperation):
            mgmt_root.tm.gtm.topology_s.topology.update()


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Resource disabled for TMOS 12.0.0')
class TestModify(object):
    def test_modify_raises(self, mgmt_root):
        with pytest.raises(UnsupportedOperation):
            mgmt_root.tm.gtm.topology_s.topology.modify()


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) <
                    '12.1.0', reason='Needs > v12.1.0 TMOS to pass')
class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, NAME)
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.topology_s.topology.load(name=NAME)
        assert err.value.response.status_code == 404


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) >=
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs < v12.1.0 TMOS to pass')
class TestDelete_pre_12_1_0(object):
    def test_delete(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, NAME_SPACES)
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.topology_s.topology.load(name=NAME_SPACES)
        assert err.value.response.status_code == 404


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) <
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs > v12.1.0 TMOS to pass')
class TestTopologyCollection(object):
    def test_region_collection(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, NAME)
        top1 = mgmt_root.tm.gtm.topology_s.topology.create(
            name=NAME)
        assert top1.name == NAME
        assert top1.kind == 'tm:gtm:topology:topologystate'
        assert top1.score and isinstance(top1.score, int)
        assert top1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/topology/'
            'ldns:%20subnet%20192.168.100.0~24%20'
            'server:%20subnet%20192.168.200.0~24')

        rc = mgmt_root.tm.gtm.topology_s.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Topology)


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) >=
                    '12.1.0' or
                    LooseVersion(pytest.config.getoption('--release')) ==
                    '12.0.0', reason='Needs < v12.1.0 TMOS to pass')
class TestTopologyCollection_pre_12_1_0(object):
    def test_region_collection(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, NAME_SPACES)
        top1 = mgmt_root.tm.gtm.topology_s.topology.create(
            name=NAME_SPACES)
        assert top1.name == NAME_SPACES
        assert top1.score and isinstance(top1.score, int)
        assert top1.kind == 'tm:gtm:topology:topologystate'
        assert top1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/topology/'
            '%20ldns:%20subnet%20192.168.100.0~24%20%20'
            'server:%20subnet%20192.168.200.0~24')

        rc = mgmt_root.tm.gtm.topology_s.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Topology)


@pytest.mark.skipif(LooseVersion(pytest.config.getoption('--release')) !=
                    '12.0.0', reason='Only TMOS 12.0.0 test')
class TestTopology_12_0_0(object):
    def test_topology_raises(self, request, mgmt_root):
        with pytest.raises(UnsupportedTmosVersion):
            a = mgmt_root.tm.gtm.topology_s.topology
        del a
