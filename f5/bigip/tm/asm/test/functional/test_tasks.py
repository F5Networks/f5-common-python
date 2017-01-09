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


import pytest
import time

from f5.bigip.tm.asm.tasks import Check_Signature
from f5.bigip.tm.asm.tasks import Export_Signature
from f5.bigip.tm.asm.tasks import Update_Signature

from requests.exceptions import HTTPError


def delete_chksig_item(mgmt_root, id):
    try:
        foo = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature\
            .load(id=id)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def set_chksig_test(request, mgmt_root):
    def teardown():
        delete_chksig_item(mgmt_root, t1.id)
    t1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
    request.addfinalizer(teardown)
    return t1


def delete_updsig_item(mgmt_root, id):
    try:
        foo = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature\
            .load(id=id)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def set_updsig_test(request, mgmt_root):
    def teardown():
        delete_updsig_item(mgmt_root, t1.id)
    t1 = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.fetch()
    request.addfinalizer(teardown)
    return t1


def delete_export_item(request, mgmt_root, id):
    try:
        foo = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(
            id=id)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def set_export_basic_test(request, mgmt_root, filename):
    def teardown():
        delete_export_item(request, mgmt_root, exp1.id)
    exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
        .create(filename=filename)
    request.addfinalizer(teardown)
    return exp1


class TestCheckSignature(object):
    def test_fetch(self, request, mgmt_root):
        chk1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature\
            .fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/check-signatures/'
        final_uri = base_uri+endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status == 'NEW'
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == \
            'tm:asm:tasks:check-signatures:check-signatures-taskstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.load(
                id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        chk1 = set_chksig_test(request, mgmt_root)
        hashid = str(chk1.id)
        t1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.load(
            id=hashid)
        assert t1.id == chk1.id
        assert t1.selfLink == chk1.selfLink

    def test_exists(self, request, mgmt_root):
        chk1 = set_chksig_test(request, mgmt_root)
        hashid = str(chk1.id)
        assert chk1.exists(id=hashid)

    def test_refresh(self, request, mgmt_root):
        chk1 = set_chksig_test(request, mgmt_root)
        hashid = str(chk1.id)
        link = chk1.selfLink
        chk1.refresh()
        assert chk1.id == hashid
        assert chk1.selfLink == link

    def test_delete(self, request, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        chk1.delete()
        assert chk1.__dict__['deleted']

    def test_signature_update_collection(self, request, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/check-signatures/'
        final_uri = base_uri+endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status == 'NEW'
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == \
            'tm:asm:tasks:check-signatures:check-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.check_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Check_Signature)


class TestExportSignature(object):
    def test_create_req_arg(self, request, mgmt_root):
        f = 'fake_export.xml'
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .create(filename=f)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == f
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert exp1.inline is False

    def test_create_optional_args(self, request, mgmt_root):
        f = 'fake_export.xml'
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature \
            .create(filename=f, inline=True)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == f
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert exp1.inline is True

    def test_refresh(self, request, mgmt_root):
        f = 'fake_export.xml'
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .create(filename=f)
        exp2 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink
        exp1.refresh()
        assert exp1.selfLink == exp2.selfLink

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_signatures_s.export_signature \
                .load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        f = 'fake_export.xml'
        exp1 = set_export_basic_test(request, mgmt_root, f)
        exp2 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature \
            .load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink

    def test_delete(self, request, mgmt_root):
        f = 'fake_export.xml'
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .create(filename=f)
        hashid = str(exp1.id)
        exp1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(
                id=hashid)
        assert err.value.response.status_code == 404

    def test_signature_export_collection(self, request, mgmt_root):
        f = 'fake_export.xml'
        exp1 = set_export_basic_test(request, mgmt_root, f)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == f
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.export_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Export_Signature)


class TestUpdateSignature(object):
    def test_fetch(self, request, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/update-signatures/'
        final_uri = base_uri+endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status == 'NEW'
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == \
            'tm:asm:tasks:update-signatures:update-signatures-taskstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.load(
                id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        chk1 = set_updsig_test(request, mgmt_root)
        hashid = str(chk1.id)
        time.sleep(6)
        t1 = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.load(
            id=hashid)
        assert t1.id == chk1.id
        assert t1.selfLink == chk1.selfLink

    def test_exists(self, request, mgmt_root):
        chk1 = set_updsig_test(request, mgmt_root)
        hashid = str(chk1.id)
        assert chk1.exists(id=hashid)

    def test_refresh(self, request, mgmt_root):
        chk1 = set_updsig_test(request, mgmt_root)
        hashid = str(chk1.id)
        link = chk1.selfLink
        chk1.refresh()
        assert chk1.id == hashid
        assert chk1.selfLink == link

    def test_delete(self, request, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        chk1.delete()
        assert chk1.__dict__['deleted']

    def test_signature_update_collection(self, request, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/update-signatures/'
        final_uri = base_uri+endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status == 'NEW'
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == \
            'tm:asm:tasks:update-signatures:update-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.update_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Update_Signature)
