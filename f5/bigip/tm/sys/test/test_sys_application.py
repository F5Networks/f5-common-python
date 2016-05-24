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
from requests import HTTPError

from f5.bigip import BigIP
from f5.bigip.resource import KindTypeMismatch
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from f5.bigip.resource import URICreationCollision
from f5.bigip.tm.sys.application import Aplscript
from f5.bigip.tm.sys.application import Customstat
from f5.bigip.tm.sys.application import Service
from f5.bigip.tm.sys.application import Template


KIND_MISMATCH = {
    "kind": "tm:sys:application:service:servicecollectionstate",
    "name": "tt_serv",
    "partition": "Common",
    "subPath": "tt_serv.app",
    "selfLink": "https://localhost/mgmt/tm/sys/application/service/' \
        '~Common~tt_serv.app~tt_serv?ver=11.6.0",
    "template": "/Common/tt"
}

SUCCESSFUL_CREATE = {
    "kind": "tm:sys:application:service:servicestate",
    "name": "test_service",
    "partition": "Common",
    "subPath": "tt_serv.app",
    "selfLink": "https://localhost/mgmt/tm/sys/application/service/' \
        '~Common~tt_serv.app~tt_serv?ver=11.6.0",
    "template": "test_template"
}

TRUE_INHERITED_DEVGROUP = {
    "kind": "tm:sys:application:service:servicestate",
    "name": "test_service",
    "partition": "Common",
    "inheritedDevicegroup": "true",
    "deviceGroup": "test_dev_group",
    "subPath": "tt_serv.app",
    "selfLink": "https://localhost/mgmt/tm/sys/application/service/' \
        '~Common~tt_serv.app~tt_serv?ver=11.6.0",
    "template": "test_template"
}

FALSE_INHERITED_DEVGROUP = {
    "kind": "tm:sys:application:service:servicestate",
    "name": "test_service",
    "partition": "Common",
    "inheritedDevicegroup": "false",
    "subPath": "tt_serv.app",
    "selfLink": "https://localhost/mgmt/tm/sys/application/service/' \
        '~Common~tt_serv.app~tt_serv?ver=11.6.0",
    "template": "test_template"
}

SIDE_EFFECT = {'only_key': 'this is the only key'}


@pytest.fixture
def FakeService():
    fake_serv_s = mock.MagicMock()
    return Service(fake_serv_s)


@pytest.fixture
def FakeTemplate():
    fake_templ_s = mock.MagicMock()
    return Template(fake_templ_s)


@pytest.fixture
def FakeAplscript():
    fake_apl_s = mock.MagicMock()
    return Aplscript(fake_apl_s)


@pytest.fixture
def FakeCustomstat():
    fake_custom_stat_s = mock.MagicMock()
    return Customstat(fake_custom_stat_s)


@pytest.fixture
@mock.patch('f5.bigip')
def MakeFakeContainer(FakeService, mock_json, mock_bigip):
    mock_session = mock.MagicMock(name='mock_session')
    mock_get_response = mock.MagicMock(name='mock_get_response')
    mock_put_response = mock.MagicMock(name='mock_put_response')
    mock_get_response.json.return_value = mock_json.copy()
    mock_put_response.json.return_value = SUCCESSFUL_CREATE.copy()
    # Mock the get and put when the container calls icr_session.get/put
    mock_session.get.return_value = mock_get_response
    mock_session.put.return_value = mock_put_response
    mock_bigip._meta_data = {
        'hostname': 'testhost',
        'icr_session': mock_session,
        'uri': '',
        'icontrol_version': ''
    }
    FakeService._meta_data['bigip'] = mock_bigip
    FakeService._meta_data['icontrol_version'] = ''
    return FakeService


