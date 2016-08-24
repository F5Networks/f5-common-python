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

import copy
import pytest

from f5.bigip.tm.gtm.server import Server
from f5.bigip.tm.gtm.server import Virtual_Servers
from requests.exceptions import HTTPError


def delete_server(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.servers.server.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def delete_dc(mgmt_root, name, partition):
    try:
        delete_server(mgmt_root, 'fake_serv1')
        foo = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name=name, partition=partition
        )
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def create_dc(request, mgmt_root, name, partition):
    def teardown():
        delete_dc(mgmt_root, name, partition)

    delete_dc(mgmt_root, name, partition)
    dc = mgmt_root.tm.gtm.datacenters.datacenter.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return dc


def setup_create_test(request, mgmt_root, name, partition):
    def teardown():
        delete_server(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_server(mgmt_root, name)

    delete_dc(mgmt_root, 'dc1', partition)
    dc = create_dc(request, mgmt_root, 'dc1', partition)
    serv1 = mgmt_root.tm.gtm.servers.server.create(
        name=name, datacenter=dc.name,
        addresses=[{'name': '1.1.1.1'}])
    request.addfinalizer(teardown)
    return serv1


def delete_vs(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.servers.server.load(
            name='fake_serv1').virtual_servers_s.virtual_servers.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_vs_basic_test(request, mgmt_root, name, destination):
    def teardown():
        delete_vs(mgmt_root, name)

    s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
    vs = s1.virtual_servers_s.virtual_servers.create(
        name=name, destination=destination)
    request.addfinalizer(teardown)
    return vs


def setup_create_vs_test(request, mgmt_root, name):
    def teardown():
        delete_vs(mgmt_root, name)

    request.addfinalizer(teardown)


class TestCreate(object):
    def test_create_req_arg(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_serv1', 'Common')
        dc = create_dc(request, mgmt_root, 'dc1', 'Common')
        serv1 = mgmt_root.tm.gtm.servers.server.create(
            name='fake_serv1', datacenter=dc.name,
            addresses=[{'name': '1.1.1.1'}])
        assert serv1.name == 'fake_serv1'
        assert serv1.generation and isinstance(serv1.generation, int)
        assert serv1.kind == 'tm:gtm:server:serverstate'
        assert serv1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/server/fake_serv1')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_serv1', 'Common')
        dc = create_dc(request, mgmt_root, 'dc1', 'Common')
        serv1 = mgmt_root.tm.gtm.servers.server.create(
            name='fake_serv1', datacenter=dc.name,
            addresses=[{'name': '1.1.1.1'}],
            iqAllowPath='no', enabled=False, disabled=True)
        assert serv1.disabled is True
        assert not hasattr(serv1, 'enabled')
        assert serv1.iqAllowPath == 'no'

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.servers.server.create(
                name='fake_serv1', datacenter='dc1',
                addresses=[{'name': '1.1.1.1'}])
            assert err.response.status_code == 400


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        s2 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')

        assert s1.iqAllowPath == 'yes'
        assert s2.iqAllowPath == 'yes'

        s2.update(iqAllowPath='no')
        assert s1.iqAllowPath == 'yes'
        assert s2.iqAllowPath == 'no'

        s1.refresh()
        assert s1.iqAllowPath == 'no'


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.servers.server.load(
                name='fake_serv1')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        assert s1.enabled is True
        s1.enabled = False
        s1.disabled = True
        s1.update()
        s2 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        assert not hasattr(s1, 'enabled')
        assert hasattr(s2, 'disabled')
        assert s2.disabled is True


class Test_Update_Modify(object):
    def test_update(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        assert s1.iqAllowPath == 'yes'
        s1.update(iqAllowPath='no')
        assert s1.iqAllowPath == 'no'

    def test_modify(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        original_dict = copy.copy(s1.__dict__)
        iqpath = 'iqAllowPath'
        s1.modify(iqAllowPath='no')
        for k, v in original_dict.items():
            if k != iqpath:
                original_dict[k] = s1.__dict__[k]
            elif k == iqpath:
                assert s1.__dict__[k] == 'no'


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        s1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
            assert err.response.status_code == 404


class TestServerCollection(object):
    def test_server_collection(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        assert s1.name == 'fake_serv1'
        assert s1.generation and isinstance(s1.generation, int)
        assert s1.fullPath == 'fake_serv1'
        assert s1.kind == 'tm:gtm:server:serverstate'
        assert s1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/server/fake_serv1')

        sc = mgmt_root.tm.gtm.servers.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Server)


class TestVirtualServerSubCollection(object):
    def test_create_req_arg(self, request, mgmt_root):
        setup_create_vs_test(request, mgmt_root, 'vs1')
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        vs = s1.virtual_servers_s
        vs1 = vs.virtual_servers.create(name='vs1', destination='5.5.5.5:80')
        assert vs1.name == 'vs1'
        assert vs1.generation and isinstance(vs1.generation, int)
        assert vs1.kind == 'tm:gtm:server:virtual-servers:virtual-serversstate'
        assert vs1.selfLink.startswith('https://localhost/mgmt/tm/gtm/server/'
                                       'fake_serv1/virtual-servers/vs1')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_vs_test(request, mgmt_root, 'vs1')
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        vs = s1.virtual_servers_s
        vs1 = vs.virtual_servers.create(name='vs1',
                                        destination='5.5.5.5:80',
                                        description='FancyFakeVS',
                                        limitMaxBpsStatus='enabled',
                                        limitMaxBps=1337)
        assert vs1.name == 'vs1'
        assert vs1.description == 'FancyFakeVS'
        assert vs1.limitMaxBps == 1337

    def test_create_duplicate(self, request, mgmt_root):
        setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        try:
            s1.virtual_servers_s.virtual_servers.create(
                name='vs1', destination='5.5.5.5:80')
        except HTTPError as err:
            assert err.response.status_code == 409

    def test_refresh(self, request, mgmt_root):
        setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        vs1 = s1.virtual_servers_s.virtual_servers.load(name='vs1')
        vs2 = s1.virtual_servers_s.virtual_servers.load(name='vs1')

        assert vs1.limitMaxBpsStatus == 'disabled'
        assert vs2.limitMaxBpsStatus == 'disabled'

        vs2.update(limitMaxBpsStatus='enabled')
        assert vs1.limitMaxBpsStatus == 'disabled'
        assert vs2.limitMaxBpsStatus == 'enabled'

        vs1.refresh()
        assert vs2.limitMaxBpsStatus == 'enabled'

    def test_load_no_object(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
        try:
            s1.virtual_servers_s.virtual_servers.load(name='vs1')
        except HTTPError as err:
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        vs1 = s1.virtual_servers_s.virtual_servers.load(name='vs1')
        assert vs1.name == 'vs1'
        assert vs1.limitMaxBpsStatus == 'disabled'

        vs1.limitMaxBpsStatus = 'enabled'
        vs1.update()
        vs2 = s1.virtual_servers_s.virtual_servers.load(name='vs1')
        assert vs2.name == 'vs1'
        assert vs2.limitMaxBpsStatus == 'enabled'

    def test_update(self, request, mgmt_root):
        vs1 = setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        assert vs1.limitMaxBpsStatus == 'disabled'
        vs1.update(limitMaxBpsStatus='enabled')
        assert vs1.limitMaxBpsStatus == 'enabled'

    def test_modify(self, request, mgmt_root):
        vs1 = setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        original_dict = copy.copy(vs1.__dict__)
        limit = 'limitMaxBpsStatus'
        vs1.modify(limitMaxBpsStatus='enabled')
        for k, v in original_dict.items():
            if k != limit:
                original_dict[k] = vs1.__dict__[k]
            elif k == limit:
                assert vs1.__dict__[k] == 'enabled'

    def test_delete(self, request, mgmt_root):
        vs1 = setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        vs1.delete()
        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        try:
            s1.virtual_servers_s.virtual_servers.load(name='vs1')
        except HTTPError as err:
                assert err.response.status_code == 404

    def test_virtual_server_collection(self, request, mgmt_root):
        vs1 = setup_vs_basic_test(request, mgmt_root, 'vs1', '5.5.5.5:80')
        assert vs1.name == 'vs1'
        assert vs1.generation and isinstance(vs1.generation, int)
        assert vs1.kind == 'tm:gtm:server:virtual-servers:virtual-serversstate'
        assert vs1.selfLink.startswith('https://localhost/mgmt/tm/gtm/server/'
                                       'fake_serv1/virtual-servers/vs1')

        s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
        vsc = s1.virtual_servers_s.get_collection()
        assert isinstance(vsc, list)
        assert len(vsc)
        assert isinstance(vsc[0], Virtual_Servers)
