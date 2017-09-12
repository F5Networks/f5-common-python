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
import time

from distutils.version import LooseVersion
from f5.bigip.tm.asm.tasks import Apply_Policy
from f5.bigip.tm.asm.tasks import Check_Signature
from f5.bigip.tm.asm.tasks import Export_Policy
from f5.bigip.tm.asm.tasks import Export_Signature
from f5.bigip.tm.asm.tasks import Import_Policy
from f5.bigip.tm.asm.tasks import Import_Vulnerabilities
from f5.bigip.tm.asm.tasks import Update_Signature
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation
from jinja2 import Environment
from jinja2 import FileSystemLoader
from requests.exceptions import HTTPError


if LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('12.1.0'):
    SCAN = 'trustwave'
else:
    SCAN = 'cenzic-hailstorm'

F = ''


def file_read():
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    dirpath = os.path.dirname(__file__)
    path = os.path.join(dirpath, 'test_files')
    loader = FileSystemLoader(path)
    env = Environment(
        loader=loader
    )
    template = env.get_template('fake_policy.xml')
    result = template.render(fake_policy=name)
    return result


@pytest.fixture(scope='function')
def check_sig(mgmt_root):
    task = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def update_sig(mgmt_root):
    task = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.fetch()
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def export_basic(mgmt_root):
    task = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.create(
        filename='fake_export.xml'
    )
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def set_policy(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    pol1 = mgmt_root.tm.asm.policies_s.policy.create(
        name=name
    )
    pol1.vulnerability_assessment.modify(scannerType=SCAN)
    yield pol1.selfLink


@pytest.fixture(scope='function')
def set_policy2(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    pol1 = mgmt_root.tm.asm.policies_s.policy.create(
        name=name
    )
    yield pol1.selfLink
    pol1.delete()


@pytest.fixture(scope='function')
def apply_policy(mgmt_root, set_policy2):
    reference = {'link': set_policy2}
    task = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.create(
        policyReference=reference
    )
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def export_policy(mgmt_root, set_policy2):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)

    reference = {'link': set_policy2}
    exp1 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy.create(
        filename=name + '.xml',
        policyReference=reference
    )
    while True:
        exp1.refresh()
        if exp1.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield exp1
    exp1.delete()


@pytest.fixture(scope='function')
def export_policy_inline(mgmt_root, set_policy2):
    reference = {'link': set_policy2}
    exp1 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy.create(
        inline=True,
        policyReference=reference
    )
    while True:
        exp1.refresh()
        if exp1.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield exp1
    exp1.delete()


@pytest.fixture(scope='function')
def import_policy_base64(mgmt_root):
    content = file_read()
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    task = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.create(
        file=content,
        name=name,
        isBase64=True
    )
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def import_policy_template(mgmt_root):
    tmpl = mgmt_root.tm.asm.policy_templates_s.get_collection()
    link = {'link': tmpl[0].selfLink}
    f = tempfile.NamedTemporaryFile()
    name = os.path.basename(f.name)
    task = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.create(
        policyTemplateReference=link,
        name=name,
    )
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def import_policy(mgmt_root):
    content = file_read()
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    task = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.create(
        file=content,
        name=name
    )
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def import_vuln(mgmt_root, set_policy):
    reference = {'link': set_policy}
    imports = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
    content = file_read()
    file = tempfile.NamedTemporaryFile()
    fh = open(file.name, 'w')
    fh.write(content)
    fh.close()
    mgmt_root.tm.asm.file_transfer.uploads.upload_file(file.name)
    task = imports.import_vulnerabilities.create(
        filename=file.name,
        policyReference=reference,
        importAllDomainNames=True
    )
    while True:
        task.refresh()
        if task.status in ['COMPLETED', 'FAILURE']:
            break
        time.sleep(1)
    yield task
    task.delete()


class TestApplyPolicy(object):
    def test_create_req_arg(self, apply_policy, set_policy2):
        reference = {'link': set_policy2}
        ap = apply_policy
        assert ap.status == 'COMPLETED'
        assert ap.kind == 'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        assert ap.policyReference == reference

    def test_refresh(self, apply_policy, set_policy2):
        reference = {'link': set_policy2}
        ap = apply_policy
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

    def test_load(self, apply_policy, mgmt_root):
        ap = apply_policy
        ap2 = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.load(id=ap.id)
        assert ap.id == ap2.id
        assert ap.selfLink == ap2.selfLink
        assert ap.policyReference == ap2.policyReference

    def test_exists(self, apply_policy):
        ap = apply_policy
        hashid = str(ap.id)
        assert ap.exists(id=hashid)

    def test_delete(self, mgmt_root, set_policy2):
        reference = {'link': set_policy2}
        task = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.create(
            policyReference=reference
        )
        while True:
            task.refresh()
            if task.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        task.delete()
        assert task.__dict__['deleted']

    def test_apply_policy_collection(self, mgmt_root, apply_policy, set_policy2):
        reference = {'link': set_policy2}
        ap = apply_policy
        assert ap.status == 'COMPLETED'
        assert ap.kind == 'tm:asm:tasks:apply-policy:apply-policy-taskstate'
        assert ap.policyReference == reference

        col = mgmt_root.tm.asm.tasks.apply_policy_s.get_collection()
        assert isinstance(col, list)
        assert len(col)
        assert isinstance(col[0], Apply_Policy)


class TestExportPolicy(object):
    def test_create_req_arg(self, export_policy):
        exp1 = export_policy
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri+endpoint
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'COMPLETED'
        assert exp1.kind == 'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is False

    def test_create_inline_export(self, export_policy_inline):
        exp1 = export_policy_inline
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri+endpoint
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.kind == 'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is True

    def test_create_optional_args(self, mgmt_root, set_policy2):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        reference = {'link': set_policy2}
        exp1 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy.create(
            filename=name + '.xml',
            policyReference=reference,
            inline=True
        )
        while True:
            exp1.refresh()
            if exp1.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri + endpoint
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'COMPLETED'
        assert exp1.kind == 'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is True

    def test_refresh(self, export_policy, mgmt_root):
        exp1 = export_policy
        exp2 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy.load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink
        exp1.refresh()
        assert exp1.selfLink == exp2.selfLink

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_policy_s.export_policy.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, export_policy, mgmt_root):
        exp1 = export_policy
        exp2 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy.load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink

    def test_delete(self, mgmt_root, set_policy2):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)

        reference = {'link': set_policy2}
        exp1 = mgmt_root.tm.asm.tasks.export_policy_s.export_policy.create(
            filename=name + '.xml',
            policyReference=reference
        )
        while True:
            exp1.refresh()
            if exp1.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        hashid = str(exp1.id)
        exp1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_policy_s.export_policy.load(id=hashid)
        assert err.value.response.status_code == 404

    def test_policy_export_collection(self, export_policy, mgmt_root):
        exp1 = export_policy
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-policy/'
        final_uri = base_uri + endpoint
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'COMPLETED'
        assert exp1.kind == 'tm:asm:tasks:export-policy:export-policy-taskstate'
        assert exp1.inline is False

        sc = mgmt_root.tm.asm.tasks.export_policy_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Export_Policy)


