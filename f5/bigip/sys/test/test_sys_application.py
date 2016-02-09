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
from f5.bigip.sys.application import Service


KIND_MISMATCH = {
    "kind": "tm:sys:application:service:servicestate",
    "name": "tt_serv",
    "partition": "Common",
    "subPath": "tt_serv.app",
    "selfLink": "https://localhost/mgmt/tm/sys/application/service/' \
        '~Common~tt_serv.app~tt_serv?ver=11.6.0",
    "template": "/Common/tt"
}


@pytest.fixture
def FakeService():
    fake_serv_collection = mock.MagicMock()
    fake_serv = Service(fake_serv_collection)
    return fake_serv


class FakeContainer(object):
    def __init__(self):
        self._meta_data = {'uri': mock.MagicMock(name='uri')}


class MockResource(object):
    def __init__(self, test):
        self.x = 1


class TestCreate(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        serv1 = b.sys.applicationcollection.servicecollection.service
        serv2 = b.sys.applicationcollection.servicecollection.service
        assert serv1 is not serv2

    def test_create_no_args(self, FakeService):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeService.create()
        assert 'name' in ex.value.message
        assert 'template' in ex.value.message

    def test_create_no_template(self, FakeService):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            FakeService.create(name='test_service')
        assert 'template' in ex.value.message

    def test_create_uri_collision(self, FakeService):
        FakeService._meta_data = {'uri': 'already_defined'}
        with pytest.raises(URICreationCollision):
            FakeService.create(name='test_service', template='tt')


    def test_create_http_error_not_successful(self):
        with mock.patch(target='f5.bigip.resource.Resource._create') as mock_create:
            mock_create.side_effect = HTTPError(mock.Mock(response=mock.Mock(status_code=404)), 'testing')
            sv1 = Service(mock.MagicMock())
            sv1.create()
            assert True == False

    def test_kindtype_mismatch(self, FakeService):
        fake_container = FakeContainer()
        session_mock = mock.MagicMock(name='mock_session')
        mock_response = mock.MagicMock(name='mock_response')
        mock_response.json.return_value = KIND_MISMATCH
        session_mock.post.return_value = mock_response
        fake_container._meta_data = {
            'icr_session': session_mock
        }
        FakeService._meta_data = {
            'bigip': fake_container,
            'container': fake_container
        }
        FakeService._meta_data['required_creation_parameters'] = \
            set(('name', 'template'))
        FakeService.create(name='tt_serv', template='/Common/tt')
        with pytest.raises(KindTypeMismatch) as ex:
            pass
        assert ex is None


class TestLoad(object):
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


class TestUpdate(object):
    def atest_update_inherit_tg_true(self, FakeService):
        # need some help implementing this test
        pass

    def atest_update_inhere_tg_false(self, FakeService):
        # need some help with this test as well
        pass
