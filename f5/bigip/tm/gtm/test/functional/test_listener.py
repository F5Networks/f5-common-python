# Copyright 2015 F5 Networks Inc.
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

from distutils.version import LooseVersion
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.gtm.listener import Listener
from pytest import symbols
from requests.exceptions import HTTPError
from six import iteritems

pytestmark = pytest.mark.skipif(
    symbols
    and hasattr(symbols, 'modules')
    and not symbols.modules['gtm'],
    reason='The modules symbol for GTM is set to False.'
)


def delete_listener(mgmt_root, name, partition):
    try:
        foo = mgmt_root.tm.gtm.listeners.listener.load(name=name,
                                                       partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_create_test(request, mgmt_root, name, partition):
    def teardown():
        delete_listener(mgmt_root, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, address, partition):
    def teardown():
        delete_listener(mgmt_root, name, partition)

    reg1 = mgmt_root.tm.gtm.listeners.listener.create(name=name,
                                                      address=address,
                                                      partition=partition)
    request.addfinalizer(teardown)
    return reg1


class TestCreate(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.gtm.listeners.listener.create()

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_listener', 'Common')
        reg1 = mgmt_root.tm.gtm.listeners.listener.create(
            name='fake_listener', partition='Common', address='10.10.10.10')
        assert reg1.name == 'fake_listener'
        assert reg1.partition == 'Common'
        assert reg1.address == '10.10.10.10'
        assert reg1.generation and isinstance(reg1.generation, int)
        assert reg1.kind == 'tm:gtm:listener:listenerstate'
        assert reg1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/listener/~Common~fake_listener')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake_listener', 'Common')
        reg1 = mgmt_root.tm.gtm.listeners.listener.create(
            name='fake_listener', partition='Common', address='10.10.10.10',
            description='NewListener')
        assert hasattr(reg1, 'description')
        assert reg1.description == 'NewListener'

    def test_create_duplicate(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_listener',
                         '10.10.10.10', 'Common')
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.listeners.listener.create(
                name='fake_listener', partition='Common',
                address='10.10.10.10')
        assert err.value.response.status_code == 409


class TestRefresh(object):
    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_listener',
                         '10.10.10.10', 'Common')
        r1 = mgmt_root.tm.gtm.listeners.listener.load(
            name='fake_listener', partition='Common')
        r2 = mgmt_root.tm.gtm.listeners.listener.load(
            name='fake_listener', partition='Common')

        assert r1.name == 'fake_listener'
        assert r2.name == 'fake_listener'

        r2.update(description='NewListener')
        assert hasattr(r2, 'description')
        assert not hasattr(r1, 'description')
        assert r2.description == 'NewListener'
        r1.refresh()
        assert hasattr(r1, 'description')
        assert r1.description == 'NewListener'


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.listeners.listener.load(
                name='fake_listener', partition='Common')
        if LooseVersion(pytest.config.getoption('--release')) >= \
                LooseVersion('12.0.0'):
            assert err.value.response.status_code == 400
        else:
            assert err.value.response.status_code == 500

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake_listener',
                         '10.10.10.10', 'Common')
        r1 = mgmt_root.tm.gtm.listeners.listener.load(
            name='fake_listener', partition='Common')
        assert r1.name == 'fake_listener'
        assert not hasattr(r1, 'description')
        r1.update(description='NewListener')
        assert hasattr(r1, 'description')
        assert r1.description == 'NewListener'

        r2 = mgmt_root.tm.gtm.listeners.listener.load(
            name='fake_listener', partition='Common')
        assert hasattr(r2, 'description')
        assert r2.description == 'NewListener'


class TestUpdate(object):
    def test_update(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                              '10.10.10.10', 'Common')
        assert r1.name == 'fake_listener'
        assert not hasattr(r1, 'description')
        r1.update(description='NewListener')
        assert hasattr(r1, 'description')
        assert r1.description == 'NewListener'


class TestModify(object):
    def test_modify(self, request, mgmt_root):
        r1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                              '10.10.10.10', 'Common')
        original_dict = copy.copy(r1.__dict__)
        value = 'description'
        r1.modify(description='NewListener')
        for k, v in iteritems(original_dict):
            if k != value:
                original_dict[k] = r1.__dict__[k]
            elif k == value:
                assert r1.__dict__[k] == 'NewListener'


class TestDelete(object):
    def test_delete(self, request, mgmt_root):
        r1 = mgmt_root.tm.gtm.listeners.listener.create(
            name='fake_listener', address='10.10.10.10')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.listeners.listener.load(
                name='fake_region', partition='Common')
        if LooseVersion(pytest.config.getoption('--release')) >= \
                LooseVersion('12.0.0'):
            assert err.value.response.status_code == 400
        else:
            assert err.value.response.status_code == 500


class TestListenerCollection(object):
    def test_listener_collection(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        assert reg1.name == 'fake_listener'
        assert reg1.partition == 'Common'
        assert reg1.address == '10.10.10.10'
        assert reg1.generation and isinstance(reg1.generation, int)
        assert reg1.kind == 'tm:gtm:listener:listenerstate'
        assert reg1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/listener/~Common~fake_listener')

        rc = mgmt_root.tm.gtm.listeners.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Listener)


class TestProfile(object):
    def test_load_missing_args(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        profcol = reg1.profiles_s.get_collection()
        prname = str(profcol[0].name)
        with pytest.raises(MissingRequiredReadParameter):
            reg1.profiles_s.profile.load(name=prname)

    def test_load(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        profcol = reg1.profiles_s.get_collection()
        prname = str(profcol[0].name)
        prpart = str(profcol[0].partition)
        pr1 = reg1.profiles_s.profile.load(name=prname, partition=prpart)
        assert pr1.kind == 'tm:gtm:listener:profiles:profilesstate'
        assert pr1.selfLink.startswith('https://localhost/mgmt/tm/gtm/listener'
                                       '/~Common~fake_listener/profiles/'
                                       '~Common~dns')

    def test_refresh(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        profcol = reg1.profiles_s.get_collection()
        prname = str(profcol[0].name)
        prpart = str(profcol[0].partition)
        pr1 = reg1.profiles_s.profile.load(name=prname, partition=prpart)
        assert pr1.kind == 'tm:gtm:listener:profiles:profilesstate'
        assert pr1.selfLink.startswith('https://localhost/mgmt/tm/gtm/listener'
                                       '/~Common~fake_listener/profiles/'
                                       '~Common~dns')
        pr2 = reg1.profiles_s.profile.load(name=prname, partition=prpart)
        pr1.refresh()
        assert pr1.kind == pr2.kind
        assert pr1.selfLink == pr2.selfLink
        pr2.refresh()
        assert pr2.kind == pr1.kind
        assert pr2.selfLink == pr1.selfLink

    def test_create_raises(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        with pytest.raises(UnsupportedOperation):
            reg1.profiles_s.profile.create()

    def test_modify_raises(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        with pytest.raises(UnsupportedOperation):
            reg1.profiles_s.profile.modify()

    def test_update_raises(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        with pytest.raises(UnsupportedOperation):
            reg1.profiles_s.profile.update()

    def test_delete_raises(self, request, mgmt_root):
        reg1 = setup_basic_test(request, mgmt_root, 'fake_listener',
                                '10.10.10.10', 'Common')
        with pytest.raises(UnsupportedOperation):
            reg1.profiles_s.profile.delete()
