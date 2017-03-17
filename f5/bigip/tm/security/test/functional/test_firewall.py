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
import copy
import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.security.firewall import Address_List
from f5.bigip.tm.security.firewall import Port_List

from requests.exceptions import HTTPError
from six import iteritems

from distutils.version import LooseVersion

DESC = 'TESTADDED'


@pytest.fixture(scope='function')
def addrlst(mgmt_root):
    r1 = mgmt_root.tm.security.firewall.address_lists.address_list.create(
        name='fake_addr', partition='Common', addresses=[{
            'name': '10.10.10.10'}])
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def portlst(mgmt_root):
    r1 = mgmt_root.tm.security.firewall.port_lists.port_list.create(
        name='fake_port', partition='Common', ports=[{'name': '80'}])
    yield r1
    r1.delete()


class TestAddressList(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        ac = mgmt_root.tm.security.firewall.address_lists
        error_message = "This resource requires at least one of the " \
                        "mandatory additional " \
                        "parameters to be provided: set(['geo', 'addresses', "\
                        "'addressLists'])"
        error_message_v12 = "This resource requires at least one of the " \
                            "mandatory additional " \
                            "parameters to be provided: set(['addressLists', "\
                            "'geo', 'fqdns', 'addresses'])"
        with pytest.raises(MissingRequiredCreationParameter) as err:
            ac.address_list.create(name='fail', partition='Common')

        if LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
                '12.0.0'):
            assert err.value.message == error_message
        else:
            assert err.value.message == error_message_v12

    def test_create_req_args(self, addrlst):
        r1 = addrlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.firewall.address_lists.address_list.create(
            name='fake_addr', partition='Common', addresses=[{
                'name': '10.10.10.10'}], description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, addrlst):
        rc = mgmt_root.tm.security.firewall.address_lists
        r1 = addrlst
        r2 = rc.address_list.load(name='fake_addr', partition='Common')
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

    def test_modify(self, addrlst):
        original_dict = copy.copy(addrlst.__dict__)
        itm = 'description'
        addrlst.modify(description=DESC)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = addrlst.__dict__[k]
            elif k == itm:
                assert addrlst.__dict__[k] == DESC

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

    def test_load_and_update(self, mgmt_root, addrlst):
        r1 = addrlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.firewall.address_lists
        r2 = rc.address_list.load(name='fake_addr', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_addrlst_collection(self, mgmt_root, addrlst):
        r1 = addrlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/address-list/~Common~fake_addr'
        assert r1.name == 'fake_addr'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.firewall.address_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Address_List)


class TestPortList(object):
    def test_create_missing_mandatory_attr_raises(self, mgmt_root):
        ac = mgmt_root.tm.security.firewall.port_lists
        error_message = "This resource requires at least one of the " \
                        "mandatory additional " \
                        "parameters to be provided: set(['portLists', " \
                        "'ports'])"

        with pytest.raises(MissingRequiredCreationParameter) as err:
            ac.port_list.create(name='fail', partition='Common')
        assert err.value.message == error_message

    def test_create_req_args(self, portlst):
        r1 = portlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_opt_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.firewall.port_lists.port_list.create(
            name='fake_port', partition='Common', ports=[{
                'name': '80'}], description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r1.delete()

    def test_refresh(self, mgmt_root, portlst):
        rc = mgmt_root.tm.security.firewall.port_lists
        r1 = portlst
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

    def test_modify(self, portlst):
        original_dict = copy.copy(portlst.__dict__)
        itm = 'description'
        portlst.modify(description=DESC)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = portlst.__dict__[k]
            elif k == itm:
                assert portlst.__dict__[k] == DESC

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists
        r1 = rc.port_list.create(name='delete_me', partition='Common',
                                 ports=[{'name': '80'}])
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.port_list.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists
        with pytest.raises(HTTPError) as err:
            rc.port_list.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, portlst):
        r1 = portlst
        URI = 'https://localhost/mgmt/tm/security/' \
              'firewall/port-list/~Common~fake_port'
        assert r1.name == 'fake_port'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        rc = mgmt_root.tm.security.firewall.port_lists
        r2 = rc.port_list.load(name='fake_port', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_portlist_collection(self, mgmt_root):
        rc = mgmt_root.tm.security.firewall.port_lists.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Port_List)
