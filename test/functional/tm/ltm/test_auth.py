# coding=utf-8
#
#  Copyright 2014-2016 F5 Networks Inc.
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
from f5.bigip.tm.ltm.auth import Crldp_Server
from f5.bigip.tm.ltm.auth import Kerberos_Delegation
from f5.bigip.tm.ltm.auth import Ldap
from f5.bigip.tm.ltm.auth import Ocsp_Responder
from f5.bigip.tm.ltm.auth import Profile
from f5.bigip.tm.ltm.auth import Radius
from f5.bigip.tm.ltm.auth import Radius_Server
from f5.bigip.tm.ltm.auth import Ssl_Cc_Ldap
from f5.bigip.tm.ltm.auth import Ssl_Crldp
from f5.bigip.tm.ltm.auth import Ssl_Ocsp
from f5.bigip.tm.ltm.auth import Tacacs
from pprint import pprint as pp
import pytest
from requests.exceptions import HTTPError
TESTDESCRIPTION = "TESTDESCRIPTION"
pp(__file__)


def delete_dependency(mgmt_root, name):
    try:
        foo = mgmt_root.tm.ltm.auth.ssl_cc_ldaps.ssl_cc_ldap.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_dependency(request, mgmt_root, name, **kwargs):
    def teardown():
        delete_dependency(mgmt_root, name)
    delete_dependency(mgmt_root, name)
    res = mgmt_root.tm.ltm.auth.ssl_cc_ldaps.ssl_cc_ldap.create(name=name,
                                                                **kwargs)
    request.addfinalizer(teardown)
    return res


