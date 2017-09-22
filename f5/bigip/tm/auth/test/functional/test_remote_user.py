# Copyright 2017 F5 Networks Inc.
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


def setup_remote_user_test(request, mgmt_root):
    def teardown():
        ru.remoteConsoleAccess = console
        ru.update()
    request.addfinalizer(teardown)

    ru = mgmt_root.tm.auth.remote_user.load()
    console = ru.remoteConsoleAccess

    return ru


class TestRemoteUser(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        ru1 = setup_remote_user_test(request, mgmt_root)
        ru2 = mgmt_root.tm.auth.remote_user.load()
        assert ru1.remoteConsoleAccess == ru2.remoteConsoleAccess

        # Update
        ru1.remoteConsoleAccess = 'tmsh'
        ru1.update()
        assert 'tmsh' in ru1.remoteConsoleAccess
        assert 'tmsh' not in ru2.remoteConsoleAccess

        # Refresh
        ru2.refresh()
        assert 'tmsh' in ru2.remoteConsoleAccess
