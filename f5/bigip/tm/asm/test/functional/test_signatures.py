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

import fcntl
import os
import tempfile
import time
from f5.bigip.tm.asm.signatures import Signature
import pytest
from requests.exceptions import HTTPError


@pytest.fixture(scope='function')
def attack_id(mgmt_root):
    atckcoll = mgmt_root.tm.asm.attack_types_s.get_collection()
    # We obtain the ID for the resource to test and return the hashed id
    hashid = str(atckcoll[0].id)
    atck = mgmt_root.tm.asm.attack_types_s.attack_type.load(id=hashid)
    return atck.selfLink


@pytest.fixture(scope='function')
def sig_test(mgmt_root, attack_id):
    f = open('__lock__', 'w')
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError:
            time.sleep(1)

    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    sig1 = mgmt_root.tm.asm.signatures_s.signature.create(
        name=name,
        rule="content:\"ABC\"; depth:10;",
        attackTypeReference={
            'link': attack_id
        }
    )
    yield sig1
    sig1.delete()
    fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)
    f.close()


class TestSignature(object):
    def test_create_req_arg(self, attack_id, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        sig1 = mgmt_root.tm.asm.signatures_s.signature.create(
            name=name,
            rule="content:\"ABC\"; depth:10;",
            attackTypeReference={
                'link': attack_id
            }
        )
        endpoint = str(sig1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signatures/'
        final_uri = base_uri + endpoint
        assert sig1.name == name
        assert sig1.selfLink.startswith(final_uri)
        assert sig1.isUserDefined is True
        assert sig1.kind == 'tm:asm:signatures:signaturestate'
        sig1.delete()

    def test_create_optional_args(self, attack_id, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        sig1 = mgmt_root.tm.asm.signatures_s.signature.create(
            name=name,
            rule="content:\"ABC\"; depth:10;",
            attackTypeReference={
                'link': attack_id
            },
            signatureType='response'
        )
        endpoint = str(sig1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signatures/'
        final_uri = base_uri + endpoint
        assert sig1.selfLink.startswith(final_uri)
        assert sig1.isUserDefined is True
        assert sig1.kind == 'tm:asm:signatures:signaturestate'
        assert sig1.signatureType == 'response'
        sig1.delete()

    def test_refresh(self, sig_test, mgmt_root):
        sig1 = sig_test
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

    def test_delete(self, attack_id, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        sig1 = mgmt_root.tm.asm.signatures_s.signature.create(
            name=name,
            rule="content:\"ABC\"; depth:10;",
            attackTypeReference={
                'link': attack_id
            }
        )
        hash_id = str(sig1.id)
        sig1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signatures_s.signature.load(id=hash_id)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signatures_s.signature.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, mgmt_root, sig_test):
        sig1 = sig_test
        endpoint = str(sig1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signatures/'
        final_uri = base_uri + endpoint
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
    def test_signature_collection(self, sig_test, mgmt_root):
        # As ASM has predefined items, there is no need to create one
        # However this test might be an issue as the returned json is quite
        # large.
        sc = mgmt_root.tm.asm.signatures_s.get_collection(
            requests_params={'params': '$top=2'}
        )
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Signature)
