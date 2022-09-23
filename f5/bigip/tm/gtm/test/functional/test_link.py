# Copyright 2018 F5 Networks Inc.
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

# from distutils.version import LooseVersion
from f5.bigip.tm.gtm.link import Link
from requests.exceptions import HTTPError


def delete_link(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.links.link.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def delete_dc(mgmt_root, name, partition):
    try:
        delete_link(mgmt_root, 'fake_link1')
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

    # this line is to clean up any object that might have been left by
    # previous test
    delete_dc(mgmt_root, name, partition)

    dc = mgmt_root.tm.gtm.datacenters.datacenter.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return dc


def setup_create_test(request, mgmt_root, name):
    def teardown():
        delete_link(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_link(mgmt_root, name)

    # this line is to clean up any object that might have been left by
    # previous test
    delete_dc(mgmt_root, 'dc1', partition)

    dc = create_dc(request, mgmt_root, 'dc1', partition)
    link1 = mgmt_root.tm.gtm.links.link.create(
        name=name, datacenter=dc.name,
        routerAddresses=[{'name': '1.1.1.2'}])
    request.addfinalizer(teardown)
    return link1


class TestCreate(object):
    def test_create_req_arg(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_link1')
        dc = create_dc(request, mgmt_root, 'dc1', 'Common')
        link1 = mgmt_root.tm.gtm.links.link.create(
            name='fake_link1', datacenter=dc.name,
            routerAddresses=[{'name': '1.1.1.2'}])

        assert link1.name == 'fake_link1'
        assert link1.generation and isinstance(link1.generation, int)
        assert link1.kind == 'tm:gtm:link:linkstate'
        assert '/mgmt/tm/gtm/link/~Common~fake_link1' in link1.selfLink

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_link1')
        dc = create_dc(request, mgmt_root, 'dc1', 'Common')
        link1 = mgmt_root.tm.gtm.links.link.create(
            name='fake_link1', datacenter=dc.name,
            routerAddresses=[{'name': '1.1.1.2'}],
            duplexBilling='disabled')

        assert link1.duplexBilling == 'disabled'

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_link1', 'Common')
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.links.link.create(
                name='fake_link1', datacenter='dc1',
                routerAddresses=[{'name': '1.1.1.2'}])
        assert err.value.response.status_code == 409


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_link1', 'Common')
        l1 = mgmt_root.tm.gtm.links.link.load(name='fake_link1')
        l2 = mgmt_root.tm.gtm.links.link.load(name='fake_link1')

        assert l1.linkRatio == 1
        assert l2.linkRatio == 1

        l2.update(linkRatio=2)
        assert l1.linkRatio == 1
        assert l2.linkRatio == 2

        l1.refresh()
        assert l1.linkRatio == 2


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.links.link.load(
                name='fake_link1')
        assert err.value.response.status_code == 404

    # @pytest.mark.skipif(
    #     LooseVersion(pytest.config.getoption('--release')) == '11.5.4',
    #     reason='Needs > v11.5.4 TMOS to pass'
    # )
    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_link1', 'Common')
        l1 = mgmt_root.tm.gtm.links.link.load(name='fake_link1')
        assert l1.enabled is True
        l1.enabled = False
        l1.disabled = True
        l1.update()
        l2 = mgmt_root.tm.gtm.links.link.load(name='fake_link1')
        assert not hasattr(l1, 'enabled')
        assert hasattr(l2, 'disabled')
        assert l2.disabled is True

    # @pytest.mark.skipif(
    #     LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('11.6.0'),
    #     reason='This test is for 11.5.4 or less.'
    # )
    # def test_load_11_5_4_and_less(self, request, mgmt_root):
    #     setup_basic_test(request, mgmt_root, 'fake_serv1', 'Common')
    #     s1 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
    #     assert s1.enabled is True
    #     s1.enabled = False
    #     s1.update()
    #     s2 = mgmt_root.tm.gtm.servers.server.load(name='fake_serv1')
    #     assert hasattr(s2, 'enabled')
    #     assert s2.enabled is True


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        l1 = setup_basic_test(request, mgmt_root, 'fake_link1', 'Common')
        l1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.links.link.load(name='fake_link1')
        assert err.value.response.status_code == 404


class TestLinkCollection(object):
    def test_link_collection(self, request, mgmt_root):
        l1 = setup_basic_test(request, mgmt_root, 'fake_link1', 'Common')

        assert l1.name == 'fake_link1'
        assert l1.generation and isinstance(l1.generation, int)
        assert l1.kind == 'tm:gtm:link:linkstate'
        assert '/mgmt/tm/gtm/link/' in l1.selfLink

        lc = mgmt_root.tm.gtm.links.get_collection()
        assert isinstance(lc, list)
        assert len(lc)
        assert isinstance(lc[0], Link)
