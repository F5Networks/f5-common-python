# Copyright 2015 F5 Networks Inc.
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

from f5.bigip.tm.asm.policies.websocket_urls import Websocket_Url
from f5.sdk_exception import MissingRequiredCreationParameter


import mock
import pytest


@pytest.fixture
def FakeWebsock():
    fake_policy = mock.MagicMock()
    fake_e = Websocket_Url(fake_policy)
    fake_e._meta_data['bigip'].tmos_version = '12.1.0'
    return fake_e


class TestWebSocketUrls(object):
    def test_create_no_args(self, FakeWebsock):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeWebsock.create()

    def test_create_missing_additional_arguments(self, FakeWebsock):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeWebsock.create(name='fake', checkPayload=True)

    def test_create_additional_arguments_missing_profiles(self, FakeWebsock):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeWebsock.create(name='fake', checkPayload=True,
                               allowTextMessage=True, allowJsonMessage=True)
