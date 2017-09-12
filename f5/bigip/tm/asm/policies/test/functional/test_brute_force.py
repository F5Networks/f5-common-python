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
from f5.bigip.tm.asm.policies.brute_force import Brute_Force_Attack_Prevention
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestBruteForceAttackPreventions(object):
    def test_create_req_arg(self, policy, set_login):
        login, reference = set_login
        login.modify(authenticationType='http-basic')
        bc = policy.brute_force_attack_preventions_s
        r1 = bc.brute_force_attack_prevention.create(urlReference=reference)
        assert r1.kind == 'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventionstate'
        assert r1.preventionDuration == 'unlimited'
        assert r1.reEnableLoginAfter == 600
        r1.delete()

    def test_create_optional_args(self, policy, set_login):
        login, reference = set_login
        login.modify(authenticationType='http-basic')
        bc = policy.brute_force_attack_preventions_s
        r1 = bc.brute_force_attack_prevention.create(
            urlReference=reference,
            preventionDuration='120',
            reEnableLoginAfter=300
        )
        assert r1.kind == 'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventionstate'
        assert r1.preventionDuration == '120'
        assert r1.reEnableLoginAfter == 300
        r1.delete()

    def test_refresh(self, set_brute, policy):
        r1 = set_brute
        bc = policy.brute_force_attack_preventions_s
        r2 = bc.brute_force_attack_prevention.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.preventionDuration == r2.preventionDuration
        r2.modify(preventionDuration='120')
        assert r1.preventionDuration == 'unlimited'
        assert r2.preventionDuration == '120'
        r1.refresh()
        assert r1.preventionDuration == '120'

    def test_delete(self, policy, set_login):
        login, reference = set_login
        login.modify(authenticationType='http-basic')
        bc = policy.brute_force_attack_preventions_s
        r1 = bc.brute_force_attack_prevention.create(urlReference=reference)
        idhash = r1.id
        r1.delete()
        with pytest.raises(HTTPError) as err:
            bc.brute_force_attack_prevention.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        bc = policy.brute_force_attack_preventions_s
        with pytest.raises(HTTPError) as err:
            bc.brute_force_attack_prevention.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, set_brute, policy):
        r1 = set_brute
        bc = policy.brute_force_attack_preventions_s
        assert r1.kind == 'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventionstate'
        assert r1.reEnableLoginAfter == 600
        r1.modify(reEnableLoginAfter=300)
        assert r1.reEnableLoginAfter == 300
        r2 = bc.brute_force_attack_prevention.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.reEnableLoginAfter == r2.reEnableLoginAfter

    def test_brute_force_subcollection(self, policy, set_brute):
        r1 = set_brute
        assert r1.kind == 'tm:asm:policies:brute-force-attack-preventions:brute-force-attack-preventionstate'
        assert r1.preventionDuration == 'unlimited'
        assert r1.reEnableLoginAfter == 600
        cc = policy.brute_force_attack_preventions_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Brute_Force_Attack_Prevention)
