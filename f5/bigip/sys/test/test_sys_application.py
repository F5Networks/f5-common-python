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

from f5.bigip import BigIP
from f5.bigip.resource import KindTypeMismatch
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from f5.bigip.sys.application import Service


@pytest.fixture
def FakeService():
    fake_serv_collection = mock.MagicMock()
    fake_serv = Service(fake_serv_collection)
    return fake_serv


class TestCreate(object):
    def test_create_two(self):
        b = BigIP('192.168.1.1', 'admin', 'admin')
        serv1 = b.sys.application.servicecollection.service
        serv2 = b.sys.application.servicecollection.service
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

    def atest_kindtype_mismatch(self, FakeService):
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
