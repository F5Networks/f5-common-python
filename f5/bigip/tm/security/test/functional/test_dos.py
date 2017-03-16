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

from f5.bigip.tm.security.dos import Application
from f5.bigip.tm.security.dos import Dos_Network
from f5.bigip.tm.security.dos import Profile
from f5.bigip.tm.security.dos import Protocol_Dns
from f5.bigip.tm.security.dos import Protocol_Sip
from f5.sdk_exception import NonExtantApplication
from requests.exceptions import HTTPError
from six import iteritems

from distutils.version import LooseVersion

DESC = 'TESTCHANGEDIT'
ATCK = [{'name': 'tcp-rst-flood', 'rateLimit': 100, 'rateThreshold': 50}]


@pytest.fixture(scope='function')
def dos_profile(mgmt_root):
    profile = mgmt_root.tm.security.dos.profiles.profile.create(
        name='fake_dos', partition='Common')
    yield profile
    profile.delete()


class TestDosProfiles(object):
    def test_create_req_arg(self, dos_profile):
        r1 = dos_profile
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common~fake_dos'
        assert r1.name == 'fake_dos'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

    def test_create_optional_args(self, mgmt_root):
        r1 = mgmt_root.tm.security.dos.profiles.profile.create(
            name='fake_dos_2', partition='Common', description='FAKE_ME')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos_2'
        assert r1.name == 'fake_dos_2'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'description')
        assert r1.description == 'FAKE_ME'
        r1.delete()

    def test_refresh(self, dos_profile, mgmt_root):
        r1 = dos_profile
        r2 = mgmt_root.tm.security.dos.profiles.profile.load(
            name='fake_dos', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'description')
        assert not hasattr(r2, 'description')
        r2.description = DESC
        r2.update()
        assert r1.selfLink == r2.selfLink
        assert r1.name == r2.name
        assert hasattr(r2, 'description')
        assert r2.description == DESC
        r1.refresh()
        assert hasattr(r1, 'description')
        assert r1.description == r2.description

    def test_modify(self, dos_profile):
        original_dict = copy.copy(dos_profile.__dict__)
        itm = 'description'
        dos_profile.modify(description=DESC)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = dos_profile.__dict__[k]
            elif k == itm:
                assert dos_profile.__dict__[k] == DESC

    def test_delete(self, mgmt_root):
        r1 = mgmt_root.tm.security.dos.profiles.profile.create(
            name='delete_me', partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.dos.profiles.profile.load(name='delete_me')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.security.dos.profiles.profile.load(name='not_exist')
        assert err.value.response.status_code == 404

    def test_load_and_update(self, dos_profile, mgmt_root):
        r1 = dos_profile
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common~fake_dos'
        assert r1.name == 'fake_dos'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')
        r1.description = DESC
        r1.update()
        assert hasattr(r1, 'description')
        assert r1.description == DESC
        r2 = mgmt_root.tm.security.dos.profiles.profile.load(
            name='fake_dos', partition='Common')
        assert r1.name == r2.name
        assert r1.partition == r2.partition
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'description')
        assert r1.description == r2.description

    def test_dosprofile_collection(self, dos_profile, mgmt_root):
        r1 = dos_profile
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common~fake_dos'
        assert r1.name == 'fake_dos'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'description')

        rc = mgmt_root.tm.security.dos.profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Profile)


