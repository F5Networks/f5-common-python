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
import pytest

from f5.sdk_exception import UtilError
from tempfile import NamedTemporaryFile


def test_E_unix_mv(mgmt_root):
    ntf = NamedTemporaryFile(delete=False)
    ntf_basename = os.path.basename(ntf.name)
    ntf.write('text for test file')
    ntf.seek(0)
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)
    tpath_name = '/var/config/rest/downloads'

    fm1 = mgmt_root.tm.util.unix_mv.exec_cmd(
        'run',
        utilCmdArgs='{0}/{1} {0}/testmove.txt'.format(
            tpath_name, ntf_basename))

    # validate object was created
    assert fm1.utilCmdArgs == '{0}/{1} {0}/testmove.txt'.format(tpath_name,
                                                                ntf_basename)

    # if command was successful, commandResult should not be present
    assert 'commandResult' not in fm1.__dict__


def test_mv_file_does_not_exist(mgmt_root):
    # UtilError should be raised when non-existent file is mentioned
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.unix_mv.exec_cmd('run', utilCmdArgs='/foo/mf.txt')
    assert 'missing destination file operand after' in str(err.value)
