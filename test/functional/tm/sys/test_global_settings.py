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


def set_global_settings_test(request, bigip):
    def teardown():
        gs.usernamePrompt = 'Username'
        gs.update()
    request.addfinalizer(teardown)
    gs = bigip.sys.global_settings.load()
    return gs


class TestGlobal_Setting(object):
    def test_RUL(self, request, bigip):
        # Load
        gs1 = set_global_settings_test(request, bigip)
        gs2 = bigip.sys.global_settings.load()
        assert gs1.usernamePrompt == 'Username'
        assert gs1.usernamePrompt == gs2.usernamePrompt

        # Update
        gs1.usernamePrompt = 'User'
        gs1.update()
        assert gs1.usernamePrompt == 'User'
        assert gs2.usernamePrompt == 'Username'

        # Refresh
        gs2.refresh()
        assert gs1.usernamePrompt == gs2.usernamePrompt
