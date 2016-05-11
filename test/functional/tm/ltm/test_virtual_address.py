# Copyright 2015-2016 F5 Networks Inc.
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

TESTDESCRIPTION = "TESTDESCRIPTION"


def setup_virtual_address_s_test(request, bigip, vs_name, vs_partion):
    def teardown():
        if bigip.ltm.virtuals.virtual.exists(name=vs_name,
                                             partition=vs_partion):
            vs.delete()
    request.addfinalizer(teardown)

    vs = bigip.ltm.virtuals.virtual.create(name=vs_name, partition=vs_partion)


def setup_virtual_address_test(request, bigip, va_name, va_partition):
    def teardown():
        if bigip.ltm.virtual_address_s.virtual_address.exists(
            name=va_name, partition=va_partition
        ):
            va.delete()
    request.addfinalizer(teardown)
    vac = bigip.ltm.virtual_address_s
    va = vac.virtual_address.create(name=va_name, partition=va_partition)
    return vac, va


class TestVirtualAddress_s(object):
    def test_get_collection(self, request, bigip):
        setup_virtual_address_s_test(request, bigip, 'va_vs_test-1', 'Common')
        vas = bigip.ltm.virtual_address_s
        vac = vas.get_collection()
        assert len(vac) >= 1
        assert [va for va in vac if va.name == '0.0.0.0']


class TestVirtualAddress(object):
    def test_CURDLE(self, request, bigip):
        # Create and delete are handled by setup/teardown
        vac, va1 = setup_virtual_address_test(request, bigip, 'va-1', 'Common')
        assert va1.name == 'va-1'

        # Exists
        assert vac.virtual_address.exists(name='va-1', partition='Common')

        # Load
        va2 = vac.virtual_address.load(name='va-1', partition='Common')
        assert va1.name == va2.name
        assert va1.generation == va2.generation

        # Update
        va1.connectionLimit = 50
        va1.update()
        assert va1.connectionLimit != va2.connectionLimit
        assert va1.generation > va2.generation

        # Refresh
        va2.refresh()
        assert va1.connectionLimit == va2.connectionLimit
        assert va1.generation == va2.generation
