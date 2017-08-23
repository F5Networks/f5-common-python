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
from f5.bigip.tm.asm.policies.json_profiles import Json_Profile


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestJsonProfile(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        json1 = policy.json_profiles_s.json_profile.create(name=name)
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == name
        assert json1.description == ''
        json1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        json1 = policy.json_profiles_s.json_profile.create(
            name=name,
            description='FAKEDESC'
        )
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == name
        assert json1.description == 'FAKEDESC'
        json1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        json1 = policy.json_profiles_s.json_profile.create(name=name)
        json2 = policy.json_profiles_s.json_profile.load(id=json1.id)
        assert json1.kind == json2.kind
        assert json1.name == json2.name
        assert json1.description == json2.description
        json2.modify(description='FAKEDESC')
        assert json1.description == ''
        assert json2.description == 'FAKEDESC'
        json1.refresh()
        assert json1.description == 'FAKEDESC'
        json1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        json1 = policy.json_profiles_s.json_profile.create(name=name)
        idhash = str(json1.id)
        json1.delete()
        with pytest.raises(HTTPError) as err:
            policy.json_profiles_s.json_profile.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.json_profiles_s.json_profile.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        json1 = policy.json_profiles_s.json_profile.create(name=name)
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == name
        assert json1.description == ''
        json1.modify(description='FAKEDESC')
        assert json1.description == 'FAKEDESC'
        json2 = policy.json_profiles_s.json_profile.load(id=json1.id)
        assert json1.name == json2.name
        assert json1.selfLink == json2.selfLink
        assert json1.kind == json2.kind
        assert json1.description == json2.description
        json1.delete()

    def test_jsonprofile_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        json1 = policy.json_profiles_s.json_profile.create(name=name)
        assert json1.kind == 'tm:asm:policies:json-profiles:json-profilestate'
        assert json1.name == name
        assert json1.description == ''
        cc = policy.json_profiles_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Json_Profile)
        json1.delete()
