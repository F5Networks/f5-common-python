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
from f5.bigip.tm.asm.policies.extractions import Extraction
from f5.sdk_exception import MissingRequiredCreationParameter
from requests.exceptions import HTTPError


@pytest.fixture(scope='function')
def set_extraction(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = policy.extractions_s.extraction.create(
        extractFromAllItems=True,
        name=name
    )
    yield r1
    r1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestExtractions(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.extractions_s.extraction.create(
            extractFromAllItems=True,
            name=name
        )
        assert r1.kind == 'tm:asm:policies:extractions:extractionstate'
        r1.delete()

    def test_create_mandatory_arg_missing(self, policy2):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        with pytest.raises(MissingRequiredCreationParameter) as err:
            policy2.extractions_s.extraction.create(
                extractFromAllItems=False,
                name=name
            )

        assert 'This resource requires at least one of the' in str(err.value)

    def test_create_mandatory_arg_present(self, policy2):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy2.extractions_s.extraction.create(
            extractFromAllItems=False,
            name=name,
            extractFromRegularExpression='["test"]')
        assert r1.kind == 'tm:asm:policies:extractions:extractionstate'
        assert r1.extractFromRegularExpression == '["test"]'
        assert r1.extractFromAllItems is False
        r1.delete()

    def test_refresh(self, set_extraction, policy):
        r1 = set_extraction
        r2 = policy.extractions_s.extraction.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.extractFromAllItems == r2.extractFromAllItems
        assert r1.searchInXml == r2.searchInXml
        r2.modify(searchInXml=True)
        assert r1.searchInXml is False
        assert r2.searchInXml is True
        r1.refresh()
        assert r1.searchInXml is True

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.extractions_s.extraction.create(
            extractFromAllItems=True,
            name=name
        )
        idhash = r1.id
        r1.delete()
        with pytest.raises(HTTPError) as err:
            policy.extractions_s.extraction.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.extractions_s.extraction.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, set_extraction, policy):
        r1 = set_extraction
        assert r1.kind == 'tm:asm:policies:extractions:extractionstate'
        assert r1.searchInXml is False
        r1.modify(searchInXml=True)
        assert r1.searchInXml is True
        r2 = policy.extractions_s.extraction.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.searchInXml == r2.searchInXml

    def test_extractions_subcollection(self, policy, set_extraction):
        r1 = set_extraction
        assert r1.kind == 'tm:asm:policies:extractions:extractionstate'
        cc = policy.extractions_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Extraction)
