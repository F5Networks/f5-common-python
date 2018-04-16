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


from f5.bigip.tm.security.log import Profile


DESC = 'TEST DESCRIPTION'


@pytest.fixture(scope='function')
def profile(mgmt_root):
    r1 = mgmt_root.tm.security.log.profiles.profile.create(
        name='fake_prof', partition='Common')
    yield r1
    r1.delete()


class TestProfile(object):
    """Profile functional tests"""

    def test_create_req_args(self, profile):
        URI = 'https://localhost/mgmt/tm/security/' \
              'log/profile/~Common~fake_prof'
        assert profile.name == 'fake_prof'
        assert profile.partition == 'Common'
        assert profile.selfLink.startswith(URI)
        assert not hasattr(profile, 'description')

    def test_create_opt_args(self, mgmt_root):
        prof = mgmt_root.tm.security.\
            log.profiles.profile.create(
                name='fake_prof', partition='Common',
                description=DESC)
        URI = 'https://localhost/mgmt/tm/security/' \
              'log/profile/~Common~fake_prof'
        assert prof.name == 'fake_prof'
        assert prof.partition == 'Common'
        assert prof.selfLink.startswith(URI)
        assert hasattr(prof, 'description')
        assert prof.description == DESC
        prof.delete()

    def test_refresh(self, mgmt_root, profile):
        profc = mgmt_root.tm.security.log.profiles
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
        rc = mgmt_root.tm.security.log.profiles
        r1 = rc.profile.create(name='fake_prof', partition='Common')
        r1.delete()
        with pytest.raises(HTTPError) as err:
            rc.profile.load(name='fake_prof', partition='Common')
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.security.log.profiles
        with pytest.raises(HTTPError) as err:
            rc.profile.load(name='fake_prof', partition='Common')
        assert err.value.response.status_code == 404

    def test_profile_collection(self, mgmt_root, profile):
        r1 = profile
        URI = 'https://localhost/mgmt/tm/security/' \
              'log/profile/~Common~fake_prof'
        assert r1.name == 'fake_prof'
        assert r1.partition == 'Common'
        assert r1.selfLink.startswith(URI)
        rc = mgmt_root.tm.security.log.\
            profiles.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Profile)
