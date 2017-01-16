# Copyright 2014 F5 Networks Inc.
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
import os
import pytest
import requests
import requests_mock
import struct

from f5.bigip import ManagementRoot
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.asm.file_transfer import Downloads
from f5.bigip.tm.asm.file_transfer import FileMustNotHaveDotISOExtension
from f5.sdk_exception import EmptyContent
from f5.sdk_exception import MissingHttpHeader

from requests import HTTPError


CHUNKSIZE = 20


def fake_http_server(uri, **kwargs):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock', adapter)
    adapter.register_uri('GET', uri, **kwargs)
    return session


def FakeDownload(session):
    fake_filetransfer = mock.MagicMock()
    fake_dwnld = Downloads(fake_filetransfer)
    fake_dwnld._meta_data['icr_session'] = session
    fake_dwnld._meta_data['uri'] = 'mock://test.com/'
    return fake_dwnld


class TestTasksOC(object):
    def test_OC(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        c1 = b.tm.asm.file_transfer
        assert isinstance(c1, OrganizingCollection)
        assert hasattr(c1, 'downloads')
        assert hasattr(c1, 'uploads')


def test_asm_file_uploads_70a(tmpdir, fakeicontrolsessionfactory):
    fakeicontrolsessionfactory()
    filepath = tmpdir.mkdir('testdir').join('fakeseventy.txt')
    filepath.write(70*'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    asm_fl = mr.tm.asm.file_transfer.uploads
    session_mock = mr._meta_data['icr_session']
    asm_fl.upload_file(str(filepath), chunk_size=CHUNKSIZE)
    for i in range(3):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == b'a'*CHUNKSIZE
    lchunk = session_mock.post.call_args_list[3][1]['data']
    assert b'a'*10 == lchunk


def test_asm_file_uploads_80a(tmpdir, fakeicontrolsessionfactory):
    fakeicontrolsessionfactory()
    filepath = tmpdir.mkdir('testdir').join('fakeeighty.txt')
    filepath.write(80 * 'a')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    mr._meta_data['icr_session'] = mock.MagicMock()
    asm_fl = mr.tm.asm.file_transfer.uploads
    session_mock = mr._meta_data['icr_session']
    asm_fl.upload_file(str(filepath), chunk_size=CHUNKSIZE)
    for i in range(4):
        d = session_mock.post.call_args_list[i][1]['data']
        assert d == b'a' * CHUNKSIZE


def test_ISO_extension_raises(tmpdir, fakeicontrolsessionfactory):
    fakeicontrolsessionfactory()
    filepath = tmpdir.mkdir('testdir').join('wrong.iso')
    mr = ManagementRoot('FAKENETLOC', 'FAKENAME', 'FAKEPASSWORD')
    asm_fl = mr.tm.asm.file_transfer.uploads
    with pytest.raises(FileMustNotHaveDotISOExtension) as EIO:
        asm_fl.upload_file(str(filepath), chunk_size=CHUNKSIZE)
    assert str(EIO.value) == 'wrong.iso'


def test_asm_file_download():
    # Prepare baseline file
    f = open('fakefile.txt', 'wb')
    f.write(struct.pack('B', 0))
    basefilesize = int(os.stat('fakefile.txt').st_size)
    f.close()

    # Start Testing
    server_fakefile = 'asasasas' * 40
    srvfakesize = len(server_fakefile)
    header = {'Content-Length': str(srvfakesize),
              'Content-Type': 'application/text'}
    session = fake_http_server('mock://test.com/fakefile.txt',
                               text=server_fakefile, headers=header,
                               status_code=200)
    dwnld = FakeDownload(session)
    dwnld.download_file('fakefile.txt')
    endfilesize = int(os.stat('fakefile.txt').st_size)
    assert basefilesize != srvfakesize
    assert endfilesize == srvfakesize
    assert endfilesize == 320


def test_404_response():
    # Cleanup
    os.remove('fakefile.txt')
    # Test Start
    header = {'Content-Type': 'application/text'}
    session = fake_http_server(
        'mock://test.com/fakefile.txt', headers=header,
        status_code=404, reason='Not Found')
    dwnld = FakeDownload(session)
    try:
        dwnld.download_file('fakefile.txt')
    except HTTPError as err:
        assert err.value.response.status_code == 404


def test_zero_content_length_header():
    # Test Start
    header = {'Content-Type': 'application/text',
              'Content-Length': '0'}
    session = fake_http_server(
        'mock://test.com/fakefile.txt', headers=header,
        status_code=200)
    dwnld = FakeDownload(session)
    with pytest.raises(EmptyContent) as err:
        dwnld.download_file('fakefile.txt')
        msg = "Invalid Content-Length value returned: %s ,the value " \
              "should be greater than 0"
        assert err.value.message == msg


def test_no_content_length_header():
    # Test Start
    header = {'Content-Type': 'application/text'}
    session = fake_http_server(
        'mock://test.com/fakefile.txt', headers=header,
        status_code=200)
    dwnld = FakeDownload(session)
    with pytest.raises(MissingHttpHeader) as err:
        dwnld.download_file('fakefile.txt')
        msg = "The Content-Length header is not present."
        assert err.value.message == msg
