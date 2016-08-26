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

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from icontrol.session import iControlUnexpectedHTTPError

import copy
import pytest


try:
    vcmp_host = pytest.config.getoption('--vcmp-host')
except Exception as ex:
    vcmp_host = None


@pytest.fixture
def setup_guest_test(request, vcmp_host):
    def teardown():
        guest.delete()
    request.addfinalizer(teardown)
    guests = vcmp_host.tm.vcmp.guests
    guest = guests.guest.create(name='test')
    return guests, guest


@pytest.mark.skipif(vcmp_host is None,
                    reason='Provide --vcmp-host to run vcmp tests.')
class TestGuest(object):
    def test_guests_get_collection(self, setup_guest_test):
        guests, guest1 = setup_guest_test
        gc = list(guests.get_collection())
        assert len(gc) > 1

    def test_guest_create_refresh_update_delete_load_modify(
            self, setup_guest_test
    ):
        guests, guest1 = setup_guest_test
        assert guest1.name == 'test'
        assert guest1.managementNetwork == 'bridged'
        guest1.managementGw = '10.190.0.1'
        guest1.update()
        assert guest1.managementGw == '10.190.0.1'
        old_sslmode = guest1.sslMode
        guest1.sslMode = 'dedicated'
        guest1.refresh()
        assert guest1.sslMode == old_sslmode
        guest2 = guests.guest.load(name='test')
        assert guest1.selfLink == guest2.selfLink
        guest2.modify(sslMode='dedicated')
        guest1.refresh()
        assert guest2.sslMode == guest1.sslMode

    def test_guest_modify(self, setup_guest_test):
        guests, guest1 = setup_guest_test
        original_dict = copy.copy(guest1.__dict__)
        gw = 'managementGw'
        guest1.modify(managementGw='10.190.0.1')
        for k, v in original_dict.items():
            if k != gw:
                original_dict[k] = guest1.__dict__[k]
            elif k == gw:
                guest1.__dict__[k] == '10.190.0.1'

    def test_guest_no_creation_args(self, vcmp_host):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            vcmp_host.tm.vcmp.guests.guest.create()
        assert 'name' in ex.value.message

    def test_guest_bad_creation_args(self, vcmp_host):
        with pytest.raises(iControlUnexpectedHTTPError) as ex:
            vcmp_host.tm.vcmp.guests.guest.create(
                name='test', partition='Common')
        assert '(/Common/test) is invalid' in ex.value.message

    def test_guest_no_load_args(self, vcmp_host):
        with pytest.raises(MissingRequiredReadParameter) as ex:
            vcmp_host.tm.vcmp.guests.guest.load()
        assert 'name' in ex.value.message

    def test_guest_bad_load_args(self, vcmp_host):
        with pytest.raises(iControlUnexpectedHTTPError) as ex:
            vcmp_host.tm.vcmp.guests.guest.load(
                name='test', partition='test-bad-arg')
        assert 'The requested VCMP (/test-bad-arg/test) was not found' in \
            ex.value.message

    def test_guest_bad_modify(self, setup_guest_test):
        guests, guest1 = setup_guest_test
        with pytest.raises(iControlUnexpectedHTTPError) as ex:
            guest1.modify(generation=34)
        assert 'one or more properties must be specified' in ex.value.message
