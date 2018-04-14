# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import copy
import pytest

from distutils.version import LooseVersion
from icontrol.session import iControlUnexpectedHTTPError
from six import iteritems

VERSIONS = [1, '1', '2c']
VERSIONS_AUTH = [3, '3']
AUTH_PASSWORD = 'P@ssw0rd1234'


def delete_resource(resources):
    for resource in resources.get_collection():
        resource.delete()


def setup_community_test(request, mgmt_root, partition, name):
    def teardown():
        delete_resource(s1)
    request.addfinalizer(teardown)
    s1 = mgmt_root.tm.sys.snmp.communities_s
    comm1 = s1.community.create(name=name, communityName=name,
                                partition=partition)
    return comm1, s1


def setup_user_test(**kwargs):
    def teardown():
        delete_resource(s1)
    request = kwargs.pop('request')
    mgmt_root = kwargs.pop('mgmt_root')
    kwargs['username'] = kwargs['name']

    request.addfinalizer(teardown)
    s1 = mgmt_root.tm.sys.snmp.users_s
    comm1 = s1.user.create(**kwargs)
    return comm1, s1


def setup_trap_test(**kwargs):
    def teardown():
        delete_resource(s1)
    request = kwargs.pop('request')
    mgmt_root = kwargs.pop('mgmt_root')
    kwargs['name'] = kwargs['community']
    request.addfinalizer(teardown)
    s1 = mgmt_root.tm.sys.snmp.traps_s
    comm1 = s1.trap.create(**kwargs)
    return comm1, s1


def setup_snmp_test(request, mr):
    def teardown():
        d.agentAddresses = ['tcp6:161', 'udp6:161']
        d.agentTrap = 'enabled'
        d.allowedAddresses = ['127.']
        d.authTrap = 'disabled'
        d.bigipTraps = 'enabled'
        d.loadMax1 = 12
        d.loadMax15 = 12
        d.loadMax5 = 12

        if pytest.config.getoption('--release') > LooseVersion('12.0.0'):
            d.snmpv1 = 'enable'
            d.snmpv2c = 'enable'

        d.sysContact = 'Customer Name <admin@customer.com>'
        d.sysLocation = 'Network Closet 1'
        d.sysServices = 78
        d.trapCommunity = 'public'

        if pytest.config.getoption('--release') >= LooseVersion('11.6.0'):
            d.trapSource = 'none'

        d.update()
    request.addfinalizer(teardown)
    d = mr.tm.sys.snmp.load()
    return d


