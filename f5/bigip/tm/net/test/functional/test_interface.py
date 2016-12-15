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


def cleanup_test(request, bigip):
    def teardown():
        for ifc in bigip.net.interfaces.get_collection():
            ifc.enabled = True
            ifc.update()
    request.addfinalizer(teardown)


class TestInterfaces(object):
    def test_interfaces_list(self, bigip):
        ifcs = bigip.net.interfaces.get_collection()
        assert len(ifcs)
        for ifc in ifcs:
            assert ifc.generation


class TestInterface(object):
    @pytest.mark.skip(
        'A known issue with generation number. '
        'See: https://github.com/F5Networks/f5-common-python/issues/334'
    )
    def test_RUL(self, request, bigip):
        cleanup_test(request, bigip)
        # We can't create or delete interfaces so we will load them to start
        ifc1 = bigip.net.interfaces.interface.load(name='1.1')
        ifc2 = bigip.net.interfaces.interface.load(name='1.1')
        assert ifc1.generation == ifc2.generation
        assert ifc1.name == ifc2.name

        # Update by disabling the interface
        ifc1.disabled = True
        ifc1.update()
        assert ifc1.disabled is True
        assert not hasattr(ifc1, 'enabled')
        assert ifc1.generation != ifc2.generation

        # Refresh ifc2
        ifc2.refresh()
        assert ifc2.disabled is True
        assert not hasattr(ifc2, 'enabled')
        assert ifc1.generation == ifc2.generation
