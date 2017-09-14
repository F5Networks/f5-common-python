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

import os
import pytest
import tempfile
import time

from f5.utils.responses.handlers import Stats


try:
    vcmp_host = pytest.config.getoption('--vcmp-host')
except Exception as ex:
    vcmp_host = None


@pytest.fixture
def software_images(vcmp_host):
    collection = vcmp_host.tm.sys.software.images.get_collection()
    result = sorted([x.name.split('/')[0] for x in collection])
    return result


@pytest.fixture
def vcmp_guest(vcmp_host, software_images):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    resource = vcmp_host.tm.vcmp.guests.guest.create(
        name=name,
        initialImage=software_images[0],
        state='provisioned',
        managementGw='1.1.1.254',
        managementIp='1.1.1.1/24',
        managementNetwork='bridged'
    )
    yield resource


@pytest.mark.skipif(
    vcmp_host is None,
    reason='Provide --vcmp-host to run vcmp tests.'
)
class TestGuest(object):
    def test_delete(self, vcmp_host, software_images):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        resource = vcmp_host.tm.vcmp.guests.guest.create(
            name=name,
            initialImage=software_images[0],
            state='provisioned',
            managementGw='1.1.1.254',
            managementIp='1.1.1.1/24',
            managementNetwork='bridged'
        )
        self._wait_for_provisioned(vcmp_host, resource.name)

        disk = resource.virtualDisk
        slots = resource.assignedSlots

        resource.delete()

        for slot in slots:
            self._wait_for_virtual_disk_ready(vcmp_host, disk, slot)
            vdisk = vcmp_host.tm.vcmp.virtual_disks.virtual_disk.load(
                name=disk, slot=slot
            )
            vdisk.delete()

        assert vcmp_host.tm.vcmp.guests.guest.exists(name=name) is False
        for slot in slots:
            exists = vcmp_host.tm.vcmp.virtual_disks.virtual_disk.exists(
                name=disk, slot=slot
            )
            assert exists is False

    def _wait_for_provisioned(self, vcmp_host, name):
        resource = vcmp_host.tm.vcmp.guests.guest.load(name=name)
        nops = 0
        time.sleep(5)
        while nops < 3:
            try:
                stats = Stats(resource.stats.load())
                requested_state = stats.stat['requestedState']['description']
                vm_status = stats.stat['vmStatus']['description']

                if requested_state == 'provisioned' and vm_status == 'stopped':
                    nops += 1
                else:
                    nops = 0
            except Exception:
                # This can be caused by restjavad restarting.
                pass
            time.sleep(10)

    def _wait_for_virtual_disk_ready(self, vcmp_host, disk, slot):
        resource = vcmp_host.tm.vcmp.virtual_disks.virtual_disk.load(
            name=disk, slot=slot
        )
        nops = 0
        time.sleep(5)
        while nops < 3:
            try:
                stats = Stats(resource.stats.load())
                status = stats.stat['status']['description']

                if status == 'ready':
                    nops += 1
                else:
                    nops = 0
            except Exception:
                # This can be caused by restjavad restarting.
                pass
            time.sleep(10)
