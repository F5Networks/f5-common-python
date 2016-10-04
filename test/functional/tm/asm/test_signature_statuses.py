# Copyright 2015 F5 Networks Inc.
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

from f5.bigip.tm.asm.signature_statuses import Signature_Status
import pytest
from requests.exceptions import HTTPError


def get_sigstatid(request, mgmt_root):
    sigcoll = mgmt_root.tm.asm.signature_statuses_s.get_collection()
    # We obtain the ID for the resource to test and return the hashed id
    hashid = str(sigcoll[0].id)
    return hashid


class TestSignatureStatuses(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signature_statuses_s.signature_status.load(
                id='Lx3553-321')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        hashid = get_sigstatid(request, mgmt_root)
        sigstat = mgmt_root.tm.asm.signature_statuses_s.signature_status.load(
            id=hashid)
        kind = 'tm:asm:signature-statuses:signature-statusstate'
        baseuri = 'https://localhost/mgmt/tm/asm/signature-statuses/'
        final_uri = baseuri+hashid
        assert sigstat.id == hashid
        assert sigstat.kind == kind
        assert sigstat.selfLink.startswith(final_uri)
        assert sigstat.isUserDefined is False

    def test_refresh(self, request, mgmt_root):
        hashid = get_sigstatid(request, mgmt_root)
        sigstat = mgmt_root.tm.asm.signature_statuses_s.signature_status.load(
            id=hashid)
        sigstat2 = mgmt_root.tm.asm.signature_statuses_s.signature_status.load(
            id=hashid)
        kind = 'tm:asm:signature-statuses:signature-statusstate'
        baseuri = 'https://localhost/mgmt/tm/asm/signature-statuses/'
        final_uri = baseuri+hashid
        assert sigstat.id == hashid
        assert sigstat.kind == kind
        assert sigstat.selfLink.startswith(final_uri)
        sigstat2.refresh()
        assert sigstat.id == sigstat2.id
        assert sigstat.kind == sigstat2.kind
        assert sigstat.selfLink == sigstat2.selfLink

    def test_collection(self, request, mgmt_root):
        sc = mgmt_root.tm.asm.signature_statuses_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Signature_Status)