@pytest.fixture
@mock.patch('f5.bigip')
def MakeFakeContainerRaise(FakeService, mock_json, side_effect, mock_bigip):
    mock_session = mock.MagicMock(name='mock_session')
    mock_get_response = mock.MagicMock(name='mock_get_response')
    mock_get_response.json.return_value = mock_json.copy()
    mock_session.get.side_effect = side_effect
    mock_bigip._meta_data = {
        'hostname': 'testhost',
        'icr_session': mock_session,
        'uri': '',
        'icontrol_version': ''
    }
    FakeService._meta_data['bigip'] = mock_bigip
    mock_base_uri = mock.MagicMock()
    mock_base_uri._meta_data = {'uri': 'base_uri'}
    FakeService._meta_data['container'] = mock_base_uri
    FakeService._meta_data['icontrol_version'] = ''
    return FakeService


@pytest.fixture
def SideEffectFixture():
    # Let's show that fixture side-effects can cause test interactions
    # that are surprising to the untrained eye.
    SIDE_EFFECT['new_key'] = 'Added new key to module variable.'


class MockHTTPError(HTTPError):
    def __init__(self, response_obj):
        self.response = response_obj


class MockHTTPErrorResponseSuccessful(HTTPError):
    def __init__(self):
        self.text = 'The configuration was updated successfully but could not'\
            ' be retrieved'


class MockHTTPErrorResponse404(HTTPError):
    def __init__(self):
        self.text = 'Something else happened.'
        self.status_code = 404


class MockHTTPErrorResponse400(HTTPError):
    def __init__(self):
        self.status_code = 400


