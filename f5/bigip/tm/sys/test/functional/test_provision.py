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

import time


def is_mprov_running_on_device(mgmt_root):
    output = mgmt_root.tm.util.bash.exec_cmd(
        'run',
        utilCmdArgs='-c "ps aux | grep \'[m]prov\'"'
    )
    if hasattr(output, 'commandResult'):
        return True
    return False


def wait_for_module_provisioning(mgmt_root):
    # To prevent things from running forever, the hack is to check
    # for mprov's status. If mprov is finished, then in most
    # cases (not ASM) the provisioning is probably ready.
    nops = 0

    # Sleep a little to let provisioning settle and begin properly
    time.sleep(5)

    while nops < 4:
        try:
            if not is_mprov_running_on_device(mgmt_root):
                nops += 1
            else:
                nops = 0
        except Exception as ex:
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
        ltmprov.refresh()
        assert ltmprov.level == 'minimum'

        # Undo
        ltmprov.level = 'nominal'
        ltmprov.update()
        wait_for_module_provisioning(mgmt_root)
