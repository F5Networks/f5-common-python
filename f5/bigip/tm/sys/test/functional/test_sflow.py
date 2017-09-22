
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


def set_sflow_http_settings_test(request, mgmt_root):
    def teardown():
        sf_http.pollInterval = sf_http_int
        sf_http.update()
    request.addfinalizer(teardown)
    sf_http = mgmt_root.tm.sys.sflow.global_settings.http.load()
    sf_http_int = sf_http.pollInterval
    return sf_http


def set_sflow_interface_settings_test(request, mgmt_root):
    def teardown():
        sf_interface.pollInterval = sf_interface_int
        sf_interface.update()
    request.addfinalizer(teardown)
    sf_interface = mgmt_root.tm.sys.sflow.global_settings.interface.load()
    sf_interface_int = sf_interface.pollInterval
    return sf_interface


def set_sflow_system_settings_test(request, mgmt_root):
    def teardown():
        sf_system.pollInterval = sf_system_int
        sf_system.update()
    request.addfinalizer(teardown)
    sf_system = mgmt_root.tm.sys.sflow.global_settings.system.load()
    sf_system_int = sf_system.pollInterval
    return sf_system


def set_sflow_vlan_settings_test(request, mgmt_root):
    def teardown():
        sf_vlan.pollInterval = sf_vlan_int
        sf_vlan.update()
    request.addfinalizer(teardown)
    sf_vlan = mgmt_root.tm.sys.sflow.global_settings.vlan.load()
    sf_vlan_int = sf_vlan.pollInterval
    return sf_vlan


def set_sflow_receiver_test(request, mgmt_root):
    def teardown():
        sflow_receiver.delete()
    request.addfinalizer(teardown)

    sflow_receiver = mgmt_root.tm.sys.sflow.receivers.receiver.create(
        name='sr1', address='172.16.44.20'
    )
    return sflow_receiver


class TestSflowHttp_Setting(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        h1 = set_sflow_http_settings_test(request, mgmt_root)
        h2 = mgmt_root.tm.sys.sflow.global_settings.http.load()
        assert h1.pollInterval == 10
        assert h1.pollInterval == h2.pollInterval

        # Update
        h1.pollInterval = 20
        h1.update()
        assert h1.pollInterval == 20
        assert h2.pollInterval == 10

        # Refresh
        h2.refresh()
        assert h2.pollInterval == h1.pollInterval


class TestSflowInterface_Setting(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        h1 = set_sflow_interface_settings_test(request, mgmt_root)
        h2 = mgmt_root.tm.sys.sflow.global_settings.interface.load()
        assert h1.pollInterval == 10
        assert h1.pollInterval == h2.pollInterval

        # Update
        h1.pollInterval = 20
        h1.update()
        assert h1.pollInterval == 20
        assert h2.pollInterval == 10

        # Refresh
        h2.refresh()
        assert h2.pollInterval == h1.pollInterval


class TestSflowSystem_Setting(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        h1 = set_sflow_system_settings_test(request, mgmt_root)
        h2 = mgmt_root.tm.sys.sflow.global_settings.system.load()
        assert h1.pollInterval == 10
        assert h1.pollInterval == h2.pollInterval

        # Update
        h1.pollInterval = 20
        h1.update()
        assert h1.pollInterval == 20
        assert h2.pollInterval == 10

        # Refresh
        h2.refresh()
        assert h2.pollInterval == h1.pollInterval


class TestSflowVlan_Setting(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        h1 = set_sflow_vlan_settings_test(request, mgmt_root)
        h2 = mgmt_root.tm.sys.sflow.global_settings.vlan.load()
        assert h1.pollInterval == 10
        assert h1.pollInterval == h2.pollInterval

        # Update
        h1.pollInterval = 20
        h1.update()
        assert h1.pollInterval == 20
        assert h2.pollInterval == 10

        # Refresh
        h2.refresh()
        assert h2.pollInterval == h1.pollInterval


class TestSflowReceiver(object):
    def test_CURDLE(self, request, mgmt_root):
        # Assume create/delete tested by setup/teardown
        r1 = set_sflow_receiver_test(request, mgmt_root)

        # Exists
        assert mgmt_root.tm.sys.sflow.receivers.receiver.exists(name='sr1')

        # Load
        r2 = mgmt_root.tm.sys.sflow.receivers.receiver.load(name='sr1')
        assert r1.name == r2.name

        # Update
        r1.address = '172.16.44.21'
        r1.update()
        assert r1.address != r2.address

        # Refresh
        r2.refresh()
        assert r1.address == r2.address
