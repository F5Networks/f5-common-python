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


class TestAllStats(object):
    def test_RL(self, mgmt_root):
        allstats = mgmt_root.tm.sys.performances.all_stats.load()
        assert hasattr(allstats, 'apiRawValues')
        allstats.refresh()
        assert hasattr(allstats, 'apiRawValues')
