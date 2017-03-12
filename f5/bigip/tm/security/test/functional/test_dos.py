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

from f5.bigip.tm.security.dos import Profile
from requests.exceptions import HTTPError
from six import iteritems

DESC = 'TESTCHANGEDIT'


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

    def test_policy_collection(self, dos_profile, mgmt_root):
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
