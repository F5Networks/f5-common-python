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
from icontrol.session import iControlUnexpectedHTTPError
import pytest
from requests import HTTPError


TEST_DESCR = "TEST DESCRIPTION"


def setup_device_group_test(request, mgmt_root, name, partition):
    def teardown():
        try:
            for d in dg.devices_s.get_collection():
                d.delete()
            dg.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
    request.addfinalizer(teardown)

    dgs = mgmt_root.tm.cm.device_groups
    dg = dgs.device_group.create(name=name, partition=partition)
    return dg, dgs


class TestDeviceGroup(object):
    def test_device_group_CURDL(self, request, mgmt_root):
        # Create and delete are taken care of by setup
        dg1, dgs = setup_device_group_test(
            request, mgmt_root, name='test-device-group', partition='Common')
        assert dg1.generation > 0
        assert dg1.name == 'test-device-group'

        # Load
        dg2 = mgmt_root.tm.cm.device_groups.device_group.load(
            name=dg1.name, partition=dg1.partition)
        assert dg1.generation == dg2.generation

        # Update
        dg1.update(description=TEST_DESCR)
        assert dg1.generation > dg2.generation
        assert dg1.description == TEST_DESCR

        # Refresh
        dg2.refresh()
        assert dg1.generation == dg2.generation
        assert dg2.description == TEST_DESCR

    def test_add_device(self, request, mgmt_root):
        dg1, dgs = setup_device_group_test(
            request, mgmt_root, name='test-device-group', partition='Common')
        devices = mgmt_root.tm.cm.devices.get_collection()
        this_device = devices[0]
        assert this_device.selfDevice == 'true'
        d1 = dg1.devices_s.devices.create(
            name=this_device.name, partition=this_device.partition)
        assert len(dg1.devices_s.get_collection()) == 1
        # This needs to be in this format due to the change between
        # 11.6.0 Final and other versions.
        assert this_device.name in d1.name

    def test_cm_sync_to_group(self, request, mgmt_root):
        dg1, dgs = setup_device_group_test(
            request, mgmt_root, name='test-device-group', partition='Common')
        sync_cmd = 'config-sync to-group %s' % dg1.name
        cm_obj = mgmt_root.tm.cm.exec_cmd('run', utilCmdArgs=sync_cmd)
        assert cm_obj.utilCmdArgs == sync_cmd

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) > LooseVersion('11.6.1'),
        reason='Skip test if on a version greater than or equal to 11.6.1')
    def test_cm_sync_from_group_pre_12_0(self, request, mgmt_root):
        dg1, dgs = setup_device_group_test(
            request, mgmt_root, name='test-device-group', partition='Common')
        sync_cmd = 'config-sync from-group %s' % dg1.name
        cm_obj = mgmt_root.tm.cm.exec_cmd('run', utilCmdArgs=sync_cmd)
        assert cm_obj.utilCmdArgs == sync_cmd

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) < LooseVersion('12.0.0'),
        reason='Skip test if on a version earlier than 12.0.0')
    def test_cm_sync_from_group_post_11_6(self, request, mgmt_root):
        dg1, dgs = setup_device_group_test(
            request, mgmt_root, name='test-device-group', partition='Common')
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            sync_cmd = 'config-sync from-group %s' % dg1.name
            mgmt_root.tm.cm.exec_cmd('run', utilCmdArgs=sync_cmd)
        assert err.value.response.status_code == 400
        assert 'is not allowed until a push has been done first' \
               in err.value.response.text
