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

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.gtm.datacenter import Datacenter
from pytest import symbols
from requests.exceptions import HTTPError

pytestmark = pytest.mark.skipif(
    symbols
    and hasattr(symbols, 'modules')
    and not symbols.modules['gtm'],
    reason='The modules symbol for GTM is set to False.'
)


def delete_dc(mgmt_root, name, partition):
    try:
        foo = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name=name, partition=partition
        )
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_create_test(request, mgmt_root, name, partition):
    def teardown():
        delete_dc(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_dc(mgmt_root, name, partition)

    dc1 = mgmt_root.tm.gtm.datacenters.datacenter.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return dc1


class TestCreate(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.gtm.datacenters.datacenter.create()

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'dc1', 'Common')
        dc1 = mgmt_root.tm.gtm.datacenters.datacenter.create(
            name='dc1', partition='Common')
        assert dc1.name == 'dc1'
        assert dc1.partition == 'Common'
        assert dc1.generation and isinstance(dc1.generation, int)
        assert dc1.kind == 'tm:gtm:datacenter:datacenterstate'
        assert dc1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/datacenter/~Common~dc1')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'dc1', 'Common')
        dc1 = mgmt_root.tm.gtm.datacenters.datacenter.create(
            name='dc1',
            partition='Common',
            enabled=False,
            contact="admin@root.local",
            description="A datacenter is fine too",
            location="Between the earth and the moon")
        assert dc1.enabled is False
        assert "admin@root.local" == dc1.contact
        assert "A datacenter is fine too" == dc1.description
        assert "Between the earth and the moon" == dc1.location

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'dc1', 'Common')
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.datacenters.datacenter.create(
                name='dc1', partition='Common')
            assert err.response.status_code == 400


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'dc1', 'Common')
        d1 = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name='dc1', partition='Common')
        d2 = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name='dc1', partition='Common')
        assert d1.enabled is True
        assert d2.enabled is True

        d2.update(enabled=False)
        assert d2.enabled is False
        assert d1.enabled is True

        d1.refresh()
        assert d1.enabled is False


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.datacenters.datacenter.load(
                name='dc1', partition='Common')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'dc1', 'Common')
        dc1 = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name='dc1', partition='Common')
        assert dc1.enabled is True
        dc1.update(enabled=False)
        dc2 = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name='dc1', partition='Common')
        assert dc1.enabled is False
        assert dc2.enabled is False


class TestUpdate(object):
    def test_update(self, request, mgmt_root):
        dc1 = setup_basic_test(request, mgmt_root, 'dc1', 'Common')
        assert dc1.enabled is True
        assert dc1.disabled is False
        dc1.update(enabled=False)
        assert dc1.enabled is False
        assert dc1.disabled is True

    def test_update_samevalue(self, request, mgmt_root):
        dc1 = setup_basic_test(request, mgmt_root, 'dc1', 'Common')
        dc1.update(enabled=True)
        assert dc1.enabled is True


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        dc1 = setup_basic_test(request, mgmt_root, 'dc1', 'Common')
        dc1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.datacenters.datacenter.load(
                name='dc1', partition='Common')
            assert err.response.status_code == 404


class TestDatacenterCollection(object):
    def test_datacenter_collection(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'dc1', 'Common')
        dc1 = mgmt_root.tm.gtm.datacenters.datacenter.create(
            name='dc1', partition='Common')
        assert dc1.name == 'dc1'
        assert dc1.partition == 'Common'
        assert dc1.generation and isinstance(dc1.generation, int)
        assert dc1.fullPath == '/Common/dc1'
        assert dc1.kind == 'tm:gtm:datacenter:datacenterstate'
        assert dc1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/datacenter/~Common~dc1')

        rc = mgmt_root.tm.gtm.datacenters.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Datacenter)
