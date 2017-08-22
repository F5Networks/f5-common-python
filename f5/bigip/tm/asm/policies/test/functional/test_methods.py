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
from f5.bigip.tm.asm.policies.methods import Method


class TestMethods(object):
    def test_create_req_arg(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        assert met1.kind == 'tm:asm:policies:methods:methodstate'
        assert met1.name == 'DELETE'
        assert met1.actAsMethod == 'GET'
        met1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        met1 = policy.methods_s.method.create(name=name, actAsMethod='POST')
        assert met1.kind == 'tm:asm:policies:methods:methodstate'
        assert met1.name == name
        assert met1.actAsMethod == 'POST'
        met1.delete()

    def test_refresh(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        met2 = policy.methods_s.method.load(id=met1.id)
        assert met1.kind == met2.kind
        assert met1.name == met2.name
        assert met1.actAsMethod == met2.actAsMethod
        met2.modify(actAsMethod='POST')
        assert met1.actAsMethod == 'GET'
        assert met2.actAsMethod == 'POST'
        met1.refresh()
        assert met1.actAsMethod == 'POST'
        met1.delete()

    def test_delete(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        idhash = str(met1.id)
        met1.delete()
        with pytest.raises(HTTPError) as err:
            policy.methods_s.method.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.methods_s.method.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        met1 = policy.methods_s.method.create(name='DELETE')
        assert met1.kind == 'tm:asm:policies:methods:methodstate'
        assert met1.name == 'DELETE'
        assert met1.actAsMethod == 'GET'
        met1.modify(actAsMethod='POST')
        assert met1.actAsMethod == 'POST'
        met2 = policy.methods_s.method.load(id=met1.id)
        assert met1.name == met2.name
        assert met1.selfLink == met2.selfLink
        assert met1.kind == met2.kind
        assert met1.actAsMethod == met2.actAsMethod

    def test_method_subcollection(self, policy):
        mc = policy.methods_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Method)
