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

from requests.exceptions import HTTPError
from f5.bigip.tm.asm.policies.headers import Header


class TestHeaders(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).lower()
        h1 = policy.headers_s.header.create(name=name)
        assert h1.kind == 'tm:asm:policies:headers:headerstate'
        assert h1.name == name
        assert h1.type == 'explicit'
        assert h1.mandatory is False
        h1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).lower()
        h1 = policy.headers_s.header.create(name=name, mandatory=True)
        assert h1.kind == 'tm:asm:policies:headers:headerstate'
        assert h1.name == name
        assert h1.type == 'explicit'
        assert h1.mandatory is True
        h1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).lower()
        h1 = policy.headers_s.header.create(name=name)
        h2 = policy.headers_s.header.load(id=h1.id)
        assert h1.kind == h2.kind
        assert h1.name == h2.name
        assert h1.mandatory == h2.mandatory
        h2.modify(mandatory=True)
        assert h1.mandatory is False
        assert h2.mandatory is True
        h1.refresh()
        assert h1.mandatory is True
        h1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).lower()
        h1 = policy.headers_s.header.create(name=name)
        idhash = str(h1.id)
        h1.delete()
        with pytest.raises(HTTPError) as err:
            policy.headers_s.header.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.headers_s.header.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).lower()
        h1 = policy.headers_s.header.create(name=name)
        assert h1.kind == 'tm:asm:policies:headers:headerstate'
        assert h1.name == name
        assert h1.mandatory is False
        h1.modify(mandatory=True)
        assert h1.mandatory is True
        h2 = policy.headers_s.header.load(id=h1.id)
        assert h1.name == h2.name
        assert h1.selfLink == h2.selfLink
        assert h1.kind == h2.kind
        assert h1.mandatory == h2.mandatory
        h1.delete()

    def test_headers_subcollection(self, policy):
        mc = policy.headers_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Header)
