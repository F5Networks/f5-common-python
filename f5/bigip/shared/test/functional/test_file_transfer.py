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

from distutils.version import LooseVersion

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
def uploaded_file_madm(mgmt_root, upload_content):
    fake_name = 'fooMadm.txt'
    upath = '/var/config/rest/downloads'
    dpath = '/var/config/rest/madm'
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


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '13.0.0'),
    reason='This fixture requires >= 13.0.0.'
)
@pytest.fixture(scope='function')
def uploaded_file_v13(mgmt_root, upload_content):
    fake_name = 'foo13.txt'
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


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '13.0.0'),
    reason='This fixture requires >= 13.0.0.'
)
class TestFileTransferV13(object):
    def test_download_v13(self, mgmt_root, uploaded_file_v13, upload_content):
        dest = '/tmp/{0}'.format(uploaded_file_v13)
        bulk = mgmt_root.shared.file_transfer.bulk
        bulk.download_file(uploaded_file_v13, dest)
        assert os.path.exists(dest)

        fh = open(dest, 'r')
        content = fh.read()
        assert content == upload_content


class TestMadmFileTransfer(object):
    def test_download(self, mgmt_root, uploaded_file_madm, upload_content):
        dest = '/tmp/{0}'.format(uploaded_file_madm)
        madm = mgmt_root.shared.file_transfer.madm
        madm.download_file(uploaded_file_madm, dest)
        assert os.path.exists(dest)

        fh = open(dest, 'r')
        content = fh.read()
        assert content == upload_content
