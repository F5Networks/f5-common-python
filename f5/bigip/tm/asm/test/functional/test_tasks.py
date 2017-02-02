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

from f5.bigip.tm.asm.tasks import Apply_Policy
from f5.bigip.tm.asm.tasks import Check_Signature
from f5.bigip.tm.asm.tasks import Export_Policy
from f5.bigip.tm.asm.tasks import Export_Signature
from f5.bigip.tm.asm.tasks import Import_Policy
from f5.bigip.tm.asm.tasks import Update_Signature

from requests.exceptions import HTTPError


F = 'fake_export.xml'


def delete_chksig_item(mgmt_root, hashid):
    try:
        foo = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature\
            .load(id=hashid)
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


def delete_updsig_item(mgmt_root, hashid):
    try:
        foo = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature\
            .load(id=hashid)
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


def delete_export_item(mgmt_root, hashid):
    try:
        foo = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(
            id=hashid)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def set_export_basic_test(request, mgmt_root, filename):
    def teardown():
        delete_export_item(mgmt_root, exp1.id)
    exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
        .create(filename=filename)
    request.addfinalizer(teardown)
    return exp1


def delete_policy_item(mgmt_root):
    col = mgmt_root.tm.asm.policies_s.get_collection()
    if len(col) > 0:
        for i in col:
            i.delete()


@pytest.fixture(scope='class')
def set_policy(mgmt_root):
    pol1 = \
        mgmt_root.tm.asm.policies_s.policy.create(
            name='fake_policy')
    yield pol1.selfLink
    delete_policy_item(mgmt_root)


def delete_apply_policy_task(mgmt_root):
    col = mgmt_root.tm.asm.tasks.apply_policy_s.get_collection()
    if len(col) > 0:
        for i in col:
            i.delete()


def set_apply_policy(request, mgmt_root, reference):
    def teardown():
        delete_apply_policy_task(mgmt_root)
    ap = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.create(
        policyReference=reference)
    request.addfinalizer(teardown)
    return ap


def delete_export_policy(mgmt_root):
    col = mgmt_root.tm.asm.tasks.export_policy_s.get_collection()
    if len(col) > 0:
        for i in col:
            i.delete()


def set_export_policy_test(request, mgmt_root, reference):
    def teardown():
        delete_export_policy(mgmt_root)

    exp1 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy \
        .create(filename=F, policyReference=reference)
    request.addfinalizer(teardown)
    return exp1


def delete_import_policy(mgmt_root):
    col = mgmt_root.tm.asm.tasks.import_policy_s.get_collection()
    if len(col) > 0:
        for i in col:
            i.delete()


def set_import_policy_test(request, mgmt_root, name):
    def teardown():
        delete_import_policy(mgmt_root)

    exp1 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy \
        .create(filename=F, name=name)
    request.addfinalizer(teardown)
    return exp1


