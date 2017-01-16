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
#

from f5.bigip.tm.sys import Failover
from f5.sdk_exception import ExclusiveAttributesPresent

import mock
import pytest


@pytest.fixture
def FakeFailover():
    fake_sys = mock.MagicMock()
    fake_fail = Failover(fake_sys)
    fake_fail._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_fail


class TestFailover(object):
    def test_exclusive_attr(self):
        fl = FakeFailover()
        with pytest.raises(ExclusiveAttributesPresent) as err:
            fl.exec_cmd('run', online=True, standby=True)
            assert 'Mutually exclusive arguments submitted' \
                   in err.value.message
