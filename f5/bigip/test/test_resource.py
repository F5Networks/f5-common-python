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

from f5.bigip.resource import Collection
from f5.bigip.resource import DeviceProvidesIncompatibleKey
from f5.bigip.resource import GenerationMismatch
from f5.bigip.resource import InvalidForceType
from f5.bigip.resource import InvalidResource
from f5.bigip.resource import KindTypeMismatch
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from f5.bigip.resource import OrganizingCollection
from f5.bigip.resource import RequestParamKwargCollision
from f5.bigip.resource import Resource
from f5.bigip.resource import ResourceBase
from f5.bigip.resource import UnregisteredKind
from f5.bigip.resource import URICreationCollision


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
            "Missing required params: set(['NONEMPTY'])"

    def test_KindTypeMismatch(self):
        r = Resource(mock.MagicMock())
        r._meta_data['bigip']._meta_data['icr_session'].post.return_value =\
            MockResponse({u"kind": u"tm:"})
        r._meta_data['required_json_kind'] = 'INCORRECT!'
        with pytest.raises(KindTypeMismatch) as KTMmEIO:
            r.create(partition="Common", name="test_create")
        assert KTMmEIO.value.message ==\
            "For instances of type ''Resource'' the corresponding kind must"\
            " be ''INCORRECT!'' but creation returned JSON with kind: u'tm:'"

    def test_successful(self):
        r = Resource(mock.MagicMock())
        MRO = MockResponse({u"kind": u"tm:",
                            u"selfLink": u".../~Common~test_create"})
        r._meta_data['bigip']._meta_data['icr_session'].post.return_value = MRO
        r._meta_data['required_json_kind'] = u"tm:"
        r._meta_data['allowed_lazy_attributes'] = []
        r.create(partition="Common", name="test_create")
        assert r.kind == u"tm:"
        assert r.selfLink == u".../~Common~test_create"


def test__activate_URI():
    r = Resource(mock.MagicMock())
    r._meta_data['allowed_lazy_attributes'] = []
    r._meta_data['attribute_registry'] = {u"tm:": u"SPAM"}
    r._meta_data['bigip']._meta_data = {'hostname': 'TESTDOMAIN'}
    TURI = 'https://localhost/mgmt/tm/'\
           'ltm/nat/~Common~testnat/?ver=11.5&a=b#FOO'
    assert r._meta_data['allowed_lazy_attributes'] == []
    r._activate_URI(TURI)
    assert r._meta_data['uri'] ==\
        'https://TESTDOMAIN/mgmt/tm/ltm/nat/~Common~testnat/'
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
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        r._meta_data['uri'] = 'URI'
        r._meta_data['bigip']._meta_data['icr_session'].get.return_value =\
            MockResponse({u"generation": 0})
        r.generation = 1
        with pytest.raises(GenerationMismatch) as GMEIO:
            r.update(a=u"b")
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
        submitted = r._meta_data['bigip'].\
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
             'hostname': 'TESTDOMAINNAME'}
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
             'hostname': 'TESTDOMAINNAME'}
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
            "Missing required params: set(['IMPOSSIBLE'])"

    def test_requests_params_collision(self):
        r = Resource(mock.MagicMock())
        with pytest.raises(RequestParamKwargCollision) as RPKCEIO:
            r.load(partition='Common', name='test_load',
                   requests_params={'partition': 'ERROR'})
        assert RPKCEIO.value.message ==\
            "Requests Parameter 'partition' collides with a load parameter"\
            " of the same name."

    def test_success(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        mockuri = "https://localhost/mgmt/tm/ltm/nat/~Common~test_load"
        attrs = {'get.return_value':
                 MockResponse({u"generation": 0, u"selfLink": mockuri})}
        mock_session = mock.MagicMock(**attrs)
        r._meta_data['bigip']._meta_data =\
            {'icr_session': mock_session,
             'hostname': 'TESTDOMAINNAME'}
        r.generation = 0
        r.load(partition='Common', name='test_load')
        r.raw
        assert r.selfLink == mockuri


class TestResource_exists(object):
    def test_loadable(self):
        r = Resource(mock.MagicMock())
        r._meta_data['allowed_lazy_attributes'] = []
        mockuri = "https://localhost/mgmt/tm/ltm/nat/~Common~test_exists"
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
                            'icr_session': mock_session}
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
    with pytest.raises(InvalidResource) as update_EIO:
        rb.update()
    assert update_EIO.value.message ==\
        "Only Resources support 'update'."
    with pytest.raises(InvalidResource) as delete_EIO:
        rb.delete()
    assert delete_EIO.value.message ==\
        "Only Resources support 'delete'."


class Test_s(Collection):
    def __init__(self, container):
        super(Test_s, self).__init__(container)


def test_collection_s():
    MC = mock.MagicMock()
    MC._meta_data = {'bigip': 'bigip', 'uri': 'BASEURI/'}
    tc_s = Test_s(MC)
    assert tc_s._meta_data['uri'] == 'BASEURI/test/'
