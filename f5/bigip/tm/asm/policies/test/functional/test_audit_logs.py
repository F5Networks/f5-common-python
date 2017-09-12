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

from distutils.version import LooseVersion
from f5.bigip.tm.asm.policies.audit_logs import Audit_Log
from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError


@pytest.fixture(scope='function')
def set_audit_logs(policy):
    # Audit logs fill up quickly, doing a get_collection() would return
    # first 500 entries by default (as this is how BIGIP returns it),
    # it faster to have it limited to 2
    rc = policy.audit_logs_s.get_collection(
        requests_params={'params': '$top=2'}
    )
    hashid = str(rc[0].id)
    yield hashid


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='This collection is fully implemented on 12.0.0 or greater.'
)
class TestAuditLogs(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.audit_logs_s.audit_log.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.audit_logs_s.audit_log.delete()

    def test_modify_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.audit_logs_s.audit_log.create()

    def test_refresh(self, policy, set_audit_logs):
        hashid = set_audit_logs
        r1 = policy.audit_logs_s.audit_log.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:audit-logs:audit-logstate'
        r2 = policy.audit_logs_s.audit_log.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.audit_logs_s.audit_log.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, set_audit_logs):
        hashid = set_audit_logs
        r1 = policy.audit_logs_s.audit_log.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:audit-logs:audit-logstate'
        r2 = policy.audit_logs_s.audit_log.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_auditlog_subcollection(self, policy):
        mc = policy.audit_logs_s.get_collection(
            requests_params={'params': '$top=2'}
        )
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Audit_Log)
