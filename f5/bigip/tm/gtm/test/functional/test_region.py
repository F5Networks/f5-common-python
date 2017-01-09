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


"""worthy note is that regions seem quite buggy in 12.x these tests need
some more work to determine what we need to disable for 12.x"""

import copy
import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.gtm.region import Region
from pytest import symbols
from requests.exceptions import HTTPError
from six import iteritems

pytestmark = pytest.mark.skipif(
    symbols
    and hasattr(symbols, 'modules')
    and not symbols.modules['gtm'],
    reason='The modules symbol for GTM is set to False.'
)


def delete_region(mgmt_root, name, partition):
    try:
        foo = mgmt_root.tm.gtm.regions.region.load(name=name,
                                                   partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_create_test(request, mgmt_root, name, partition):
    def teardown():
        delete_region(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_region(mgmt_root, name, partition)

    reg1 = mgmt_root.tm.gtm.regions.region.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return reg1


class TestCreate(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.gtm.regions.region.create()

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_region', 'Common')
        reg1 = mgmt_root.tm.gtm.regions.region.create(
            name='fake_region', partition='Common')
        assert reg1.name == 'fake_region'
        assert reg1.partition == 'Common'
        assert reg1.generation and isinstance(reg1.generation, int)
        assert reg1.kind == 'tm:gtm:region:regionstate'
        assert reg1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/region/~Common~fake_region')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_region', 'Common')
        reg1 = mgmt_root.tm.gtm.regions.region.create(
            name='fake_region',
            partition='Common',
            description='NewRegionSomewhere')
        assert hasattr(reg1, 'description')
        assert reg1.description == 'NewRegionSomewhere'

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_region', 'Common')
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.regions.region.create(
                name='fake_region', partition='Common')
        assert err.value.response.status_code == 409


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_region', 'Common')
        r1 = mgmt_root.tm.gtm.regions.region.load(
            name='fake_region', partition='Common')
        r2 = mgmt_root.tm.gtm.regions.region.load(
            name='fake_region', partition='Common')

        assert r1.name == 'fake_region'
        assert r2.name == 'fake_region'

        r2.update(description='NewRegionSomewhere')
        assert hasattr(r2, 'description')
        assert not hasattr(r1, 'description')
        assert r2.description == 'NewRegionSomewhere'
        r1.refresh()
        assert hasattr(r1, 'description')
        assert r1.description == 'NewRegionSomewhere'


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.regions.region.load(
                name='fake_region', partition='Common')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_region', 'Common')
        r1 = mgmt_root.tm.gtm.regions.region.load(
            name='fake_region', partition='Common')
        assert r1.name == 'fake_region'
        assert not hasattr(r1, 'description')
        r1.update(description='NewRegionSomewhere')
        r2 = mgmt_root.tm.gtm.regions.region.load(
            name='fake_region', partition='Common')
        assert r1.description == 'NewRegionSomewhere'
        assert r2.description == 'NewRegionSomewhere'


class TestUpdate(object):
    def test_update(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'fake_region', 'Common')
        assert r1.name == 'fake_region'
        assert not hasattr(r1, 'description')
        r1.update(description='NewRegionSomewhere')
        assert hasattr(r1, 'description')
        assert r1.description == 'NewRegionSomewhere'


class TestModify(object):
    def test_modify(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'fake_region', 'Common')
        original_dict = copy.copy(r1.__dict__)
        value = 'description'
        r1.modify(description='NewRegionSomewhere')
        for k, v in iteritems(original_dict):
            if k != value:
                original_dict[k] = r1.__dict__[k]
            elif k == value:
                assert r1.__dict__[k] == 'NewRegionSomewhere'


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'fake_region', 'Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.regions.region.load(
                name='fake_region', partition='Common')
        assert err.value.response.status_code == 404


class TestRegionCollection(object):
    def test_region_collection(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_region', 'Common')
        reg1 = mgmt_root.tm.gtm.regions.region.create(
            name='fake_region', partition='Common')
        assert reg1.name == 'fake_region'
        assert reg1.partition == 'Common'
        assert reg1.generation and isinstance(reg1.generation, int)
        assert reg1.kind == 'tm:gtm:region:regionstate'
        assert reg1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/region/~Common~fake_region')

        rc = mgmt_root.tm.gtm.regions.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Region)
