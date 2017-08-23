# Copyright 2017 F5 Networks Inc.
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

import os
import pytest
import tempfile

from distutils.version import LooseVersion
from requests.exceptions import HTTPError
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.bigip.tm.asm.policies.websocket_urls import Websocket_Url


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
    reason='This collection is fully implemented on 12.1.0 or greater.'
)
class TestWebsocketUrls(object):
    def test_create_req_arg(self, set_websock):
        r1 = set_websock
        assert r1.kind == 'tm:asm:policies:websocket-urls:websocket-urlstate'
        assert r1.description == ''

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.websocket_urls_s.websocket_url.create(
            name=name,
            checkPayload=False,
            description='fake_websock_text'
        )
        assert r1.kind == 'tm:asm:policies:websocket-urls:websocket-urlstate'
        assert r1.name == name
        assert r1.description == 'fake_websock_text'
        r1.delete()

    def test_create_mandatory_arg_missing(self, policy2):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        with pytest.raises(MissingRequiredCreationParameter) as err:
            policy2.websocket_urls_s.websocket_url.create(
                name=name,
                checkPayload=True
            )
        assert 'This resource requires at least one of the' in str(err.value)

    def test_create_profile_ref_missing(self, policy2):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        with pytest.raises(MissingRequiredCreationParameter) as err:
            policy2.websocket_urls_s.websocket_url.create(
                name=name,
                allowTextMessage=True,
                allowJsonMessage=True,
                checkPayload=True
            )
        assert 'Missing required params:' in str(err.value)

    def test_refresh(self, set_websock, policy):
        r1 = set_websock
        r2 = policy.websocket_urls_s.websocket_url.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.selfLink == r1.selfLink
        assert r1.description == r2.description
        r2.modify(description='changed_this')
        assert r1.description == ''
        assert r2.description == 'changed_this'
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.description == 'changed_this'

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.websocket_urls_s.websocket_url.create(
            name=name,
            checkPayload=False
        )
        idhash = r1.id
        r1.delete()
        with pytest.raises(HTTPError) as err:
            policy.websocket_urls_s.websocket_url.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.websocket_urls_s.websocket_url.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, set_websock, policy):
        r1 = set_websock
        assert r1.kind == 'tm:asm:policies:websocket-urls:websocket-urlstate'
        assert r1.description == ''
        r1.modify(description='load_this')
        assert r1.description == 'load_this'
        r2 = policy.websocket_urls_s.websocket_url.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.description == r2.description

    def test_websocketurls_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.websocket_urls_s.websocket_url.create(
            name=name,
            checkPayload=False,
            description='fake_websock_text'
        )
        cc = policy.websocket_urls_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Websocket_Url)
