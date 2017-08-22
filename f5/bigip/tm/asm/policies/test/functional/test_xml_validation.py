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

from f5.sdk_exception import UnsupportedOperation
from distutils.version import LooseVersion
from requests.exceptions import HTTPError
from f5.bigip.tm.asm.policies.xml_validation import Xml_Validation_File


XML2 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\n<shiporder " \
       "orderid=\"889923\"\nxmlns:xsi=\"" \
       "http://www.w3.org/2001/XMLSchema-instance\"\n" \
       "xsi:noNamespaceSchemaLocation=\"shiporder.xsd\">\n  " \
       "<orderperson>John Smith</orderperson>\n  <shipto>\n    " \
       "<name>Ola Nordmann</name>\n    <address>Langgt 23</address>\n    " \
       "<city>4000 Stavanger</city>\n    <country>Norway</country>\n  " \
       "</shipto>\n  <item>\n    <title>Empire Burlesque</title>\n    " \
       "<note>Special Edition</note>\n    <quantity>1</quantity>\n    " \
       "<price>10.90</price>\n  </item>\n  <item>\n    " \
       "<title>Hide your heart</title>\n    <quantity>1</quantity>\n    " \
       "<price>9.90</price>\n  </item>\n</shiporder> "


@pytest.fixture(scope='function')
def set_xml_file(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = policy.xml_validation_files_s.xml_validation_file.create(
        fileName=name,
        contents=XML2
    )
    yield r1
    r1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestXmlValidationFiles(object):
    def test_modify_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.xml_validation_files_s.xml_validation_file.modify()

    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.xml_validation_files_s.xml_validation_file.create(
            fileName=name,
            contents=XML2
        )
        assert r1.kind == 'tm:asm:policies:xml-validation-files:xml-validation-filestate'
        assert r1.fileName == name
        r1.delete()

    def test_refresh(self, set_xml_file, policy):
        r1 = set_xml_file
        r2 = policy.xml_validation_files_s.xml_validation_file.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.fileName == r2.fileName
        assert r1.id == r2.id
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.fileName == r2.fileName
        assert r1.id == r2.id

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.xml_validation_files_s.xml_validation_file.create(
            fileName=name,
            contents=XML2
        )
        idhash = r1.id
        r1.delete()
        with pytest.raises(HTTPError) as err:
            policy.xml_validation_files_s.xml_validation_file.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.xml_validation_files_s.xml_validation_file.load(
                id='Lx3553-321'
            )
        assert err.value.response.status_code == 404

    def test_load(self, set_xml_file, policy):
        r1 = set_xml_file
        assert r1.kind == 'tm:asm:policies:xml-validation-files:xml-validation-filestate'
        r2 = policy.xml_validation_files_s.xml_validation_file.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.fileName == r2.fileName

    def test_xml_validation_files_subcollection(self, set_xml_file, policy):
        r1 = set_xml_file
        assert r1.kind == 'tm:asm:policies:xml-validation-files:xml-validation-filestate'
        cc = policy.xml_validation_files_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Xml_Validation_File)
