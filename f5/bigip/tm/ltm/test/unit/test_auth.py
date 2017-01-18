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

from f5.bigip import ManagementRoot
from f5.bigip.resource import UnsupportedMethod
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
from f5.sdk_exception import MissingRequiredCreationParameter
import mock
import pytest
from six import iterkeys


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

    def set_resources(self, fakeicontrolsession_v12):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        resourcecollection =\
            getattr(getattr(getattr(mr.tm, 'ltm'), 'auth'),
                    self.lowered)
        resource1 = getattr(resourcecollection, self.urielementname())
        resource2 = getattr(resourcecollection, self.urielementname())
        return resource1, resource2

    def set_collections(self, fakeicontrolsession_v12):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        resourcecollection =\
            getattr(getattr(getattr(mr.tm, 'ltm'), 'auth'),
                    self.lowered)
        return resourcecollection

    def test_collections(self, fakeicontrolsession_v12, klass):
        rc = self.set_collections(fakeicontrolsession_v12)
        test_meta = rc._meta_data['attribute_registry']
        test_meta2 = rc._meta_data['allowed_lazy_attributes']
        kind = self.authkinds[self.urielementname()]
        assert kind in list(iterkeys(test_meta))
        assert klass in test_meta2

    def test_create_two(self, fakeicontrolsession_v12):
        r1, r2, = self.set_resources(fakeicontrolsession_v12)
        assert r1 is not r2

    def test_create_no_args(self, fakeicontrolsession_v12):
        r1, r2, = self.set_resources(fakeicontrolsession_v12)
        del r2
        with pytest.raises(MissingRequiredCreationParameter):
            r1.create()


def test_crldp_server(fakeicontrolsession_v12):
    a = HelperTest('Crldp_Servers')
    a.test_collections(fakeicontrolsession_v12, Crldp_Server)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_kerberos_kelegation(fakeicontrolsession_v12):
    a = HelperTest('Kerberos_Delegations')
    a.test_collections(fakeicontrolsession_v12, Kerberos_Delegation)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_ldap(fakeicontrolsession_v12):
    a = HelperTest('Ldaps')
    a.test_collections(fakeicontrolsession_v12, Ldap)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_ocsp_responder(fakeicontrolsession_v12):
    a = HelperTest('Ocsp_Responders')
    a.test_collections(fakeicontrolsession_v12, Ocsp_Responder)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


class TestProfile(object):
    def test_update_profile_raises(self):
        profile_resource = Profile(mock.MagicMock())
        with pytest.raises(UnsupportedMethod):
            profile_resource.update()

    def test_profile(self, fakeicontrolsession_v12):
        a = HelperTest('Profiles')
        a.test_collections(fakeicontrolsession_v12, Profile)
        a.test_create_two(fakeicontrolsession_v12)
        a.test_create_no_args(fakeicontrolsession_v12)


def test_radius(fakeicontrolsession_v12):
    a = HelperTest('Radius_s')
    a.test_collections(fakeicontrolsession_v12, Radius)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_radius_server(fakeicontrolsession_v12):
    a = HelperTest('Radius_Servers')
    a.test_collections(fakeicontrolsession_v12, Radius_Server)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_ssl_cc_ldap(fakeicontrolsession_v12):
    a = HelperTest('Ssl_Cc_Ldaps')
    a.test_collections(fakeicontrolsession_v12, Ssl_Cc_Ldap)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_ssl_clrdp(fakeicontrolsession_v12):
    a = HelperTest('Ssl_Crldps')
    a.test_collections(fakeicontrolsession_v12, Ssl_Crldp)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_ssl_ocsp(fakeicontrolsession_v12):
    a = HelperTest('Ssl_Ocsps')
    a.test_collections(fakeicontrolsession_v12, Ssl_Ocsp)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)


def test_tacacs(fakeicontrolsession_v12):
    a = HelperTest('Tacacs_s')
    a.test_collections(fakeicontrolsession_v12, Tacacs)
    a.test_create_two(fakeicontrolsession_v12)
    a.test_create_no_args(fakeicontrolsession_v12)
