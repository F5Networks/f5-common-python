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


def setup_virtual_address_s_test(request, mgmt_root, vs_name, vs_partion):
    def teardown():
        if mgmt_root.tm.ltm.virtuals.virtual.exists(name=vs_name, partition=vs_partion):
            vs.delete()
    request.addfinalizer(teardown)

    vs = mgmt_root.tm.ltm.virtuals.virtual.create(name=vs_name, partition=vs_partion)


def setup_virtual_address_test(request, mgmt_root, va_name, va_partition):
    vac = mgmt_root.tm.ltm.virtual_address_s
    if vac.virtual_address.exists(name=va_name, partition=va_partition):
        vac.virtual_address.load(
            name=va_name, partition=va_partition).delete()
    va = vac.virtual_address.create(name=va_name, partition=va_partition)
    request.addfinalizer(va.delete)
    return vac, va


class TestVirtualAddress_s(object):
    def test_get_collection(self, request, mgmt_root):
        setup_virtual_address_s_test(request, mgmt_root, 'va_vs_test-1', 'Common')
        vas = mgmt_root.tm.ltm.virtual_address_s
        vac = vas.get_collection()
        assert len(vac) >= 1
        assert [va for va in vac if va.name == '0.0.0.0']

    def test_stats(self, request, mgmt_root, opt_release):
        setup_virtual_address_s_test(request, mgmt_root, 'va_vs_test-1', 'Common')
        va_stats = mgmt_root.tm.ltm.virtual_address_s.stats.load()
        stats_link = 'https://localhost/mgmt/tm/ltm/virtual-address/' +\
            '~Common~0.0.0.0/stats'
        assert stats_link in va_stats.entries
        va_nested_stats = va_stats.entries[stats_link]['nestedStats']
        assert va_nested_stats['selfLink'] == stats_link+'?ver='+opt_release
        entries = va_nested_stats['entries']
        assert entries['tmName']['description'] == '/Common/0.0.0.0'
        assert entries['status.enabledState']['description'] == 'enabled'


class TestVirtualAddress(object):
    def test_CURDLE(self, request, mgmt_root):
        # Create and delete are handled by setup/teardown
        vac, va1 = setup_virtual_address_test(request, mgmt_root, 'va-1', 'Common')
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
