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
import mock
import copy
from f5.bigip import PathElement

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

RAW_DICT = {u'generation': 9575, u'kind': u'tm:ltm:virtual:virtualstats',
            u'selfLink': u'https://testhost/mgmt/tm/ltm/virtual/'
                         u'~Common~test_load/stats?ver=12.1.0',
            u'entries': {
                u'https://testhost/mgmt/tm/ltm/virtual/'
                u'~Common~test_load/~Common~test_load/stats': {
                    u'nestedStats': {u'kind': u'tm:ltm:virtual:virtualstats',
                                     u'selfLink': u'https://testhost/mgmt/tm/'
                                                  u'ltm/virtual/~Common'
                                                  u'~test_load/~Common~'
                                                  u'test_load/stats?'
                                                  u'ver=12.1.0',
                                     u'entries':
                                         {u'syncookie.accepts': {u'value': 0},
                                          u'ephemeral.bitsOut': {u'value': 0},
                                          u'clientside.bitsOut': {u'value': 0}
                                          }}}}}



@pytest.fixture
def FakePath():
    fake_path = mock.MagicMock()
    return PathElement(fake_path)


@pytest.fixture
def FakeVirtual():
    r = Virtual(mock.MagicMock())
    mockuri = "https://localhost:443/mgmt/tm/ltm/virtual/~Common~test_load"
    attrs = {'get.return_value': MockResponse(
            {
                u"generation": 0,
                u"selfLink": mockuri,
                u"kind": u"tm:ltm:virtual:virtualstate"
            }
        )}
    mock_session = mock.MagicMock(**attrs)
    r._meta_data['bigip']._meta_data = \
        {'icr_session': mock_session,
         'hostname': 'TESTDOMAINNAME',
         'uri': 'https://TESTDOMAIN:443/mgmt/tm/'
         }
    r._meta_data['bigip'].tmos_version = '12.1.0'
    r.generation = 0
    x = r.load(partition='Common', name='test_load')
    return x


@pytest.fixture
def MakeFakeResourceContainer(FakePath):
    class FakeMetaData(object):
        def __init__(self, **kwargs):
            self._meta_data = {}
            meta_data_defaults = {
                'uri': kwargs['uri'],
                'icontrol_version': '',
                'icr_session': kwargs['icr_session'],
                'bigip': self
            }
            self._meta_data.update(meta_data_defaults)

    mockconturi = 'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/'
    bigipuri = 'https://testhost/mgmt/tm/'
    attrs = {'get.return_value': MockResponse(RAW_DICT)}
    return_session = mock.MagicMock(**attrs)
    FakePath._meta_data = {
        'hostname': 'testhost',
        'icr_session': '',
        'uri': '',
        'icontrol_version': '',
        'bigip': FakeMetaData(icr_session=return_session, uri=bigipuri),
        'container': FakeMetaData(uri=mockconturi, icr_session='')
    }

    return FakePath


class FakeResponse(object):
    def json(self):
        return copy.deepcopy(RAW_DICT)


class TestPathElementStatsModuleHelpers(object):
    mock_session = mock.MagicMock()
    mock_session.get.return_value = FakeResponse()
    mock_stats_container = mock.MagicMock()
    mock_bigip = mock.MagicMock()
    mock_bigip._meta_data = {'icr_session': mock_session}
    mock_stats_container._meta_data =\
        {'bigip': mock_bigip,
         'icr_session': mock_session,
         'icontrol_version': '11.6.0',
         'allowed_lazy_attributes': [Stats],
         'uri': 'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/'}

    def test_key_dot_replace(self):
        p = Stats(self.mock_stats_container)
        fake_dict = {'foo.bar': 'foo', 'baz': 'baz.foo',
                     'fuz.bar': {'baz.foo': {'faz': {'baz.fuz': 1}}}}
        undotted_fake_dict = p._key_dot_replace(fake_dict)
        assert undotted_fake_dict == {'foo_bar': 'foo', 'baz': 'baz.foo',
                                      'fuz_bar': {'baz_foo': {'faz': {
                                          'baz_fuz': 1}}}}

    def test_pop_nest_stats_nested(self):
        p = Stats(self.mock_stats_container)
        nest = p._get_nest_stats(NESTED_DICT)
        assert nest == EXPECTED_CONVERTED_DICT

    def test_pop_nest_stats_not_nested(self):
        p = Stats(self.mock_stats_container)
        not_nest = p._get_nest_stats(NOT_NESTED_DICT)
        assert not_nest == EXPECTED_CONVERTED_DICT

    def test_pop_nest_stats_nested_no_uri(self):
        p = Stats(self.mock_stats_container)
        nested_nouri = p._get_nest_stats(NESTED_DICT_NO_URI)
        assert nested_nouri == EXPECTED_CONVERTED_DICT_NO_URI

    def test_get_stats_raw(self):
        v = Stats(self.mock_stats_container)
        raw_dict = v._get_stats_raw()
        ret_uri = 'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/'
        assert v._meta_data['container']._meta_data['uri'] == ret_uri
        assert raw_dict == RAW_DICT

    def test_update_stats_invalid_json(self):
        fake_dict = {'foo.bar': 'foo', 'baz': 'baz.foo',
                     'fuz.bar': {'baz.foo': {'faz': {'baz.fuz': 1}}}}
        p = Stats(self.mock_stats_container)
        with pytest.raises(InvalidStatsJsonReturned)as err:
            p._update_stats(fake_dict)
        assert err.value.message == 'Missing "entries" key in returned JSON'

    def test_update_stats(self):
        p = Stats(self.mock_stats_container)
        p._update_stats(RAW_DICT)
        assert 'stat' in p.__dict__
        assert hasattr(p.__dict__['stat'], 'syncookie_accepts')
        assert hasattr(p.__dict__['stat'], 'ephemeral_bitsOut')
        assert hasattr(p.__dict__['stat'], 'clientside_bitsOut')
