# Copyright 2018 F5 Networks Inc.
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

from icontrol.exceptions import iControlUnexpectedHTTPError


def test_cluster_load(request, mgmt_root):
    # Load will produce exception on non-cluster BIGIP.
    # iControlUnexpectedHTTPError: 404 Unexpected Error: Not Found for uri:
    try:
        assert str(mgmt_root.tm.sys.cluster.default.load().kind) == 'tm:sys:cluster:clusterstate'
    except iControlUnexpectedHTTPError as err:
        assert ('01020036:3: The requested cluster (default) was not found.' in str(err))


def test_cluster_stats_load(request, mgmt_root):
    # Load will give the result even on non-cluster BIGIP. However, the payload will be almost empty
    assert str(mgmt_root.tm.sys.cluster.stats.load().kind) == 'tm:sys:cluster:clustercollectionstats'


def test_cluster_default_stats_load(request, mgmt_root):
    # Load will produce exception on non-cluster BIGIP.
    # iControlUnexpectedHTTPError: 404 Unexpected Error: Not Found for uri:
    try:
        assert str(mgmt_root.tm.sys.cluster.default.stats.load().kind) == 'tm:sys:cluster:clusterstats'
    except iControlUnexpectedHTTPError as err:
        assert ('01020036:3: The requested cluster (default) was not found.' in str(err))
