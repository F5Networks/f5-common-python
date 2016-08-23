from __future__ import print_function
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

import mock
import pytest

from f5.bigip.cm.autodeploy.software_images import\
    ImageFilesMustHaveDotISOExtension
from f5.bigip import ManagementRoot


CHUNKSIZE = 20


def test_software_image_uploads_80a(tmpdir, fakeicontrolsessionfactory):
    fakeicontrolsessionfactory()
    filepath = tmpdir.mkdir('testdir').join('eightya.iso')
    filepath.write(80*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    sius = mr.cm.autodeploy.software_image_uploads
    sius.upload_image(str(filepath), chunk_size=CHUNKSIZE)
    session_mock = mr._meta_data['icr_session']
    for i in range(4):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == 'a'*CHUNKSIZE


def test_software_image_uploads_70a(tmpdir, fakeicontrolsessionfactory):
    fakeicontrolsessionfactory()
    filepath = tmpdir.mkdir('testdir').join('seventya.iso')
    filepath.write(70*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    sius = mr.cm.autodeploy.software_image_uploads
    session_mock = mr._meta_data['icr_session']
    sius.upload_image(str(filepath), chunk_size=CHUNKSIZE)
    for i in range(3):
        print(i)
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == 'a'*CHUNKSIZE
    lchunk = session_mock.post.call_args_list[3][1]['data']
    assert 10*'a' == lchunk


def test_non_ISO_extension(tmpdir, fakeicontrolsessionfactory):
    fakeicontrolsessionfactory()
    filepath = tmpdir.mkdir('testdir').join('wrong.name')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    sius = mr.cm.autodeploy.software_image_uploads
    with pytest.raises(ImageFilesMustHaveDotISOExtension) as EIO:
        sius.upload_image(str(filepath), chunk_size=CHUNKSIZE)
    assert EIO.value.message == 'wrong.name'
