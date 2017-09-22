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


def setup_cert_ldap_test(request, mgmt_root):
    def teardown():
        auth_cldapobj.delete()
    request.addfinalizer(teardown)

    auth_cldapobj = mgmt_root.tm.auth.cert_ldaps.cert_ldap.create(
        name='system-auth',
        servers=['my.test.local']
        )
    return auth_cldapobj


class TestCertLdap(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        cldap1 = setup_cert_ldap_test(request, mgmt_root)
        cldap2 = mgmt_root.tm.auth.cert_ldaps.cert_ldap.load(name='system-auth')
        assert cldap1.name == cldap2.name

        # Update
        cldap1.servers = ['my.test.local', 'myother.test.local']
        cldap1.update()
        assert len(cldap1.servers) != len(cldap2.servers)

        # Refresh
        cldap2.refresh()
        assert len(cldap1.servers) == len(cldap2.servers)
