# Copyright 2015 F5 Networks Inc.
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


import pytest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from requests.exceptions import HTTPError


@pytest.fixture(scope='function')
def iapp_lx(mgmt_root):
    fake_iapp_name = 'foo-iapp.rpm'
    sio = StringIO(80*'a')
    ftu = mgmt_root.shared.file_transfer.uploads
    ftu.upload_stringio(sio, fake_iapp_name, chunk_size=20)
    yield fake_iapp_name
    tpath_name = '/var/config/rest/downloads/{0}'.format(fake_iapp_name)
    mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs=tpath_name)


@pytest.fixture(scope='function')
def pkg_task(mgmt_root, iapp_lx):
    collection = mgmt_root.shared.iapp.package_management_tasks_s
    task = collection.package_management_task.create(
        operation='INSTALL',
        packageFilePath='/var/config/rest/downloads/foo-iapp.rpm'
    )
    yield task


class TestPackageManagementTasks(object):
    def test_create_task(self, pkg_task):
        assert pkg_task.operation == "INSTALL"
        assert pkg_task.kind == \
            'shared:iapp:package-management-tasks:iapppackagemanagementtaskstate'  # NOQA

    def test_load_no_task(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            collection = mgmt_root.shared.iapp.package_management_tasks_s
            collection.package_management_task.load(
                id='asdasdasd'
            )
        assert err.value.response.status_code == 404

    def test_load(self, mgmt_root, pkg_task):
        collection = mgmt_root.shared.iapp.package_management_tasks_s
        resource = collection.package_management_task.load(id=pkg_task.id)
        assert pkg_task.id == resource.id
        assert pkg_task.selfLink == resource.selfLink

    def test_exists(self, mgmt_root, pkg_task):
        pid = str(pkg_task.id)
        collection = mgmt_root.shared.iapp.package_management_tasks_s
        exists = collection.package_management_task.exists(id=pid)
        assert exists is True

    def test_cancel(self, pkg_task):
        pkg_task.cancel()
        assert pkg_task.__dict__['canceled']

    def test_delete(self, pkg_task):
        pkg_task.cancel()
        while True:
            pkg_task.refresh()
            if pkg_task.status in ['CANCELED', 'FAILED', 'FINISHED']:
                pkg_task.delete()
                break
        assert pkg_task.__dict__['deleted']

    def test_package_mgmt_tasks_collection(self, mgmt_root, iapp_lx):
        col = mgmt_root.shared.iapp.package_management_tasks_s.get_collection()
        assert isinstance(col, list)
        assert len(col) > 0
