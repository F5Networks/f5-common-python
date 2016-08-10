
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

import os
from requests import HTTPError
from tempfile import NamedTemporaryFile


def setup_ifile_test(request, mgmt_root, name, sourcepath):
    if1 = mgmt_root.tm.sys.file.ifiles.ifile.create(name=name,
                                                    sourcePath=sourcepath)

    def teardown():
        # Remove the ifile.
        try:
            if1.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
    request.addfinalizer(teardown)

    return if1


def test_CURDL(request, mgmt_root):
    # Create
    ntf = NamedTemporaryFile()
    ntf_basename = os.path.basename(ntf.name)
    ntf.write('this is a test file')
    ntf.seek(0)
    # Upload the file
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)

    tpath_name = 'file:/var/config/rest/downloads/{0}'.format(ntf_basename)
    if1 = setup_ifile_test(request, mgmt_root, ntf_basename, tpath_name)
    assert if1.name == ntf_basename

    # Load Object
    if2 = mgmt_root.tm.sys.file.ifiles.ifile.load(name=ntf_basename)
    assert if1.name == if2.name

    # Rewrite file contents and Update Object
    ntf.write('this is still a test file')
    ntf.seek(0)
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)

    if3 = mgmt_root.tm.sys.file.ifiles.ifile.load(name=ntf_basename)
    if3.update(sourcePath=tpath_name)
    assert if1.revision != if3.revision

    # Refresh if2 and make sure revision matches if3
    if2.refresh()
    assert if2.revision == if3.revision
