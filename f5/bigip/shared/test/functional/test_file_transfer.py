# Copyright 2017 F5 Networks Inc.
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
import pytest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@pytest.fixture(scope='function')
def upload_content():
    content = 80*'a'
    yield content


@pytest.fixture(scope='function')
def uploaded_file(mgmt_root, upload_content):
    fake_name = 'foo.txt'
    upath = '/var/config/rest/downloads'
    dpath = '/var/config/rest/bulk'
    content = StringIO(upload_content)

    ftu = mgmt_root.shared.file_transfer.uploads
    ftu.upload_stringio(content, fake_name, chunk_size=20)
    mgmt_root.tm.util.unix_mv.exec_cmd(
        'run',
        utilCmdArgs='{0}/{2} {1}/{2}'.format(upath, dpath, fake_name)
    )

    yield fake_name
    tpath_name = '{0}/{1}'.format(dpath, fake_name)
    mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs=tpath_name)


class TestSoftwareImage(object):
    def test_download(self, mgmt_root, uploaded_file, upload_content):
        dest = '/tmp/{0}'.format(uploaded_file)
        bulk = mgmt_root.shared.file_transfer.bulk
        bulk.download_file(uploaded_file, dest)
        assert os.path.exists(dest)

        fh = open(dest, 'r')
        content = fh.read()
        assert content == upload_content
