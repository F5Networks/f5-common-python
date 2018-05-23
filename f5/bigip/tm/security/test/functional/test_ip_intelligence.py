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


from f5.bigip.tm.security.ip_intelligence import Blacklist_Category
from f5.bigip.tm.security.ip_intelligence import Feed_list
from f5.bigip.tm.security.ip_intelligence import Policy
import pytest
from requests.exceptions import HTTPError

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def feedlist(mgmt_root):
    flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
        name='fake_feedlist', partition='Common')
    yield flst
    flst.delete()


@pytest.fixture(scope='function')
def feeds(mgmt_root):
    flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
        name='fake_feedlist', partition='Common',
        feeds=[{'name': 'fake_feed', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url.html"}}])
    yield flst.feeds
    flst.delete()


@pytest.fixture(scope='function')
def blacklistcategory(mgmt_root):
    b1 = mgmt_root.tm.security.ip_intelligence.blacklist_categorys.blacklist_category.create(
        name='fake_blacklist_category', partition='Common')
    yield b1
    b1.delete()


@pytest.fixture(scope='function')
def policy(mgmt_root):
    p1 = mgmt_root.tm.security.ip_intelligence.policy_s.policy.create(
        name='fake_policy', partition='Common')
    yield p1
    p1.delete()


@pytest.fixture(scope='function')
def globalpolicy(mgmt_root):
    p1 = mgmt_root.tm.security.ip_intelligence.global_policy.load(partition='Common')
    yield p1
    p1.delete()


class TestFeedlistFeeds(object):
    def test_mandatory_attribute_missing(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
                name='fake_feedlist', partition='Common', feeds=[{'name': 'fake_feed', 'poll': {"url": "http://test_url.html"}}])
        assert err.value.response.status_code == 400
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
                name='fake_feedlist', partition='Common', feeds=[{'name': 'fake_feed'}])
        assert err.value.response.status_code == 400

    def test_create_req_arg(self, feeds):
        f1 = feeds[0]
        assert f1['name'] == 'fake_feed'
        assert f1['defaultListType'] == 'blacklist'
        assert f1['defaultBlacklistCategory'] == '/Common/spam_sources'
        assert f1['poll']['url'] == 'http://test_url.html'
        assert f1['poll']['interval'] == 'default'
        assert not hasattr(f1, 'description')

    def test_create_optional_args(self, mgmt_root):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
            name='fake_feedlist', partition='Common',
            feeds=[{'name': 'fake_feed', 'default-blacklist-category': '/Common/spam_sources', 'defaultListType': 'whitelist',
                    'poll': {"url": "http://test_url.html", "interval": "450"}}])
        f1 = flst.feeds[0]
        assert f1['defaultListType'] == 'whitelist'
        assert f1['poll']['interval'] == '450'
        flst.delete()

    def test_refresh(self, feeds, mgmt_root):
        f1 = feeds[0]
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s
        flst2 = flst.feed_list.load(name='fake_feedlist', partition='Common')
        f2 = flst2.feeds[0]
        assert f1['name'] == f2['name']
        assert f1['defaultListType'] == f2['defaultListType']
        assert f1['defaultBlacklistCategory'] == f2['defaultBlacklistCategory']
        assert f1['poll']['url'] == f2['poll']['url']
        assert f1['poll']['interval'] == f2['poll']['interval']

    def test_multiple_feeds(self, mgmt_root):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
            name='fake_feedlist', partition='Common',
            feeds=[{'name': 'fake_feed', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url.html"}},
                   {'name': 'fake_feed2', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url2.html"}}])
        f = flst.feeds
        assert isinstance(f, list)
        assert len(f) == 2
        assert f[0]['name'] == 'fake_feed'
        assert f[1]['name'] == 'fake_feed2'
        flst.delete()

    def test_load_and_update(self, mgmt_root):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
            name='fake_feedlist', partition='Common',
            feeds=[{'name': 'fake_feed', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url.html"}}])
        f1 = flst.feeds[0]
        assert f1['name'] == 'fake_feed'
        assert f1['defaultListType'] == 'blacklist'
        assert f1['defaultBlacklistCategory'] == '/Common/spam_sources'
        assert f1['poll']['url'] == 'http://test_url.html'
        assert f1['poll']['interval'] == 'default'
        assert not hasattr(f1, 'description')
        flst.update(name='fake_feedlist', partition='Common',
                    feeds=[{'name': 'fake_feed1', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url1.html"}}])
        f2 = flst.feeds[0]
        assert f2['name'] == 'fake_feed1'
        assert f2['defaultListType'] == 'blacklist'
        assert f2['defaultBlacklistCategory'] == '/Common/spam_sources'
        assert f2['poll']['url'] == 'http://test_url1.html'
        assert f2['poll']['interval'] == 'default'
        assert not hasattr(f2, 'description')
        flst.delete()

    def test_delete(self, mgmt_root):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
            name='fake_feedlist', partition='Common',
            feeds=[{'name': 'fake_feed', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url.html"}},
                   {'name': 'fake_feed2', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url2.html"}}])
        flst.update(name='fake_feedlist', partition='Common',
                    feeds=[{'name': 'fake_feed2', 'default-blacklist-category': '/Common/spam_sources', 'poll': {"url": "http://test_url2.html"}}])
        assert len(flst.feeds) == 1
        f1 = flst.feeds[0]
        assert f1['name'] == 'fake_feed2'
        assert f1['defaultListType'] == 'blacklist'
        assert f1['defaultBlacklistCategory'] == '/Common/spam_sources'
        assert f1['poll']['url'] == 'http://test_url2.html'
        assert f1['poll']['interval'] == 'default'
        assert not hasattr(f1, 'description')
        flst.delete()


class TestFeedList(object):
    def test_create_req_args(self, feedlist):
        f1 = feedlist
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/feed-list/~Common~fake_feedlist'
        assert f1.name == 'fake_feedlist'
        assert f1.partition == 'Common'
        assert f1.selfLink.startswith(URI)
        assert f1.kind == 'tm:security:ip-intelligence:feed-list:feed-liststate'
        assert not hasattr(f1, 'description')

    def test_create_opt_args(self, mgmt_root):
        f1 = mgmt_root.tm.security.ip_intelligence.feed_list_s.feed_list.create(
            name='fake_feedlist', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/feed-list/~Common~fake_feedlist'
        assert f1.name == 'fake_feedlist'
        assert f1.partition == 'Common'
        assert f1.selfLink.startswith(URI)
        f1.modify(description=DESC)
        assert hasattr(f1, 'description')
        assert f1.description == DESC
        f1.delete()

    def test_refresh(self, mgmt_root, feedlist):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s
        f1 = feedlist
        f2 = flst.feed_list.load(name='fake_feedlist', partition='Common')
        assert f1.name == f2.name
        assert f1.kind == f2.kind
        assert f1.selfLink == f2.selfLink
        assert not hasattr(f1, 'description')
        assert not hasattr(f2, 'description')
        f2.modify(description=DESC)
        assert hasattr(f2, 'description')
        assert f2.description == DESC
        f1.refresh()
        assert f1.selfLink == f2.selfLink
        assert hasattr(f1, 'description')
        assert f1.description == f2.description

    def test_delete(self, mgmt_root):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s
        f1 = flst.feed_list.create(name='fake_feedlist', partition='Common')
        f1.delete()
        with pytest.raises(HTTPError) as err:
            flst.feed_list.load(partition='Common', name='fake_feedlist')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s
        with pytest.raises(HTTPError) as err:
            flst.feed_list.load(partition='Common', name='not_exists')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, feedlist):
        f1 = feedlist
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/feed-list/~Common~fake_feedlist'
        assert f1.name == 'fake_feedlist'
        assert f1.partition == 'Common'
        assert f1.selfLink.startswith(URI)
        assert not hasattr(f1, 'description')
        f1.description = DESC
        f1.update()
        assert hasattr(f1, 'description')
        assert f1.description == DESC
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s
        f2 = flst.feed_list.load(partition='Common', name='fake_feedlist')
        assert f1.name == f2.name
        assert f1.partition == f2.partition
        assert f1.selfLink == f2.selfLink
        assert hasattr(f2, 'description')
        assert f1.description == f2.description

    def test_feedlist_collection(self, mgmt_root, feedlist):
        f1 = feedlist
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/feed-list/~Common~fake_feedlist'
        assert f1.name == 'fake_feedlist'
        assert f1.partition == 'Common'
        assert f1.selfLink.startswith(URI)
        flst = mgmt_root.tm.security.ip_intelligence.feed_list_s.get_collection()
        assert isinstance(flst, list)
        assert len(flst)
        assert isinstance(flst[0], Feed_list)


class TestBlackList(object):
    def test_create_req_args(self, blacklistcategory):
        b1 = blacklistcategory
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/blacklist-category/~Common~fake_blacklist_category'
        assert b1.name == 'fake_blacklist_category'
        assert b1.partition == 'Common'
        assert b1.selfLink.startswith(URI)
        assert b1.kind == 'tm:security:ip-intelligence:blacklist-category:blacklist-categorystate'
        assert not hasattr(b1, 'description')

    def test_create_opt_args(self, mgmt_root):
        b1 = mgmt_root.tm.security.ip_intelligence.blacklist_categorys.blacklist_category.create(
            name='fake_blacklist_category', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/blacklist-category/~Common~fake_blacklist_category'
        assert b1.name == 'fake_blacklist_category'
        assert b1.partition == 'Common'
        assert b1.selfLink.startswith(URI)
        b1.modify(description=DESC)
        assert hasattr(b1, 'description')
        assert b1.description == DESC
        b1.delete()

    def test_refresh(self, mgmt_root, blacklistcategory):
        bc = mgmt_root.tm.security.ip_intelligence.blacklist_categorys
        b1 = blacklistcategory
        b2 = bc.blacklist_category.load(name='fake_blacklist_category', partition='Common')
        assert b1.name == b2.name
        assert b1.kind == b2.kind
        assert b1.selfLink == b2.selfLink
        assert not hasattr(b1, 'description')
        assert not hasattr(b2, 'description')
        b2.modify(description=DESC)
        assert hasattr(b2, 'description')
        assert b2.description == DESC
        b1.refresh()
        assert b1.selfLink == b2.selfLink
        assert hasattr(b1, 'description')
        assert b1.description == b2.description

    def test_delete(self, mgmt_root):
        bc = mgmt_root.tm.security.ip_intelligence.blacklist_categorys
        b1 = bc.blacklist_category.create(name='fake_blacklist_category', partition='Common')
        b1.delete()
        with pytest.raises(HTTPError) as err:
            bc.blacklist_category.load(partition='Common', name='fake_blacklist_category')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        bc = mgmt_root.tm.security.ip_intelligence.blacklist_categorys
        with pytest.raises(HTTPError) as err:
            bc.blacklist_category.load(partition='Common', name='not_exists')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, blacklistcategory):
        b1 = blacklistcategory
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/blacklist-category/~Common~fake_blacklist_category'
        assert b1.name == 'fake_blacklist_category'
        assert b1.partition == 'Common'
        assert b1.selfLink.startswith(URI)
        assert not hasattr(b1, 'description')
        b1.description = DESC
        b1.update()
        assert hasattr(b1, 'description')
        assert b1.description == DESC
        bc = mgmt_root.tm.security.ip_intelligence.blacklist_categorys
        b2 = bc.blacklist_category.load(partition='Common', name='fake_blacklist_category')
        assert b1.name == b2.name
        assert b1.partition == b2.partition
        assert b1.selfLink == b2.selfLink
        assert hasattr(b2, 'description')
        assert b1.description == b2.description

    def test_blacklist_category_collection(self, mgmt_root, blacklistcategory):
        b1 = blacklistcategory
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/blacklist-category/~Common~fake_blacklist_category'
        assert b1.name == 'fake_blacklist_category'
        assert b1.partition == 'Common'
        assert b1.selfLink.startswith(URI)
        bc = mgmt_root.tm.security.ip_intelligence.blacklist_categorys.get_collection()
        assert isinstance(bc, list)
        assert len(bc)
        assert isinstance(bc[0], Blacklist_Category)


class TestPolicy(object):
    def test_create_req_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.ip_intelligence.policy_s.policy.create(
            name='fake_policy', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.delete()

    def test_refresh(self, mgmt_root, policy):
        p1 = policy
        p2 = mgmt_root.tm.security.ip_intelligence.policy_s.policy.load(
            name='fake_policy', partition='Common')
        assert p1.name == p2.name
        assert p1.kind == p2.kind
        assert p1.selfLink == p2.selfLink
        assert not hasattr(p1, 'description')
        assert not hasattr(p2, 'description')
        p2.modify(description=DESC)
        p1.modify(description=DESC)
        assert hasattr(p2, 'description')
        assert p2.description == DESC
        p1.refresh()
        assert p1.selfLink == p2.selfLink
        assert hasattr(p1, 'description')
        assert p1.description == p2.description

    def test_delete(self, mgmt_root):
        p = mgmt_root.tm.security.ip_intelligence.policy_s.policy
        p1 = p.create(name='delete_me', partition='Common')
        p1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.ip_intelligence.policy_s.policy.load(
                name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p = mgmt_root.tm.security.ip_intelligence.policy_s.policy
        with pytest.raises(HTTPError) as err:
            p.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, policy):
        p1 = policy
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.description = DESC
        p1.update()
        assert hasattr(p1, 'description')
        assert p1.description == DESC
        p = mgmt_root.tm.security.ip_intelligence.policy_s.policy
        p2 = p.load(name='fake_policy', partition='Common')
        assert p1.name == p2.name
        assert p1.partition == p2.partition
        assert p1.selfLink == p2.selfLink
        assert hasattr(p2, 'description')
        assert p1.description == p2.description

    def test_policies_collection(self, mgmt_root, policy):
        p1 = policy
        URI = 'https://localhost/mgmt/tm/security/ip-intelligence/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        pc = mgmt_root.tm.security.ip_intelligence.policy_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Policy)


class TestGlobalPolicy(object):
    def test_modify_req_args(self, mgmt_root, policy):
        rules = mgmt_root.tm.security.ip_intelligence.global_policy.load(partition='Common')
        assert "ipIntelligencePolicy" not in rules.__dict__
        rules.modify(ipIntelligencePolicy='fake_policy', partition='Common')
        assert rules.ipIntelligencePolicy == "/Common/fake_policy"
        rules.modify(ipIntelligencePolicy='none', partition='Common')
        assert "ipIntelligencePolicy" not in rules.__dict__
