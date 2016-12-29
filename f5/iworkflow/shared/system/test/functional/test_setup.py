# Copyright 2016 F5 Networks Inc.
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


def setup_setup_test(request, mgmt_root):
    def teardown():
        # There is a difference in 11.6.0 and 12.0.0 default for max clients.
        # Added explicit maxClient to facilitate this change.
        initial_setup.update(
            isSystemSetup=True,
            isAdminPasswordChanged=False,
            isRootPasswordChanged=False,
        )
    request.addfinalizer(teardown)
    initial_setup = mgmt_root.shared.system.setup.load()
    return initial_setup


class TestSetup(object):
    def test_load(self, request, mgmt_root):
        setup = setup_setup_test(request, mgmt_root)
        assert setup.isSystemSetup is True
        setup.refresh()
        assert setup.isSystemSetup is True

    def test_update(self, request, mgmt_root):
        setup = setup_setup_test(request, mgmt_root)
        setup.update(isSystemSetup=False)
        assert setup.isSystemSetup is False
        setup.update(isSystemSetup=True)
        assert setup.isSystemSetup is True