class TestServiceCreate(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        serv1 = b.sys.applications.services.service
        serv2 = b.sys.applications.services.service
        assert serv1 is not serv2

    def test_create_no_args(self, FakeService):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeService.create()
        assert 'name' in ex.value.message
        assert 'template' in ex.value.message
        assert 'partition' in ex.value.message

    def test_create_no_template(self, FakeService):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeService.create(name='test_service')
        assert 'template' in ex.value.message

    def test_create_no_partition(self, FakeService):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeService.create(name='test_service', template='test_template')
        assert 'partition' in ex.value.message

    def test_create_uri_collision(self, FakeService):
        FakeService._meta_data = {'uri': 'already_defined'}
        with pytest.raises(URICreationCollision) as ex:
            FakeService.create(fakeuri='FAKEURI')
        assert "There was an attempt to assign a new uri to this resource, " \
            "the _meta_data['uri'] is already_defined and it should not be " \
            "changed." in ex.value.message

    def test_create_http_error_not_successful(self):
        with mock.patch(target='f5.bigip.resource.Resource._create') as \
                mock_create:
            mock_create.side_effect = MockHTTPError(
                MockHTTPErrorResponse404()
            )
            sv1 = Service(mock.MagicMock())
            with pytest.raises(HTTPError):
                sv1.create()
                assert sv1 is None

    def test_create_kindtype_mismatch(self, FakeService):
        FakeService = MakeFakeContainer(FakeService, KIND_MISMATCH)
        with mock.patch(target='f5.bigip.resource.Resource._create') as \
                mock_create:
            mock_create.side_effect = MockHTTPError(
                MockHTTPErrorResponseSuccessful()
            )
            with pytest.raises(KindTypeMismatch):
                FakeService.create(
                    name='test_server', template='test_template'
                )

    def test_create_success(self, FakeService):
        FakeService = MakeFakeContainer(FakeService, SUCCESSFUL_CREATE)
        with mock.patch(target='f5.bigip.resource.Resource._create') as \
                mock_create:
            mock_create.side_effect = MockHTTPError(
                MockHTTPErrorResponseSuccessful()
            )
            sv1 = FakeService.create(
                name='test_service',
                template='test_template'
            )
            assert sv1 is not None
            assert sv1.name == 'test_service'
            assert sv1.template == 'test_template'


class TestServiceExists(object):
    def test_exists(self, FakeService):
        FakeService = MakeFakeContainer(FakeService, {})
        assert FakeService.exists(name='test', partition='test') is True

    def test_exists_failure(self, FakeService):
        FakeService = MakeFakeContainerRaise(FakeService, {}, Exception())
        with pytest.raises(Exception):
            FakeService.exists(name='test', partition='test')
        assert FakeService._meta_data['bigip']._meta_data['icr_session'].get.\
            call_args == mock.call(
                'base_uri~test~test.app~test',
                uri_as_parts=False
            )

    def test_exists_false(self, FakeService):
        FakeService = MakeFakeContainerRaise(
            FakeService,
            {},
            MockHTTPError(MockHTTPErrorResponse404())
        )
        assert FakeService.exists(name='test', partition='test') is False

    def test_exists_http_error_raise(self, FakeService):
        FakeService = MakeFakeContainerRaise(
            FakeService,
            {},
            MockHTTPError(MockHTTPErrorResponse400())
        )
        with pytest.raises(HTTPError):
            FakeService.exists(name='test', partition='test')


class TestServiceLoad(object):
    def test_load_no_args(self, FakeService):
        with pytest.raises(MissingRequiredReadParameter) as ex:
            FakeService.load()
        assert ex.value.message == \
            "Missing required params: set(['partition', 'name'])"

    def test_load_no_partition(self, FakeService):
        with pytest.raises(MissingRequiredReadParameter) as ex:
            FakeService.load(name='test_service')
        assert ex.value.message == \
            "Missing required params: set(['partition'])"


class TestServiceUpdate(object):
    def test_update_inherit_tg_true(self, FakeService):
        FakeService = MakeFakeContainer(FakeService, TRUE_INHERITED_DEVGROUP)
        with mock.patch(target='f5.bigip.resource.Resource._create') as \
                mock_create:
            mock_create.side_effect = MockHTTPError(
                MockHTTPErrorResponseSuccessful()
            )
            sv1 = FakeService.create(
                name='test_service',
                template='test_template'
            )
            sv1.update()
            assert hasattr(sv1, 'deviceGroup') is False

    def test_update_inherit_tg_false(self, FakeService):
        FakeService = MakeFakeContainer(FakeService, FALSE_INHERITED_DEVGROUP)
        with mock.patch(target='f5.bigip.resource.Resource._create') as \
                mock_create:
            mock_create.side_effect = MockHTTPError(
                MockHTTPErrorResponseSuccessful()
            )
            sv1 = FakeService.create(
                name='test_service',
                template='test_template'
            )
            sv1.update()
            # Since the SUCCESSFUL_CREATE dictionary is the result of the
            # update, the inheritedDevicegroup and deviceGroup should not
            # be there.
            assert hasattr(sv1, 'deviceGroup') is False
            assert hasattr(sv1, 'inheritedDevicegroup') is False


class TestTemplateCreate(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        templ1 = b.sys.applications.templates.template
        templ2 = b.sys.applications.templates.template
        assert templ1 is not templ2

    def test_create_no_args(self, FakeTemplate):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeTemplate.create()
        assert 'name' in ex.value.message
        assert 'partition' in ex.value.message


class TestAplscript(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        templ1 = b.sys.applications.aplscripts.aplscript
        templ2 = b.sys.applications.aplscripts.aplscript
        assert templ1 is not templ2

    def test_create_no_args(self, FakeAplscript):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeAplscript.create()
        assert 'name' in ex.value.message


class TestCustomstat(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        templ1 = b.sys.applications.customstats.customstat
        templ2 = b.sys.applications.customstats.customstat
        assert templ1 is not templ2

    def test_create_no_args(self, FakeCustomstat):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeCustomstat.create()
        assert 'name' in ex.value.message


def test_setup_side_effect_in_fixture(SideEffectFixture):
    # Show the module dict has the new key while this fixture is in use.
    assert 'new_key' in SIDE_EFFECT


def test_side_effect_from_fixture():
    # Show the added key from the previous fixture is still there
    assert 'new_key' in SIDE_EFFECT
