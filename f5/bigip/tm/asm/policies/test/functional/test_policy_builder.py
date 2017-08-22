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

import copy
import pytest

from six import iteritems
from distutils.version import LooseVersion
from f5.sdk_exception import UnsupportedOperation


class TestPolicyBuilder(object):
    def test_update_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.policy_builder.update()

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) > LooseVersion('11.5.4'),
        reason='This test is for versions below 11.6.0.'
    )
    def test_load_modify_v11_5(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:pbconfigstate'
        assert r1.enablePolicyBuilder is False
        r1.modify(enablePolicyBuilder=True)
        assert r1.enablePolicyBuilder is True
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
        assert hasattr(r2, 'responseStatusCodes')
        assert hasattr(r2, 'learnFromResponses')

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) > LooseVersion('11.6.1'),
        reason='This test is for versions greater than 11.5.4.'
    )
    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) <= LooseVersion('11.5.4'),
        reason='This test is for versions not below 11.6.0.'
    )
    def test_load_modify(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:pbconfigstate'
        assert r1.enablePolicyBuilder is False
        assert not hasattr(r1, 'responseStatusCodes')
        assert not hasattr(r1, 'learnFromResponses')
        r1.modify(enablePolicyBuilder=True)
        assert r1.enablePolicyBuilder is True
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
        assert hasattr(r2, 'responseStatusCodes')
        assert hasattr(r2, 'learnFromResponses')

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) > LooseVersion('12.0.0'),
        reason='This test is for version greater than 12.'
    )
    def test_refresh_modify(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:pbconfigstate'
        assert r1.enablePolicyBuilder is False
        assert not hasattr(r1, 'responseStatusCodes')
        assert not hasattr(r1, 'learnFromResponses')
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
        assert r2.enablePolicyBuilder is False
        assert not hasattr(r2, 'responseStatusCodes')
        assert not hasattr(r2, 'learnFromResponses')
        r2.modify(enablePolicyBuilder=True)
        assert r2.enablePolicyBuilder is True
        assert hasattr(r2, 'responseStatusCodes')
        assert hasattr(r2, 'learnFromResponses')
        r1.refresh()
        assert hasattr(r1, 'responseStatusCodes')
        assert hasattr(r1, 'learnFromResponses')
        assert r1.enablePolicyBuilder == r2.enablePolicyBuilder

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
        reason='This test is for version 12.1.0 or greater.'
    )
    def test_refresh_modify_v12(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:policy-builderstate'
        assert r1.trustAllIps is False
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
        assert r2.trustAllIps is False
        r2.modify(trustAllIps=True)
        assert r2.trustAllIps is True
        r1.refresh()
        assert r1.trustAllIps == r2.trustAllIps

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
        reason='This test is for version 12.0.0 or greater.'
    )
    def test_load_modify_v12(self, policy):
        r1 = policy.policy_builder.load()
        assert r1.kind == 'tm:asm:policies:policy-builder:policy-builderstate'
        assert r1.trustAllIps is False
        r1.modify(trustAllIps=True)
        assert r1.trustAllIps is True
        r2 = policy.policy_builder.load()
        assert r1.kind == r2.kind
