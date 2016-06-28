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
import pytest

from f5.bigip.mixins import CommandExecutionMixin
from f5.bigip.mixins import ToDictMixin
from f5.bigip.mixins import UnsupportedMethod


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
    assert json.dumps(mtc_as_dict) == '{"y": 1, "x": [1, "a"]}'


def test_list_and_int_and_list2():
    MTCobj = MixinTestClass()
    MTCobj.x = [1, 'a']
    MTCobj.y = 1
    MTCobj.z = [1, 'a']
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) == '{"y": 1, "x": [1, "a"], "z": [1, "a"]}'


def test_two_refs():
    MTCobj = MixinTestClass()
    MTCobj.x = [1, 'a']
    MTCobj.z = MTCobj.x
    mtc_as_dict = MTCobj.to_dict()
    assert json.dumps(mtc_as_dict) ==\
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
