# Copyright 2018 F5 Networks Inc.
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

import os
import pytest
import tempfile

from f5.bigip.tm.security.log import Application
from f5.bigip.tm.security.log import Network
from f5.bigip.tm.security.log import Profile
from f5.bigip.tm.security.log import Protocol_Dns
from f5.bigip.tm.security.log import Protocol_Sip
from requests.exceptions import HTTPError


@pytest.fixture(scope='function')
def profile(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = mgmt_root.tm.security.log.profiles.profile.create(
        name=name, partition='Common'
    )
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def application_profile(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = mgmt_root.tm.security.log.profiles.profile.create(
        name=name, partition='Common'
    )
    r2 = r1.applications.application.create(name=name, partition='Common')
    yield r2
    r1.delete()


@pytest.fixture(scope='function')
def network_profile(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = mgmt_root.tm.security.log.profiles.profile.create(
        name=name, partition='Common'
    )
    r2 = r1.networks.network.create(name=name, partition='Common')
    yield r2
    r1.delete()


@pytest.fixture(scope='function')
def protocol_dns_profile(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = mgmt_root.tm.security.log.profiles.profile.create(
        name=name, partition='Common'
    )
    r2 = r1.protocol_dns_s.protocol_dns.create(name=name, partition='Common')
    yield r2
    r1.delete()


@pytest.fixture(scope='function')
def protocol_sip_profile(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    r1 = mgmt_root.tm.security.log.profiles.profile.create(
        name=name, partition='Common'
    )
    r2 = r1.protocol_sips.protocol_sip.create(name=name, partition='Common')
    yield r2
    r1.delete()


class TestProfileGeneral(object):
    def test_create_req_args(self, profile):
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert profile.partition == 'Common'
        assert profile.selfLink.startswith(URI)

    def test_refresh(self, mgmt_root, profile):
        rc = mgmt_root.tm.security.log.profiles
        r1 = profile
        r2 = rc.profile.load(name=profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.modify(description='my description')
        assert hasattr(r2, 'description')
        assert r2.description == 'my description'
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.log.profiles
        r1 = rc.profile.create(name='delete_me', partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.profile.load(name='delete_me', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.log.profiles
        with pytest.raises(HTTPError) as err:
            rc.profile.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, profile):
        r1 = profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = 'my description'
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == 'my description'
        rc = mgmt_root.tm.security.log.profiles
        r2 = rc.profile.load(name=profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_profiles_collection(self, mgmt_root, profile):
        r1 = profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.log.profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Profile)


class TestProfileApplication(object):
    def test_refresh(self, mgmt_root, application_profile):
        rc = mgmt_root.tm.security.log.profiles
        r1 = application_profile
        r2 = rc.profile.load(name=application_profile.name, partition='Common')
        r2 = r2.applications.application.load(name=application_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.guaranteeLogging == r2.guaranteeLogging
        r2.modify(guaranteeLogging='disabled')
        assert r2.guaranteeLogging == 'disabled'
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert r1.guaranteeLogging == r2.guaranteeLogging

    def test_delete(self, profile):
        r1 = profile.applications.application.create(name=profile.name, partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            profile.applications.application.load(name=profile.name, partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, profile):
        with pytest.raises(HTTPError) as err:
            profile.applications.application.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, application_profile):
        r1 = application_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        r1.guaranteeLogging = 'disabled'
        r1.update()
        assert hasattr(r1, 'guaranteeLogging')
        assert r1.guaranteeLogging == 'disabled'
        rc = mgmt_root.tm.security.log.profiles.profile.load(name=application_profile.name, partition='Common')
        r2 = rc.applications.application.load(name=application_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'guaranteeLogging')
        assert r1.guaranteeLogging == r2.guaranteeLogging

    def test_profiles_collection(self, mgmt_root, application_profile):
        r1 = application_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.log.profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)

        resource = next((x for x in rc if x.name == application_profile.name), None)

        rc2 = resource.applications.get_collection()
        assert isinstance(rc, list)
        assert len(rc)

        assert isinstance(rc2[0], Application)


class TestProfileNetwork(object):
    def test_refresh(self, mgmt_root, network_profile):
        rc = mgmt_root.tm.security.log.profiles
        r1 = network_profile
        r2 = rc.profile.load(name=network_profile.name, partition='Common')
        r2 = r2.networks.network.load(name=network_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.filter['logIpErrors'] == r2.filter['logIpErrors']

        r2.modify(filter={'logIpErrors': 'enabled'})
        assert r2.filter['logIpErrors'] == 'enabled'
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert r1.filter['logIpErrors'] == r2.filter['logIpErrors']

    def test_delete(self, profile):
        r1 = profile.networks.network.create(name=profile.name, partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            profile.networks.network.load(name=profile.name, partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, profile):
        with pytest.raises(HTTPError) as err:
            profile.networks.network.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, network_profile):
        r1 = network_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        r1.filter['logIpErrors'] = 'enabled'
        r1.update()
        assert r1.filter['logIpErrors'] == 'enabled'
        rc = mgmt_root.tm.security.log.profiles.profile.load(name=network_profile.name, partition='Common')
        r2 = rc.networks.network.load(name=network_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'filter')
        assert r1.filter['logIpErrors'] == r2.filter['logIpErrors']

    def test_profiles_collection(self, mgmt_root, network_profile):
        r1 = network_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.log.profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)

        resource = next((x for x in rc if x.name == network_profile.name), None)

        rc2 = resource.networks.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc2[0], Network)


class TestProfileProtocolDns(object):
    def test_refresh(self, mgmt_root, protocol_dns_profile):
        rc = mgmt_root.tm.security.log.profiles
        r1 = protocol_dns_profile
        r2 = rc.profile.load(name=protocol_dns_profile.name, partition='Common')
        r2 = r2.protocol_dns_s.protocol_dns.load(name=protocol_dns_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.filter['logDnsDrop'] == r2.filter['logDnsDrop']

        r2.modify(filter={'logDnsDrop': 'enabled'})
        assert r2.filter['logDnsDrop'] == 'enabled'
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert r1.filter['logDnsDrop'] == r2.filter['logDnsDrop']

    def test_delete(self, profile):
        r1 = profile.protocol_dns_s.protocol_dns.create(name=profile.name, partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            profile.protocol_dns_s.protocol_dns.load(name=profile.name, partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, profile):
        with pytest.raises(HTTPError) as err:
            profile.protocol_dns_s.protocol_dns.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, protocol_dns_profile):
        r1 = protocol_dns_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        r1.filter['logDnsDrop'] = 'enabled'
        r1.update()
        assert r1.filter['logDnsDrop'] == 'enabled'
        rc = mgmt_root.tm.security.log.profiles.profile.load(name=protocol_dns_profile.name, partition='Common')
        r2 = rc.protocol_dns_s.protocol_dns.load(name=protocol_dns_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'filter')
        assert r1.filter['logDnsDrop'] == r2.filter['logDnsDrop']

    def test_profiles_collection(self, mgmt_root, protocol_dns_profile):
        r1 = protocol_dns_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.log.profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)

        resource = next((x for x in rc if x.name == protocol_dns_profile.name), None)

        rc2 = resource.protocol_dns_s.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc2[0], Protocol_Dns)


class TestProfileProtocolSip(object):
    def test_refresh(self, mgmt_root, protocol_sip_profile):
        rc = mgmt_root.tm.security.log.profiles
        r1 = protocol_sip_profile
        r2 = rc.profile.load(name=protocol_sip_profile.name, partition='Common')
        r2 = r2.protocol_sips.protocol_sip.load(name=protocol_sip_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.filter['logSipDrop'] == r2.filter['logSipDrop']

        r2.modify(filter={'logSipDrop': 'enabled'})
        assert r2.filter['logSipDrop'] == 'enabled'
        r1.refresh()
        assert r1.selfLink == r2.selfLink
        assert r1.filter['logSipDrop'] == r2.filter['logSipDrop']

    def test_delete(self, profile):
        r1 = profile.protocol_sips.protocol_sip.create(name=profile.name, partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            profile.protocol_sips.protocol_sip.load(name=profile.name, partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, profile):
        with pytest.raises(HTTPError) as err:
            profile.protocol_sips.protocol_sip.load(name='not_exists', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, mgmt_root, protocol_sip_profile):
        r1 = protocol_sip_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        r1.filter['logSipDrop'] = 'enabled'
        r1.update()
        assert r1.filter['logSipDrop'] == 'enabled'
        rc = mgmt_root.tm.security.log.profiles.profile.load(name=protocol_sip_profile.name, partition='Common')
        r2 = rc.protocol_sips.protocol_sip.load(name=protocol_sip_profile.name, partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'filter')
        assert r1.filter['logSipDrop'] == r2.filter['logSipDrop']

    def test_profiles_collection(self, mgmt_root, protocol_sip_profile):
        r1 = protocol_sip_profile
        URI = 'https://localhost/mgmt/tm/security/log/profile/~Common~'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)

        rc = mgmt_root.tm.security.log.profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)

        resource = next((x for x in rc if x.name == protocol_sip_profile.name), None)

        rc2 = resource.protocol_sips.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc2[0], Protocol_Sip)