class TestImportPolicy(object):
    def test_create_req_arg(self, import_policy):
        imp1 = import_policy
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri + endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'COMPLETED'
        assert imp1.kind == 'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is False

    def test_create_import_template(self, import_policy_template):
        imp1 = import_policy_template
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri + endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.kind == 'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is False

    def test_create_import_fails(self, import_policy_base64):
        imp1 = import_policy_base64
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri + endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.kind == 'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.status == 'FAILURE'

    def test_create_optional_args(self, mgmt_root):
        content = file_read()
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        imp1 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.create(
            file=content,
            isBase64=True,
            name=name
        )
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri+endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'NEW'
        assert imp1.kind == 'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is True

    def test_refresh(self, import_policy, mgmt_root):
        imp1 = import_policy
        imp2 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.load(id=imp1.id)
        assert imp1.selfLink == imp2.selfLink
        imp1.refresh()
        assert imp1.selfLink == imp2.selfLink

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.import_policy_s.import_policy.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, import_policy, mgmt_root):
        imp1 = import_policy
        imp2 = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.load(id=imp1.id)
        assert imp1.selfLink == imp2.selfLink

    def test_delete(self, mgmt_root):
        content = file_read()
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        task = mgmt_root.tm.asm.tasks.import_policy_s.import_policy.create(
            file=content,
            name=name
        )
        while True:
            task.refresh()
            if task.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        hash_id = task.id
        task.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.import_policy_s.import_policy.load(
                id=hash_id
            )
        assert err.value.response.status_code == 404

    def test_policy_import_collection(self, import_policy, mgmt_root):
        imp1 = import_policy
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-policy/'
        final_uri = base_uri+endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'COMPLETED'
        assert imp1.kind == 'tm:asm:tasks:import-policy:import-policy-taskstate'
        assert imp1.isBase64 is False

        sc = mgmt_root.tm.asm.tasks.import_policy_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Import_Policy)


