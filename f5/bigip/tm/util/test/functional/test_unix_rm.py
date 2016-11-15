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

import pytest

from f5.bigip.mixins import UtilError
import os
from tempfile import NamedTemporaryFile


def test_E_unix_rm(mgmt_root):
    ntf = NamedTemporaryFile(delete=False)
    ntf_basename = os.path.basename(ntf.name)
    ntf.write('text for test file')
    ntf.seek(0)
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)
    tpath_name = '/var/config/rest/downloads/{0}'.format(ntf_basename)

    fr1 = mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs=tpath_name)

    # validate object was created
    assert fr1.utilCmdArgs == '/var/config/rest/downloads/{0}'.format(
        ntf_basename)

    # if command was successful, commandResult should not be present
    assert 'commandResult' not in fr1.__dict__


def test_rm_file_does_not_exist(mgmt_root):
    # UtilError should be raised when non-existent file is mentioned
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs='testfile.txt')
    assert 'No such file or directory' in str(err.value)
