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

def set_trust(request, bigip, name, device, dev_name, usr, passwd):
    dvcs = bigip.cm
    trust = dvcs.add_to_trust.run(name=name, device=device, deviceName=dev_name, username=usr, password=passwd)
    return trust

def unset_trust(request, bigip, name, dev_name):
    dvcs = bigip.cm
    reset = dvcs.remove_from_trust.run(name=name, deviceName=dev_name)
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

class TestTrust(object):
    def test_run(self, request, bigip):
        #Check sync state, assume standalone
        assert check_sync(request, bigip) == u"Standalone"
        #Setup trust
        set_trust(request, bigip, 'Root', '192.168.202.155', 'v12b-apm-ltm-test.labnet.local', 'admin', 'admin')
        #Verify sync state assume disconnected
        assert check_sync(request, bigip) == u"Disconnected"
        #Remove trust
        unset_trust(request, bigip, 'Root', 'v12b-apm-ltm-test.labnet.local')
        #Verify device sync state is Standalone
        assert check_sync(request, bigip) == u"Standalone"

