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

import os
import pytest
import tempfile

from distutils.version import LooseVersion


pytestmark = pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='This series of tests requires BIG-IP version 12.0.0 or greater.'
)


@pytest.fixture
def timer_policy(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    resource = mgmt_root.tm.net.timer_policys.timer_policy.create(
        name=name
    )
    yield resource
    resource.delete()


@pytest.fixture
def timer_policies(mgmt_root):
    collection = mgmt_root.tm.net.timer_policys
    return collection


class TestResource(object):
    def test_get_collection(self, timer_policy, timer_policies):
        assert len(list(timer_policies.get_collection())) > 0

    def test_create(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        resource = mgmt_root.tm.net.timer_policys.timer_policy.create(
            name=name
        )
        assert resource.name == name
        resource.delete()

    def test_update(self, timer_policy):
        timer_policy.description = 'my description'
        timer_policy.rules = [
            {
                "name": "rule1",
                "description": "rule description",
                "ipProtocol": "all-other",
                "timers": [
                    {
                        "name": "flow-idle-timeout",
                        "value": "346"
                    }
                ]
            }
        ]
        timer_policy.update()
        assert timer_policy.description == 'my description'
        assert len(timer_policy.rules) == 1

    def test_refresh(self, timer_policy):
        assert not hasattr(timer_policy, 'description')
        timer_policy.description = 'disabled'

        # A refresh without an update should show no change
        timer_policy.refresh()
        assert not hasattr(timer_policy, 'description')
