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
from distutils.version import LooseVersion
import pytest

TEST_MAC = '02:00:00:00:00:01'

V12PAYLOAD = [{'name': '02:00:00:00:00:01', 'endpoint': '10.1.1.1'}]


def test_tunnels_get_collection(mgmt_root):
    tunnels_collection = mgmt_root.tm.net.fdb.tunnels.get_collection()
    for tunnel in tunnels_collection:
        assert tunnel.name == 'http-tunnel' or tunnel.name == 'socks-tunnel'


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion(
        '12.1.0'), reason='This test is for 12.0.0 or less.')
def test_tunnel_exists_load_update_refresh(mgmt_root):
    t_fact = mgmt_root.tm.net.fdb.tunnels.tunnel
    assert t_fact.exists(partition='Common', name='http-tunnel')
    assert t_fact.exists(partition='Common', name='socks-tunnel')
    http_tunnel = t_fact.load(partition='Common', name='http-tunnel')
    http2_tunnel = t_fact.load(partition='Common', name='http-tunnel')
    http_tunnel.update(records=TEST_MAC)
    http2_tunnel.refresh()
    assert http2_tunnel.records == [{'name': '02:00:00:00:00:01'}]
    http_tunnel.update(records=None)
    assert 'records' not in http_tunnel.__dict__


# @pytest.mark.skipif(
#     LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
#         '12.1.0'), reason='This test is for 12.1.0 or greater.')
# def test_tunnel_exists_load_update_refresh_v12_1(mgmt_root):
#     t_fact = mgmt_root.tm.net.fdb.tunnels.tunnel
#     assert t_fact.exists(partition='Common', name='http-tunnel')
#     assert t_fact.exists(partition='Common', name='socks-tunnel')
#     http_tunnel = t_fact.load(partition='Common', name='http-tunnel')
#     http2_tunnel = t_fact.load(partition='Common', name='http-tunnel')
#     http_tunnel.update(records=V12PAYLOAD)
#     http2_tunnel.refresh()
#     assert http2_tunnel.records == [{'name': '02:00:00:00:00:01',
#                                      'endpoint': '10.1.1.1'}]
#     http_tunnel.update(records=None)
#     assert 'records' not in http_tunnel.__dict__
