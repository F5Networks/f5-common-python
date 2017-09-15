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


def setup_tacacs_test(request, mgmt_root):
    def teardown():
        auth_tacobj.delete()
    request.addfinalizer(teardown)

    auth_tacobj = mgmt_root.tm.auth.tacacs_s.tacacs.create(name='system-auth',
                                                           protocol='ip',
                                                           service='ppp',
                                                           servers=[
                                                               '172.16.44.20'],
                                                           secret='letmein00')
    return auth_tacobj


class TestTacacs(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        tac1 = setup_tacacs_test(request, mgmt_root)
        tac2 = mgmt_root.tm.auth.tacacs_s.tacacs.load(name='system-auth')
        assert tac1.name == tac2.name

        # Update
        tac1.secret = 'letmeinagain00'
        tac1.update()
        assert tac1.secret != tac2.secret

        # Refresh
        tac2.refresh()
        assert tac1.secret == tac2.secret
