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
from distutils.version import LooseVersion


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


pytestmark = pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='Needs v12 TMOS or greater to pass.'
)


@pytest.fixture(scope='function')
def upload_content():
    content = 80*'a'
    yield content


@pytest.fixture(scope='function')
def uploaded_file(mgmt_root, upload_content):
    fake_name = 'foo.iso'
    tpath_name = '/var/config/rest/downloads'
    content = StringIO(upload_content)

    ftu = mgmt_root.shared.file_transfer.uploads
    ftu.upload_stringio(content, fake_name, chunk_size=20)
    mgmt_root.tm.util.unix_mv.exec_cmd(
        'run',
        utilCmdArgs='{0}/{1} /shared/images/{1}'.format(tpath_name, fake_name)
    )
    yield fake_name
    tpath_name = '/shared/images/{0}'.format(fake_name)
    mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs=tpath_name)


class TestSoftwareImage(object):
    def test_download(self, mgmt_root, uploaded_file, upload_content):
        dest = "/tmp/{0}".format(uploaded_file)
        downloads = mgmt_root.cm.autodeploy.software_image_downloads
        downloads.download_file(uploaded_file, dest)
        assert os.path.exists(dest)

        fh = open(dest, 'r')
        content = fh.read()
        assert content == upload_content
