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
import json
import mock
import os
import pytest
import requests
import requests_mock
import struct

from f5.bigip.mixins import AsmFileMixin
from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.mixins import EmptyContent
from f5.bigip.mixins import MissingHttpHeader
from f5.bigip.mixins import ToDictMixin
from f5.bigip.mixins import UnsupportedMethod
from f5.bigip.resource import Resource

from requests import HTTPError


class MixinTestClass(ToDictMixin):
    def __init__(self):
        pass


def test_int():
    MTCobj = MixinTestClass()
    MTCobj.x = 1
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"x": 1}'


def test_list():
    MTCobj = MixinTestClass()
    MTCobj.x = [1, 'a']
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"x": [1, "a"]}'


def test_list_and_int():
    MTCobj = MixinTestClass()
    MTCobj.x = [1, 'a']
    MTCobj.y = 1
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict, sort_keys=True) == \
        '{"x": [1, "a"], "y": 1}'


def test_list_and_int_and_list2():
    MTCobj = MixinTestClass()
    MTCobj.x = [1, 'a']
    MTCobj.y = 1
    MTCobj.z = [1, 'a']
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict, sort_keys=True) == \
        '{"x": [1, "a"], "y": 1, "z": [1, "a"]}'


def test_two_refs():
    MTCobj = MixinTestClass()
    MTCobj.x = [1, 'a']
    MTCobj.z = MTCobj.x
    mtc_as_dict = MTCobj.to_dict()
    dict1 = json.dumps(mtc_as_dict, sort_keys=True)
    assert dict1 ==\
        '{"x": [1, "a"], "z": ["TraversalRecord", "x"]}'


def test_tuple():
    MTCobj = MixinTestClass()
    MTCobj.x = (1, 'a')
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"x": [1, "a"]}'


class ToDictMixinAttribute(ToDictMixin):
    def __init__(self):
        pass


def test_ToDictMixinAttribute():
    MTCobj = MixinTestClass()
    TDMAttrObj = ToDictMixinAttribute()
    MTCobj.x = TDMAttrObj
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"x": {}}'


def test_ToDictMixinAttribute_Nested():
    MTCobj = MixinTestClass()
    TDMAttrObj = ToDictMixinAttribute()
    TDMAttrObj.y = {'a': 3}
    MTCobj.x = TDMAttrObj
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"x": {"y": {"a": 3}}}'


class DictableClass(object):
    def __init__(self):
        self.test_attribute = 42


def test_TestClass_Basic():
    TDMAttrObj = ToDictMixinAttribute()
    TDMAttrObj.y = DictableClass()
    mtc_as_dict = TDMAttrObj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"y": {"test_attribute": 42}}'


class MockResponse(object):
    def __init__(self, attr_dict):
        self.__dict__ = attr_dict

    def json(self):
        return self.__dict__


class FakeCommandResource(CommandExecutionMixin, Resource):
    def __init__(self, container):
        super(FakeCommandResource, self).__init__(container)
        self._meta_data['allowed_commands'] = ['fakecommand', 'fakecommand2']
        self._meta_data['required_json_kind'] = 'tm:ltm:fakeendpoint:fakeres'
        self._meta_data['allowed_lazy_attributes'] = []
        mockuri = 'https://localhost/mgmt/tm/ltm/fakeendpoint/fakeres'
        self._meta_data['uri'] = mockuri
        self._meta_data['bigip']._meta_data[
            'icr_session'].post.return_value =\
            MockResponse({u"generation": 0, u"selfLink": mockuri,
                          u"kind": u"tm:ltm:fakeendpoint:fakeres"})


class TestCommandExecutionMixin(object):
    def test_create_raises(self):
        command_resource = CommandExecutionMixin()
        with pytest.raises(UnsupportedMethod):
            command_resource.create()

    def test_delete_raises(self):
        command_resource = CommandExecutionMixin()
        with pytest.raises(UnsupportedMethod):
            command_resource.delete()

    def test_load_raises(self):
        command_resource = CommandExecutionMixin()
        with pytest.raises(UnsupportedMethod):
            command_resource.load()

    def test_exec_cmd_instance(self):
        fake_res = FakeCommandResource(mock.MagicMock())
        cmd1 = fake_res.exec_cmd('fakecommand')
        cmd2 = fake_res.exec_cmd('fakecommand2')
        assert cmd1 is not cmd2


def fake_http_server(uri, **kwargs):
    session = requests.Session()
    adapter = requests_mock.Adapter()
    session.mount('mock', adapter)
    adapter.register_uri('GET', uri, **kwargs)
    return session


class FakeAsmFileMixin(AsmFileMixin):
        def __init__(self, uri, **kwargs):
            session = fake_http_server(uri, **kwargs)
            self._meta_data = {'icr_session': session}
            self.file_bound_uri = uri


class TestAsmFileMixin(object):
    def test_download(self):
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
        dwnld = FakeAsmFileMixin('mock://test.com/fakefile.txt',
                                 text=server_fakefile, headers=header,
                                 status_code=200)
        dwnld._download_file('fakefile.txt')
        endfilesize = int(os.stat('fakefile.txt').st_size)
        assert basefilesize != srvfakesize
        assert endfilesize == srvfakesize
        assert endfilesize == 320

    def test_404_response(self):
        # Cleanup
        os.remove('fakefile.txt')
        # Test Start
        header = {'Content-Type': 'application/text'}
        dwnld = FakeAsmFileMixin(
            'mock://test.com/fakefile.txt', headers=header,
            status_code=404, reason='Not Found')
        try:
            dwnld._download_file('fakefile.txt')
        except HTTPError as err:
            assert err.response.status_code == 404

    def test_zero_content_length_header(self):
        # Test Start
        header = {'Content-Type': 'application/text',
                  'Content-Length': '0'}
        dwnld = FakeAsmFileMixin(
            'mock://test.com/fake_file.txt', headers=header,
            status_code=200)
        with pytest.raises(EmptyContent) as err:
            dwnld._download_file('fakefile.txt')
            msg = "Invalid Content-Length value returned: %s ,the value " \
                  "should be greater than 0"
            assert err.value.message == msg

    def test_no_content_length_header(self):
        # Test Start
        header = {'Content-Type': 'application/text'}
        dwnld = FakeAsmFileMixin(
            'mock://test.com/fakefile.txt', headers=header,
            status_code=200)
        with pytest.raises(MissingHttpHeader) as err:
            dwnld._download_file('fakefile.txt')
            msg = "The Content-Length header is not present."
            assert err.value.message == msg
