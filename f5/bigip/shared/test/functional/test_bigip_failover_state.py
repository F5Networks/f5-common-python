# Copyright 2016 F5 Networks Inc.
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

import pytest

from f5.sdk_exception import UnsupportedMethod


@pytest.mark.skipif(pytest.config.getoption('--release') != '12.0.0',
                    reason='Needs v12 TMOS to pass')
class TestBigIPFailoverState(object):
    def test_load(self, request, mgmt_root):
        a = mgmt_root.shared.bigip_failover_state.load()
        assert hasattr(a, 'generation')

    def test_update(self, request, mgmt_root):
        with pytest.raises(UnsupportedMethod):
            mgmt_root.shared.bigip_failover_state.update()
