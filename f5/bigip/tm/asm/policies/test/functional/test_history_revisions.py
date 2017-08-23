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
from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestHistoryRevisions(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.history_revisions_s.history_revision.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.history_revisions_s.history_revision.delete()

    def test_modify_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.history_revisions_s.history_revision.create()

    def test_refresh(self, policy, set_history):
        hashid = set_history
        r1 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:history-revisions:history-revisionstate'
        r2 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.history_revisions_s.history_revision.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, set_history):
        hashid = set_history
        r1 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == 'tm:asm:policies:history-revisions:history-revisionstate'
        r2 = policy.history_revisions_s.history_revision.load(id=hashid)
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
