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

import pytest
import time

from pytest import symbols

MISSING_SYMBOLS_VCMP = True
if hasattr(symbols, 'run_vcmp_tests'):
    if symbols.run_vcmp_tests is True:
        MISSING_SYMBOLS_VCMP = False


def is_mprov_running_on_device(mgmt_root):
    output = mgmt_root.tm.util.bash.exec_cmd(
        'run',
        utilCmdArgs='-c "ps aux | grep \'[m]prov\'"'
    )
    if hasattr(output, 'commandResult'):
        return True
    return False


def get_last_reboot(mgmt_root):
    output = mgmt_root.tm.util.bash.exec_cmd(
        'run',
        utilCmdArgs='-c "/usr/bin/last reboot | head - 1"'
    )
    if hasattr(output, 'commandResult'):
        return str(output.commandResult)
    return None


def wait_for_module_provisioning(mgmt_root):
    # To prevent things from running forever, the hack is to check
    # for mprov's status. If mprov is finished, then in most
    # cases (not ASM) the provisioning is probably ready.
    nops = 0

    # Sleep a little to let provisioning settle and begin properly
    time.sleep(5)

    while nops < 6:
        try:
            if not is_mprov_running_on_device(mgmt_root):
                nops += 1
            else:
                nops = 0
        except Exception:
            # This can be caused by restjavad restarting.
            pass
        time.sleep(10)


def wait_for_reboot(mgmt_root):
    nops = 0

    last_reboot = get_last_reboot(mgmt_root)

    # Sleep a little to let provisioning settle and begin properly
    time.sleep(5)

    while nops < 6:
        try:
            next_reboot = get_last_reboot(mgmt_root)
            if next_reboot is None:
                nops = 0
            if next_reboot == last_reboot:
                nops = 0
            else:
                nops += 1
        except Exception:
            # This can be caused by restjavad restarting.
            pass
        time.sleep(10)


class TestProvision(object):
    def test_Provision(self, mgmt_root):
        # Load
        ltmprov = mgmt_root.tm.sys.provision.ltm.load()
        assert ltmprov.name == 'ltm'

        # Update
        ltmprov.level = 'minimum'
        ltmprov.update()
        wait_for_module_provisioning(mgmt_root)
        assert ltmprov.level == 'minimum'

        # Refresh
        assert ltmprov.level == 'minimum'

        # Undo
        ltmprov.level = 'nominal'
        ltmprov.update()
        wait_for_module_provisioning(mgmt_root)


@pytest.mark.skipif(
    MISSING_SYMBOLS_VCMP,
    reason="You must opt-in to run VCMP tests. To run them, set the symbols variable 'run_vcmp_tests: True'"
)
class TestProvisionVcmp(object):
    def test_provision_vcmp(self, mgmt_root):
        # Load
        resource = mgmt_root.tm.sys.provision.vcmp.load()

        # Update
        resource.level = 'dedicated'
        resource.update()
        assert resource.level == 'dedicated'

        wait_for_reboot(mgmt_root)

        # Refresh
        resource.refresh()
        assert resource.level == 'dedicated'

        # Undo
        resource.level = 'none'
        resource.update()
        wait_for_reboot(mgmt_root)
