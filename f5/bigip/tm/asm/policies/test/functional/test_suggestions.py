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
from f5.bigip.tm.asm.policies.suggestions import Suggestion
from f5.sdk_exception import UnsupportedOperation


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='This collection is fully implemented on 12.0.0 or greater.'
)
class TestSuggestions(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.suggestions_s.suggestion.create()

    def test_suggestions_subcollection(self, policy):
        mc = policy.suggestions_s.get_collection(
            requests_params={'params': '$top=2'}
        )
        m = policy.suggestions_s
        # Same situation where the BIGIP will return 500 entries by default.
        # This list is populated when policy is in learning mode. Very
        # limited testing can be performed
        assert Suggestion in m._meta_data['allowed_lazy_attributes']
        assert isinstance(mc, list)
        assert not len(mc)
