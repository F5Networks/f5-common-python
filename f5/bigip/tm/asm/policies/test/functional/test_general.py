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
from f5.sdk_exception import UnsupportedMethod


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='This collection is fully implemented on 13.0.0 or greater.'
)
class TestGeneral(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedMethod):
            policy.general.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedMethod):
            policy.general.delete()

    def test_load(self, policy):
        r1 = policy.general.load()
        assert r1.kind == 'tm:asm:policies:general:generalstate'
        assert r1.enforcementReadinessPeriod == 7
        r1.modify(enforcementReadinessPeriod=10)
        assert r1.enforcementReadinessPeriod == 10
        r2 = policy.general.load()
        assert r1.kind == r2.kind
        assert r1.enforcementReadinessPeriod == r2.enforcementReadinessPeriod
        r1.modify(enforcementReadinessPeriod=7)

    def test_refresh(self, policy):
        r1 = policy.general.load()
        assert r1.kind == 'tm:asm:policies:general:generalstate'
        assert r1.enforcementReadinessPeriod == 7
        r2 = policy.general.load()
        assert r1.kind == r2.kind
        assert r1.enforcementReadinessPeriod == r2.enforcementReadinessPeriod
        r2.modify(enforcementReadinessPeriod=10)
        assert r2.enforcementReadinessPeriod == 10
        r1.refresh()
        assert r1.enforcementReadinessPeriod == r2.enforcementReadinessPeriod
        r2.modify(enforcementReadinessPeriod=10)
