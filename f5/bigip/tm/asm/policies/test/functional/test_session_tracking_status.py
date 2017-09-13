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
import time

from distutils.version import LooseVersion
from f5.bigip.tm.asm.policies.session_tracking_status import Session_Tracking_Status
from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestSessionTrackingStatuses(object):
    def test_create_req_arg(self, set_policy_status):
        args = {'action': 'block-all', 'scope': 'user', 'value': 'fake'}
        tracking = set_policy_status.session_tracking_statuses_s
        r1 = tracking.session_tracking_status.create(**args)
        assert r1.kind == 'tm:asm:policies:session-tracking-statuses:session-tracking-statusstate'
        assert r1.action == 'block-all'
        assert r1.scope == 'user'
        assert r1.value == 'fake'
        assert hasattr(r1, 'createdDatetime')

    def test_refresh(self, set_policy_status):
        args = {'action': 'block-all', 'scope': 'user', 'value': 'fake2'}
        tracking = set_policy_status.session_tracking_statuses_s
        r1 = tracking.session_tracking_status.create(**args)
        r2 = tracking.session_tracking_status.load(id=r1.id)
        assert r1.kind == 'tm:asm:policies:session-tracking-statuses:session-tracking-statusstate'
        assert r1.action == 'block-all'
        assert r1.scope == 'user'
        assert r1.value == 'fake2'
        assert hasattr(r1, 'createdDatetime')
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.action == r2.action
        assert r1.scope == r2.scope
        assert r1.value == r2.value

    def test_modify_raises(self, set_policy_status):
        with pytest.raises(UnsupportedOperation):
            tracking = set_policy_status.session_tracking_statuses_s
            tracking.session_tracking_status.modify(value='test')

    def test_delete(self, set_policy_status):
        args = {'action': 'block-all', 'scope': 'user', 'value': 'fake3'}
        tracking = set_policy_status.session_tracking_statuses_s
        r1 = tracking.session_tracking_status.create(**args)
        idhash = str(r1.id)
        time.sleep(5)
        r1.delete()
        with pytest.raises(HTTPError) as err:
            tracking.session_tracking_status.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, set_policy_status):
        with pytest.raises(HTTPError) as err:
            tracking = set_policy_status.session_tracking_statuses_s
            tracking.session_tracking_status.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, set_policy_status):
        args = {'action': 'block-all', 'scope': 'user', 'value': 'fake4'}
        tracking = set_policy_status.session_tracking_statuses_s
        r1 = tracking.session_tracking_status.create(**args)
        r2 = tracking.session_tracking_status.load(id=r1.id)
        assert r1.kind == 'tm:asm:policies:session-tracking-statuses:session-tracking-statusstate'
        assert r1.action == 'block-all'
        assert r1.scope == 'user'
        assert r1.value == 'fake4'
        assert hasattr(r1, 'createdDatetime')
        assert r1.kind == r2.kind
        assert r1.action == r2.action
        assert r1.scope == r2.scope
        assert r1.value == r2.value

    def test_session_tracking_subcollection(self, set_policy_status):
        args = {'action': 'block-all', 'scope': 'user', 'value': 'fake5'}
        tracking = set_policy_status.session_tracking_statuses_s
        r1 = tracking.session_tracking_status.create(**args)
        assert r1.kind == 'tm:asm:policies:session-tracking-statuses:session-tracking-statusstate'
        assert r1.value == 'fake5'
        mc = set_policy_status.session_tracking_statuses_s.get_collection()
        assert isinstance(mc, list)
        assert len(mc)
        assert isinstance(mc[0], Session_Tracking_Status)
