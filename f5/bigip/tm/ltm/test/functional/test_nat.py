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

from pprint import pprint as pp
import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from requests.exceptions import HTTPError


def delete_nat(bigip, name, partition):
    try:
        nat = bigip.ltm.nats.nat.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    nat.delete()


def setup_loadable_nat_test(request, bigip, nat):
    def teardown():
        delete_nat(bigip, 'nat1', 'Common')

    request.addfinalizer(teardown)

    nat1 = nat.create(name='nat1', partition='Common',
                      translationAddress='192.168.1.1',
                      originatingAddress='192.168.2.1')
    assert nat1.name == 'nat1'


def setup_create_test(request, bigip):
    def teardown():
        delete_nat(bigip, 'nat1', 'Common')
    request.addfinalizer(teardown)


def setup_create_two(request, bigip):
    def teardown():
        for name in ['nat1', 'nat2']:
            delete_nat(bigip, name, 'Common')
    request.addfinalizer(teardown)


class TestCreate(object):
    def test_create_two(self, request, bigip):
        setup_create_two(request, bigip)

        n1 = bigip.ltm.nats.nat.create(
            name='nat1', partition='Common',
            translationAddress='192.168.1.1',
            originatingAddress='192.168.2.1')
        n2 = bigip.ltm.nats.nat.create(
            name='nat2', partition='Common',
            translationAddress='192.168.1.2',
            originatingAddress='192.168.2.2')

        assert n1 is not n2
        assert n2.name != n1.name

    def test_create_no_args(self, bigip):
        '''Test that nat.create() with no options throws a ValueError '''
        with pytest.raises(MissingRequiredCreationParameter):
            bigip.ltm.nats.nat.create()

    def test_create_min_args(self, request, bigip):
        '''Test that nat.create() with only required arguments work.

        This will also test that the default values are set correctly and are
        part of the nat object after creating the instance on the BigIP
        '''
        setup_create_test(request, bigip)

        nat1 = bigip.ltm.nats.nat.create(
            name='nat1', partition='Common',
            translationAddress='192.168.1.1',
            originatingAddress='192.168.2.1')

        assert nat1.name == 'nat1'
        assert nat1.partition == 'Common'
        assert nat1.translationAddress == '192.168.1.1'
        assert nat1.originatingAddress == '192.168.2.1'
        assert nat1.generation is not None and isinstance(nat1.generation, int)
        assert nat1.fullPath == '/Common/nat1'
        assert nat1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/nat/~Common~nat1')
        # Default Values
        assert nat1.arp == 'enabled'
        assert nat1.autoLasthop == 'default'
        assert nat1.enabled is True
        assert nat1.inheritedTrafficGroup == 'true'
        assert nat1.trafficGroup == '/Common/traffic-group-1'
        assert nat1.unit is not None and isinstance(nat1.unit, int)
        assert nat1.vlansDisabled is True

    def test_create_arp_enabled(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        arp='enabled')
        assert n1.arp == 'enabled'

    def test_create_arp_disabled(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        arp='disabled')
        assert n1.arp == 'disabled'

    def test_create_autolasthop_default(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        autoLasthop='default')
        assert n1.autoLasthop == 'default'

    def test_create_autolasthop_enabled(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        autoLasthop='enabled')
        assert n1.autoLasthop == 'enabled'

    def test_create_autolasthop_disabled(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        autoLasthop='disabled')
        assert n1.autoLasthop == 'disabled'

    def test_create_enabled_true(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        enabled=True)
        assert n1.enabled is True

    def itest_create_enabled_false(self, request, bigip, NAT):
        '''Test that you can set enabled to false and create nat as disabled

        This will fail until some fixups are made to the create function for
        nat because in BIGIP you need to set disabled to True to disable it
        and not use enable at all.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        enabled=False)
        assert n1.enabled is False

    def test_create_disabled_true(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        disabled=True)
        assert n1.disabled is True

    def test_create_disabled_false(self, request, bigip, NAT):
        '''Test that you can set enabled to false and create nat as disabled

        This will fail until some fixups are made to the create function for
        nat because in BIGIP you need to set disabled to True to disable it
        and not use enable at all.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        disabled=False)
        pp(n1.raw)
        assert 'disabled' not in n1.raw
        assert n1.enabled is True
        n1.enabled = False
        n1.update()
        assert 'enabled' not in n1.raw
        assert n1.disabled is True

        n1.disabled = False
        n1.update()
        assert 'disabled' not in n1.raw
        assert n1.enabled is True

    def test_create_inheritedtrafficgroup_true(self, request, bigip, NAT):
        '''Test that you can set inheritedTrafficGroup to True on create

        This MUST be the string 'true' not the built-in True that you would
        think makes sense for a true/false setting like the other properties
        of NAT.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        inheritedTrafficGroup='true')
        assert n1.inheritedTrafficGroup == 'true'

    def test_create_inheritedtrafficgroup_false(self, request, bigip, NAT):
        '''Test that you can set inheritedTrafficGroup to True on create

        This MUST be the string 'false' not the built-in True that you would
        think makes sense for a true/false setting like the other properties
        of NAT.

        This also requires that the trafficGroup parameter also be set or the
        setting will not take effect on the system and silently be ignored.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        inheritedTrafficGroup='false',
                        trafficGroup='/Common/traffic-group-1')
        assert n1.inheritedTrafficGroup == 'false'

    def test_create_trafficgroup(self, request, bigip, NAT):
        '''Test that you can set the trafficgroup on create.

        Using the existing default group because we don't have the TG object
        done yet.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        trafficGroup='/Common/traffic-group-1')
        assert n1.trafficGroup == '/Common/traffic-group-1'

    def test_create_vlans_disabled(self, request, bigip, NAT):
        '''Test that you can set the VLANs that you want to disable

        The default setting is disabled so we want to add some VLANs to the
        disabled list.  We are using one of the built in VLAN lists.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        vlans=['/Common/http-tunnel'])
        assert len(n1.vlans) == 1
        assert '/Common/http-tunnel' in n1.vlans
        assert n1.vlansDisabled is True

    def test_create_vlans_enabled(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        vlansEnabled=True,
                        vlans=['/Common/http-tunnel'])
        assert len(n1.vlans) == 1
        assert '/Common/http-tunnel' in n1.vlans
        assert n1.vlansEnabled is True

    def test_create_vlansenabled_true(self, request, bigip, NAT):
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        vlansEnabled=True)
        assert n1.vlansEnabled is True

    def itest_create_vlansenabled_false(self, request, bigip, NAT):
        '''Test setting vlansEnabled to False on create

        This has the same issue as the enable/disable properties for the nat
        object.  You need to use the vlansEnabled property to enable them.
        '''
        setup_create_test(request, bigip)
        n1 = NAT.create(name='nat1', partition='Common',
                        translationAddress='192.168.1.1',
                        originatingAddress='192.168.2.1',
                        vlansEnabled=False)
        assert n1.vlansEnabled is False
        assert n1.vlansDisabled is True


