# Copyright 2106 F5 Networks Inc.
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


def setup(request, mgmt_root, name, partition, ipaddr):
    def teardown():
        if sp.exists(name=name, partition=partition):
            sp.delete()
    request.addfinalizer(teardown)

    spc = mgmt_root.tm.ltm.snatpools
    sp = spc.snatpool.create(name=name, partition=partition, members=[ipaddr])
    return spc, sp


class TestSnatpools(object):
    def test_get_collection(self, request, mgmt_root):
        spc, sp = setup(
            request, mgmt_root, 'test-snatpool', 'Common', '192.168.101.1')
        sps = spc.get_collection()
        assert len(sps) >= 1
        assert [s for s in sps if s.name == 'test-snatpool']


class TestSnatpool(object):
    def test_CURDLE(self, request, mgmt_root):
        # Assume create and delete are tested by setup/teardown
        spc, sp1 = setup(
            request, mgmt_root, 'test-snatpool', 'Common', '192.168.101.1')

        # Exists
        assert spc.snatpool.exists(name='test-snatpool', partition='Common')

        # Load
        sp2 = spc.snatpool.load(name='test-snatpool', partition='Common')
        assert sp1.generation == sp2.generation
        assert sp1.name == sp2.name

        #  Update
        sp1.members.append('192.168.101.2')
        sp1.update()
        assert len(sp1.members) == 2
        assert sp1.generation != sp2.generation

        # Refresh
        sp2.refresh()
        assert len(sp2.members) == 2
        assert sp1.generation == sp2.generation
