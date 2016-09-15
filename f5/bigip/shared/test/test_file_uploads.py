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
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from f5.bigip import ManagementRoot
from f5.bigip.shared.file_transfer import\
    FileMustNotHaveDotISOExtension


def test_file_upload_80a(tmpdir, fakeicontrolsession):
    filepath = tmpdir.mkdir('testdir').join('eightya.txt')
    filepath.write(80*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    ftu = mr.shared.file_transfer.uploads
    ftu.upload_file(filepath.__str__(), chunk_size=20)
    session_mock = mr._meta_data['icr_session']
    for i in range(4):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == b'aaaaaaaaaaaaaaaaaaaa'


def test_file_upload_70a(tmpdir, fakeicontrolsession):
    filepath = tmpdir.mkdir('testdir').join('seventya.txt')
    filepath.write(70*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    ftu = mr.shared.file_transfer.uploads
    ftu.upload_file(filepath.__str__(), chunk_size=20)
    session_mock = mr._meta_data['icr_session']
    for i in range(3):
        print(i)
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == b'aaaaaaaaaaaaaaaaaaaa'
    lchunk = session_mock.post.call_args_list[3][1]['data']
    assert b'a'*10 == lchunk


def test_ISO_extension(tmpdir, fakeicontrolsession):
    filepath = tmpdir.mkdir('testdir').join('wrongname.iso')
    filepath.write('fake')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    ftu = mr.shared.file_transfer.uploads
    with pytest.raises(FileMustNotHaveDotISOExtension) as EIO:
        ftu.upload_file(filepath.__str__(), chunk_size=21)
    assert str(EIO.value) == 'wrongname.iso'


def test_stringio_upload_80a(tmpdir, fakeicontrolsession):
    sio = StringIO(80*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    ftu = mr.shared.file_transfer.uploads
    ftu.upload_stringio(sio, 'testtarget', chunk_size=20)
    session_mock = mr._meta_data['icr_session']
    for i in range(4):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == 'aaaaaaaaaaaaaaaaaaaa'


def test_stringio_upload_70a(tmpdir, fakeicontrolsession):
    sio = StringIO(70*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    ftu = mr.shared.file_transfer.uploads
    ftu.upload_stringio(sio, 'testtarget', chunk_size=20)
    session_mock = mr._meta_data['icr_session']
    for i in range(3):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == 'aaaaaaaaaaaaaaaaaaaa'
    lchunk = session_mock.post.call_args_list[3][1]['data']
    assert 10*'a' == lchunk


def test_bytes_upload_80a(tmpdir, fakeicontrolsession):
    bytestring80a = 80*'a'
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    ftu = mr.shared.file_transfer.uploads
    ftu.upload_bytes(bytestring80a, 'testtarget', chunk_size=20)
    session_mock = mr._meta_data['icr_session']
    for i in range(4):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == 'aaaaaaaaaaaaaaaaaaaa'


def test_bytes_upload_70a(tmpdir, fakeicontrolsession):
    bytestring70a = 70*'a'
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    ftu = mr.shared.file_transfer.uploads
    ftu.upload_bytes(bytestring70a, 'testtarget', chunk_size=20)
    session_mock = mr._meta_data['icr_session']
    for i in range(3):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == 'aaaaaaaaaaaaaaaaaaaa'
    lchunk = session_mock.post.call_args_list[3][1]['data']
    assert 10*'a' == lchunk
