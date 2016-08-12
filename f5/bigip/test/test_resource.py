# Copyright 2016 F5 Networks Inc.
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
import pytest
import requests

from f5.bigip.resource import _missing_required_parameters
from f5.bigip.resource import AttemptedMutationOfReadOnly
from f5.bigip.resource import BooleansToReduceHaveSameValue
from f5.bigip.resource import Collection
from f5.bigip.resource import DeviceProvidesIncompatibleKey
from f5.bigip.resource import DottedDict
from f5.bigip.resource import ExclusiveAttributesPresent
from f5.bigip.resource import GenerationMismatch
from f5.bigip.resource import InvalidForceType
from f5.bigip.resource import InvalidStatsJsonReturned
from f5.bigip.resource import InvalidResource
from f5.bigip.resource import KindTypeMismatch
from f5.bigip.resource import MissingRequiredCommandParameter
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import PathElement
from f5.bigip.resource import RequestParamKwargCollision
from f5.bigip.resource import Resource
from f5.bigip.resource import ResourceBase
from f5.bigip.resource import UnnamedResource
from f5.bigip.resource import UnregisteredKind
from f5.bigip.resource import URICreationCollision
from f5.bigip.tm.cm.sync_status import Sync_Status
from f5.bigip.tm.ltm.virtual import Virtual
from f5.sdk_exception import UnsupportedMethod

from types import *

NESTED_DICT = {
        u'https://localhost/mgmt/tm/fakemod/fake/fakeone/~Common~fakeone/stats': {
            u'nestedStats': {
                u'kind': u'tm:fakemod:fake:fakestats',
                u'selfLink': u'https://localhost/mgmt/tm/fakemod/fake/fakeone/~Common~fakeone/stats?ver=12.1.0',
                u'entries': {u'syncookie.accepts': {u'value': 0}, u'ephemeral.bitsOut': {u'value': 0},
                             u'clientside.bitsOut': {u'value': 0}}}}}

NOT_NESTED_DICT = {u'syncookie.accepts': {u'value': 0}, u'ephemeral.bitsOut': {u'value': 0},
                    u'clientside.bitsOut': {u'value': 0}}

NESTED_DICT_NO_URI = {u'fakekey.some': {
    u'nestedStats': {u'kind': u'tm:fakemod:fake:fakestats',
                     u'selfLink': u'https://localhost/mgmt/tm/fakemod/fake/fakeone/~Common~fakeone/stats?ver=12.1.0',
                     u'entries': {u'syncookie.accepts': {u'value': 0},
                                  u'ephemeral.bitsOut': {u'value': 0},
                                  u'clientside.bitsOut': {u'value': 0}}}}}

EXPECTED_CONVERTED_DICT = {u'syncookie_accepts': {u'value': 0},
                                      u'ephemeral_bitsOut': {u'value': 0},
                                      u'clientside_bitsOut': {u'value': 0}}

EXPECTED_CONVERTED_DICT_NO_URI = {u'fakekey_some': {u'nestedStats': {
    u'kind': u'tm:fakemod:fake:fakestats', u'selfLink':
        u'https://localhost/mgmt/tm/fakemod/fake/fakeone/~Common~fakeone/stats?ver=12.1.0',
    u'entries': {u'syncookie_accepts': {u'value': 0}, u'ephemeral_bitsOut': {u'value': 0},
                 u'clientside_bitsOut': {u'value': 0}}}}}

RAW_DICT = {u'generation': 9575, u'kind': u'tm:ltm:virtual:virtualstats',
            u'selfLink': u'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/stats?ver=12.1.0',
            u'entries': { u'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/~Common~test_load/stats':{
                u'nestedStats': {u'kind': u'tm:ltm:virtual:virtualstats',
                                 u'selfLink':
                                     u'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/~Common~test_load/stats?ver=12.1.0',
                                 u'entries': {u'syncookie.accepts': {u'value': 0}, u'ephemeral.bitsOut': {u'value': 0},
                                              u'clientside.bitsOut': {u'value': 0}}}}}}


@pytest.fixture
def fake_vs():
    r = Virtual(mock.MagicMock())
    MRO = MockResponse({u"kind": u"tm:ltm:virtual:virtualstate",
                        u"selfLink": u".../~Common~test_create"})
    r._meta_data['bigip']._meta_data['icr_session'].post.return_value = MRO
    r._meta_data['required_json_kind'] = u"tm:ltm:virtual:virtualstate"
    r._meta_data['allowed_lazy_attributes'] = []
    return r


@pytest.fixture
def fake_rsrc():
    r = Resource(mock.MagicMock())
    r._meta_data['allowed_lazy_attributes'] = []
    r._meta_data['uri'] = 'URI'
    r._meta_data['read_only_attributes'] = [u"READONLY"]
    attrs = {'put.return_value': MockResponse({u"generation": 0}),
             'get.return_value': MockResponse({u"generation": 0}),
             'patch.return_value': MockResponse({u"generation": 0})}
    mock_session = mock.MagicMock(**attrs)
    r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
    return r


