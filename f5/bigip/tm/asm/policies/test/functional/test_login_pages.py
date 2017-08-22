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
from f5.bigip.tm.asm.policies.login_pages import Login_Page


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestLoginPages(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name + '.com')
        reference = {'link': url.selfLink}
        valid = {'responseContains': '201 OK'}
        r1 = policy.login_pages_s.login_page.create(
            urlReference=reference,
            accessValidation=valid
        )
        assert r1.kind == 'tm:asm:policies:login-pages:login-pagestate'
        assert r1.authenticationType == 'none'
        assert r1.urlReference == reference
        r1.delete()
        url.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name + '.com')
        reference = {'link': url.selfLink}
        valid = {'responseContains': '201 OK'}
        r1 = policy.login_pages_s.login_page.create(
            urlReference=reference,
            accessValidation=valid,
            authenticationType='http-basic'
        )
        assert r1.kind == 'tm:asm:policies:login-pages:login-pagestate'
        assert r1.authenticationType == 'http-basic'
        assert r1.urlReference == reference
        r1.delete()
        url.delete()

    def test_refresh(self, set_login, policy):
        r1, _ = set_login
        r2 = policy.login_pages_s.login_page.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.authenticationType == r2.authenticationType
        r2.modify(authenticationType='http-basic')
        assert r1.authenticationType == 'none'
        assert r2.authenticationType == 'http-basic'
        r1.refresh()
        assert r1.authenticationType == 'http-basic'

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name + '.com')
        reference = {'link': url.selfLink}
        valid = {'responseContains': '201 OK'}
        r1 = policy.login_pages_s.login_page.create(
            urlReference=reference, accessValidation=valid)
        idhash = r1.id
        r1.delete()
        with pytest.raises(HTTPError) as err:
            policy.login_pages_s.login_page.load(id=idhash)
        assert err.value.response.status_code == 404
        url.delete()

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.login_pages_s.login_page.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, set_login, policy):
        r1, _ = set_login
        assert r1.kind == 'tm:asm:policies:login-pages:login-pagestate'
        assert r1.authenticationType == 'none'
        r1.modify(authenticationType='http-basic')
        assert r1.authenticationType == 'http-basic'
        r2 = policy.login_pages_s.login_page.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.authenticationType == r2.authenticationType

    def test_login_pages_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        url = policy.urls_s.url.create(name=name + '.com')
        reference = {'link': url.selfLink}
        valid = {'responseContains': '201 OK'}
        policy.login_pages_s.login_page.create(
            urlReference=reference,
            accessValidation=valid,
            authenticationType='http-basic'
        )
        cc = policy.login_pages_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Login_Page)
