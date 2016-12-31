# Copyright 2015-2106 F5 Networks Inc.
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

from requests.exceptions import HTTPError


def delete_tenant(mgmt_root, name):
    try:
        p = mgmt_root.cm.cloud.tenants_s.tenant.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_basic_test(request, mgmt_root, name):
    def teardown():
        delete_tenant(mgmt_root, name)

    tenant1 = mgmt_root.cm.cloud.tenants_s.tenant.create(name=name)
    request.addfinalizer(teardown)
    return tenant1


class TestTenant(object):
    def test_create(self, request, mgmt_root):
        tenant = setup_basic_test(request, mgmt_root, 'tenant1')
        assert tenant.name == 'tenant1'
        tenant.refresh()
        assert tenant.name == 'tenant1'
        assert tenant.selfLink == \
            "https://localhost/mgmt/cm/cloud/tenants/tenant1"

    def test_update(self, request, mgmt_root):
        tenant1 = setup_basic_test(request, mgmt_root, 'tenant2')
        assert tenant1.name == 'tenant2'
        assert not hasattr(tenant1, 'description')
        assert not hasattr(tenant1, 'addressContact')
        assert not hasattr(tenant1, 'phone')
        assert not hasattr(tenant1, 'email')

        tenant1.description = 'description'
        tenant1.addressContact = 'address'
        tenant1.phone = 'phone'
        tenant1.email = 'email@foo.com'
        tenant1.update()

        tenant2 = mgmt_root.cm.cloud.tenants_s.tenant.load(name='tenant2')
        assert tenant2.name == 'tenant2'
        assert tenant2.description == 'description'
        assert tenant2.addressContact == 'address'
        assert tenant2.phone == 'phone'
        assert tenant2.email == 'email@foo.com'