class MockResponse(object):
    def __init__(self, attr_dict):
        self.__dict__ = attr_dict

    def json(self):
        return self.__dict__


def test_Resource__local_update_IncompatibleKeys():
    r = Resource(mock.MagicMock())
    with pytest.raises(DeviceProvidesIncompatibleKey) as DPIKIO:
        r._local_update({"_meta_data": "foo"})
    assert DPIKIO.value.message ==\
        "Response contains key '_meta_data' which is incompatible"\
        " with this API!!\n Response json: {'_meta_data': 'foo'}"
    with pytest.raises(DeviceProvidesIncompatibleKey) as DPIKIO:
        r._local_update({"__MANGLENAME": "foo"})
    assert DPIKIO.value.message ==\
        "Device provided '__MANGLENAME' which is disallowed,"\
        " it mangles into a Python non-public attribute."
    with pytest.raises(DeviceProvidesIncompatibleKey) as DPIKIO:
        r._local_update({"for": "foo"})
    assert DPIKIO.value.message ==\
        "Device provided 'for' which is disallowed because"\
        " it's a Python keyword."
    with pytest.raises(DeviceProvidesIncompatibleKey) as DPIKIO:
        r._local_update({"%abcd": "foo"})
    assert DPIKIO.value.message ==\
        "Device provided '%abcd' which is disallowed because"\
        " it's not a valid Python 2.7 identifier."


def test_Resource__local_update():
    r = Resource(mock.MagicMock())
    stash = r._meta_data.copy()
    r._local_update({'test': 1})
    assert stash == r._meta_data
    r.__dict__.pop('_meta_data')
    assert r.__dict__ == {'test': 1}


def test_Resource__check_keys_valid_rict():
    r = Resource(mock.MagicMock())
    res = r._check_keys({})
    assert res == {}


def test_Resource_refresh():
    r = Resource(mock.MagicMock())

    r._meta_data['bigip']._meta_data['icr_session'].get.return_value =\
        MockResponse({u"a": 1})
    r._meta_data['uri'] = 'URI'
    r.refresh()
    assert r.a == 1


class TestResourcecreate(object):
    def test_missing_required_creation_parameter(self):
        r = Resource(mock.MagicMock())
        r._meta_data['required_creation_parameters'] = set(['NONEMPTY'])
        with pytest.raises(MissingRequiredCreationParameter) as MRCPEIO:
            r.create(partition="Common", name='CreateTest')
        assert MRCPEIO.value.message ==\
            "Missing required params: ['NONEMPTY']"

    def test_KindTypeMismatch(self):
        r = Virtual(mock.MagicMock())
        r._meta_data['bigip']._meta_data['icr_session'].post.return_value =\
            MockResponse({u"kind": u"tm:"})
        with pytest.raises(KindTypeMismatch) as KTMmEIO:
            r.create(partition="Common", name="test_create")
        assert KTMmEIO.value.message ==\
            "For instances of type ''Virtual'' the corresponding kind must "\
            "be ''tm:ltm:virtual:virtualstate'' but creation returned "\
            "JSON with kind: u'tm:'"

    def test_success(self, fake_vs):
        x = fake_vs.create(partition="Common", name="test_create")
        assert x.kind == u"tm:ltm:virtual:virtualstate"
        assert x.selfLink == u".../~Common~test_create"

    def test_reduce_boolean_removes_enabled(self, fake_vs):
        assert fake_vs._meta_data['reduction_forcing_pairs'] == \
            [
                ('enabled', 'disabled'),
                ('online', 'offline'),
                ('vlansEnabled', 'vlansDisabled')
            ]
        fake_vs.create(partition="Common", name="test_create", enabled=False)
        pos, kwargs = fake_vs._meta_data['bigip']._meta_data['icr_session'].post.\
            call_args
        assert kwargs['json']['disabled'] is True
        assert 'enabled' not in kwargs['json']

    def test_reduce_boolean_removes_disabled(self, fake_vs):
        fake_vs.create(partition='Common', name='test_create', disabled=False)
        pos, kwargs = fake_vs._meta_data['bigip']._meta_data['icr_session'].post.\
            call_args
        assert kwargs['json']['enabled'] is True
        assert 'disabled' not in kwargs['json']

    def test_reduce_boolean_removes_nothing(self, fake_vs):
        fake_vs.create(partition='Common', name='test_create', enabled=True)
        pos, kwargs = fake_vs._meta_data['bigip']._meta_data['icr_session'].post.\
            call_args
        assert kwargs['json']['enabled'] is True
        assert 'disabled' not in kwargs['json']

    def test_reduce_boolean_same_value(self, fake_vs):
        with pytest.raises(BooleansToReduceHaveSameValue) as ex:
            fake_vs.create(
                partition='Common',
                name='test_create',
                enabled=True,
                disabled=True
            )
        msg = 'Boolean pair, enabled and disabled, have same value: True. ' \
            'If both are given to this method, they cannot be the same, as ' \
            'this method cannot decide which one should be True.'
        assert msg == ex.value.message


