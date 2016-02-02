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

from requests import HTTPError


TESTDESCRIPTION = "TESTDESCRIPTION"


def setup_folder_test(request, bigip, name, subpath):
    def teardown():
        '''Remove the f1 folder only.

        We don't want to delete all folders because some of them are system
        folders that we didn't create.
        '''
        try:
            f1.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
    request.addfinalizer(teardown)

    fc1 = bigip.sys.foldercollection
    f1 = fc1.folder.create(name=name, subPath=subpath)
    return f1, fc1


class TestFolder(object):
    def test_CURDL(self, request, bigip):
        # Create
        f1, fc1 = setup_folder_test(request, bigip, 'testfolder', '/')
        assert f1.name == 'testfolder'
        assert f1.subPath == '/'
        assert f1.fullPath == '/testfolder'

        # Load - Test with the various partition/name combinations
        f2 = fc1.folder.load(partition='testfolder')
        f3 = fc1.folder.load(name='testfolder')
        for f in [f2, f3]:
            assert f.name == f1.name
            assert f.generation == f1.generation

        # Update - Make sure that the deviceGroup logic is working
        f1.description = TESTDESCRIPTION
        f1.update()
        assert f1.description == TESTDESCRIPTION
        assert f1.deviceGroup == 'none'
        assert f1.inheritedDevicegroup == 'true'
        assert f1.generation > f2.generation

        # Refresh
        f2.refresh()
        assert f1.generation == f2.generation

        # We assume delete is taken care of by teardown

    def test_load_root_folder_by_name(self, bigip):
        fc = bigip.sys.foldercollection
        f = fc.folder.load(name='/')
        assert f.name == '/'
        assert f.fullPath == '/'

    def test_load_root_folder_by_partition(self, bigip):
        fc = bigip.sys.foldercollection
        f = fc.folder.load(partition='/')
        assert f.name == '/'
        assert f.fullPath == '/'

    def test_load_root_no_attributes(self, bigip):
        fc = bigip.sys.foldercollection
        f = fc.folder.load()
        assert f.name == '/'
        assert f.fullPath == '/'


class TestFolderCollection(object):
    def test_get_collection(self, request, bigip):
        setup_folder_test(request, bigip, 'testfolder', '/')
        fc = bigip.sys.foldercollection
        folders = fc.get_collection()

        assert len(folders)
        found_folder = False

        for folder in folders:
            if folder.__dict__.get('name', '') == 'testfolder':
                found_folder = True
                break
        assert found_folder
