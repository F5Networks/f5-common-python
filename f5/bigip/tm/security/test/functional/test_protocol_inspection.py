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
from requests.exceptions import HTTPError

from distutils.version import LooseVersion
from f5.bigip.tm.security.protocol_inspection import Compliance
from f5.bigip.tm.security.protocol_inspection import Profile
from f5.bigip.tm.security.protocol_inspection import Signature

DESC = 'TEST DESCRIPTION'


@pytest.fixture(scope='function')
def profile(mgmt_root):
    r1 = mgmt_root.tm.security.protocol_inspection.profiles.profile.create(
        name='fake_prof', partition='Common')
    yield r1
    r1.delete()


@pytest.fixture(scope='function')
def signature(mgmt_root):
    param_set = {'name': 'fake_signature', 'description': DESC,
                 'sig': 'content:\"hello\";', 'partition': 'Common'}
    r1 = mgmt_root.tm.security.protocol_inspection.\
        signatures.signature.create(**param_set)
    yield r1
    r1.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='This collection is fully implemented on 13.1.0 or greater.'
)
class TestProfile(object):
    """Profile functional tests"""

    def test_create_req_args(self, profile):
        URI = 'https://localhost/mgmt/tm/security/' \
              'protocol-inspection/profile/~Common~fake_prof'
        assert profile.name == 'fake_prof'
        assert profile.partition == 'Common'
        assert profile.selfLink.startswith(URI)
        assert not hasattr(profile, 'description')

    def test_create_opt_args(self, mgmt_root):
        prof = mgmt_root.tm.security.\
            protocol_inspection.profiles.profile.create(
                name='fake_prof', partition='Common',
                defaultsFrom='/Common/protocol_inspection_http',
                description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'protocol-inspection/profile/~Common~fake_prof'
        assert prof.name == 'fake_prof'
        assert prof.partition == 'Common'
        assert prof.selfLink.startswith(URI)
        assert hasattr(prof, 'description')
        assert hasattr(prof, 'defaultsFrom')
        assert prof.description == DESC
        prof.delete()

    def test_refresh(self, mgmt_root, profile):
        profc = mgmt_root.tm.security.protocol_inspection.profiles
        prof = profc.profile.load(name='fake_prof', partition='Common')
        assert profile.name == prof.name
        assert profile.kind == prof.kind
        assert profile.selfLink == prof.selfLink
        assert not hasattr(profile, 'description')
        assert not hasattr(prof, 'description')
        prof.modify(description=DESC)
        assert hasattr(prof, 'description')
        assert prof.description == DESC
        profile.refresh()
        assert profile.selfLink == prof.selfLink
        assert hasattr(profile, 'description')
        assert profile.description == prof.description

    def test_delete(self, mgmt_root):
        rc = mgmt_root.tm.security.protocol_inspection.profiles
        r1 = rc.profile.create(name='fake_prof', partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.profile.load(name='fake_prof', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.protocol_inspection.profiles
        with pytest.raises(HTTPError) as err:
            rc.profile.load(name='fake_prof', partition='Common')
        assert err.value.response.status_code == 404

    def test_profile_collection(self, mgmt_root, profile):
        r1 = profile
        URI = 'https://localhost/mgmt/tm/security/' \
              'protocol-inspection/profile/~Common~fake_prof'
        assert r1.name == 'fake_prof'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        rc = mgmt_root.tm.security.protocol_inspection.\
            profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Profile)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='This collection is fully implemented on 13.1.0 or greater.'
)
class TestSignature(object):
    """Signature functional tests"""

    def test_create_req_args(self, signature):
        r1 = signature
        URI = 'https://localhost/mgmt/tm/security/' \
              'protocol-inspection/signature/~Common~fake_signature'
        assert r1.name == 'fake_signature'
        assert r1.partition == 'Common'
        assert r1.description == DESC
        assert r1.selfLink.startswith(URI)

    def test_create_opt_args(self, mgmt_root):
        prof = mgmt_root.tm.security.protocol_inspection.signatures.\
            signature.create(name='fake_signature',
                             partition='Common', sig='content:"abc";',
                             service='http', description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'protocol-inspection/signature/~Common~fake_signature'
        assert prof.name == 'fake_signature'
        assert prof.partition == 'Common'
        assert prof.selfLink.startswith(URI)
        assert hasattr(prof, 'description')
        assert hasattr(prof, 'service')
        assert prof.description == DESC
        prof.delete()

    def test_refresh(self, mgmt_root, signature):
        sigc = mgmt_root.tm.security.protocol_inspection.signatures
        sig = sigc.signature.load(name='fake_signature', partition='Common')
        assert signature.name == sig.name
        assert signature.kind == sig.kind
        assert signature.selfLink == sig.selfLink
        assert not hasattr(signature, 'documentation')
        assert not hasattr(sig, 'documentation')
        sig.modify(documentation='custom doc')
        assert hasattr(sig, 'documentation')
        assert sig.documentation == 'custom doc'
        signature.refresh()
        assert signature.selfLink == sig.selfLink
        assert hasattr(signature, 'documentation')
        assert signature.documentation == sig.documentation

    def test_delete(self, mgmt_root):
        sigc = mgmt_root.tm.security.protocol_inspection.signatures
        sig = sigc.signature.create(name='fake_signature',
                                    partition='Common', sig='content:"abc";',
                                    description=DESC)
        sig.delete()
        with pytest.raises(HTTPError) as err:
            sigc.signature.load(name='fake_signature', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        sigc = mgmt_root.tm.security.protocol_inspection.signatures
        with pytest.raises(HTTPError) as err:
            sigc.signature.load(name='fake_signature', partition='Common')
        assert err.value.response.status_code == 404

    def test_signature_collection(self, mgmt_root, signature):
        s1 = signature
        URI = 'https://localhost/mgmt/tm/security/' \
              'protocol-inspection/signature/~Common~fake_signature'
        assert s1.name == 'fake_signature'
        assert s1.partition == 'Common'
        assert s1.selfLink.startswith(URI)
        sigc = mgmt_root.tm.security.protocol_inspection.\
            signatures.get_collection()
        assert isinstance(sigc, list)
        assert len(sigc)
        assert isinstance(sigc[0], Signature)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.1.0'),
    reason='This collection is fully implemented on 13.1.0 or greater.'
)
class TestCompliance(object):
    """Compliance functional tests"""

    def test_compliance_collection(self, mgmt_root):
        compc = mgmt_root.tm.security.protocol_inspection.\
            compliances.get_collection()
        assert isinstance(compc, list)
        assert len(compc)
        assert isinstance(compc[0], Compliance)