class TestCheckSignature(object):
    def test_fetch(self, mgmt_root):
        chk1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/check-signatures/'
        final_uri = base_uri + endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status == 'NEW'
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == 'tm:asm:tasks:check-signatures:check-signatures-taskstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.load(
                id='Lx3553-321'
            )
        assert err.value.response.status_code == 404

    def test_load(self, check_sig, mgmt_root):
        chk1 = check_sig
        hashid = str(chk1.id)
        t1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.load(id=hashid)
        assert t1.id == chk1.id
        assert t1.selfLink == chk1.selfLink

    def test_exists(self, check_sig):
        chk1 = check_sig
        hashid = str(chk1.id)
        assert chk1.exists(id=hashid)

    def test_refresh(self, check_sig):
        chk1 = check_sig
        hashid = str(chk1.id)
        link = chk1.selfLink
        chk1.refresh()
        assert chk1.id == hashid
        assert chk1.selfLink == link

    def test_delete(self, mgmt_root):
        task = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        while True:
            task.refresh()
            if task.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        task.delete()
        assert task.__dict__['deleted']

    def test_signature_update_collection(self, mgmt_root):
        chk1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/check-signatures/'
        final_uri = base_uri+endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status == 'NEW'
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == 'tm:asm:tasks:check-signatures:check-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.check_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Check_Signature)


