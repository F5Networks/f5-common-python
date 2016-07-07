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

TEST_MAC = '02:00:00:00:00:01'


def test_tunnels_get_collection(mgmt_root):
    tunnels_collection = mgmt_root.tm.net.fdb.tunnels.get_collection()
    for tunnel in tunnels_collection:
        assert tunnel.name == 'http-tunnel' or tunnel.name == 'socks-tunnel'


def test_tunnel_exists_load_update_refresh(mgmt_root):
    t_fact = mgmt_root.tm.net.fdb.tunnels.tunnel
    assert t_fact.exists(partition='Common', name='http-tunnel')
    assert t_fact.exists(partition='Common', name='socks-tunnel')
    http_tunnel = t_fact.load(partition='Common', name='http-tunnel')
    http2_tunnel = t_fact.load(partition='Common', name='http-tunnel')
    http_tunnel.update(records=TEST_MAC)
    http2_tunnel.refresh()
    assert http2_tunnel.records == [{u'name': u'02:00:00:00:00:01'}]
    http_tunnel.update(records=None)
    assert 'records' not in http_tunnel.__dict__
