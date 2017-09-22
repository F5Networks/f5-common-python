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


def setup_ldap_test(request, mgmt_root):
    def teardown():
        auth_ldapobj.delete()
    request.addfinalizer(teardown)

    auth_ldapobj = mgmt_root.tm.auth.ldaps.ldap.create(
        name='system-auth',
        servers=['my.test.local'],

    )
    return auth_ldapobj


class TestLdap(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        ldap1 = setup_ldap_test(request, mgmt_root)
        ldap2 = mgmt_root.tm.auth.ldaps.ldap.load(name='system-auth')
        assert ldap1.name == ldap2.name

        # Update
        ldap1.servers = ['my.test.local', 'my.othertest.local']
        ldap1.update()
        assert len(ldap1.servers) != len(ldap2.servers)

        # Refresh
        ldap2.refresh()
        assert len(ldap1.servers) == len(ldap2.servers)
