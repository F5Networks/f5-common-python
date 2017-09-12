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

import pytest

from distutils.version import LooseVersion
from f5.bigip.tm.asm.policies.response_pages import Response_Page
from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestResponsePages(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.response_pages_s.response_page.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.response_pages_s.response_page.delete()

    def test_refresh(self, policy, resp_page):
        hashid = resp_page
        r1 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:response-pages:response-pagestate'
        assert r1.responseActionType == 'default'
        assert r1.responsePageType == 'default'
        r2 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.responseActionType == r2.responseActionType
        assert r1.responsePageType == r2.responsePageType
        r2.responseActionType = 'redirect'
        r2.responseRedirectUrl = 'http://fake-site.com'
        r2.modify(
            responseActionType='redirect',
            responseRedirectUrl='http://fake-site.com'
        )
        assert r1.responseActionType == 'default'
        assert r2.responseActionType == 'redirect'
        assert not hasattr(r1, 'responseRedirectUrl')
        assert hasattr(r2, 'responseRedirectUrl')
        r1.refresh()
        assert hasattr(r1, 'responseRedirectUrl')
        assert r1.responseActionType == r2.responseActionType
        assert r1.responseRedirectUrl == 'http://fake-site.com'

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.response_pages_s.response_page.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, resp_page):
        hashid = resp_page
        r1 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:response-pages:response-pagestate'
        assert r1.responsePageType == 'default'
        assert r1.responseActionType == 'default'
        r2 = policy.response_pages_s.response_page.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.responseActionType == r2.responseActionType
        assert r1.responsePageType == r2.responsePageType

    def test_responsepages_subcollection(self, policy):
        mc = policy.response_pages_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Response_Page)
