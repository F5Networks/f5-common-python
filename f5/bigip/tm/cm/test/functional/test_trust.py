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

from f5.sdk_exception import InvalidCommand
import pytest


def set_trust(request, bigip, name, device, dev_name, usr, passwd):
    dvcs = bigip.cm
    trust = dvcs.add_to_trust.exec_cmd('run', name=name, device=device,
                                       deviceName=dev_name, username=usr,
                                       caDevice=True, password=passwd)
    return trust


def unset_trust(request, bigip, name, dev_name):
    dvcs = bigip.cm
    reset = dvcs.remove_from_trust.exec_cmd('run', name=name,
                                            deviceName=dev_name)
    return reset


def check_sync(request, bigip):
    sync_status = bigip.cm.sync_status
    sync_status.refresh()
    des = \
        (sync_status.entries['https://localhost/mgmt/tm/cm/sync-status/0']
         ['nestedStats']
         ['entries']
         ['status']
         ['description'])
    return des


def check_peer(request, bigip):
    dvcs = bigip.cm.devices.get_collection()
    device = str(dvcs[0].managementIp)
    devname = str(dvcs[0].hostname)
    return device, devname


@pytest.mark.skipif(pytest.config.getoption('--peer') == 'none',
                    reason='Needs peer defined to run')
class TestTrust(object):
    def test_run(self, request, bigip, peer):
        # Check sync state, assume standalone
        assert check_sync(request, bigip) == "Standalone"
        assert check_sync(request, peer) == "Standalone"

        # Obtain peer information
        device1, devicename1 = check_peer(request, peer)
        device2, devicename2 = check_peer(request, bigip)

        # Setup trust
        set_trust(request, bigip, 'Root', device1,
                  devicename1, 'admin', 'admin')

        # Verify sync state assume disconnected
        assert check_sync(request, bigip) == "Disconnected"
        assert check_sync(request, peer) == "Disconnected"

        # Remove trust from both units
        unset_trust(request, bigip, 'Root', devicename1)
        unset_trust(request, peer, 'Root', devicename2)

        # Verify devices sync state is Standalone
        assert check_sync(request, bigip) == "Standalone"
        assert check_sync(request, peer) == "Standalone"

    def test_invalid_cmd_meta(self, request, bigip):
        dvcs = bigip.cm
        with pytest.raises(InvalidCommand):
            dvcs.add_to_trust.exec_cmd('foo', name='fooname',
                                       device='foodev',
                                       deviceName='foo_name',
                                       username='foouser',
                                       caDevice=True, password='foopasswd')