def test__activate_URI_with_stats():
    r = Resource(mock.MagicMock())
    r._meta_data['allowed_lazy_attributes'] = []
    r._meta_data['attribute_registry'] = {u"tm:": u"SPAM"}
    r._meta_data['bigip']._meta_data = {
        'hostname': 'TESTDOMAIN',
        'uri': 'https://TESTDOMAIN:443/mgmt/tm/'
    }
    assert r._meta_data['object_has_stats'] == False
    r._meta_data['object_has_stats'] = True
    assert r._meta_data['object_has_stats'] == True
    TURI = 'https://localhost:443/mgmt/tm/'\
           'ltm/virtual/~Common~testvirtual/?ver=11.6&a=b#FOO'
    assert r._meta_data['allowed_lazy_attributes'] == []
    r._activate_URI(TURI)
    assert r._meta_data['uri'] ==\
        'https://TESTDOMAIN:443/mgmt/tm/ltm/virtual/~Common~testvirtual/'
    assert r._meta_data['creation_uri_qargs'] ==\
        {'a': ['b'], 'ver': ['11.6']}
    assert r._meta_data['creation_uri_frag'] == 'FOO'
    chk_lst = r._meta_data['allowed_lazy_attributes']
    assert u"SPAM" in chk_lst
    assert 'stats' in [cls.__name__.lower() for cls in chk_lst
                       if type(cls) in [TypeType, ClassType]]


def test__activate_URI_no_stats():
    r = Resource(mock.MagicMock())
    r._meta_data['allowed_lazy_attributes'] = []
    r._meta_data['attribute_registry'] = {u"tm:": u"SPAM"}
    r._meta_data['bigip']._meta_data = {
        'hostname': 'TESTDOMAIN',
        'uri': 'https://TESTDOMAIN:443/mgmt/tm/'
    }
    TURI = 'https://localhost:443/mgmt/tm/'\
           'ltm/nat/~Common~testnat/?ver=11.5&a=b#FOO'
    assert r._meta_data['object_has_stats'] == False
    assert r._meta_data['allowed_lazy_attributes'] == []
    r._activate_URI(TURI)
    assert r._meta_data['uri'] ==\
        'https://TESTDOMAIN:443/mgmt/tm/ltm/nat/~Common~testnat/'
    assert r._meta_data['creation_uri_qargs'] ==\
        {'a': ['b'], 'ver': ['11.5']}
    assert r._meta_data['creation_uri_frag'] == 'FOO'
    assert r._meta_data['allowed_lazy_attributes'] == [u"SPAM"]


def test__create_with_Collision():
    r = Resource(mock.MagicMock())
    r._meta_data['uri'] = 'URI'
    with pytest.raises(URICreationCollision) as UCCEIO:
        r.create(uri='URI')
    assert UCCEIO.value.message ==\
        "There was an attempt to assign a new uri to this resource,"\
        " the _meta_data['uri'] is URI and it should not be changed."


