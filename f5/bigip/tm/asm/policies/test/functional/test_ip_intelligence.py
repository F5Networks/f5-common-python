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
from f5.sdk_exception import UnsupportedOperation


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestIPIntelligence(object):
    def test_update_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.ip_intelligence.update()

    def test_load(self, policy):
        r1 = policy.ip_intelligence.load()
        assert r1.kind == 'tm:asm:policies:ip-intelligence:ip-intelligencestate'
        assert r1.enabled is False
        assert not hasattr(r1, 'ipIntelligenceCategories')
        r1.modify(enabled=True)
        assert r1.enabled is True
        assert hasattr(r1, 'ipIntelligenceCategories')
        r2 = policy.ip_intelligence.load()
        assert r1.kind == r2.kind
        assert r1.enabled == r2.enabled

    def test_refresh(self, policy):
        r1 = policy.ip_intelligence.load()
        assert r1.kind == 'tm:asm:policies:ip-intelligence:ip-intelligencestate'
        assert r1.enabled is False
        assert not hasattr(r1, 'ipIntelligenceCategories')
        r2 = policy.ip_intelligence.load()
        assert r1.kind == r2.kind
        assert r1.enabled == r2.enabled
        r2.modify(enabled=True)
        assert r2.enabled is True
        assert hasattr(r2, 'ipIntelligenceCategories')
        r1.refresh()
        assert r1.enabled is True
        assert hasattr(r1, 'ipIntelligenceCategories')
