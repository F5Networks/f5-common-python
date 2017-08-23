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
class TestGeolocationEnforcement(object):
    def test_update_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.geolocation_enforcement.update()

    def test_load(self, policy):
        r1 = policy.geolocation_enforcement.load()
        assert r1.kind == 'tm:asm:policies:geolocation-enforcement:geolocation-enforcementstate'
        assert r1.disallowedLocations == []
        r1.modify(disallowedLocations=['Poland'])
        assert r1.disallowedLocations == ['Poland']
        r2 = policy.geolocation_enforcement.load()
        assert r1.kind == r2.kind
        assert r1.disallowedLocations == r2.disallowedLocations

    def test_refresh(self, policy):
        r1 = policy.geolocation_enforcement.load()
        assert r1.kind == 'tm:asm:policies:geolocation-enforcement:geolocation-enforcementstate'
        assert r1.disallowedLocations == []
        r2 = policy.geolocation_enforcement.load()
        assert r1.kind == r2.kind
        assert r1.disallowedLocations == r2.disallowedLocations
        r2.modify(disallowedLocations=['Poland'])
        assert r2.disallowedLocations == ['Poland']
        r1.refresh()
        assert r1.disallowedLocations == r2.disallowedLocations
