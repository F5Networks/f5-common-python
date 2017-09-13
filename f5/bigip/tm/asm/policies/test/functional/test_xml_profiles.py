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
from f5.bigip.tm.asm.policies.xml_profiles import Xml_Profile
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestXmlProfile(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        xml1 = policy.xml_profiles_s.xml_profile.create(name=name)
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == name
        assert xml1.description == ''
        xml1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        xml1 = policy.xml_profiles_s.xml_profile.create(
            name=name,
            description='FAKEDESC'
        )
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == name
        assert xml1.description == 'FAKEDESC'
        xml1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        xml1 = policy.xml_profiles_s.xml_profile.create(name=name)
        xml2 = policy.xml_profiles_s.xml_profile.load(id=xml1.id)
        assert xml1.kind == xml2.kind
        assert xml1.name == xml2.name
        assert xml1.description == xml2.description
        xml2.modify(description='FAKEDESC')
        assert xml1.description == ''
        assert xml2.description == 'FAKEDESC'
        xml1.refresh()
        assert xml1.description == 'FAKEDESC'
        xml1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        xml1 = policy.xml_profiles_s.xml_profile.create(name=name)
        idhash = str(xml1.id)
        xml1.delete()
        with pytest.raises(HTTPError) as err:
            policy.xml_profiles_s.xml_profile.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.xml_profiles_s.xml_profile.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        xml1 = policy.xml_profiles_s.xml_profile.create(name=name)
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == name
        assert xml1.description == ''
        xml1.modify(description='FAKEDESC')
        assert xml1.description == 'FAKEDESC'
        xml2 = policy.xml_profiles_s.xml_profile.load(id=xml1.id)
        assert xml1.name == xml2.name
        assert xml1.selfLink == xml2.selfLink
        assert xml1.kind == xml2.kind
        assert xml1.description == xml2.description
        xml1.delete()

    def test_xmlprofile_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        xml1 = policy.xml_profiles_s.xml_profile.create(name=name)
        assert xml1.kind == 'tm:asm:policies:xml-profiles:xml-profilestate'
        assert xml1.name == name
        assert xml1.description == ''
        cc = policy.xml_profiles_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Xml_Profile)
        xml1.delete()