class TestExportSignature(object):
    def test_create_req_arg(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.create(
            filename=name + '.xml'
        )
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri+endpoint
        assert exp1.filename == name + '.xml'
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == 'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert exp1.inline is False

    def test_create_optional_args(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.create(
            filename=name + '.xml',
            inline=True
        )
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri + endpoint
        assert exp1.filename == name + '.xml'
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'NEW'
        assert exp1.kind == 'tm:asm:tasks:export-signatures:export-signatures-taskstate'
        assert exp1.inline is True

    def test_refresh(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.create(
            filename=name + '.xml'
        )
        exp2 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink
        exp1.refresh()
        assert exp1.selfLink == exp2.selfLink

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, export_basic, mgmt_root):
        exp1 = export_basic
        exp2 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(id=exp1.id)
        assert exp1.selfLink == exp2.selfLink

    def test_delete(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        exp1 = mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.create(
            filename=name + '.xml'
        )
        hashid = str(exp1.id)
        exp1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.export_signatures_s.export_signature.load(
                id=hashid
            )
        assert err.value.response.status_code == 404

    def test_signature_export_collection(self, export_basic, mgmt_root):
        exp1 = export_basic
        endpoint = str(exp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/export-signatures/'
        final_uri = base_uri + endpoint
        assert exp1.selfLink.startswith(final_uri)
        assert exp1.status == 'COMPLETED'
        assert exp1.kind == 'tm:asm:tasks:export-signatures:export-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.export_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Export_Signature)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='This collection is completely broken on 11.6.0.'
)
class TestUpdateSignature(object):
    def test_fetch(self, mgmt_root):
        chk1 = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/update-signatures/'
        final_uri = base_uri+endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status in ['COMPLETED', 'NEW']
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == 'tm:asm:tasks:update-signatures:update-signatures-taskstate'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.load(
                id='Lx3553-321'
            )
            assert err.response.status_code == 404

    def test_load(self, update_sig, mgmt_root):
        chk1 = update_sig
        hashid = str(chk1.id)
        time.sleep(6)
        t1 = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.load(id=hashid)
        assert t1.id == chk1.id
        assert t1.selfLink == chk1.selfLink

    def test_exists(self, update_sig):
        chk1 = update_sig
        hashid = str(chk1.id)
        assert chk1.exists(id=hashid)

    def test_refresh(self, update_sig):
        chk1 = update_sig
        hashid = str(chk1.id)
        link = chk1.selfLink
        chk1.refresh()
        assert chk1.id == hashid
        assert chk1.selfLink == link

    def test_delete(self, mgmt_root):
        chk1 = mgmt_root.tm.asm.tasks.check_signatures_s.check_signature.fetch()
        chk1.delete()
        assert chk1.__dict__['deleted']

    def test_signature_update_collection(self, mgmt_root):
        chk1 = mgmt_root.tm.asm.tasks.update_signatures_s.update_signature.fetch()
        endpoint = str(chk1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/update-signatures/'
        final_uri = base_uri + endpoint
        assert hasattr(chk1, 'id')
        assert hasattr(chk1, 'status')
        assert hasattr(chk1, 'selfLink')
        assert not hasattr(chk1, 'generation')
        assert chk1.status in ['COMPLETED', 'NEW']
        assert chk1.selfLink.startswith(final_uri)
        assert chk1.kind == 'tm:asm:tasks:update-signatures:update-signatures-taskstate'

        sc = mgmt_root.tm.asm.tasks.update_signatures_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Update_Signature)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestImportVulnerabilities(object):
    def test_modify_raises(self, mgmt_root):
        rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        with pytest.raises(UnsupportedOperation):
            rc.import_vulnerabilities.modify()

    def test_create_mandatory_arg_missing(self, mgmt_root, set_policy):
        reference = {'link': set_policy}
        rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        content = file_read()
        file = tempfile.NamedTemporaryFile()
        fh = open(file.name, 'w')
        fh.write(content)
        fh.close()
        with pytest.raises(MissingRequiredCreationParameter) as err:
            rc.import_vulnerabilities.create(
                filename=file.name,
                policyReference=reference
            )
        assert 'This resource requires at least one of the' in str(err.value)

    def test_create_req_arg(self, import_vuln):
        imp1 = import_vuln
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-vulnerabilities/'
        final_uri = base_uri + endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'COMPLETED'
        assert imp1.kind == 'tm:asm:tasks:import-vulnerabilities:import-vulnerabilities-taskstate'
        assert imp1.importAllDomainNames is True

    def test_refresh(self, import_vuln, mgmt_root):
        rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        imp1 = import_vuln
        imp2 = rc.import_vulnerabilities.load(id=imp1.id)
        assert imp1.selfLink == imp2.selfLink
        assert imp1.importAllDomainNames == imp2.importAllDomainNames
        imp1.refresh()
        assert imp1.selfLink == imp2.selfLink
        assert imp1.importAllDomainNames == imp2.importAllDomainNames

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        with pytest.raises(HTTPError) as err:
            rc.import_vulnerabilities.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, mgmt_root, import_vuln):
        rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        imp1 = import_vuln
        imp2 = rc.import_vulnerabilities.load(id=imp1.id)
        assert imp1.selfLink == imp2.selfLink
        assert imp1.importAllDomainNames == imp2.importAllDomainNames

    def test_delete(self, mgmt_root, set_policy):
        reference = {'link': set_policy}
        imports = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        content = file_read()
        file = tempfile.NamedTemporaryFile()
        fh = open(file.name, 'w')
        fh.write(content)
        fh.close()
        mgmt_root.tm.asm.file_transfer.uploads.upload_file(file.name)
        task = imports.import_vulnerabilities.create(
            filename=file.name,
            policyReference=reference,
            importAllDomainNames=True
        )
        while True:
            task.refresh()
            if task.status in ['COMPLETED', 'FAILURE']:
                break
            time.sleep(1)
        hashid = str(task.id)
        task.delete()
        rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
        with pytest.raises(HTTPError) as err:
            rc.import_vulnerabilities.load(id=hashid)
        assert err.value.response.status_code == 404

    def test_import_vuln_collection(self, mgmt_root, import_vuln):
        imp1 = import_vuln
        endpoint = str(imp1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/tasks/import-vulnerabilities/'
        final_uri = base_uri + endpoint
        assert imp1.selfLink.startswith(final_uri)
        assert imp1.status == 'COMPLETED'
        assert imp1.kind == 'tm:asm:tasks:import-vulnerabilities:import-vulnerabilities-taskstate'
        assert imp1.importAllDomainNames is True

        sc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Import_Vulnerabilities)
