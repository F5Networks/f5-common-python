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


class TestAnalytics(object):
    _enable_settings = {"aclRules": {"collectClientIp": "enabled"}}
    _disable_settings = {"aclRules": {"collectClientIp": "disabled"}}

    def test_modify_settings(self, mgmt_root):
        settings = mgmt_root.tm.security.analytics.settings.load()
        assert "aclRules" in settings.__dict__
        assert settings.aclRules["collectClientIp"] == "enabled"
        settings.modify(**self._disable_settings)
        assert settings.aclRules["collectClientIp"] == "disabled"
        settings.modify(**self._enable_settings)