# Helper class to limit code repetition
class HelperTest(object):
    def __init__(self, collection_name):
        self.partition = 'Common'
        self.lowered = collection_name.lower()
        self.test_name = 'fake_' + self.urielementname()
        self.authkinds = {
            'crldp_server': 'tm:ltm:auth:crldp-server:crldp-serverstate',
            'kerberos_delegation':
                'tm:ltm:auth:kerberos-delegation:kerberos-delegationstate',
            'ldap': 'tm:ltm:auth:ldap:ldapstate',
            'ocsp_responder': 'tm:ltm:auth:ocsp-responder:ocsp-responderstate',
            'profile': 'tm:ltm:auth:profile:profilestate',
            'radius': 'tm:ltm:auth:radius:radiusstate',
            'radius_server': 'tm:ltm:auth:radius-server:radius-serverstate',
            'ssl_cc_ldap': 'tm:ltm:auth:ssl-cc-ldap:ssl-cc-ldapstate',
            'ssl_crldp': 'tm:ltm:auth:ssl-crldp:ssl-crldpstate',
            'ssl_ocsp': 'tm:ltm:auth:ssl-ocsp:ssl-ocspstate',
            'tacacs': 'tm:ltm:auth:tacacs:tacacsstate'
            }

    def urielementname(self):
        if self.lowered[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        return self.lowered[:-endind]

    def delete_resource(self, resource):
        try:
            foo = resource.load(name=self.test_name, partition=self.partition)
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            return
        foo.delete()

    def setup_test(self, request, mgmt_root, **kwargs):
        def teardown():
            self.delete_resource(resource)

        resourcecollection = \
            getattr(getattr(getattr(mgmt_root.tm, 'ltm'), 'auth'),
                    self.lowered)
        resource = getattr(resourcecollection, self.urielementname())
        self.delete_resource(resource)
        created = resource.create(name=self.test_name,
                                  partition=self.partition,
                                  **kwargs)
        request.addfinalizer(teardown)
        return created, resourcecollection

    def test_MCURDL(self, request, mgmt_root, **kwargs):
        # Testing create
        authres, authcollection = self.setup_test(request, mgmt_root, **kwargs)
        assert authres.name == self.test_name
        assert authres.fullPath == '/Common/'+self.test_name
        assert authres.generation and isinstance(authres.generation, int)
        assert authres.kind == self.authkinds[self.urielementname()]

        # Testing update
        authres.description = TESTDESCRIPTION
        pp(authres.raw)
        authres.update()
        assert hasattr(authres, 'description')
        assert authres.description == TESTDESCRIPTION

        # Testing refresh
        authres.description = ''
        authres.refresh()
        assert hasattr(authres, 'description')
        assert authres.description == TESTDESCRIPTION

        # Testing modify
        meta_data = authres.__dict__.pop('_meta_data')
        start_dict = copy.deepcopy(authres.__dict__)
        authres.__dict__['_meta_data'] = meta_data
        authres.modify(description='MODIFIED')
        desc = 'description'
        for k, v in authres.__dict__.items():
            if k != desc:
                start_dict[k] = authres.__dict__[k]
                assert getattr(authres, k) == start_dict[k]
            elif k == desc:
                assert getattr(authres, desc) == 'MODIFIED'

        # Testing load
        a2 = getattr(authcollection, self.urielementname())
        authres2 = a2.load(partition=self.partition, name=self.test_name)
        assert authres.selfLink == authres2.selfLink

    def test_collection(self, request, mgmt_root, **kwargs):
        authres, authcollection = self.setup_test(request, mgmt_root, **kwargs)
        assert authres.name == self.test_name
        assert authres.fullPath == '/Common/' + self.test_name
        assert authres.generation and isinstance(authres.generation, int)
        assert authres.kind == self.authkinds[self.urielementname()]

        coll = authcollection.get_collection()
        assert isinstance(coll, list)
        assert len(coll)

        if self.lowered == 'crldp_servers':
            assert isinstance(coll[0], Crldp_Server)
        elif self.lowered == 'kerberos_delegations':
            assert isinstance(coll[0], Kerberos_Delegation)
        elif self.lowered == 'ldaps':
            assert isinstance(coll[0], Ldap)
        elif self.lowered == 'ocsp_responders':
            assert isinstance(coll[0], Ocsp_Responder)
        elif self.lowered == 'profiles':
            assert isinstance(coll[0], Profile)
        elif self.lowered == 'radius_s':
            assert isinstance(coll[0], Radius)
        elif self.lowered == 'radius_server_s':
            assert isinstance(coll[0], Radius_Server)
        elif self.lowered == 'ssl_cc_ldaps':
            assert isinstance(coll[0], Ssl_Cc_Ldap)
        elif self.lowered == 'ssl_crldps':
            assert isinstance(coll[0], Ssl_Crldp)
        elif self.lowered == 'ssl_ocsps':
            assert isinstance(coll[0], Ssl_Ocsp)
        elif self.lowered == 'tacacs':
            assert isinstance(coll[0], Tacacs)

    def test_profile_MCRDL(self, request, mgmt_root, **kwargs):
        # Testing create
        authres, authcollection = self.setup_test(request, mgmt_root, **kwargs)
        assert authres.name == self.test_name
        assert authres.fullPath == '/Common/' + self.test_name
        assert authres.generation and isinstance(authres.generation, int)
        assert authres.kind == self.authkinds[self.urielementname()]
        assert authres.idleTimeout == 300

        # Testing refresh
        authres.idleTimeout = 0
        authres.refresh()
        assert hasattr(authres, 'idleTimeout')
        assert authres.idleTimeout == 300

        # Testing modify
        meta_data = authres.__dict__.pop('_meta_data')
        start_dict = copy.deepcopy(authres.__dict__)
        authres.__dict__['_meta_data'] = meta_data
        authres.modify(idleTimeout=100)
        desc = 'idleTimeout'
        for k, v in authres.__dict__.items():
            if k != desc:
                start_dict[k] = authres.__dict__[k]
                assert getattr(authres, k) == start_dict[k]
            elif k == desc:
                assert getattr(authres, desc) == 100

        # Testing load
        a2 = getattr(authcollection, self.urielementname())
        authres2 = a2.load(partition=self.partition, name=self.test_name)
        assert authres.selfLink == authres2.selfLink


class TestCrldpServer(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Crldp_Servers')
        auth.test_MCURDL(request, mgmt_root, host='10.10.10.10')

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Crldp_Servers')
        auth.test_collection(request, mgmt_root, host='10.10.10.10')


@pytest.mark.skipif(True, reason='this depends on an optional module')
class TestKerberosDelegation(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Kerberos_Delegations')
        auth.test_MCURDL(request, mgmt_root,
                         serverPrincipal='HTTP/fake.com',
                         clientPrincipal='HTTP/faketoo.com')

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Kerberos_Delegations')
        auth.test_collection(request, mgmt_root,
                             serverPrincipal='HTTP/fake.com',
                             clientPrincipal='HTTP/faketoo.com')


@pytest.mark.skipif(True, reason='this depends on an optional module')
class TestLdap(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Ldaps')
        auth.test_MCURDL(request, mgmt_root, servers=['10.10.10.10'])

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Ldaps')
        auth.test_collection(request, mgmt_root, servers=['10.10.10.10'])


class TestOcspResponder(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Ocsp_Responders')
        auth.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Ocsp_Responders')
        auth.test_collection(request, mgmt_root)


class TestProfile(object):
    def test_MCURDL(self, request, mgmt_root):
        setup_dependency(request, mgmt_root, 'fakeldap', servers=[
            '10.10.10.10'], userKey=12345)
        auth = HelperTest('Profiles')
        auth.test_profile_MCRDL(request, mgmt_root,
                                defaultsFrom='/Common/ssl_cc_ldap',
                                configuration='/Common/fakeldap')

    def test_collection(self, request, mgmt_root):
        setup_dependency(request, mgmt_root, 'fakeldap', servers=[
            '10.10.10.10'], userKey=12345)
        auth = HelperTest('Profiles')
        auth.test_profile_MCRDL(request, mgmt_root,
                                defaultsFrom='/Common/ssl_cc_ldap',
                                configuration='/Common/fakeldap')


@pytest.mark.skipif(True, reason='this depends on an optional module')
class TestRadius(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Radius_s')
        auth.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Radius_s')
        auth.test_collection(request, mgmt_root)


class TestRadiusServer(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Radius_Servers')
        auth.test_MCURDL(request, mgmt_root, server='10.10.10.10',
                         secret='sekrit')

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Radius_Servers')
        auth.test_collection(request, mgmt_root, server='10.10.10.10',
                             secret='sekrit')


class TestSSLCcLdap(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Ssl_Cc_Ldaps')
        auth.test_MCURDL(request, mgmt_root, servers=['10.10.10.10'],
                         userKey=12345)

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Ssl_Cc_Ldaps')
        auth.test_collection(request, mgmt_root, servers=['10.10.10.10'],
                             userKey=12345)


class TestSSLClrdp(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Ssl_Crldps')
        auth.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Ssl_Crldps')
        auth.test_collection(request, mgmt_root)


class TestSSLOcsp(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Ssl_Ocsps')
        auth.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Ssl_Ocsps')
        auth.test_collection(request, mgmt_root)


class TestTacacs(object):
    def test_MCURDL(self, request, mgmt_root):
        auth = HelperTest('Radius_Servers')
        auth.test_MCURDL(request, mgmt_root, server='10.10.10.10',
                         secret='fortytwo')

    def test_collection(self, request, mgmt_root):
        auth = HelperTest('Radius_Servers')
        auth.test_collection(request, mgmt_root, server='10.10.10.10',
                             secret='fortytwo')