class TestSnmp(object):
    def test_load(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        assert s1.agentAddresses == s2.agentAddresses
        assert s1.agentTrap == s2.agentTrap
        assert s1.allowedAddresses == s2.allowedAddresses
        assert s1.authTrap == s2.authTrap
        assert s1.bigipTraps == s2.bigipTraps
        assert s1.loadMax1 == s2.loadMax1
        assert s1.loadMax15 == s2.loadMax15
        assert s1.loadMax5 == s2.loadMax5

        if pytest.config.getoption('--release') > LooseVersion('12.0.0'):
            assert s1.snmpv1 == s2.snmpv1
            assert s1.snmpv2c == s2.snmpv2c

        assert s1.sysContact == s2.sysContact
        assert s1.sysLocation == s2.sysLocation
        assert s1.sysServices == s2.sysServices
        assert s1.trapCommunity == s1.trapCommunity

        if pytest.config.getoption('--release') >= LooseVersion('11.6.0'):
            assert s1.trapSource == s1.trapSource

    def test_update_agent_addresses(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.agentAddresses = ['tcp6:161']
        s1.update()
        assert ['tcp6:161'] == s1.agentAddresses
        assert ['tcp6.161'] != s2.agentAddresses

        # Refresh
        s2.refresh()
        assert ['tcp6:161'] == s2.agentAddresses

    def test_update_agent_trap(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.agentTrap = 'disabled'
        s1.update()
        assert 'disabled' == s1.agentTrap
        assert 'disabled' != s2.agentTrap

        # Refresh
        s2.refresh()
        assert 'disabled' == s2.agentTrap

    def test_update_allowed_addresses(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.allowedAddresses = ['192.168.1.1']
        s1.update()
        assert ['192.168.1.1'] == s1.allowedAddresses
        assert ['192.168.1.1'] != s2.allowedAddresses

        # Refresh
        s2.refresh()
        assert ['192.168.1.1'] == s2.allowedAddresses

    def test_update_auth_trap(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.authTrap = 'enabled'
        s1.update()
        assert 'enabled' == s1.authTrap
        assert 'enabled' != s2.authTrap

        # Refresh
        s2.refresh()
        assert 'enabled' == s2.authTrap

    def test_update_bigip_traps(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.bigipTraps = 'disabled'
        s1.update()
        assert 'disabled' == s1.bigipTraps
        assert 'disabled' != s2.bigipTraps

        # Refresh
        s2.refresh()
        assert 'disabled' == s2.bigipTraps

    def test_update_loadmax1(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.loadMax1 = 20
        s1.update()
        assert 20 == s1.loadMax1
        assert 20 != s2.loadMax1

        # Refresh
        s2.refresh()
        assert 20 == s2.loadMax1

    def test_update_loadmax5(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.loadMax5 = 20
        s1.update()
        assert 20 == s1.loadMax5
        assert 20 != s2.loadMax5

        # Refresh
        s2.refresh()
        assert 20 == s2.loadMax5

    def test_update_loadmax15(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.loadMax15 = 20
        s1.update()
        assert 20 == s1.loadMax15
        assert 20 != s2.loadMax15

        # Refresh
        s2.refresh()
        assert 20 == s2.loadMax15

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release'))
        < LooseVersion('12.0.0'),
        reason='Needs v12 TMOS or greater to pass.'
    )
    def test_update_snmpv1(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.snmpv1 = 'disabled'
        s1.update()
        assert 'disabled' == s1.snmpv1
        assert 'disabled' != s2.snmpv1

        # Refresh
        s2.refresh()
        assert 'disabled' == s2.snmpv1

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release'))
        < LooseVersion('12.0.0'),
        reason='Needs v12 TMOS or greater to pass.'
    )
    def test_update_snmpv2c(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.snmpv2c = 'disabled'
        s1.update()
        assert 'disabled' == s1.snmpv2c
        assert 'disabled' != s2.snmpv2c

        # Refresh
        s2.refresh()
        assert 'disabled' == s2.snmpv2c

    def test_update_sys_contact(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.sysContact = 'Customer Foo Bar'
        s1.update()
        assert 'Customer Foo Bar' == s1.sysContact
        assert 'Customer Foo Bar' != s2.sysContact

        # Refresh
        s2.refresh()
        assert 'Customer Foo Bar' == s2.sysContact

    def test_update_sys_location(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.sysLocation = 'Outer Planet'
        s1.update()
        assert 'Outer Planet' == s1.sysLocation
        assert 'Outer Planet' != s2.sysLocation

        # Refresh
        s2.refresh()
        assert 'Outer Planet' == s2.sysLocation

    def test_update_sys_services(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.sysServices = 20
        s1.update()
        assert 20 == s1.sysServices
        assert 20 != s2.sysServices

        # Refresh
        s2.refresh()
        assert 20 == s2.sysServices

    def test_update_trap_community(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.trapCommunity = 'foo'
        s1.update()
        assert 'foo' == s1.trapCommunity
        assert 'foo' != s2.trapCommunity

        # Refresh
        s2.refresh()
        assert 'foo' == s2.trapCommunity

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release'))
        < LooseVersion('11.6.0'),
        reason='Needs v11.6.0 TMOS or greater to pass.'
    )
    def test_update_trap_source(self, request, mgmt_root):
        s1 = setup_snmp_test(request, mgmt_root)
        s2 = setup_snmp_test(request, mgmt_root)

        s1.trapSource = '10.10.10.10'
        s1.update()
        assert '10.10.10.10' == s1.trapSource
        assert '10.10.10.10' != s2.trapSource

        # Refresh
        s2.refresh()
        assert '10.10.10.10' == s2.trapSource


class TestCommunity(object):
    def test_community_create_refresh_update_delete_load(
            self, request, mgmt_root, setup_device_snapshot
    ):
        comm1, s1 = setup_community_test(
            request, mgmt_root, 'Common', 'commtest1'
        )

        assert comm1.communityName == 'commtest1'

        # In 12.1.0 there seems to be an issue where selfLink and SNMP
        # Community object names returned when we create them (POST),
        # is different when we load them (GET) and provide partition as
        # parameter. Since simply doing refresh() won't cut it as we do not
        # pass on partition parameter we need to make few conditionals to
        # the asserts

        # In 11.6.1 and later they started prepending the partition name
        # to the name attribute here. So we handle this case for our tests.
        #
        # According to Narendra, they should always have behaved this way
        # so this must have been a bugfix

        if pytest.config.getoption('--release') < LooseVersion('11.6.1') or \
           pytest.config.getoption('--release') == LooseVersion('12.1.0'):
            assert comm1.name == 'commtest1'
        else:
            assert comm1.name == '/Common/commtest1'

        assert comm1.access == 'ro'
        assert comm1.ipv6 == 'disabled'

        comm1.ipv6 = 'enabled'
        comm1.source = '10.10.10.10'
        comm1.oidSubset = '.1.3.6.1.4.1.2021.4.1'
        comm1.access = 'rw'

        comm1.update()
        assert comm1.ipv6 == 'enabled'
        assert comm1.source == '10.10.10.10'
        assert comm1.oidSubset == '.1.3.6.1.4.1.2021.4.1'
        assert comm1.access == 'rw'

        comm1.ipv6 = ''
        comm1.source = ''
        comm1.oidSubset = ''
        comm1.access = ''

        comm1.refresh()
        assert comm1.ipv6 == 'enabled'
        assert comm1.source == '10.10.10.10'
        assert comm1.oidSubset == '.1.3.6.1.4.1.2021.4.1'
        assert comm1.access == 'rw'

        comm2 = s1.community.load(partition='Common', name='commtest1')

        if pytest.config.getoption('--release') == LooseVersion('12.1.0'):
            link1 = 'https://localhost/mgmt/tm/sys/snmp/communities/commtest1'
            link2 = 'https://localhost/mgmt/tm/sys/snmp/communities/' \
                    '~Common~commtest1'
            assert comm1.selfLink.startswith(link1)
            assert comm2.selfLink.startswith(link2)
        else:
            assert comm2.selfLink == comm1.selfLink

    def test_community_modify(self, request, mgmt_root, setup_device_snapshot):
        comm1, s1 = setup_community_test(
            request, mgmt_root, 'Common', 'modtest1'
        )
        original_dict = copy.copy(comm1.__dict__)
        commName = 'communityName'
        comm1.modify(communityName='footest1')
        for k, v in iteritems(original_dict):
            if k != commName:
                original_dict[k] = comm1.__dict__[k]
            elif k == commName:
                assert comm1.__dict__[k] == 'footest1'


class TestUser(object):
    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) > LooseVersion('12.0.0'),
        reason='Skip this test if v12.1.0 or above is set.'
    )
    def test_user_create_refresh_update_delete_load(
            self, request, mgmt_root, setup_device_snapshot
    ):
        user1, u1 = setup_user_test(
            request=request,
            mgmt_root=mgmt_root,
            partition='Common',
            name='usertest1',
            authProtocol='sha',
            privacyProtocol='aes',
            authPassword=AUTH_PASSWORD,
            privacyPassword=AUTH_PASSWORD
        )

        assert user1.access == 'ro'
        assert user1.authProtocol == 'sha'
        assert user1.privacyProtocol == 'aes'
        assert user1.securityLevel == 'auth-no-privacy'
        assert user1.username == 'usertest1'

        user1.access = 'rw'
        user1.authProtocol = 'md5'
        user1.oidSubset = '.1.3.6.1.4.1.2021.4.3'
        user1.privacyProtocol = 'des'
        user1.securityLevel = 'auth-privacy'

        user1.update()
        assert user1.access == 'rw'
        assert user1.authProtocol == 'md5'
        assert user1.oidSubset == '.1.3.6.1.4.1.2021.4.3'
        assert user1.privacyProtocol == 'des'
        assert user1.securityLevel == 'auth-privacy'

        user1.ipv6 = ''
        user1.source = ''
        user1.oidSubset = ''
        user1.access = ''

        user1.refresh()
        assert user1.access == 'rw'
        assert user1.authProtocol == 'md5'
        assert user1.oidSubset == '.1.3.6.1.4.1.2021.4.3'
        assert user1.privacyProtocol == 'des'

        user2 = u1.user.load(partition='Common', name='usertest1')

        assert user2.selfLink == user1.selfLink

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
        reason='Skip if the version is NOT 12.1.0 or above'
    )
    def test_user_create_refresh_delete_load_12_1_0(
        self, request, mgmt_root, setup_device_snapshot
    ):
        user1, u1 = setup_user_test(
            request=request,
            mgmt_root=mgmt_root,
            partition='Common',
            name='usertest1',
            authProtocol='sha',
            privacyProtocol='aes',
            authPassword=AUTH_PASSWORD,
            privacyPassword=AUTH_PASSWORD
            )

        assert user1.access == 'ro'
        assert user1.authProtocol == 'sha'
        assert user1.privacyProtocol == 'aes'
        assert user1.securityLevel == 'auth-no-privacy'
        assert user1.username == 'usertest1'

        user1.access = ''
        user1.authProtocol = ''
        user1.privacyProtocol = ''

        user1.refresh()
        assert user1.access == 'ro'
        assert user1.authProtocol == 'sha'
        assert user1.privacyProtocol == 'aes'

        user2 = u1.user.load(partition='Common', name='usertest1')

        link1 = 'https://localhost/mgmt/tm/sys/snmp/users/usertest1'
        link2 = 'https://localhost/mgmt/tm/sys/snmp/users/' \
                '~Common~usertest1'
        assert user1.selfLink.startswith(link1)
        assert user2.selfLink.startswith(link2)

    def test_user_modify(self, request, mgmt_root, setup_device_snapshot):
        user1, s1 = setup_user_test(
            request=request,
            mgmt_root=mgmt_root,
            partition='Common',
            name='moduser1',
            authProtocol='sha',
            privacyProtocol='aes',
            authPassword=AUTH_PASSWORD,
            privacyPassword=AUTH_PASSWORD
        )
        original_dict = copy.copy(user1.__dict__)
        accessName = 'access'
        user1.modify(access='rw')
        for k, v in iteritems(original_dict):
            if k != accessName:
                original_dict[k] = user1.__dict__[k]
            elif k == accessName:
                assert user1.__dict__[k] == 'rw'


class TestTrap(object):
    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) > LooseVersion('12.0.0'),
        reason='Skip this test if v12.1.0 or above is set.'
    )
    def test_trap_create_refresh_update_delete_load(self, request, mgmt_root, setup_device_snapshot):
        trap1, t1 = setup_trap_test(
            request=request,
            mgmt_root=mgmt_root,
            partition='Common',
            community='traptest1',
            host='10.10.10.10',
            port=1234
        )

        assert trap1.community == 'traptest1'
        assert trap1.host == '10.10.10.10'
        assert trap1.port == 1234
        assert trap1.securityLevel == 'no-auth-no-privacy'
        assert trap1.version == '2c'

        trap1.community = 'traptest1a'
        trap1.host = '20.20.20.20'
        trap1.port = 4321
        trap1.version = '1'
        trap1.securityLevel = 'no-auth-no-privacy'
        trap1.update()
        assert trap1.community == 'traptest1a'
        assert trap1.host == '20.20.20.20'
        assert trap1.port == 4321
        assert trap1.version == '1'

        trap1.community = ''
        trap1.host = ''
        trap1.port = ''
        trap1.version = ''

        trap1.refresh()
        assert trap1.community == 'traptest1a'
        assert trap1.host == '20.20.20.20'
        assert trap1.port == 4321
        assert trap1.version == '1'

        trap2 = t1.trap.load(partition='Common', name='traptest1')
        assert trap2.selfLink == trap1.selfLink

    @pytest.mark.skipif(
        LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
        reason='Skip if the version is NOT 12.1.0 or above'
    )
    def test_trap_create_refresh_delete_load_12_1_0(self, request, mgmt_root, setup_device_snapshot):
        trap1, t1 = setup_trap_test(
            request=request,
            mgmt_root=mgmt_root,
            partition='Common',
            community='traptest1',
            host='10.10.10.10',
            port=1234
            )

        assert trap1.community == 'traptest1'
        assert trap1.host == '10.10.10.10'
        assert trap1.port == 1234
        assert trap1.securityLevel == 'no-auth-no-privacy'
        assert trap1.version == '2c'

        trap1.community = ''
        trap1.host = ''
        trap1.port = ''
        trap1.version = ''

        trap1.refresh()
        assert trap1.community == 'traptest1'
        assert trap1.host == '10.10.10.10'
        assert trap1.port == 1234
        assert trap1.version == '2c'

        trap2 = t1.trap.load(partition='Common', name='traptest1')

        link1 = 'https://localhost/mgmt/tm/sys/snmp/traps/traptest1'

        link2 = 'https://localhost/mgmt/tm/sys/snmp/traps/~Common~traptest1'

        assert trap1.selfLink.startswith(link1)
        assert trap2.selfLink.startswith(link2)

    def test_trap_create_bad_version(self, request, mgmt_root, setup_device_snapshot):
        badVals = ['ads', 12, '12', '#^$%&#%', '', -1, '-1']
        for badVal in badVals:
            with pytest.raises(iControlUnexpectedHTTPError) as err:
                trap1, t1 = setup_trap_test(
                    request=request,
                    mgmt_root=mgmt_root,
                    partition='Common',
                    community='traptest1',
                    host='10.10.10.10',
                    port=1234,
                    version=badVal
                )
            assert 'expected one of the following' in str(err.value)

    def test_trap_create_bad_port(self, request, mgmt_root, setup_device_snapshot):
        """Test digit service ports

        The port can be a valid digit between 0 and 65,535. This matches
        what one would expect to find in the Web UI

        :param request:
        :param mgmt_root:
        :param setup_device_snapshot:
        :return:
        """
        badVals = ['asd', 65536, '#^$%&#%', '', -1, '-1']
        for idx1, version in enumerate(VERSIONS):
            for idx2, badVal in enumerate(badVals):
                with pytest.raises(iControlUnexpectedHTTPError) as err:
                    trap1, t1 = setup_trap_test(
                        request=request,
                        mgmt_root=mgmt_root,
                        partition='Common',
                        community='traptest-bv-port-%s-%s' % (idx1, idx2),
                        host='10.10.10.10',
                        port=badVal,
                        version=version
                    )
                assert 'invalid or ambiguous service' in str(err.value)

    def test_trap_create_named_port(self, request, mgmt_root, setup_device_snapshot):
        """Test named service ports

        The port can be a valid service name instead of a digit. This differs
        from the Web UI where it expects it to be a digit.

        :param request:
        :param mgmt_root:
        :param setup_device_snapshot:
        :return:
        """
        vals = ['ads', 'smtp', 'http', 'kerberos', 'pop3']
        for idx1, version in enumerate(VERSIONS):
            for idx2, val in enumerate(vals):
                trap1, t1 = setup_trap_test(
                    request=request,
                    mgmt_root=mgmt_root,
                    partition='Common',
                    community='traptest-name-port-%s-%s' % (idx1, idx2),
                    host='10.10.10.10',
                    port=val,
                    version=version
                )

    def test_trap_create_named_port_v3(self, request, mgmt_root, setup_device_snapshot):
        """Test named service ports

        The port can be a valid service name instead of a digit. This differs
        from the Web UI where it expects it to be a digit.

        :param request:
        :param mgmt_root:
        :param setup_device_snapshot:
        :return:
        """
        vals = ['ads', 'smtp', 'http', 'kerberos', 'pop3']
        for idx1, version in enumerate(VERSIONS_AUTH):
            for idx2, val in enumerate(vals):
                trap1, t1 = setup_trap_test(
                    request=request,
                    mgmt_root=mgmt_root,
                    partition='Common',
                    community='traptest-name-port-%s-%s' % (idx1, idx2),
                    host='10.10.10.10',
                    port=val,
                    version=version,
                    securityLevel='auth-no-privacy',
                    securityName='foo',
                    authProtocol='md5',
                    authPassword=AUTH_PASSWORD
                )

    def test_trap_modify(self, request, mgmt_root, setup_device_snapshot):
        trap1, u1 = setup_trap_test(
            request=request,
            mgmt_root=mgmt_root,
            partition='Common',
            community='modtest1',
            host='10.10.10.10',
            port='1234'
        )
        original_dict = copy.copy(trap1.__dict__)
        host = 'host'
        trap1.modify(host='20.20.20.20')
        for k, v in iteritems(original_dict):
            if k != host:
                original_dict[k] = trap1.__dict__[k]
            elif k == host:
                assert trap1.__dict__[k] == '20.20.20.20'
