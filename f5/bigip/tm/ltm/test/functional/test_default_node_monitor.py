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


def set_default_node_monitor_test(request, mgmt_root):
    def teardown():
        dnm.rule = ''
        dnm.update()
    request.addfinalizer(teardown)
    dnm = mgmt_root.tm.ltm.default_node_monitor.load()
    return dnm


class TestDefault_Node_Monitor(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        dnm1 = set_default_node_monitor_test(request, mgmt_root)
        dnm2 = mgmt_root.tm.ltm.default_node_monitor.load()
        assert not hasattr(dnm1, 'rule')
        assert not hasattr(dnm2, 'rule')

        # Update
        dnm1.rule = 'min 1 of /Common/gateway_icmp'
        dnm1.update()
        assert dnm1.rule == 'min 1 of { /Common/gateway_icmp }'

        # Refresh
        dnm2.refresh()
        assert dnm1.rule == dnm2.rule
