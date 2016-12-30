# Copyright 2015-2016 F5 Networks Inc.
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


def delete_resource(mgmt_root, uuid):
    try:
        local = mgmt_root.cm.cloud.connectors.locals.local.load(uuid=uuid)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    local.delete()


def setup_create_test(request, mgmt_root, name):
    def teardown():
        delete_resource(mgmt_root, uuid)
    request.addfinalizer(teardown)
    lo = mgmt_root.cm.cloud.connectors.locals
    local = lo.local.create(name=name)
    uuid = local.connectorId
    return local, lo


class TestLocal(object):
    def test_local_curdl(self, request, mgmt_root):
        local, lo = setup_create_test(request, mgmt_root, 'local1')
        assert local.name == 'local1'
        assert local.kind == 'cm:cloud:connectors:cloudconnectorstate'
        assert local.selfLink.startswith(
            'https://localhost/mgmt/cm/cloud/connectors/local/')