class TestApplication(object):
    def test_create_req_arg(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/application/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.triggerIrule == 'disabled'

    def test_create_optional_args(self, dos_profile):
        r1 = dos_profile.applications.application.create(
            name='fake_app', triggerIrule='enabled')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/application/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.triggerIrule == 'enabled'

    def test_refresh(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        r2 = dos_profile.applications.application.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.triggerIrule == r2.triggerIrule
        r2.triggerIrule = 'enabled'
        r2.update()
        assert r1.selfLink == r2.selfLink
        assert r1.name == r2.name
        assert r2.triggerIrule == 'enabled'
        assert r1.triggerIrule != r2.triggerIrule
        r1.refresh()
        assert r1.triggerIrule == r2.triggerIrule

    def test_modify(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        original_dict = copy.deepcopy(r1.__dict__)
        itm = 'triggerIrule'
        r1.modify(triggerIrule='enabled')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 'enabled'

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_delete(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            dos_profile.applications.application.load(name='fake_app')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_load_no_object(self, dos_profile):
        with pytest.raises(HTTPError) as err:
            dos_profile.applications.application.load(name='not_exist')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_delete_11_6_0(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        r1.delete()
        try:
            dos_profile.applications.application.load(name='fake_app')

        except NonExtantApplication as err:
            msg = 'The application resource named, fake_app, does not exist ' \
                  'on the device.'

            assert err.message == msg

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_load_no_object_11_6_0(self, dos_profile):
        try:
            dos_profile.applications.application.load(name='not_exists')

        except NonExtantApplication as err:
            msg = 'The application resource named, not_exists, ' \
                  'does not exist on the device.'

            assert err.message == msg

    def test_load_and_update(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/application/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.triggerIrule == 'disabled'
        r1.triggerIrule = 'enabled'
        r1.update()
        assert r1.triggerIrule == 'enabled'
        r2 = dos_profile.applications.application.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.triggerIrule == r2.triggerIrule

    def test_app_subcollection(self, dos_profile):
        r1 = dos_profile.applications.application.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/application/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.triggerIrule == 'disabled'

        rc = dos_profile.applications.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Application)


class TestDosNetwork(object):
    def test_create_req_arg(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/dos-network/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'networkAttackVector')

    def test_create_optional_args(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(
            name='fake_app', networkAttackVector=ATCK)
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/dos-network/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert hasattr(r1, 'networkAttackVector')

    def test_refresh(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        r2 = dos_profile.dos_networks.dos_network.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert not hasattr(r1, 'networkAttackVector')
        assert not hasattr(r2, 'networkAttackVector')
        r2.networkAttackVector = ATCK
        r2.update()
        assert r1.selfLink == r2.selfLink
        assert r1.name == r2.name
        assert not hasattr(r1, 'networkAttackVector')
        assert hasattr(r2, 'networkAttackVector')
        r1.refresh()
        assert r1.networkAttackVector == r2.networkAttackVector

    def test_modify(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        original_dict = copy.deepcopy(r1.__dict__)
        itm = 'networkAttackVector'
        r1.modify(networkAttackVector=ATCK)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == ATCK

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_delete(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            dos_profile.dos_networks.dos_network.load(name='fake_app')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_load_no_object(self, dos_profile):
        with pytest.raises(HTTPError) as err:
            dos_profile.dos_networks.dos_network.load(name='not_exist')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_delete_11_6_0(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        r1.delete()
        try:
            dos_profile.dos_networks.dos_network.load(name='fake_app')

        except NonExtantApplication as err:
            msg = 'The application resource named, fake_app, does not exist ' \
                  'on the device.'

            assert err.message == msg

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_load_no_object_11_6_0(self, dos_profile):
        try:
            dos_profile.dos_networks.dos_network.load(name='not_exists')

        except NonExtantApplication as err:
            msg = 'The application resource named, not_exists, does not ' \
                  'exist on the device.'

            assert err.message == msg

    def test_load_and_update(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/dos-network/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert not hasattr(r1, 'networkAttackVector')
        r1.networkAttackVector = ATCK
        r1.update()
        assert hasattr(r1, 'networkAttackVector')
        r2 = dos_profile.dos_networks.dos_network.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert hasattr(r2, 'networkAttackVector')
        assert r1.networkAttackVector == r2.networkAttackVector

    def test_dosnet_subcollection(self, dos_profile):
        r1 = dos_profile.dos_networks.dos_network.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/dos-network/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)

        rc = dos_profile.dos_networks.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Dos_Network)


class TestProtocolDns(object):
    def test_create_req_arg(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-dns/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'disabled'

    def test_create_optional_args(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(
            name='fake_app', protErrAttackDetection='enabled')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-dns/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'enabled'

    def test_refresh(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        r2 = dos_profile.protocol_dns_s.protocol_dns.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.protErrAttackDetection == r2.protErrAttackDetection
        r2.protErrAttackDetection = 'enabled'
        r2.update()
        assert r1.selfLink == r2.selfLink
        assert r1.name == r2.name
        assert r2.protErrAttackDetection == 'enabled'
        assert r1.protErrAttackDetection != r2.protErrAttackDetection
        r1.refresh()
        assert r1.protErrAttackDetection == r2.protErrAttackDetection

    def test_modify(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        original_dict = copy.deepcopy(r1.__dict__)
        itm = 'protErrAttackDetection'
        r1.modify(protErrAttackDetection='enabled')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 'enabled'

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_delete(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            dos_profile.protocol_dns_s.protocol_dns.load(name='fake_app')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_load_no_object(self, dos_profile):
        with pytest.raises(HTTPError) as err:
            dos_profile.protocol_dns_s.protocol_dns.load(name='not_exist')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_delete_11_6_0(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        r1.delete()
        try:
            dos_profile.protocol_dns_s.protocol_dns.load(name='fake_app')

        except NonExtantApplication as err:
            msg = 'The application resource named, fake_app, does not exist ' \
                  'on the device.'

            assert err.message == msg

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_load_no_object_11_6_0(self, dos_profile):
        try:
            dos_profile.protocol_dns_s.protocol_dns.load(name='not_exists')

        except NonExtantApplication as err:
            msg = 'The application resource named, not_exists, ' \
                  'does not exist on the device.'

            assert err.message == msg

    def test_load_and_update(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-dns/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'disabled'
        r1.protErrAttackDetection = 'enabled'
        r1.update()
        assert r1.protErrAttackDetection == 'enabled'
        r2 = dos_profile.protocol_dns_s.protocol_dns.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.protErrAttackDetection == r2.protErrAttackDetection

    def test_dns_subcollection(self, dos_profile):
        r1 = dos_profile.protocol_dns_s.protocol_dns.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-dns/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'disabled'

        rc = dos_profile.protocol_dns_s.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Protocol_Dns)


class TestProtocolSip(object):
    def test_create_req_arg(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-sip/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'disabled'

    def test_create_optional_args(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(
            name='fake_app', protErrAttackDetection='enabled')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-sip/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'enabled'

    def test_refresh(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        r2 = dos_profile.protocol_sips.protocol_sip.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.protErrAttackDetection == r2.protErrAttackDetection
        r2.protErrAttackDetection = 'enabled'
        r2.update()
        assert r1.selfLink == r2.selfLink
        assert r1.name == r2.name
        assert r2.protErrAttackDetection == 'enabled'
        assert r1.protErrAttackDetection != r2.protErrAttackDetection
        r1.refresh()
        assert r1.protErrAttackDetection == r2.protErrAttackDetection

    def test_modify(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        original_dict = copy.deepcopy(r1.__dict__)
        itm = 'protErrAttackDetection'
        r1.modify(protErrAttackDetection='enabled')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 'enabled'

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_delete(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            dos_profile.protocol_sips.protocol_sip.load(name='fake_app')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) == LooseVersion('11.6.0'),
        reason='This test will fail on 11.6.0 due to a known bug.'
    )
    def test_load_no_object(self, dos_profile):
        with pytest.raises(HTTPError) as err:
            dos_profile.protocol_sips.protocol_sip.load(name='not_exist')
        assert err.value.response.status_code == 404

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_delete_11_6_0(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        r1.delete()
        try:
            dos_profile.protocol_sips.protocol_sip.load(name='fake_app')

        except NonExtantApplication as err:
            msg = 'The application resource named, fake_app, does not exist ' \
                  'on the device.'

            assert err.message == msg

    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) != LooseVersion('11.6.0'),
        reason='This test is for 11.6.0 TMOS only, due to a known bug.'
    )
    def test_load_no_object_11_6_0(self, dos_profile):
        try:
            dos_profile.protocol_sips.protocol_sip.load(name='not_exists')

        except NonExtantApplication as err:
            msg = 'The application resource named, not_exists, ' \
                  'does not exist on the device.'

            assert err.message == msg

    def test_load_and_update(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-sip/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'disabled'
        r1.protErrAttackDetection = 'enabled'
        r1.update()
        assert r1.protErrAttackDetection == 'enabled'
        r2 = dos_profile.protocol_sips.protocol_sip.load(name='fake_app')
        assert r1.name == r2.name
        assert r1.selfLink == r2.selfLink
        assert r1.protErrAttackDetection == r2.protErrAttackDetection

    def test_sip_subcollection(self, dos_profile):
        r1 = dos_profile.protocol_sips.protocol_sip.create(name='fake_app')
        URI = 'https://localhost/mgmt/tm/security/dos/profile/~Common' \
              '~fake_dos/protocol-sip/fake_app'
        assert r1.name == 'fake_app'
        assert r1.selfLink.startswith(URI)
        assert r1.protErrAttackDetection == 'disabled'

        rc = dos_profile.protocol_sips.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Protocol_Sip)
