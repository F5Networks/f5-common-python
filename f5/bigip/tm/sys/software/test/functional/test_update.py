# Copyright 2016 F5 Networks Inc.
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
def cleaner(request, mgmt_root):
    initial = mgmt_root.tm.sys.software.update.load()

    def teardown():
        initial.update()
    request.addfinalizer(teardown)


class TestUpdate(object):
    def test_load(self, cleaner, mgmt_root):
        su = mgmt_root.tm.sys.software.update.load()
        assert su.autoCheck == 'enabled'
        su.refresh()
        assert su.autoCheck == 'enabled'

    def test_update_autocheck(self, cleaner, mgmt_root):
        su = mgmt_root.tm.sys.software.update.load()
        su.update(autoCheck='disabled')
        assert su.autoCheck == 'disabled'
        su.update(autoCheck='enabled')
        assert su.autoCheck == 'enabled'

    def test_update_frequency(self, cleaner, mgmt_root):
        frequencies = ['daily', 'monthly', 'weekly']
        su = mgmt_root.tm.sys.software.update.load()

        for frequency in frequencies:
            su.update(frequency=frequency)
            assert su.frequency == frequency