class TestResource_update(object):
    def test__check_generation_with_mismatch(self):
        # generation is borked server-side
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['bigip']._meta_data['icr_session'].get.return_value =\
            MockResponse({u"generation": 0})
        r._meta_data['bigip']._meta_data['icr_session'].put.return_value =\
            MockResponse({u"generation": 0})
        r.generation = 1
        with pytest.raises(GenerationMismatch) as GMEIO:
            r.update(a=u"b", force=False)
        assert GMEIO.value.message ==\
            'The generation of the object on the BigIP (0)'\
            ' does not match the current object(1)'

    def test__meta_data_state(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['bigip']._meta_data['icr_session'].get.return_value =\
            MockResponse({u"generation": 0})
        r._meta_data['bigip']._meta_data['icr_session'].put.return_value =\
            MockResponse({u"generation": 0})
        r.generation = 0
        pre_meta = r._meta_data.copy()
        r.update(a=u"b")
        assert pre_meta == r._meta_data
        assert r.raw == r.__dict__

    def test_Collection_removal(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        attrs = {'put.return_value': MockResponse({u"generation": 0}),
                 'get.return_value': MockResponse({u"generation": 0})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        r.contained = Collection(mock.MagicMock())
        assert 'contained' in r.__dict__
        r.update(a=u"b")
        submitted = r._meta_data['bigip']. \
            _meta_data['icr_session'].put.call_args[1]['json']

        assert 'contained' not in submitted

    def test_read_only_removal(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['read_only_attributes'] = [u"READONLY"]
        attrs = {'put.return_value': MockResponse({u"generation": 0}),
                 'get.return_value': MockResponse({u"generation": 0})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        r.READONLY = True
        assert 'READONLY' in r.__dict__
        r.update(a=u"b")
        submitted = r._meta_data['bigip'].\
            _meta_data['icr_session'].put.call_args[1]['json']
        assert 'READONLY' not in submitted

    def test_reduce_boolean_removes_enabled(self, fake_rsrc):
        fake_rsrc.update(enabled=False)
        pos, kwargs = fake_rsrc._meta_data['bigip'].\
            _meta_data['icr_session'].put.call_args
        assert kwargs['json']['disabled'] is True
        assert 'enabled' not in kwargs['json']

    def test_reduce_boolean_removes_disabled(self, fake_rsrc):
        fake_rsrc.update(disabled=False)
        pos, kwargs = fake_rsrc._meta_data['bigip'].\
            _meta_data['icr_session'].put.call_args
        assert kwargs['json']['enabled'] is True
        assert 'disabled' not in kwargs['json']

    def test_reduce_boolean_removes_nothing(self, fake_rsrc):
        fake_rsrc.update(partition='Common', name='test_create', enabled=True)
        pos, kwargs = fake_rsrc._meta_data['bigip'].\
            _meta_data['icr_session'].put.call_args
        assert kwargs['json']['enabled'] is True
        assert 'disabled' not in kwargs['json']

    def test_reduce_boolean_same_value(self, fake_rsrc):
        with pytest.raises(BooleansToReduceHaveSameValue) as ex:
            fake_rsrc.update(
                partition='Common',
                name='test_create',
                enabled=True,
                disabled=True
            )
        msg = 'Boolean pair, enabled and disabled, have same value: True. ' \
            'If both are given to this method, they cannot be the same, as ' \
            'this method cannot decide which one should be True.'
        assert msg == ex.value.message


class TestResource_modify(object):

    def test__meta_data_state(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['bigip']._meta_data['icr_session'].get.return_value =\
            MockResponse({u"generation": 0})
        r._meta_data['bigip']._meta_data['icr_session'].patch.return_value =\
            MockResponse({u"generation": 0})
        r.generation = 0
        pre_meta = r._meta_data.copy()
        r.modify(a=u"b")
        assert pre_meta == r._meta_data

    def test_Collection_removal(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        attrs = {'patch.return_value': MockResponse({u"generation": 0}),
                 'get.return_value': MockResponse({u"generation": 0})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        r.contained = Collection(mock.MagicMock())
        assert 'contained' in r.__dict__
        r.modify(a=u"b")
        submitted = r._meta_data['bigip']. \
            _meta_data['icr_session'].patch.call_args[1]['json']

        assert 'contained' not in submitted

    def test_read_only_validate(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['read_only_attributes'] = [u"READONLY"]
        attrs = {'patch.return_value': MockResponse({u"generation": 0}),
                 'get.return_value': MockResponse({u"generation": 0})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        with pytest.raises(AttemptedMutationOfReadOnly) as AMOROEIO:
            r.modify(READONLY=True)
        assert "READONLY" in AMOROEIO.value.message

    def test_reduce_boolean_removes_enabled(self, fake_rsrc):
        fake_rsrc.modify(enabled=False)
        pos, kwargs = fake_rsrc._meta_data['bigip'].\
            _meta_data['icr_session'].patch.call_args
        assert kwargs['json']['disabled'] is True
        assert 'enabled' not in kwargs['json']

    def test_reduce_boolean_removes_disabled(self, fake_rsrc):
        fake_rsrc.modify(disabled=False)
        pos, kwargs = fake_rsrc._meta_data['bigip'].\
            _meta_data['icr_session'].patch.call_args
        assert kwargs['json']['enabled'] is True
        assert 'disabled' not in kwargs['json']

    def test_reduce_boolean_removes_nothing(self, fake_rsrc):
        fake_rsrc.modify(partition='Common', name='test_create', enabled=True)
        pos, kwargs = fake_rsrc._meta_data['bigip'].\
            _meta_data['icr_session'].patch.call_args
        assert kwargs['json']['enabled'] is True
        assert 'disabled' not in kwargs['json']

    def test_reduce_boolean_same_value(self, fake_rsrc):
        with pytest.raises(BooleansToReduceHaveSameValue) as ex:
            fake_rsrc.modify(
                partition='Common',
                name='test_create',
                enabled=True,
                disabled=True
            )
        msg = 'Boolean pair, enabled and disabled, have same value: True. ' \
            'If both are given to this method, they cannot be the same, as ' \
            'this method cannot decide which one should be True.'
        assert msg == ex.value.message


class TestResource_delete(object):
    def test_success(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        attrs = {'delete.return_value':
                 MockResponse({u"generation": 0, u"status_code": 200}),
                 'get.return_value':
                 MockResponse({u"generation": 0, u"status_code": 200})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        r.delete(force=False)
        assert r.__dict__ == {'deleted': True}

    def test_invalid_force(self):
        r = Resource(mock.MagicMock())
        r._meta_data['uri'] = 'URI'
        mock_session = mock.MagicMock()
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        with pytest.raises(InvalidForceType) as IFTEIO:
            r.delete(force='true')
        assert IFTEIO.value.message == 'force parameter must be type bool'


class Element(Resource):
    def __init__(self, container):
        super(Element, self).__init__(container)
        self._meta_data['allowed_lazy_attributes'] = []


class TestCollection_get_collection(object):
    def test_success(self):
        c = Collection(mock.MagicMock())
        c._meta_data['attribute_registry'] = {u"tm:": Element}
        c._meta_data['uri'] = 'URI'
        items = [{'kind': 'tm:', 'selfLink': 'htpps://...'},
                 {'reference': {'link': 'https://...'}}]
        attrs = {'get.return_value':
                 MockResponse({u"generation": 0,
                               u"items": items})}
        mock_session = mock.MagicMock(**attrs)
        c._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME',
             'uri': 'https://TESTDOMAIN:443/mgmt/tm/'}
        c.generation = 0
        c.get_collection()

    def test_unregistered_kind(self):
        c = Collection(mock.MagicMock())
        c._meta_data['attribute_registry'] = {u"t:": Element}
        c._meta_data['uri'] = 'URI'
        items = [{'kind': 'tm:', 'selfLink': 'htpps://...'},
                 {'reference': {'link': 'https://...'}}]
        attrs = {'get.return_value':
                 MockResponse({u"generation": 0,
                               u"items": items})}
        mock_session = mock.MagicMock(**attrs)
        c._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME',
             'uri': 'https://TESTDOMAIN:443/mgmt/tm/'}
        c.generation = 0
        with pytest.raises(UnregisteredKind) as UKEIO:
            c.get_collection()
        assert UKEIO.value.message ==\
            "'tm:' is not registered!"


class TestResource_load(object):
    def test_missing_required_params(self):
        r = Resource(mock.MagicMock())
        r._meta_data['required_load_parameters'] = set(['IMPOSSIBLE'])
        with pytest.raises(MissingRequiredReadParameter) as MRREIO:
            r.load(partition='Common', name='test_load')
        assert MRREIO.value.message ==\
            "Missing required params: ['IMPOSSIBLE']"

    def test_requests_params_collision(self):
        r = Resource(mock.MagicMock())
        with pytest.raises(RequestParamKwargCollision) as RPKCEIO:
            r.load(partition='Common', name='test_load',
                   requests_params={'partition': 'ERROR'})
        assert RPKCEIO.value.message ==\
            "Requests Parameter 'partition' collides with a load parameter"\
            " of the same name."

    def test_icontrol_version_set(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['icontrol_version'] = '11.6.0'
        attrs = {'put.return_value': MockResponse({u"generation": 0}),
                 'get.return_value': MockResponse({u"generation": 0})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        r.contained = Collection(mock.MagicMock())
        assert 'contained' in r.__dict__
        r.update(a=u"b")
        submitted = r._meta_data['bigip']. \
            _meta_data['icr_session'].put.call_args[1]['params']
        assert submitted['ver'] == '11.6.0'

    def test_icontrol_version_default(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        attrs = {'put.return_value': MockResponse({u"generation": 0}),
                 'get.return_value': MockResponse({u"generation": 0})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data = {'icr_session': mock_session}
        r.generation = 0
        r.contained = Collection(mock.MagicMock())
        assert 'contained' in r.__dict__
        r.update(a=u"b")
        submitted = r._meta_data['bigip']. \
            _meta_data['icr_session'].put.call_args
        assert 'params' not in submitted

    def test_success(self):
        r = Virtual(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        mockuri = "https://localhost:443/mgmt/tm/ltm/virtual/~Common~test_load"
        attrs = {'get.return_value':
                 MockResponse(
                     {
                         u"generation": 0,
                         u"selfLink": mockuri,
                         u"kind": u"tm:ltm:virtual:virtualstate"
                     }
                 )}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME',
             'uri': 'https://TESTDOMAIN:443/mgmt/tm/'}
        r.generation = 0
        x = r.load(partition='Common', name='test_load')
        assert x.selfLink == mockuri

    def test_URICreationCollision(self):
        r = Virtual(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        mockuri = "https://localhost:443/mgmt/tm/ltm/virtual/~Common~test_load"
        attrs = {'get.return_value':
                 MockResponse(
                     {
                         u"generation": 0,
                         u"selfLink": mockuri,
                         u"kind": u"tm:ltm:virtual:virtualstate"
                     }
                 )}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME',
             'uri': 'https://TESTDOMAIN:443/mgmt/tm/'}
        r.generation = 0
        x = r.load(partition='Common', name='test_load')
        assert x.selfLink == mockuri
        with pytest.raises(URICreationCollision) as UCCEIO:
            x.load(uri='URI')
        assert UCCEIO.value.message ==\
            "There was an attempt to assign a new uri to this resource, the"\
            " _meta_data['uri'] is "\
            "https://TESTDOMAIN:443/mgmt/tm/ltm/virtual/"\
            "~Common~test_load/ and it should not be changed."


class TestResource_exists(object):
    def test_loadable(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        mockuri = "https://localhost:443/mgmt/tm/ltm/nat/~Common~test_exists"
        attrs = {'get.return_value':
                 MockResponse({u"generation": 0, u"selfLink": mockuri})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME'}
        r.generation = 0
        assert r.exists(partition='Common', name='test_exists')

    def test_not_found(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        response = requests.Response()
        response.status_code = 404
        mock_session = mock.MagicMock()
        mock_session.get.side_effect = requests.HTTPError(response=response)
        r._meta_data['bigip']._meta_data = {
            'icr_session': mock_session,
            'hostname': 'TESTDOMAINNAME'
        }
        assert not r.exists(partition='Common', name='test_exists')

    def test_error(self):
        response = requests.Response()
        response.status_code = 400
        mock_session = mock.MagicMock()
        mock_session.get.side_effect = requests.HTTPError(response=response)
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['bigip']._meta_data = {
            'icr_session': mock_session,
            'hostname': 'TESTDOMAINNAME'
        }
        with pytest.raises(requests.HTTPError) as err:
            r.exists(partition='Common', name='test_exists')
            assert err.response.status_code == 400


def test_OrganizingCollection():
    MockBigIP = mock.MagicMock(name='MockBigIP')
    items = [{'reference': {'link': 'https://...A'}},
             {'reference': {'link': 'https://...B'}}]
    attrs = {'get.return_value':
             MockResponse({u"generation": 0,
                           u"selfLink": 'mockuri',
                           u"items": items})}
    mock_session = mock.MagicMock(**attrs)
    MockBigIP._meta_data = {'uri': 'https://TESTDOMAIN/mgmt/tm/',
                            'bigip': MockBigIP,
                            'icr_session': mock_session,
                            'icontrol_version': ''}
    oc = OrganizingCollection(MockBigIP)
    assert oc.get_collection() == [{'reference': {'link': 'https://...A'}},
                                   {'reference': {'link': 'https://...B'}}]


def test_ResourceBase():
    MockBigIP = mock.MagicMock(name='MockBigIP')
    rb = ResourceBase(MockBigIP)
    with pytest.raises(InvalidResource) as load_EIO:
        rb.load()
    assert load_EIO.value.message ==\
        "Only Resources support 'load'."
    with pytest.raises(InvalidResource) as create_EIO:
        rb.create()
    assert create_EIO.value.message ==\
        "Only Resources support 'create'."
    with pytest.raises(InvalidResource) as delete_EIO:
        rb.delete()
    assert delete_EIO.value.message ==\
        "Only Resources support 'delete'."


class Under_s(Collection):
    def __init__(self, container):
        super(Under_s, self).__init__(container)


def test_collection_s():
    MC = mock.MagicMock()
    MC._meta_data = {
        'bigip': 'bigip',
        'uri': 'BASEURI/',
        'icontrol_version': '',
        'icr_session': 'FAKEICRSESSION'
    }
    tc_s = Under_s(MC)
    assert tc_s._meta_data['uri'] == 'BASEURI/under/'


class TestPathElement(object):

    def test_missing_req_param_true(self):
        rqset = set(['FOOPAR1', 'FOOPAR2'])
        fakearg = {'FOOPAR1': 'FOOVAL'}
        mrq = _missing_required_parameters(rqset, **fakearg)
        assert mrq
        assert mrq == ['FOOPAR2']

    def test_missing_req_param_false(self):
        rqset = set(['FOOPAR1'])
        fakearg = {'FOOPAR1': 'FOOVAL'}
        mrq = _missing_required_parameters(rqset, **fakearg)
        assert not mrq

    def test_check_load_parameters_fail(self):
        p = Resource(mock.MagicMock())
        p._meta_data['required_load_parameters'] = set(['FAKELOAD'])
        with pytest.raises(MissingRequiredReadParameter) as RLPEIO:
            p._check_load_parameters(FOOLOAD='FOOVAL')
        assert "['FAKELOAD']" in RLPEIO.value.message

    def test_check_create_parameters_fail(self):
        p = Resource(mock.MagicMock())
        p._meta_data['required_creation_parameters'] = set(['FAKECREATE'])
        with pytest.raises(MissingRequiredCreationParameter) as RCPEIO:
            p._check_create_parameters(FOOCREATE='FOOVAL')
        assert "['FAKECREATE']" in RCPEIO.value.message

    def test_check_command_parameters_fail(self):
        p = PathElement(mock.MagicMock())
        p._meta_data['required_command_parameters'] = set(['FAKECOMMAND'])
        with pytest.raises(MissingRequiredCommandParameter) as RCPEIO:
            p._check_command_parameters(BARCOMMAND='FOOVAL')
        assert "['FAKECOMMAND']" in RCPEIO.value.message

    def test_check_exclusive_parameters_empty_attr(self):
        p = PathElement(mock.MagicMock())
        p._meta_data['exclusive_attributes'] = []
        fakearg = {'FOOEX': 'FOOVAL'}
        # Check that any other exception is not thrown
        p._check_exclusive_parameters(**fakearg)

    def test_check_exclusive_parameters_pass(self):
        p = PathElement(mock.MagicMock())
        p._meta_data['exclusive_attributes'] = [('FOOEX', 'BAREX')]
        fakearg = {'FOOEX': 'FOOVAL'}
        # Check ExclusiveAttributesPresent is not thrown
        p._check_exclusive_parameters(**fakearg)

    def test_check_exclusive_parameters_fail(self):
        p = PathElement(mock.MagicMock())
        p._meta_data['exclusive_attributes'] = [('FOOEX', 'BAREX')]
        fakearg = {'FOOEX': 'FOOVAL', 'BAREX': 'BARVAL'}
        with pytest.raises(ExclusiveAttributesPresent) as EAEIO:
            p._check_exclusive_parameters(**fakearg)
        assert 'FOOEX, BAREX' in EAEIO.value.message


@pytest.fixture
def FakePath():
    fake_path = mock.MagicMock()
    return PathElement(fake_path)

@pytest.fixture
def FakeVirtual():
    r = Virtual(mock.MagicMock())
    mockuri = "https://localhost:443/mgmt/tm/ltm/virtual/~Common~test_load"
    attrs = {'get.return_value':
        MockResponse(
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
    attrs = {'get.return_value':
                 MockResponse(RAW_DICT)}

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


class TestPathElementStatsModuleHelpers(object):
    def test_key_dot_replace(self):
        p = PathElement(mock.MagicMock())
        fake_dict = {'foo.bar': 'foo', 'baz': 'baz.foo',
                     'fuz.bar': {'baz.foo': {'faz': {'baz.fuz': 1}}}}
        undotted_fake_dict = p._key_dot_replace(fake_dict)
        assert undotted_fake_dict == {'foo_bar': 'foo', 'baz': 'baz.foo',
                     'fuz_bar': {'baz_foo': {'faz': {'baz_fuz': 1}}}}

    def test_pop_nest_stats_nested(self):
        p = PathElement(mock.MagicMock())
        nest = p._get_nest_stats(NESTED_DICT)
        assert nest == EXPECTED_CONVERTED_DICT

    def test_pop_nest_stats_not_nested(self):
        p = PathElement(mock.MagicMock())
        not_nest = p._get_nest_stats(NOT_NESTED_DICT)
        assert not_nest == EXPECTED_CONVERTED_DICT

    def test_pop_nest_stats_nested_no_uri(self):
        p = PathElement(mock.MagicMock())
        nested_nouri = p._get_nest_stats(NESTED_DICT_NO_URI)
        assert nested_nouri == EXPECTED_CONVERTED_DICT_NO_URI

    def test_get_stats_raw(self, FakePath):
        v = MakeFakeResourceContainer(FakePath)
        raw_dict = v._get_stats_raw()
        ret_uri = 'https://testhost/mgmt/tm/ltm/virtual/~Common~test_load/'
        assert v._meta_data['container']._meta_data['uri'] == ret_uri
        assert raw_dict == RAW_DICT

    def test_update_stats_invalid_json(self):
        fake_dict = {'foo.bar': 'foo', 'baz': 'baz.foo',
                     'fuz.bar': {'baz.foo': {'faz': {'baz.fuz': 1}}}}
        p = PathElement(mock.MagicMock())
        with pytest.raises(InvalidStatsJsonReturned)as err:
            p._update_stats(fake_dict)
        assert err.value.message == 'Missing "entries" key in returned JSON'

    def test_update_stats(self):
        p = PathElement(mock.MagicMock())
        p._update_stats(RAW_DICT)
        assert 'stat' in p.__dict__
        assert hasattr(p.__dict__['stat'], 'syncookie_accepts')
        assert hasattr(p.__dict__['stat'], 'ephemeral_bitsOut')
        assert hasattr(p.__dict__['stat'], 'clientside_bitsOut')


class TestStats(object):
    def test_resource_preload(self):
        virt = FakeVirtual()
        chk_lst = virt._meta_data['allowed_lazy_attributes']
        assert virt._meta_data['object_has_stats'] == True
        assert 'stats' in [cls.__name__.lower() for cls in chk_lst
                           if type(cls) in [TypeType, ClassType]]

    def test_stats_init(self):
        virt = FakeVirtual()
        attrs = {'get.return_value':
                     MockResponse(RAW_DICT)}

        return_session = mock.MagicMock(**attrs)
        virt._meta_data['bigip']._meta_data['icr_session'] = return_session
        fake_stats = virt.stats
        uri = 'https://TESTDOMAIN:443/mgmt/tm/ltm/virtual/~Common~test_load/stats/'
        assert fake_stats._meta_data['uri'] == uri
        assert 'stat' in fake_stats.__dict__
        assert hasattr(fake_stats.stat, 'syncookie_accepts')
        assert hasattr(fake_stats.stat, 'ephemeral_bitsOut')
        assert hasattr(fake_stats.stat, 'clientside_bitsOut')
        assert fake_stats.stat.syncookie_accepts.value == 0
        assert fake_stats.stat.ephemeral_bitsOut.value == 0
        assert fake_stats.stat.clientside_bitsOut.value == 0

    def test_stats_raw(self):
        virt = FakeVirtual()
        attrs = {'get.return_value':
                     MockResponse(RAW_DICT)}

        return_session = mock.MagicMock(**attrs)
        virt._meta_data['bigip']._meta_data['icr_session'] = return_session
        fake_stats = virt.stats
        assert fake_stats.stats_raw == RAW_DICT


class TestDottedDict(object):
        def test_init_dict(self):
            undotted_fake_dict = {'foo_bar': 'foo', 'baz': 'baz.foo',
                           'fuz_bar': {'baz_foo': {'faz': {'baz_fuz': 1}}}}
            testdotted = DottedDict(undotted_fake_dict)
            assert testdotted.keys() == undotted_fake_dict.keys()
            assert not hasattr(testdotted, 'baz_foo')
            assert isinstance(testdotted['fuz_bar'], dict)

        def test_init_nondict_elements(self):
            undotted_fake_mixed_dict = {'foo_bar': ('one', 'two'), 'baz': ['baz', 'foo'],
                                        'fuz_bar': {'baz_foo': {'faz': ['baz_fuz', (1, 2, 3)]}}}
            testdotted = DottedDict(undotted_fake_mixed_dict)
            assert testdotted.keys() == undotted_fake_mixed_dict.keys()
            assert not hasattr(testdotted, 'baz_foo')
            assert isinstance(testdotted['foo_bar'], tuple)
            assert isinstance(testdotted['baz'], list)

        def test_getattr(self):
            undotted_fake_dict = {'foo_bar': 'foo', 'baz': 'baz.foo',
                                  'fuz_bar': {'baz_foo': {'faz': {'baz_fuz': 1}}}}
            testdotted = DottedDict(undotted_fake_dict)
            assert isinstance(testdotted.fuz_bar, DottedDict)
            assert hasattr(testdotted.fuz_bar.baz_foo , 'faz')
            assert isinstance(testdotted.fuz_bar.baz_foo.faz, DottedDict)
            assert hasattr(testdotted.fuz_bar.baz_foo.faz, 'baz_fuz')
            assert testdotted.fuz_bar.baz_foo.faz.baz_fuz == 1

        def test_getattr_nondict_elements(self):
            undotted_fake_mixed_dict = {'foo_bar': ('one', 'two'), 'baz': ['baz', 'foo'],
                                  'fuz_bar': {'baz_foo': {'faz': ['baz_fuz', (1, 2, 3)]}}}
            testdotted = DottedDict(undotted_fake_mixed_dict)
            assert isinstance(testdotted.fuz_bar, DottedDict)
            assert hasattr(testdotted.fuz_bar.baz_foo, 'faz')
            assert isinstance(testdotted.fuz_bar.baz_foo.faz, list)
            assert not hasattr(testdotted.fuz_bar.baz_foo.faz, 'baz_fuz')
            assert testdotted.fuz_bar.baz_foo.faz == ['baz_fuz', (1, 2, 3)]


class TestUnnamedResource(object):
    def test_create_raises(self):
        unnamed_resource = UnnamedResource(mock.MagicMock())
        with pytest.raises(UnsupportedMethod):
            unnamed_resource.create()

    def test_delete_raises(self):
        unnamed_resource = UnnamedResource(mock.MagicMock())
        with pytest.raises(UnsupportedMethod):
            unnamed_resource.delete()

    def test_load(self):
        r = Sync_Status(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        mockuri = "https://localhost:443/mgmt/tm/cm/sync-status"
        attrs = {'get.return_value':
                 MockResponse(
                     {
                         u"generation": 0,
                         u"selfLink": mockuri,
                         u"kind": u"tm:cm:sync-status:sync-statusstats"
                     }
                 )}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME',
             'uri': 'https://TESTDOMAIN:443/mgmt/tm/'}
        r.generation = 0
        x = r.load(partition='Common', name='test_load')
        assert x.selfLink == 'https://localhost:443/mgmt/tm/cm/sync-status'
