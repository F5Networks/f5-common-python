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

from f5.bigip.tm.asm.policies.signature_sets import Signature_Set
from requests.exceptions import HTTPError


class TestSignatureSets(object):
    def test_create_req_arg(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature}
        )
        assert ss1.kind == 'tm:asm:policies:signature-sets:signature-setstate'
        assert ss1.alarm is True
        assert ss1.learn is True
        ss1.delete()

    def test_create_optional_args(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature},
            alarm=False,
            learn=False
        )
        assert ss1.kind == 'tm:asm:policies:signature-sets:signature-setstate'
        assert ss1.alarm is False
        assert ss1.learn is False
        ss1.delete()

    def test_refresh(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature}
        )
        ss2 = policy.signature_sets_s.signature_set.load(id=ss1.id)
        assert ss1.kind == ss2.kind
        assert ss1.alarm == ss2.alarm
        assert ss1.learn == ss2.learn
        ss2.modify(alarm=False)
        assert ss1.alarm is True
        assert ss2.alarm is False
        ss1.refresh()
        assert ss1.alarm is False
        ss1.delete()

    def test_delete(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature}
        )
        idhash = str(ss1.id)
        ss1.delete()
        with pytest.raises(HTTPError) as err:
            policy.signature_sets_s.signature_set.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.signature_sets_s.signature_set.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, signature, policy):
        ss1 = policy.signature_sets_s.signature_set.create(
            signatureSetReference={'link': signature}
        )
        assert ss1.kind == 'tm:asm:policies:signature-sets:signature-setstate'
        assert ss1.alarm is True
        assert ss1.learn is True
        ss1.modify(alarm=False)
        assert ss1.alarm is False
        ss2 = policy.signature_sets_s.signature_set.load(id=ss1.id)
        assert ss1.selfLink == ss2.selfLink
        assert ss1.kind == ss2.kind
        assert ss1.alarm == ss2.alarm
        assert ss1.learn == ss2.learn
        ss1.delete()

    def test_signatureset_subcollection(self, policy):
        cc = policy.signature_sets_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Signature_Set)
