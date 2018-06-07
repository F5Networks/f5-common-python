# Copyright 2017 F5 Networks Inc.
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
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.security.nat import Destination_Translation
from f5.bigip.tm.security.nat import Policy
from f5.bigip.tm.security.nat import Rule
from f5.bigip.tm.security.nat import Source_Translation


from f5.sdk_exception import ExclusiveAttributesPresent
from requests.exceptions import HTTPError

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def srctranslation(mgmt_root):
    s1 = mgmt_root.tm.security.nat.source_translations.source_translation.create(
        name='fake_src', partition='Common', addresses=['40.1.1.1', '40.1.1.2'], ports=['1025-65535'], type='dynamic-pat')
    yield s1
    s1.delete()


@pytest.fixture(scope='function')
def dsttranslation(mgmt_root):
    d1 = mgmt_root.tm.security.nat.destination_translations.destination_translation.create(
        partition='Common', name='fake_dst', addresses=['40.2.1.1', '40.2.1.2'], ports=['1025-65535'], type='static-pat')
    yield d1
    d1.delete()


@pytest.fixture(scope='function')
def policy(mgmt_root):
    p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
        name='fake_policy', partition='Common')
    yield p1
    p1.delete()


@pytest.fixture(scope='function')
def rule(mgmt_root):
    p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
        name='fake_policy', partition='Common')
    rule_lst = p1.rules_s
    param_set = {'name': 'fake_rule', 'place-after': 'last'}
    rule1 = rule_lst.rule.create(**param_set)
    yield rule1
    rule1.delete()
    p1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
    reason='This collection is fully implemented on 12.1.0 or greater.'
)
class TestSrcTranslation(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        s1 = mgmt_root.tm.security.nat.source_translations.source_translation
        with pytest.raises(HTTPError) as err:
            s1.create(name='fail', partition='Common', type='dynamic-pat')
        assert err.value.response.status_code == 400

    def test_create_req_args(self, srctranslation):
        s1 = srctranslation
        URI = 'https://localhost/mgmt/tm/security/nat/source-translation/~Common~fake_src'
        assert s1.name == 'fake_src'
        assert s1.partition == 'Common'
        assert s1.selfLink.startswith(URI)
        assert s1.kind == 'tm:security:nat:source-translation:source-translationstate'
        assert not hasattr(s1, 'description')

    def test_create_opt_args(self, mgmt_root):
        s1 = mgmt_root.tm.security.nat.source_translations.source_translation.create(
            name='fake_src', partition='Common', addresses=['40.1.1.1', '40.1.1.2'], ports=['1025-65535'], type='dynamic-pat')
        URI = 'https://localhost/mgmt/tm/security/nat/source-translation/~Common~fake_src'
        assert s1.name == 'fake_src'
        assert s1.partition == 'Common'
        assert s1.selfLink.startswith(URI)
        s1.modify(description=DESC)
        assert hasattr(s1, 'description')
        assert s1.description == DESC
        s1.delete()

    def test_refresh(self, mgmt_root, srctranslation):
        sc = mgmt_root.tm.security.nat.source_translations
        s1 = srctranslation
        s2 = sc.source_translation.load(name='fake_src', partition='Common')
        assert s1.name == s2.name
        assert s1.kind == s2.kind
        assert s1.selfLink == s2.selfLink
        assert not hasattr(s1, 'description')
        assert not hasattr(s2, 'description')
        s2.modify(description=DESC)
        assert hasattr(s2, 'description')
        assert s2.description == DESC
        s1.refresh()
        assert s1.selfLink == s2.selfLink
        assert hasattr(s1, 'description')
        assert s1.description == s2.description

    def test_delete(self, mgmt_root):
        src = mgmt_root.tm.security.nat.source_translations
        s1 = src.source_translation.create(name='fake_src', partition='Common', addresses=['40.1.1.1', '40.1.1.2'], ports=['1025-65535'], type='dynamic-pat')
        s1.delete()
        with pytest.raises(HTTPError) as err:
            src.source_translation.load(partition='Common', name='fake_src')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        src = mgmt_root.tm.security.nat.source_translations
        with pytest.raises(HTTPError) as err:
            src.source_translation.load(partition='Common', name='not_exists')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, srctranslation):
        s1 = srctranslation
        URI = 'https://localhost/mgmt/tm/security/nat/source-translation/~Common~fake_src'
        assert s1.name == 'fake_src'
        assert s1.partition == 'Common'
        assert s1.selfLink.startswith(URI)
        assert not hasattr(s1, 'description')
        s1.description = DESC
        s1.update()
        assert hasattr(s1, 'description')
        assert s1.description == DESC
        sc = mgmt_root.tm.security.nat.source_translations
        s2 = sc.source_translation.load(partition='Common', name='fake_src')
        assert s1.name == s2.name
        assert s1.partition == s2.partition
        assert s1.selfLink == s2.selfLink
        assert hasattr(s2, 'description')
        assert s1.description == s2.description

    def test_src_translation_collection(self, mgmt_root, srctranslation):
        s1 = srctranslation
        URI = 'https://localhost/mgmt/tm/security/nat/source-translation/~Common~fake_src'
        assert s1.name == 'fake_src'
        assert s1.partition == 'Common'
        assert s1.selfLink.startswith(URI)
        src = mgmt_root.tm.security.nat.source_translations.get_collection()
        assert isinstance(src, list)
        assert len(src)
        assert isinstance(src[0], Source_Translation)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
    reason='This collection is fully implemented on 12.1.0 or greater.'
)
class TestDstTranslation(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        d1 = mgmt_root.tm.security.nat.destination_translations.destination_translation
        with pytest.raises(HTTPError) as err:
            d1.create(name='fail', partition='Common', type='static-nat')
        assert err.value.response.status_code == 400
        d2 = mgmt_root.tm.security.nat.destination_translations.destination_translation
        with pytest.raises(HTTPError) as err:
            d2.create(name='fail', partition='Common', type='static-pat')
        assert err.value.response.status_code == 400

    def test_create_req_args(self, dsttranslation):
        d1 = dsttranslation
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/destination-translation/~Common~fake_dst'
        assert d1.name == 'fake_dst'
        assert d1.partition == 'Common'
        assert d1.selfLink.startswith(URI)
        assert d1.kind == 'tm:security:nat:destination-translation:destination-translationstate'
        assert not hasattr(d1, 'description')

    def test_create_opt_args(self, mgmt_root):
        d1 = mgmt_root.tm.security.nat.destination_translations.destination_translation.create(
            partition='Common', name='fake_dst', addresses=['40.6.1.1', '40.6.1.2'], ports=['1025-65535'], type='static-pat')
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/destination-translation/~Common~fake_dst'
        assert d1.name == 'fake_dst'
        assert d1.partition == 'Common'
        assert d1.selfLink.startswith(URI)
        d1.modify(description=DESC)
        assert hasattr(d1, 'description')
        assert d1.description == DESC
        d1.delete()

    def test_refresh(self, mgmt_root, dsttranslation):
        d1 = dsttranslation
        dst = mgmt_root.tm.security.nat.destination_translations
        d2 = dst.destination_translation.load(
            name='fake_dst', partition='Common')
        assert d1.name == d2.name
        assert d1.partition == d2.partition
        assert d1.kind == d2.kind
        assert d1.selfLink == d2.selfLink
        assert not hasattr(d1, 'description')
        assert not hasattr(d2, 'description')
        d2.modify(description=DESC)
        assert hasattr(d2, 'description')
        assert d2.description == DESC
        d1.refresh()
        assert d1.selfLink == d2.selfLink
        assert hasattr(d1, 'description')
        assert d1.description == d2.description

    def test_delete(self, mgmt_root):
        dst = mgmt_root.tm.security.nat.destination_translations
        d1 = dst.destination_translation.create(
            partition='Common', name='fake_dst', addresses=['40.6.1.1', '40.6.1.2'], ports=['1025-65535'], type='static-pat')
        d1.delete()
        with pytest.raises(HTTPError) as err:
            dst.destination_translation.load(partition='Common', name='fake_dst')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        dst = mgmt_root.tm.security.nat.destination_translations
        with pytest.raises(HTTPError) as err:
            dst.destination_translation.load(partition='Common', name='not_exists')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, dsttranslation):
        d1 = dsttranslation
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/destination-translation/~Common~fake_dst'
        assert d1.name == 'fake_dst'
        assert d1.partition == 'Common'
        assert d1.selfLink.startswith(URI)
        assert not hasattr(d1, 'description')
        d1.description = DESC
        d1.update()
        assert hasattr(d1, 'description')
        assert d1.description == DESC
        dst = mgmt_root.tm.security.nat.destination_translations
        d2 = dst.destination_translation.load(partition='Common', name='fake_dst')
        assert d1.name == d2.name
        assert d1.partition == d2.partition
        assert d1.kind == d2.kind
        assert d1.selfLink == d2.selfLink
        assert hasattr(d2, 'description')
        assert d1.description == d2.description

    def test_dst_translation_collection(self, mgmt_root, dsttranslation):
        d1 = dsttranslation
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/destination-translation/~Common~fake_dst'
        assert d1.name == 'fake_dst'
        assert d1.partition == 'Common'
        assert d1.selfLink.startswith(URI)
        dst = mgmt_root.tm.security.nat.destination_translations.get_collection()
        assert isinstance(dst, list)
        assert len(dst)
        assert isinstance(dst[0], Destination_Translation)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
    reason='This collection is fully implemented on 12.1.0 or greater.'
)
class TestRules(object):
    def test_mutually_exclusive_raises(self, mgmt_root):
        p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
            name='fake_policy', partition='Common')
        rule_lst = p1.rules_s
        param_set = {'name': 'fake_rule', 'place-after': 'first',
                     'action': 'reject', 'place-before': 'last'}
        ERR = 'Mutually exclusive arguments submitted. The following arguments cannot be set together: "place-after, place-before".'
        with pytest.raises(ExclusiveAttributesPresent) as err:
            rule_lst.rule.create(**param_set)
        assert str(err.value) == ERR
        p1.delete()

    def test_mandatory_attribute_missing(self, mgmt_root):
        p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
            name='fake_policy', partition='Common')
        rule_lst = p1.rules_s
        param_set = {'name': 'fake_rule', 'action': 'reject'}
        ERR = "This resource requires at least one of the mandatory additional parameters to be provided: place-after, place-before"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            rule_lst.rule.create(**param_set)
        assert str(err.value) == ERR
        p1.delete()

    def test_create_req_arg(self, rule):
        r1 = rule
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_optional_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
            name='fake_policy', partition='Common')
        rule_lst = p1.rules_s
        param_set = {'name': 'fake_rule', 'action': 'reject', 'place-after': 'first', 'description': DESC}
        r1 = rule_lst.rule.create(**param_set)
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert r1.kind == 'tm:security:nat:policy:rules:rulesstate'
        assert r1.description == DESC
        r1.delete()
        p1.delete()

    def test_refresh(self, rule, mgmt_root):
        r1 = rule
        rc = mgmt_root.tm.security.nat.policy_s.policy.load(
            name='fake_policy', partition='Common')
        rule_lst = rc.rules_s
        r2 = rule_lst.rule.load(name='fake_rule')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.kind == r2.kind
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()

    def test_delete(self, mgmt_root):
        p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
            name='fake_policy', partition='Common')
        rule_lst = p1.rules_s
        param_set = {'name': 'delete_me', 'place-after': 'first'}
        r1 = rule_lst.rule.create(**param_set)
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rule_lst.rule.load(name='delete_me')
        assert err.value.response.status_code == 404
        p1.delete()

    def test_load_no_object(self, mgmt_root):
        p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
            name='fake_policy', partition='Common')
        rule_lst = p1.rules_s
        with pytest.raises(HTTPError) as err:
            rule_lst.rule.load(name='not_exist')
        assert err.value.response.status_code == 404
        p1.delete()

    def test_load_and_update(self, rule, mgmt_root):
        r1 = rule
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.nat.policy_s.policy.load(name='fake_policy', partition='Common')
        rule_lst = rc.rules_s
        r2 = rule_lst.rule.load(name='fake_rule')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_rules_subcollection(self, rule, mgmt_root):
        r1 = rule
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~Common~fake_policy/rules/fake_rule'
        assert r1.name == 'fake_rule'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        nat_policy = mgmt_root.tm.security.nat.policy_s.policy.load(name='fake_policy', partition='Common')
        rule_list = nat_policy.rules_s
        rc = rule_list.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Rule)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
    reason='This collection is fully implemented on 12.1.0 or greater.'
)
class TestPolicy(object):
    def test_create_req_args(self, mgmt_root):
        p1 = mgmt_root.tm.security.nat.policy_s.policy.create(
            name='fake_policy1', partition='Common')
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy1'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.delete()

    def test_refresh(self, mgmt_root, policy):
        p1 = policy
        p2 = mgmt_root.tm.security.nat.policy_s.policy.load(
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
        p = mgmt_root.tm.security.nat.policy_s.policy
        p1 = p.create(name='delete_me', partition='Common')
        p1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.nat.policy_s.policy.load(
                name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        p = mgmt_root.tm.security.nat.policy_s.policy
        with pytest.raises(HTTPError) as err:
            p.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, policy):
        p1 = policy
        URI = 'https://localhost/mgmt/tm/security/' \
              'nat/policy/~Common~fake_policy'
        assert p1.name == 'fake_policy'
        assert p1.partition == 'Common'
        assert p1.selfLink.startswith(URI)
        assert not hasattr(p1, 'description')
        p1.description = DESC
        p1.update()
        assert hasattr(p1, 'description')
        assert p1.description == DESC
        p = mgmt_root.tm.security.nat.policy_s.policy
        p2 = p.load(name='fake_policy', partition='Common')
        assert p1.name == p2.name
        assert p1.partition == p2.partition
        assert p1.selfLink == p2.selfLink
        assert hasattr(p2, 'description')
        assert p1.description == p2.description

    def test_policies_collection(self, mgmt_root, policy):
        pc = mgmt_root.tm.security.nat.policy_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Policy)
