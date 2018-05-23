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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.security.ip_intelligence import Blacklist_Category
from f5.bigip.tm.security.ip_intelligence import Feed_list
from f5.bigip.tm.security.ip_intelligence import Feed_list_s
from f5.bigip.tm.security.ip_intelligence import Global_Policy
from f5.bigip.tm.security.ip_intelligence import Policy
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeFeedlist():
    fake_col = mock.MagicMock()
    fake_feedlist = Feed_list(fake_col)
    return fake_feedlist


@pytest.fixture
def FakeBlacklistCategories():
    fake_col = mock.MagicMock()
    fake_Blacklistcategory = Blacklist_Category(fake_col)
    return fake_Blacklistcategory


@pytest.fixture
def FakePolicy():
    fake_col = mock.MagicMock()
    fake_policy = Policy(fake_col)
    return fake_policy


@pytest.fixture
def FakeGlobalPolicy():
    fake_col = mock.MagicMock()
    fake_global_policy = Global_Policy(fake_col)
    return fake_global_policy


def MakeFeedlist(fakeicontrolsession):
    a = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = a.tm.security.ip_intelligence.feed_list_s.feed_list
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/ip-intelligence/feed-list/~Common' \
        '~testfeedlist/'
    return p


def MakeBlacklistCategory(fakeicontrolsesion):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.ip_intelligence.blacklist_Categorys.blacklist_Category
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/ip-intelligence/blacklist-category/~Common' \
        '~testbacklistcategory/'
    return p


def MakePolicy(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.ip_intelligence.policy_s.policy
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/ip-intelligence/policy/' \
        '~Common~fakepolicy/'
    return p


def MakeGlobalPolicy(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.security.ip_intelligence.global_policy
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/security/ip-intelligence/global-policy/'
    return p


class TestFeedList(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        s1 = b.tm.security.ip_intelligence.feed_list_s.feed_list
        s2 = b.tm.security.ip_intelligence.feed_list_s.feed_list
        assert s1 is not s2

    def test_create_no_arguments(self, FakeFeedlist):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeFeedlist.create()


class TestBlacklistCategory(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        d1 = b.tm.security.ip_intelligence.blacklist_categorys.blacklist_category
        d2 = b.tm.security.ip_intelligence.blacklist_categorys.blacklist_category
        assert d1 is not d2

    def test_create_no_arguments(self, FakeBlacklistCategories):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeBlacklistCategories.create()


class TestPolicy(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.security.ip_intelligence.policy_s.policy
        p2 = b.tm.security.ip_intelligence.policy_s.policy
        assert p1 is not p2

    def test_create_no_arguments(self, FakePolicy):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePolicy.create()


class TestPolicyFeedlistSubCollection(object):
    def test_policy_feedlist_subcollection(self, fakeicontrolsession):
        pc = Feed_list_s(MakePolicy(fakeicontrolsession))
        kind = 'tm:security:ip-intelligence:feed-list:feed-liststate'
        test_meta = pc._meta_data['attribute_registry']
        test_meta2 = pc._meta_data['allowed_lazy_attributes']
        assert isinstance(pc, Feed_list_s)
        assert kind in list(iterkeys(test_meta))
        assert Feed_list in test_meta2


class TestGlobalPolicy(object):
    def test_global_policy(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        kind = "tm:security:ip-intelligence:global-policy:global-policystate"
        rules = b.tm.security.ip_intelligence.global_policy
        rules_kind = rules._meta_data["required_json_kind"]
        assert rules_kind == kind
