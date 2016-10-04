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
from f5.bigip.tm.asm.signature_sets import Signature_Set
import pytest
from requests.exceptions import HTTPError
from six import iteritems


def delete_sigset(mgmt_root, id):
    try:
        foo = mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=id)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def create_sigset(request, mgmt_root, name):
    def teardown():
        delete_sigset(mgmt_root, sig.id)

    sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
        name=name)
    request.addfinalizer(teardown)
    return sig


def set_create_test(request, mgmt_root, id):
    def teardown():
        delete_sigset(mgmt_root, id=id)
    request.addfinalizer(teardown)


class TestSignatureSets(object):
    def test_create_req_arg(self, request, mgmt_root):
        sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
            name='fake_sig')
        endpoint = str(sig.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signature-sets/'
        final_uri = base_uri + endpoint
        assert sig.name == 'fake_sig'
        assert sig.selfLink.startswith(final_uri)
        assert sig.defaultBlock is True
        assert sig.kind == 'tm:asm:signature-sets:signature-setstate'
        delete_sigset(mgmt_root, sig.id)

    def test_create_optional_args(self, request, mgmt_root):
        sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
            name='fake_sig', defaultBlock=False)
        endpoint = str(sig.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signature-sets/'
        final_uri = base_uri + endpoint
        assert sig.name == 'fake_sig'
        assert sig.selfLink.startswith(final_uri)
        assert sig.defaultBlock is False
        assert sig.kind == 'tm:asm:signature-sets:signature-setstate'
        delete_sigset(mgmt_root, sig.id)

    def test_create_duplicate(self, request, mgmt_root):
        create_sigset(request, mgmt_root, name='fake_sig')
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signature_sets_s.signature_set.create(
                name='fake_sig')
            assert err.response.status_code == 400

    def test_refresh(self, request, mgmt_root):
        sig1 = create_sigset(request, mgmt_root, name='fake_sig')
        sig2 = mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=sig1.id)
        assert sig1.id == sig2.id
        assert sig1.name == sig2.name
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
            mgmt_root.tm.asm.signature_sets_s.signature_set.load(
                id='Lx3553-321')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        sig1 = create_sigset(request, mgmt_root, name='fake_sig')
        sig2 = mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=sig1.id)
        assert sig1.id == sig2.id
        assert sig1.name == sig2.name
        assert sig1.selfLink == sig2.selfLink
        assert sig1.defaultBlock == sig2.defaultBlock
        sig2.modify(defaultBlock=False)
        assert sig1.id == sig2.id
        assert sig1.name == sig2.name
        assert sig1.selfLink == sig2.selfLink
        assert not sig1.defaultBlock == sig2.defaultBlock
        sig1.refresh()
        assert sig1.id == sig2.id
        assert sig1.name == sig2.name
        assert sig1.selfLink == sig2.selfLink
        assert sig1.defaultBlock == sig2.defaultBlock

    def test_delete(self, request, mgmt_root):
        sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
            name='fake_sig')
        hashid = str(sig.id)
        sig.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.signature_sets_s.signature_set.load(id=hashid)
            assert err.response.status_code == 404

    def test_modify(self, request, mgmt_root):
        sig = create_sigset(request, mgmt_root, name='fake_sig')
        meta_data = sig.__dict__.pop('_meta_data')
        start_dict = copy.deepcopy(sig.__dict__)
        sig.__dict__['_meta_data'] = meta_data
        sig.modify(defaultBlock=False)
        itm = 'defaultBlock'
        for k, v in iteritems(sig.__dict__):
            if k != itm:
                start_dict[k] = sig.__dict__[k]
                assert getattr(sig, k) == start_dict[k]
            elif k == itm:
                assert getattr(sig, itm) is False

    def test_signature_set_collection(self, request, mgmt_root):
        sig = mgmt_root.tm.asm.signature_sets_s.signature_set.create(
            name='fake_sig')
        endpoint = str(sig.id)
        base_uri = 'https://localhost/mgmt/tm/asm/signature-sets/'
        final_uri = base_uri + endpoint
        assert sig.name == 'fake_sig'
        assert sig.selfLink.startswith(final_uri)
        assert sig.defaultBlock is True
        assert sig.kind == 'tm:asm:signature-sets:signature-setstate'

        sc = mgmt_root.tm.asm.signature_sets_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Signature_Set)
        delete_sigset(mgmt_root, sig.id)
