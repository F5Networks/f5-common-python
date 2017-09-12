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

from f5.bigip.tm.asm.policies.cookies import Cookie
from requests.exceptions import HTTPError


class TestCookies(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        cook1 = policy.cookies_s.cookie.create(name=name)
        assert cook1.kind == 'tm:asm:policies:cookies:cookiestate'
        assert cook1.name == name
        assert cook1.enforcementType == 'allow'
        cook1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        cook1 = policy.cookies_s.cookie.create(
            name=name,
            enforcementType='enforce'
        )
        assert cook1.kind == 'tm:asm:policies:cookies:cookiestate'
        assert cook1.name == name
        assert cook1.enforcementType == 'enforce'
        cook1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        cook1 = policy.cookies_s.cookie.create(name=name)
        cook2 = policy.cookies_s.cookie.load(id=cook1.id)
        assert cook1.kind == cook2.kind
        assert cook1.name == cook2.name
        assert cook1.enforcementType == cook2.enforcementType
        cook2.modify(enforcementType='enforce')
        assert cook1.enforcementType == 'allow'
        assert cook2.enforcementType == 'enforce'
        cook1.refresh()
        assert cook1.enforcementType == 'enforce'
        cook1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        cook1 = policy.cookies_s.cookie.create(name=name)
        idhash = str(cook1.id)
        cook1.delete()
        with pytest.raises(HTTPError) as err:
            policy.cookies_s.cookie.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.cookies_s.cookie.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        cook1 = policy.cookies_s.cookie.create(name=name)
        assert cook1.kind == 'tm:asm:policies:cookies:cookiestate'
        assert cook1.name == name
        assert cook1.enforcementType == 'allow'
        cook1.modify(enforcementType='enforce')
        assert cook1.enforcementType == 'enforce'
        cook2 = policy.cookies_s.cookie.load(id=cook1.id)
        assert cook1.name == cook2.name
        assert cook1.selfLink == cook2.selfLink
        assert cook1.kind == cook2.kind
        assert cook1.enforcementType == cook2.enforcementType
        cook1.delete()

    def test_cookies_subcollection(self, policy):
        cc = policy.cookies_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Cookie)
