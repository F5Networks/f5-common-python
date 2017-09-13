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

import os
import pytest
import tempfile

from f5.bigip.tm.asm.signature_sets import Signature_Set
from requests.exceptions import HTTPError


class TestSignatureSets(object):
    def test_create_req_arg(self, sigset):
        endpoint = str(sigset.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signature-sets/'
        final_uri = base_uri + endpoint
        assert sigset.selfLink.startswith(final_uri)
        assert sigset.defaultBlock is True
        assert sigset.kind == 'tm:asm:signature-sets:signature-setstate'

    def test_create_optional_args(self, sigset2):
        endpoint = str(sigset2.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signature-sets/'
        final_uri = base_uri + endpoint
        assert sigset2.selfLink.startswith(final_uri)
        assert sigset2.defaultBlock is False
        assert sigset2.kind == 'tm:asm:signature-sets:signature-setstate'

    def test_create_duplicate(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        foo = mgmt_root.tm.asm.signature_sets_s.signature_set.create(name=name)
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signature_sets_s.signature_set.create(name=name)
        assert err.value.response.status_code == 400
        foo.delete()

    def test_refresh(self, mgmt_root, sigset):
        sig1 = sigset
        sig2 = mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=sig1.id)
        assert sig1.id == sig2.id
        assert sig1.selfLink == sig2.selfLink
        assert sig1.defaultBlock is True
        assert sig2.defaultBlock is True
        sig1.modify(defaultBlock=False)
        assert sig1.defaultBlock is False
        assert sig2.defaultBlock is True
        sig2.refresh()
        assert sig2.defaultBlock is False

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signature_sets_s.signature_set.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, mgmt_root, sigset):
        sig1 = sigset
        sig2 = mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=sig1.id)
        assert sig1.id == sig2.id
        assert sig1.selfLink == sig2.selfLink
        assert sig1.defaultBlock == sig2.defaultBlock
        sig2.modify(defaultBlock=False)
        assert sig1.id == sig2.id
        assert sig1.name == sig2.name
        assert sig1.selfLink == sig2.selfLink
        assert not sig1.defaultBlock == sig2.defaultBlock
        sig1.refresh()
        assert sig1.id == sig2.id
        assert sig1.selfLink == sig2.selfLink
        assert sig1.defaultBlock == sig2.defaultBlock

    def test_delete(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
            name=name
        )
        hashid = str(sig.id)
        sig.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=hashid)
        assert err.value.response.status_code == 404

    def test_signature_set_collection(self, mgmt_root, sigset):
        endpoint = str(sigset.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signature-sets/'
        final_uri = base_uri + endpoint
        assert sigset.selfLink.startswith(final_uri)
        assert sigset.defaultBlock is True
        assert sigset.kind == 'tm:asm:signature-sets:signature-setstate'

        sc = mgmt_root.tm.asm.signature_sets_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Signature_Set)
