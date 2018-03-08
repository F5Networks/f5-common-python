# Copyright 2018 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import pytest


@pytest.fixture
def cgnat1(mgmt_root):
    resource = mgmt_root.tm.sys.feature_module.cgnat.load()
    yield resource
    resource.update(enabled=True)


@pytest.fixture
def cgnat2(mgmt_root):
    resource = mgmt_root.tm.sys.feature_module.cgnat.load()
    yield resource


class TestFeatureModule(object):

    def test_RUL(self, cgnat1, cgnat2):
        assert cgnat1.disabled == cgnat2.disabled
        assert cgnat1.enabled is True

        # Update
        cgnat1.update(disabled=True)
        assert cgnat1.disabled is True
        assert cgnat1.disabled != cgnat2.disabled

        # Refresh
        cgnat2.refresh()
        assert cgnat1.disabled == cgnat2.disabled