class TestApplyPolicy(object):
    def test_create_req_arg(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        ap = set_apply_policy(request, mgmt_root, reference)
        assert ap.status == 'NEW'
        assert ap.kind == 'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        assert ap.policyReference == reference
        delete_apply_policy_task(mgmt_root)

    def test_refresh(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        ap = set_apply_policy(request, mgmt_root, reference)
        hashid = str(ap.id)
        link = ap.selfLink
        ap.refresh()
        assert ap.kind == 'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        assert ap.policyReference == reference
        assert ap.id == hashid
        assert ap.selfLink == link

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.load(
                id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        ap = set_apply_policy(request, mgmt_root, reference)
        ap2 = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.load(id=ap.id)
        assert ap.id == ap2.id
        assert ap.selfLink == ap2.selfLink
        assert ap.policyReference == ap2.policyReference

    def test_exists(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        ap = set_apply_policy(request, mgmt_root, reference)
        hashid = str(ap.id)
        assert ap.exists(id=hashid)

    def test_delete(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        ap = set_apply_policy(request, mgmt_root, reference)
        ap.delete()
        assert ap.__dict__['deleted']

    def test_apply_policy_collection(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        ap = set_apply_policy(request, mgmt_root, reference)
        assert ap.status == 'NEW'
        assert ap.kind == 'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        assert ap.policyReference == reference

        col = mgmt_root.tm.asm.tasks.apply_policy_s.get_collection()
        assert isinstance(col, list)
        assert len(col)
        assert isinstance(col[0], Apply_Policy)


class TestExportPolicy(object):
    def test_create_req_arg(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        exp1 = set_export_policy_test(request, mgmt_root, reference)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri+endpoint
        assert exp1.filename == F
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is False

    def test_create_optional_args(self, mgmt_root, set_policy):
        reference = {'link': set_policy}
        exp1 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy\
            .create(filename=F, policyReference=reference, inline=True)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri+endpoint
        assert exp1.filename == F
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is True

    def test_refresh(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        exp1 = set_export_policy_test(request, mgmt_root, reference)
        exp2 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy\
            .load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink
        exp1.refresh()
        assert exp1.selfLink == exp2.selfLink

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_policy_s.export_policy \
                .load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        exp1 = set_export_policy_test(request, mgmt_root, reference)
        exp2 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy\
            .load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink

    def test_delete(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        exp1 = set_export_policy_test(request, mgmt_root, reference)
        hashid = str(exp1.id)
        exp1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_policy_s.export_policy.load(
                id=hashid)
        assert err.value.response.status_code == 404

    def test_policy_export_collection(self, request, mgmt_root, set_policy):
        reference = {'link': set_policy}
        exp1 = set_export_policy_test(request, mgmt_root, reference)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri+endpoint
        assert exp1.filename == F
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is False

        sc = mgmt_root.tm.asm.tasks.export_policy_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Export_Policy)


class TestImportPolicy(object):
    def test_create_req_arg(self, request, mgmt_root):
        imp1 = set_import_policy_test(request, mgmt_root, 'fake_one')
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri+endpoint
        assert imp1.filename == F
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'NEW'
        assert imp1.kind == \
            'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is False

    def test_create_optional_args(self, mgmt_root):
        imp1 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy\
            .create(filename=F, isBase64=True, name='fake_one')
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri+endpoint
        assert imp1.filename == F
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'NEW'
        assert imp1.kind == \
            'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is True

    def test_refresh(self, request, mgmt_root):
        imp1 = set_import_policy_test(request, mgmt_root, 'fake_one')
        imp2 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy\
            .load(id=imp1.id)
        assert imp1.selfLink == imp2.selfLink
        imp1.refresh()
        assert imp1.selfLink == imp2.selfLink

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.import_policy_s.import_policy \
                .load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        imp1 = set_import_policy_test(request, mgmt_root, 'fake_one')
        imp2 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy\
            .load(id=imp1.id)
        assert imp1.selfLink == imp2.selfLink

    def test_delete(self, request, mgmt_root):
        imp1 = set_import_policy_test(request, mgmt_root, 'fake_one')
        hashid = str(imp1.id)
        imp1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.import_policy_s.import_policy.load(
                id=hashid)
        assert err.value.response.status_code == 404

    def test_policy_import_collection(self, request, mgmt_root):
        imp1 = set_import_policy_test(request, mgmt_root, 'fake_one')
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri+endpoint
        assert imp1.filename == F
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'NEW'
        assert imp1.kind == \
            'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is False

        sc = mgmt_root.tm.asm.tasks.import_policy_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Import_Policy)


class TestCheckSignature(object):
    def test_fetch(self, mgmt_root):
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

    def test_delete(self, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        chk1.delete()
        assert chk1.__dict__['deleted']

    def test_signature_update_collection(self, mgmt_root):
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
    def test_create_req_arg(self, mgmt_root):
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .create(filename=F)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == F
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert exp1.inline is False

    def test_create_optional_args(self, mgmt_root):
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature \
            .create(filename=F, inline=True)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == F
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert exp1.inline is True

    def test_refresh(self, mgmt_root):
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .create(filename=F)
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
        exp1 = set_export_basic_test(request, mgmt_root, F)
        exp2 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature \
            .load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink

    def test_delete(self, mgmt_root):
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature\
            .create(filename=F)
        hashid = str(exp1.id)
        exp1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(
                id=hashid)
        assert err.value.response.status_code == 404

    def test_signature_export_collection(self, request, mgmt_root):
        exp1 = set_export_basic_test(request, mgmt_root, F)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == F
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == \
            'tm:asm:tasks:export-signatures:export-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.export_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Export_Signature)


class TestUpdateSignature(object):
    def test_fetch(self, mgmt_root):
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
            assert err.response.status_code == 404

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

    def test_delete(self, mgmt_root):
        chk1 = \
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        chk1.delete()
        assert chk1.__dict__['deleted']

    def test_signature_update_collection(self, mgmt_root):
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
