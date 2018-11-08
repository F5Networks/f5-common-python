# Copyright 2017 F5 Networks Inc.
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

from distutils.version import LooseVersion
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.security.shared_objects import Address_List
from f5.bigip.tm.security.shared_objects import Port_List
from requests.exceptions import HTTPError


DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def addrlist(mgmt_root):
    a1 = mgmt_root.tm.security.shared_objects.address_lists.address_list.create(
        name='fake_addr', partition='Common', addresses=[{'name': '10.10.10.10'}])
    yield a1
    a1.delete()


@pytest.fixture(scope='function')
def portlist(mgmt_root):
    p1 = mgmt_root.tm.security.shared_objects.port_lists.port_list.create(
        name='fake_port', partition='Common', ports=[{'name': '80'}])
    yield p1
    p1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('14.0.0'),
    reason='This collection is fully implemented on 14.0.0 or greater.'
)
class TestAddressList(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        ac = mgmt_root.tm.security.shared_objects.address_lists
        with pytest.raises(MissingRequiredCreationParameter) as err:
            ac.address_list.create(name='fail', partition='Common')

        if LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'):
            error = "This resource requires at least one of the mandatory additional parameters to be provided: addressLists, addresses, geo"
            assert str(err.value) == error
        else:
            error = "This resource requires at least one of the mandatory additional parameters to be provided: addressLists, addresses, fqdns, geo"
            assert str(err.value) == error

    def test_create_req_args(self, addrlist):
        r1 = addrlist
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.shared_objects.address_lists.address_list.create(
            name='fake_addr', partition='Common', addresses=[{'name': '10.10.10.10'}], description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, addrlist):
        rc = mgmt_root.tm.security.shared_objects.address_lists
        r1 = addrlist
        r2 = rc.address_list.load(name='fake_addr', partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert hasattr(r2, 'description')
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.address_lists
        r1 = rc.address_list.create(name='delete_me', partition='Common',
                                    addresses=[{'name': '10.10.10.10'}])
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.address_list.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.address_lists
        with pytest.raises(HTTPError) as err:
            rc.address_list.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, addrlist):
        r1 = addrlist
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.shared_objects.address_lists
        r2 = rc.address_list.load(name='fake_addr', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_addrlst_collection(self, mgmt_root, addrlist):
        r1 = addrlist
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.shared_objects.address_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Address_List)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('14.0.0'),
    reason='This collection is fully implemented on 14.0.0 or greater.'
)
class TestPortList(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        ac = mgmt_root.tm.security.shared_objects.port_lists
        error_message = "This resource requires at least one of the mandatory additional parameters to be provided: portLists, ports"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            ac.port_list.create(name='fail', partition='Common')
        assert str(err.value) == error_message

    def test_create_req_args(self, portlist):
        r1 = portlist
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.shared_objects.port_lists.port_list.create(
            name='fake_port', partition='Common', ports=[{
                'name': '80'}], description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, portlist):
        rc = mgmt_root.tm.security.shared_objects.port_lists
        r1 = portlist
        r2 = rc.port_list.load(name='fake_port', partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description=DESC)
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists
        r1 = rc.port_list.create(name='delete_me', partition='Common',
                                 ports=[{'name': '80'}])
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.port_list.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.shared_objects.port_lists
        with pytest.raises(HTTPError) as err:
            rc.port_list.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, portlist):
        r1 = portlist
        URI = 'https://localhost/mgmt/tm/security/' \
              'shared-objects/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.shared_objects.port_lists
        r2 = rc.port_list.load(name='fake_port', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_portlist_collection(self, mgmt_root):
        rc = mgmt_root.tm.security.shared_objects.port_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Port_List)
