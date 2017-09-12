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

from f5.bigip.tm.asm.policies.urls import Url
from requests.exceptions import HTTPError


class TestUrls(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url1 = policy.urls_s.url.create(name=name)
        assert url1.kind == 'tm:asm:policies:urls:urlstate'
        assert url1.type == 'explicit'
        assert url1.name == '/' + name
        assert url1.clickjackingProtection is False
        # url1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url1 = policy.urls_s.url.create(
            name=name,
            clickjackingProtection=True
        )
        assert url1.kind == 'tm:asm:policies:urls:urlstate'
        assert url1.name == '/' + name
        assert url1.type == 'explicit'
        assert url1.clickjackingProtection is True
        url1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url1 = policy.urls_s.url.create(name=name)
        url2 = policy.urls_s.url.load(id=url1.id)
        assert url1.kind == url2.kind
        assert url1.name == url2.name
        assert url1.clickjackingProtection == url2.clickjackingProtection
        url2.modify(clickjackingProtection=True)
        assert url1.clickjackingProtection is False
        assert url2.clickjackingProtection is True
        url1.refresh()
        assert url1.clickjackingProtection is True
        url1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url1 = policy.urls_s.url.create(name=name)
        idhash = str(url1.id)
        url1.delete()
        with pytest.raises(HTTPError) as err:
            policy.urls_s.url.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.urls_s.url.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url1 = policy.urls_s.url.create(name=name)
        assert url1.kind == 'tm:asm:policies:urls:urlstate'
        assert url1.name == '/' + name
        assert url1.type == 'explicit'
        assert url1.clickjackingProtection is False
        url1.modify(clickjackingProtection=True)
        assert url1.clickjackingProtection is True
        url2 = policy.urls_s.url.load(id=url1.id)
        assert url1.name == url2.name
        assert url1.selfLink == url2.selfLink
        assert url1.kind == url2.kind
        assert url1.clickjackingProtection == url2.clickjackingProtection
        url1.delete()

    def test_urls_subcollection(self, policy):
        cc = policy.urls_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Url)
