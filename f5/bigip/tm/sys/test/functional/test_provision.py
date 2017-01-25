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


class TestProvision(object):
    def test_Provision(self, request, bigip):
        # Load
        ltmprov = bigip.sys.provision.ltm.load()
        assert ltmprov.level == 'nominal'
        assert ltmprov.name == 'ltm'

        # Update
        ltmprov.level = 'minimum'
        ltmprov.update()
        assert ltmprov.level == 'minimum'

        # Refresh
        ltmprov.refresh()
        assert ltmprov.level == 'minimum'
