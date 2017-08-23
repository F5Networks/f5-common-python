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

from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError
from f5.bigip.tm.asm.policies.signatures import Signature


class TestSignature(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.signatures_s.signature.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.signatures_s.signature.delete()

    def test_refresh(self, policy):
        coll = policy.signatures_s.get_collection()
        hashid = str(coll[1].id)
        ws1 = policy.signatures_s.signature.load(id=hashid)
        ws2 = policy.signatures_s.signature.load(id=hashid)
        assert ws1.kind == ws2.kind
        assert ws1.performStaging == ws2.performStaging
        ws2.modify(performStaging=False)
        assert ws1.performStaging is True
        assert ws2.performStaging is False
        ws1.refresh()
        assert ws1.performStaging is False

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.signatures_s.signature.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.signatures_s.get_collection()
        hashid = str(coll[1].id)
        ws1 = policy.signatures_s.signature.load(id=hashid)
        assert ws1.kind == 'tm:asm:policies:signatures:signaturestate'
        assert ws1.performStaging is True
        ws1.modify(performStaging=False)
        assert ws1.performStaging is False
        ws2 = policy.signatures_s.signature.load(id=ws1.id)
        assert ws1.selfLink == ws2.selfLink
        assert ws1.kind == ws2.kind
        assert ws1.performStaging == ws2.performStaging

    def test_signatures_subcollection(self, policy):
        coll = policy.signatures_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Signature)