class TestLoad(object):

    def test_load_no_object(self, NAT):
        with pytest.raises(HTTPError) as err:
            NAT.load(name='mynat', partition='Common')
            assert err.response.status == 404

    def test_load(self, request, bigip, NAT):
        setup_loadable_nat_test(request, bigip, NAT)
        n1 = bigip.ltm.nats.nat.load(name='nat1', partition='Common')
        assert n1.name == 'nat1'
        assert n1.partition == 'Common'
        assert isinstance(n1.generation, int)


class TestRefresh(object):

    def test_refresh(self, request, bigip, NAT):
        setup_loadable_nat_test(request, bigip, NAT)

        n1 = bigip.ltm.nats.nat.load(name='nat1', partition='Common')
        n2 = bigip.ltm.nats.nat.load(name='nat1', partition='Common')
        assert n1.arp == 'enabled'
        assert n2.arp == 'enabled'

        n2.update(arp='disabled')
        assert n2.arp == 'disabled'
        assert n1.arp == 'enabled'

        n1.refresh()
        assert n1.arp == 'disabled'


class TestDelete(object):

    def test_delete(self, request, bigip, NAT):
        setup_loadable_nat_test(request, bigip, NAT)
        n1 = bigip.ltm.nats.nat.load(name='nat1', partition='Common')
        n1.delete()
        del(n1)
        with pytest.raises(HTTPError) as err:
            bigip.ltm.nats.nat.load(name='nat1', partition='Common')
            assert err.response.status_code == 404


class TestUpdate(object):
    def test_update_with_args(self, request, bigip, NAT):
        setup_loadable_nat_test(request, bigip, NAT)
        n1 = bigip.ltm.nats.nat.load(name='nat1', partition='Common')
        assert n1.arp == 'enabled'
        n1.update(arp='disabled')
        assert n1.arp == 'disabled'

    def test_update_parameters(self, request, bigip, NAT):
        setup_loadable_nat_test(request, bigip, NAT)
        n1 = bigip.ltm.nats.nat.load(name='nat1', partition='Common')
        assert n1.arp == 'enabled'
        n1.arp = 'disabled'
        n1.update()
        assert n1.arp == 'disabled'
