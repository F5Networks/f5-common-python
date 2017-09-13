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
from f5.bigip.tm.asm.policies.gwt_profiles import Gwt_Profile
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestGwtProfiles(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name=name)
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == name
        assert gwt1.description == ''
        gwt1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(
            name=name,
            description='FAKEDESC'
        )
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == name
        assert gwt1.description == 'FAKEDESC'
        gwt1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name=name)
        gwt2 = policy.gwt_profiles_s.gwt_profile.load(id=gwt1.id)
        assert gwt1.kind == gwt2.kind
        assert gwt1.name == gwt2.name
        assert gwt1.description == gwt2.description
        gwt2.modify(description='FAKEDESC')
        assert gwt1.description == ''
        assert gwt2.description == 'FAKEDESC'
        gwt1.refresh()
        assert gwt1.description == 'FAKEDESC'
        gwt1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name=name)
        idhash = str(gwt1.id)
        gwt1.delete()
        with pytest.raises(HTTPError) as err:
            policy.gwt_profiles_s.gwt_profile.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.gwt_profiles_s.gwt_profile.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name=name)
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == name
        assert gwt1.description == ''
        gwt1.modify(description='FAKEDESC')
        assert gwt1.description == 'FAKEDESC'
        gwt2 = policy.gwt_profiles_s.gwt_profile.load(id=gwt1.id)
        assert gwt1.name == gwt2.name
        assert gwt1.selfLink == gwt2.selfLink
        assert gwt1.kind == gwt2.kind
        assert gwt1.description == gwt2.description
        gwt1.delete()

    def test_gwtprofile_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        gwt1 = policy.gwt_profiles_s.gwt_profile.create(name=name)
        assert gwt1.kind == 'tm:asm:policies:gwt-profiles:gwt-profilestate'
        assert gwt1.name == name
        assert gwt1.description == ''
        cc = policy.gwt_profiles_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Gwt_Profile)
        gwt1.delete()
