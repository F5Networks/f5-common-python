# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from f5.utils.responses.handlers import Stats

NESTED_DICT = \
    {u'https://localhost/mgmt/tm/fakemod/fake/fakeone/~Common~fakeone/stats': {
        u'nestedStats': {
            u'kind': u'tm:fakemod:fake:fakestats',
            u'selfLink': u'https://localhost/mgmt/tm/fakemod/fake/fakeone/'
                         u'~Common~fakeone/stats?ver=12.1.0',
            u'entries': {u'syncookie.accepts': {
                u'value': 0}, u'ephemeral.bitsOut': {
                u'value': 0}, u'clientside.bitsOut': {u'value': 0}}}}}

NOT_NESTED_DICT = {u'syncookie.accepts': {u'value': 0},
                   u'ephemeral.bitsOut': {u'value': 0},
                   u'clientside.bitsOut': {u'value': 0}}

NESTED_DICT_NO_URI = {u'fakekey.some': {
    u'nestedStats': {
        u'kind': u'tm:fakemod:fake:fakestats',
        u'selfLink': u'https://localhost/mgmt/tm/fakemod/'
                     u'fake/fakeone/~Common~fakeone/stats?ver=12.1.0',
        u'entries': {u'syncookie.accepts': {u'value': 0},
                     u'ephemeral.bitsOut': {u'value': 0},
                     u'clientside.bitsOut': {u'value': 0}}}}}

EXPECTED_CONVERTED_DICT = {u'syncookie_accepts': {u'value': 0},
                           u'ephemeral_bitsOut': {u'value': 0},
                           u'clientside_bitsOut': {u'value': 0}}

EXPECTED_CONVERTED_DICT_NO_URI = {u'fakekey_some': {u'nestedStats': {
    u'kind': u'tm:fakemod:fake:fakestats', u'selfLink':
        u'https://localhost/mgmt/tm/fakemod/fake/fakeone/'
        u'~Common~fakeone/stats?ver=12.1.0',
    u'entries': {u'syncookie_accepts': {u'value': 0},
                 u'ephemeral_bitsOut': {u'value': 0},
                 u'clientside_bitsOut': {u'value': 0}}}}}


class FakeStatResource(object):
    def __init__(self, obj):
        self.entries = obj


class TestStatsHandlerMethods(object):
    def test_key_dot_replace(self):
        fake_dict = {'foo.bar': 'foo', 'baz': 'baz.foo',
                     'fuz.bar': {'baz.foo': {'faz': {'baz.fuz': 1}}}}
        p = Stats(FakeStatResource(fake_dict))
        assert 'stat' in p.__dict__
        assert hasattr(p.__dict__['stat'], 'foo_bar')
        assert hasattr(p.__dict__['stat'], 'fuz_bar')
        assert p.__dict__['stat'] == {'foo_bar': 'foo', 'baz': 'baz.foo',
                                      'fuz_bar': {'baz_foo': {'faz': {
                                          'baz_fuz': 1}}}}

    def test_pop_nest_stats_nested(self):
        p = Stats(FakeStatResource(NESTED_DICT))
        assert 'stat' in p.__dict__
        assert p.__dict__['stat'] == EXPECTED_CONVERTED_DICT

    def test_pop_nest_stats_not_nested(self):
        p = Stats(FakeStatResource(NOT_NESTED_DICT))
        assert 'stat' in p.__dict__
        assert p.__dict__['stat'] == EXPECTED_CONVERTED_DICT

    def test_pop_nest_stats_nested_no_uri(self):
        p = Stats(FakeStatResource(NESTED_DICT_NO_URI))
        assert 'stat' in p.__dict__
        assert p.__dict__['stat'] == EXPECTED_CONVERTED_DICT_NO_URI
