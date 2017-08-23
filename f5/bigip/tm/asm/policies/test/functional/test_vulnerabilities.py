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
from requests.exceptions import HTTPError
from f5.sdk_exception import UnsupportedOperation
from f5.bigip.tm.asm.policies.vulnerabilities import Vulnerabilities


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestVulnerabilities(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.vulnerabilities_s.vulnerabilities.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.vulnerabilities_s.vulnerabilities.delete()

    def test_modify_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.vulnerabilities_s.vulnerabilities.create()

    def test_refresh(self, policy, set_vulnerability):
        hashid = set_vulnerability
        r1 = policy.vulnerabilities_s.vulnerabilities.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:vulnerabilities:vulnerabilitystate'
        r2 = policy.vulnerabilities_s.vulnerabilities.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.vulnerabilities_s.vulnerabilities.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, set_vulnerability):
        hashid = set_vulnerability
        r1 = policy.vulnerabilities_s.vulnerabilities.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:vulnerabilities:vulnerabilitystate'
        r2 = policy.vulnerabilities_s.vulnerabilities.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_vulnerabilities_subcollection(self, set_vulnerability, policy):
        mc = policy.vulnerabilities_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Vulnerabilities)
