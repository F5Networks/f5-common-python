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

import copy
from f5.bigip.tm.asm.signatures import Signature
import pytest
from requests.exceptions import HTTPError
from six import iteritems


def delete_signature_item(request, mgmt_root, id):
    try:
        foo = mgmt_root.tm.asm.signatures_s.signature.load(
            id=id)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def get_atckid(request, mgmt_root):
    atckcoll = mgmt_root.tm.asm.attack_types_s.get_collection()
    # We obtain the ID for the resource to test and return the hashed id
    hashid = str(atckcoll[0].id)
    atck = mgmt_root.tm.asm.attack_types_s.attack_type.load(id=hashid)
    return atck.selfLink


def set_sig_test(request, mgmt_root, name, rule, atck, **kwargs):
    def teardown():
        delete_signature_item(request, mgmt_root, sig1.id)
    sig1 = \
        mgmt_root.tm.asm.signatures_s.signature.create(
            name=name, rule=rule, attackTypeReference=atck, **kwargs)
    request.addfinalizer(teardown)
    return sig1


class TestSignature(object):
    def test_create_req_arg(self, request, mgmt_root):
        rule = "content:\"ABC\"; depth:10;"
        lnk = get_atckid(request, mgmt_root)
        atck = {'link': lnk}
        sig1 = \
            mgmt_root.tm.asm.signatures_s.signature.create(
                name='fake_sigs', rule=rule, attackTypeReference=atck)
        endpoint = str(sig1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signatures/'
        final_uri = base_uri+endpoint
        assert sig1.name == 'fake_sigs'
        assert sig1.selfLink.startswith(final_uri)
        assert sig1.isUserDefined is True
        assert sig1.kind == 'tm:asm:signatures:signaturestate'
        delete_signature_item(request, mgmt_root, endpoint)

    def test_create_optional_args(self, request, mgmt_root):
        rule = "content:\"ABC\"; depth:10;"
        lnk = get_atckid(request, mgmt_root)
        atck = {'link': lnk}
        sig1 = \
            mgmt_root.tm.asm.signatures_s.signature.create(
                name='fake_sigs', rule=rule, attackTypeReference=atck,
                signatureType='response')
        endpoint = str(sig1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signatures/'
        final_uri = base_uri+endpoint
        assert sig1.name == 'fake_sigs'
        assert sig1.selfLink.startswith(final_uri)
        assert sig1.isUserDefined is True
        assert sig1.kind == 'tm:asm:signatures:signaturestate'
        assert sig1.signatureType == 'response'
        delete_signature_item(request, mgmt_root, endpoint)

    def test_refresh(self, request, mgmt_root):
        rule = "content:\"ABC\"; depth:10;"
        lnk = get_atckid(request, mgmt_root)
        atck = {'link': lnk}
        sig1 = set_sig_test(request, mgmt_root, 'fake_sigs', rule, atck)
        sig2 = mgmt_root.tm.asm.signatures_s.signature.load(id=sig1.id)
        assert sig1.name == sig2.name
        assert sig1.selfLink == sig2.selfLink
        assert sig1.kind == sig2.kind
        assert sig1.signatureType == sig2.signatureType
        assert sig1.isUserDefined == sig2.isUserDefined
        sig2.modify(signatureType='response')
        assert sig1.selfLink == sig2.selfLink
        assert sig1.signatureType != sig2.signatureType
        sig1.refresh()
        assert sig1.signatureType == sig2.signatureType

    def test_modify(self, request, mgmt_root):
        rule = "content:\"ABC\"; depth:10;"
        lnk = get_atckid(request, mgmt_root)
        atck = {'link': lnk}
        sig1 = set_sig_test(request, mgmt_root, 'fake_sigs', rule, atck)
        original_dict = copy.copy(sig1.__dict__)
        itm = 'signatureType'
        sig1.modify(signatureType='response')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = sig1.__dict__[k]
            elif k == itm:
                assert sig1.__dict__[k] == 'response'

    def test_delete(self, request, mgmt_root):
        rule = "content:\"ABC\"; depth:10;"
        lnk = get_atckid(request, mgmt_root)
        atck = {'link': lnk}
        sig1 = mgmt_root.tm.asm.signatures_s.signature.create(
            name='fake_sigs', rule=rule, attackTypeReference=atck)
        idhash = str(sig1.id)
        sig1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signatures_s.signature.load(id=idhash)
            assert err.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signatures_s.signature.load(id='Lx3553-321')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        rule = "content:\"ABC\"; depth:10;"
        lnk = get_atckid(request, mgmt_root)
        atck = {'link': lnk}
        sig1 = set_sig_test(request, mgmt_root, 'fake_sigs', rule, atck)
        endpoint = str(sig1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signatures/'
        final_uri = base_uri+endpoint
        assert sig1.name == 'fake_sigs'
        assert sig1.selfLink.startswith(final_uri)
        assert sig1.isUserDefined is True
        assert sig1.kind == 'tm:asm:signatures:signaturestate'
        sig1.modify(signatureType='response')
        assert sig1.signatureType == 'response'
        sig2 = mgmt_root.tm.asm.signatures_s.signature.load(id=sig1.id)
        assert sig1.name == sig2.name
        assert sig1.selfLink == sig2.selfLink
        assert sig1.signatureType == sig2.signatureType


class TestSignaturesCollection(object):
    def test_signature_collection(self, request, mgmt_root):
        # As ASM has predefined items, there is no need to create one
        # However this test might be an issue as the returned json is quite
        # large.
        sc = mgmt_root.tm.asm.signatures_s.get_collection(
            requests_params={'params': '$top=2'})
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Signature)
