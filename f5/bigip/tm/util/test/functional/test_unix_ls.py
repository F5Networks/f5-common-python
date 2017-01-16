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

from distutils.version import LooseVersion
import pytest

from f5.sdk_exception import UtilError
from icontrol.session import iControlUnexpectedHTTPError
import os
from tempfile import NamedTemporaryFile


def test_E_unix_ls(mgmt_root):
    ntf = NamedTemporaryFile(delete=False)
    ntf_basename = os.path.basename(ntf.name)
    ntf.write('text for test file')
    ntf.seek(0)
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)
    tpath_name = '/var/config/rest/downloads/{0}'.format(ntf_basename)

    # create
    fls1 = mgmt_root.tm.util.unix_ls.exec_cmd('run', utilCmdArgs=tpath_name)

    # validate object was created
    assert fls1.utilCmdArgs == tpath_name

    # commandResult should be present with successful listing
    assert 'commandResult' in fls1.__dict__

    # commandResult listing should match the file we requested a listing for
    assert '{0}\n'.format(fls1.utilCmdArgs) == fls1.commandResult

    # UtilError should be raised when non-existent file is mentioned
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.unix_ls.exec_cmd('run',
                                           utilCmdArgs='/configs/testfile.txt')
    assert 'No such file or directory' in str(err)

    # clean up created file
    mgmt_root.tm.util.unix_rm.exec_cmd('run', utilCmdArgs=tpath_name)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release'))
    < LooseVersion('12.0.0'),
    reason='Needs v12.0.0 TMOS or greater to pass.'
)
def test_bad_command_options_post_v12(mgmt_root):
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.util.unix_ls.exec_cmd('run', utilCmdArgs='-9')
    assert 'unix-ls does not support' in err.value.response.text


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release'))
    >= LooseVersion('12.0.0'),
    reason='Needs TMOS version less than v12.0.0 to pass.'
)
def test_bad_command_options_pre_v12(mgmt_root):
    with pytest.raises(UtilError) as err:
        mgmt_root.tm.util.unix_ls.exec_cmd('run', utilCmdArgs='-9')
    assert 'invalid option -- 9' in str(err)
