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

from f5.bigip.tm.security.blacklist_publisher import Category
from f5.bigip.tm.security.blacklist_publisher import Profile
from requests.exceptions import HTTPError

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def profile(mgmt_root):
    p1 = mgmt_root.tm.security.blacklist_publisher.profile_s.profile.create(
        name='fake_profile', partition='Common', routeDomain='/Common/0', routeAdvertisementNexthop='3.3.3.3')
    yield p1
    p1.delete()


@pytest.fixture(scope='function')
def category(mgmt_root):
    c1 = mgmt_root.tm.security.blacklist_publisher.category_s.category.create(
        name='proxy', partition='Common')
    yield c1
    c1.delete()


class TestBlProfile(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        p1 = mgmt_root.tm.security.blacklist_publisher.profile_s.profile
        with pytest.raises(HTTPError) as err:
            p1.create(name='fail', partition='Common', routeDomain='/Common/0')
        assert err.value.response.status_code == 400

    def test_create_req_args(self, profile):
        p1 = profile
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/profile/~Common~fake_profile'
        assert p1.name == 'fake_profile'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert p1.kind == 'tm:security:blacklist-publisher:profile:profilestate'
        assert not hasattr(p1, 'description')

    def test_create_opt_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.blacklist_publisher.profile_s.profile.create(
            name='fake_profile', partition='Common', routeDomain='/Common/0', routeAdvertisementNexthop='3.3.3.3')
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/profile/~Common~fake_profile'
        assert p1.name == 'fake_profile'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        p1.modify(description=DESC)
        assert hasattr(p1, 'description')
        assert p1.description == DESC
        p1.delete()

    def test_refresh(self, mgmt_root, profile):
        prof = mgmt_root.tm.security.blacklist_publisher.profile_s
        p1 = profile
        p2 = prof.profile.load(name='fake_profile', partition='Common')
        assert p1.name == p2.name
        assert p1.kind == p2.kind
        assert p1.selfLink == p2.selfLink
        assert not hasattr(p1, 'description')
        assert not hasattr(p2, 'description')
        p2.modify(description=DESC)
        assert hasattr(p2, 'description')
        assert p2.description == DESC
        p1.refresh()
        assert p1.selfLink == p2.selfLink
        assert hasattr(p1, 'description')
        assert p1.description == p2.description

    def test_delete(self, mgmt_root):
        prof = mgmt_root.tm.security.blacklist_publisher.profile_s
        p1 = prof.profile.create(name='fake_profile', partition='Common', routeDomain='/Common/0', routeAdvertisementNexthop='3.3.3.3')
        p1.delete()
        with pytest.raises(HTTPError) as err:
            prof.profile.load(partition='Common', name='fake_profile')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        prof = mgmt_root.tm.security.blacklist_publisher.profile_s
        with pytest.raises(HTTPError) as err:
            prof.profile.load(partition='Common', name='not_exists')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, profile):
        p1 = profile
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/profile/~Common~fake_profile'
        assert p1.name == 'fake_profile'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.description = DESC
        p1.update()
        assert hasattr(p1, 'description')
        assert p1.description == DESC
        prof = mgmt_root.tm.security.blacklist_publisher.profile_s
        p2 = prof.profile.load(partition='Common', name='fake_profile')
        assert p1.name == p2.name
        assert p1.partition == p2.partition
        assert p1.selfLink == p2.selfLink
        assert hasattr(p2, 'description')
        assert p1.description == p2.description

    def test_profile_collection(self, mgmt_root, profile):
        p1 = profile
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/profile/~Common~fake_profile'
        assert p1.name == 'fake_profile'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        prof = mgmt_root.tm.security.blacklist_publisher.profile_s.get_collection()
        assert isinstance(prof, list)
        assert len(prof)
        assert isinstance(prof[0], Profile)


class TestBlCategory(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        c1 = mgmt_root.tm.security.blacklist_publisher.category_s.category
        with pytest.raises(HTTPError) as err:
            c1.create(name='fail', partition='Common')
        assert err.value.response.status_code == 400

    def test_create_req_args(self, category):
        c1 = category
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/category/~Common~proxy'
        assert c1.name == 'proxy'
        assert c1.partition == 'Common'
        assert c1.selfLink.startswith(URI)
        assert c1.kind == 'tm:security:blacklist-publisher:category:categorystate'
        assert not hasattr(c1, 'description')

    def test_create_opt_args(self, mgmt_root):
        c1 = mgmt_root.tm.security.blacklist_publisher.category_s.category.create(
            name='proxy', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/category/~Common~proxy'
        assert c1.name == 'proxy'
        assert c1.partition == 'Common'
        assert c1.selfLink.startswith(URI)
        c1.delete()

    def test_refresh(self, mgmt_root, category):
        cat = mgmt_root.tm.security.blacklist_publisher.category_s
        c1 = category
        c2 = cat.category.load(name='proxy', partition='Common')
        assert c1.name == c2.name
        assert c1.kind == c2.kind
        assert c1.selfLink == c2.selfLink

    def test_delete(self, mgmt_root):
        cat = mgmt_root.tm.security.blacklist_publisher.category_s
        c1 = cat.category.create(name='proxy', partition='Common')
        c1.delete()
        with pytest.raises(HTTPError) as err:
            cat.category.load(partition='Common', name='proxy')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        cat = mgmt_root.tm.security.blacklist_publisher.category_s
        with pytest.raises(HTTPError) as err:
            cat.category.load(partition='Common', name='not_exists')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, category):
        c1 = category
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/category/~Common~proxy'
        assert c1.name == 'proxy'
        assert c1.partition == 'Common'
        assert c1.selfLink.startswith(URI)
        cat = mgmt_root.tm.security.blacklist_publisher.category_s
        c2 = cat.category.load(partition='Common', name='proxy')
        assert c1.name == c2.name
        assert c1.partition == c2.partition
        assert c1.selfLink == c2.selfLink

    def test_category_collection(self, mgmt_root, category):
        c1 = category
        URI = 'https://localhost/mgmt/tm/security/blacklist-publisher/category/~Common~proxy'
        assert c1.name == 'proxy'
        assert c1.partition == 'Common'
        assert c1.selfLink.startswith(URI)
        cat = mgmt_root.tm.security.blacklist_publisher.category_s.get_collection()
        assert isinstance(cat, list)
        assert len(cat)
        assert isinstance(cat[0], Category)
