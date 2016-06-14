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

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingUpdateParameter
from icontrol.session import iControlUnexpectedHTTPError
from requests.exceptions import HTTPError

DESCRIPTION = "TESTDESCRIPTION"


def delete_vlan(bigip, name, partition):
    try:
        v = bigip.net.vlans.vlan.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    v.delete()


def setup_basic_test(request, bigip, name, partition):
    def teardown():
        delete_vlan(bigip, name, partition)

    teardown()
    v = bigip.net.vlans.vlan.create(name=name, partition=partition)
    request.addfinalizer(teardown)
    return v


def setup_interfaces_test(request, bigip, name, partition, iname='1.1'):
    v = setup_basic_test(request, bigip, name, partition)
    i = v.interfaces_s.interfaces.create(name=iname)
    return i, v


def setup_vlan_collection_get_test(request, bigip):
    def teardown():
        vc = bigip.net.vlans
        for v in vc.get_collection():
            v.delete()
    request.addfinalizer(teardown)


class TestVLANInterfacesCollection(object):
    def test_get_collection(self, request, bigip):
        # Setup will create a VLAN and one interfaces
        v1 = setup_basic_test(request, bigip, 'v1', 'Common')
        v1.interfaces_s.interfaces.create(name='1.1')
        ifcs = v1.interfaces_s.get_collection()
        i2 = ifcs[0]
        assert len(ifcs) is 1
        assert ifcs[0].name == '1.1'
        i2.delete()
        ifcs = v1.interfaces_s.get_collection()
        assert len(ifcs) is 0


class TestVLANInterfaces(object):
    def test_create_interfaces(self, request, bigip):
        i, _ = setup_interfaces_test(request, bigip, 'v1', 'Common')
        assert i.name == '1.1'

    def test_update_exclusive_attrs(self, request, bigip):
        '''Test that we remove the other exclusive args if we set one.

        The default interfaces that is made has the vlans set to tagged.
        We change it to untagged and make sure that the tagged is no longer
        an attribute.
        '''
        ifc, _ = setup_interfaces_test(request, bigip, 'somevlan', 'Common')
        ifc.untagged = True
        assert not hasattr(ifc, 'tagged')
        ifc.update()
        assert ifc.untagged is True
        ifc.tagged = True
        ifc.tagMode = 'service'
        assert not hasattr(ifc, 'untagged')
        ifc.update()
        assert ifc.tagged is True

    def test_update(self, request, bigip):
        i, _ = setup_interfaces_test(request, bigip, 'v1', 'Common')
        i.update(untagged=True)
        assert not hasattr(i, 'tagged')
        assert i.untagged is True

    def test_update_mixed_attr_set(self, request, bigip):
        '''Test that we get an Exception because we have both exclusives set.

        This only happens when the user sets the attribute and then does the
        update with the other attribute set.  We don't actually know which one
        the user wants to set.
        '''
        i, _ = setup_interfaces_test(request, bigip, 'v1', 'Common')
        i.untagged = True
        assert not hasattr(i, 'tagged')
        assert i.untagged is True
        with pytest.raises(iControlUnexpectedHTTPError) as err:
            i.update(tagged=True, tagMode='service')
            assert err.response.status_code == 400
            assert "may not be specified with" in err.response.text

    def test_update_without_tagmode(self, request, bigip):
        i, _ = setup_interfaces_test(request, bigip, 'v1', 'Common')
        i.tagged = True
        with pytest.raises(MissingUpdateParameter):
            i.update()

    def test_load(self, request, bigip):
        i1, v = setup_interfaces_test(request, bigip, 'v1', 'Common')
        i2 = v.interfaces_s.interfaces.load(name='1.1')
        assert i1.name == i2.name
        assert i1.generation == i2.generation


class TestVLANCollection(object):
    def test_get_collection(self, request, bigip):
        setup_vlan_collection_get_test(request, bigip)
        vlans = ['v1', 'v2', 'v3']
        for vlan in vlans:
            bigip.net.vlans.vlan.create(name=vlan)
        vc = bigip.net.vlans.get_collection()
        assert len(vc) == 3
        for v in vc:
            assert v.name in vlans


class TestVLAN(object):
    def test_create_no_args(self, bigip):
        v1 = bigip.net.vlans.vlan
        with pytest.raises(MissingRequiredCreationParameter):
            v1.create()

    def test_CURDL(self, request, bigip):
        setup_vlan_collection_get_test(request, bigip)
        # Create a VLAN and verify some of the attributes
        v1 = bigip.net.vlans.vlan.create(name='v1', partition='Common')
        v1.interfaces_s.interfaces.create(
            name='1.1', tagged=True, tagMode='service')
        v1_ifcs = v1.interfaces_s.get_collection()
        gen1 = v1.generation
        assert v1.name == 'v1'
        assert hasattr(v1, 'generation') and isinstance(v1.generation, int)
        assert len(v1_ifcs) == 1
        assert v1_ifcs[0].name == '1.1'

        # Update it
        v1.description = DESCRIPTION
        v1.update()
        gen2 = v1.generation
        assert hasattr(v1, 'description')
        assert v1.description == DESCRIPTION
        assert gen2 > gen1

        # Refresh it
        v1.refresh()
        assert v1.generation == gen2

        # Load into a new variable
        v2 = bigip.net.vlans.vlan.load(name='v1', partition='Common')

        # Update v1 again
        v1.description = DESCRIPTION + DESCRIPTION
        v1.update()
        assert v1.generation > gen2
        assert v1.generation > v2.generation
        assert v2.description == DESCRIPTION
        assert v1.description == DESCRIPTION + DESCRIPTION

    def test_load_subcollection_(self, request, bigip):
        '''This tests for issue #148.

        Test that we we load a vlan object we can see the sub-s
        '''
        setup_interfaces_test(request, bigip, 'v1', 'Common')
        v2 = bigip.net.vlans.vlan.load(name='v1', partition='Common')
        v2_ifcs = v2.interfaces_s.get_collection()
        assert len(v2_ifcs) == 1
