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

import mock
import pytest

from f5.bigip.mixins import UnsupportedMethod
from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.sys.performance import Performances


@pytest.fixture
def FakePerformance():
    fake_sys = mock.MagicMock()
    performances = Performances(fake_sys)
    performances._meta_data['bigip'].tmos_version = '11.6.0'
    return performances


class TestPerformance(object):
    def test_get_collection_raises(self):
        perf = FakePerformance()
        with pytest.raises(UnsupportedOperation):
            perf.get_collection()


class TestAllStats(object):
    def test_create_raises(self):
        perf = FakePerformance()
        allstats = perf.all_stats
        with pytest.raises(UnsupportedMethod):
            allstats.create()

    def test_update_raises(self):
        perf = FakePerformance()
        allstats = perf.all_stats
        with pytest.raises(UnsupportedOperation):
            allstats.update()

    def test_delete_raises(self):
        perf = FakePerformance()
        allstats = perf.all_stats
        with pytest.raises(UnsupportedMethod):
            allstats.delete()
