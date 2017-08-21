# Copyright 2015-2016 F5 Networks Inc.
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

import logging
import os
import pytest
import shutil
import tempfile
import time
import fcntl
from f5.sdk_exception import F5SDKError
from distutils.version import LooseVersion

logger = logging.getLogger()
logger.setLevel(logging.WARNING)


@pytest.fixture(scope='function')
def policy(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    pol1 = mgmt_root.tm.asm.policies_s.policy.create(name=name)
    yield pol1
    pol1.delete()


@pytest.fixture(scope='function')
def policy2(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    pol2 = mgmt_root.tm.asm.policies_s.policy.create(name=name)
    yield pol2
    pol2.delete()


@pytest.fixture(scope='function')
def set_login(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    url = policy.urls_s.url.create(name=name + '.com')
    reference = {'link': url.selfLink}
    valid = {'responseContains': '201 OK'}
    login = policy.login_pages_s.login_page.create(
        urlReference=reference,
        accessValidation=valid
    )
    yield login, reference
    login.delete()
    url.delete()


@pytest.fixture(scope='function')
def set_brute(policy, set_login):
    login, reference = set_login
    login.modify(authenticationType='http-basic')
    r1 = policy.brute_force_attack_preventions_s.brute_force_attack_prevention.create(urlReference=reference)
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def set_history(mgmt_root, policy):
    reference = {'link': policy.selfLink}
    pol1 = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.create(
        policyReference=reference
    )
    # We need to pause here as the history revisions take time to update
    col = list()
    while not col:
        col = policy.history_revisions_s.get_collection()
        time.sleep(3)
    hashid = str(col[0].id)
    yield hashid
    pol1.delete()


@pytest.fixture(scope='function')
def set_navi_par(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = policy.navigation_parameters_s.navigation_parameter.create(
        name=name
    )
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def set_plaintext(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = policy.plain_text_profiles_s.plain_text_profile.create(
        name=name
    )
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def resp_page(policy):
    rescol = policy.response_pages_s.get_collection()
    for item in rescol:
        if item.responsePageType == 'default':
            yield item.id


@pytest.fixture(scope='function')
def set_s_par(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = policy.sensitive_parameters_s.sensitive_parameter.create(
        name=name
    )
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def set_policy_status(mgmt_root, policy):
    """Fixture for Session Tracking Status

    This fixture __must__ be serialized due to the constraints placed
    on this ASM policy feature. The Session Tracking Status' can __only__
    be created when the policy is active.

    If the policy you are using is not active, you will receive an error
    message that resembles the following

        Could not add the Session Awareness Data Point ... .  Session Awareness
        Data Point cannot be added to an inactive security policy

    This can happen when parallel pytest runs all try to activate their
    policy at once. Ultimately, only 1 will succeed and the rest will fail
    in a cascade causing the tests themselves to fail.

    Therefore, we use a simple file lock and looping to get around this and
    serialize the test.

    :param mgmt_root:
    :param policy:
    :return:
    """
    f = open('__lock__', 'w')
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except IOError:
            time.sleep(1)

    reference = {'link': policy.selfLink}
    task = mgmt_root.tm.asm.tasks.apply_policy_s.apply_policy.create(
        policyReference=reference
    )
    while True:
        task.refresh()
        if task.status == 'COMPLETED':
            break
        if task.status == 'FAILURE':
            raise F5SDKError(
                task.status['message']
            )
        time.sleep(1)

    tmp = {'enableSessionAwareness': True}
    policy.session_tracking.modify(sessionTrackingConfiguration=tmp)
    time.sleep(5)
    policy.refresh()
    yield policy

    fcntl.flock(f, fcntl.LOCK_UN | fcntl.LOCK_NB)
    f.close()


@pytest.fixture(scope='function')
def signature(mgmt_root):
    coll = mgmt_root.tm.asm.signature_sets_s.get_collection(
        requests_params={'params': '$top=2'})
    lnk = str(coll[1].selfLink)
    yield lnk


@pytest.fixture(scope='function')
def set_vulnerability(mgmt_root, policy, scan_type):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    reference = {'link': policy.selfLink}
    policy.vulnerability_assessment.modify(scannerType=scan_type)
    dirpath = os.path.dirname(__file__)
    path = os.path.join(dirpath, 'test_files')
    fake_report = os.path.join(path, 'fake_scan.xml')
    shutil.copyfile(fake_report, file.name)
    mgmt_root.tm.asm.file_transfer.uploads.upload_file(file.name)
    time.sleep(1)
    rc = mgmt_root.tm.asm.tasks.import_vulnerabilities_s
    pol1 = rc.import_vulnerabilities.create(
        filename=name,
        policyReference=reference,
        importAllDomainNames=True
    )
    time.sleep(3)
    col = policy.vulnerabilities_s.get_collection()
    hashid = str(col[0].id)
    yield hashid
    pol1.delete()


@pytest.fixture(scope='function')
def scan_type():
    if LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('12.1.0'):
        return 'qualys'
    else:
        return 'qualys-guard'


@pytest.fixture(scope='function')
def set_websock(policy):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = policy.websocket_urls_s.websocket_url.create(
        name=name,
        checkPayload=False
    )
    yield r1
    r1.delete()
