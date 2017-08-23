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

from distutils.version import LooseVersion
from requests.exceptions import HTTPError
from f5.sdk_exception import UnsupportedOperation
from f5.bigip.tm.asm.policies.character_sets import Character_Sets


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestCharacterSets(object):
    def test_create_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.character_sets_s.character_sets.create()

    def test_delete_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.character_sets_s.character_sets.delete()

    def test_refresh(self, policy):
        coll = policy.character_sets_s.get_collection()
        hashid = str(coll[0].id)
        char1 = policy.character_sets_s.character_sets.load(id=hashid)
        char2 = policy.character_sets_s.character_sets.load(id=hashid)
        assert char1.kind == char2.kind
        assert char1.characterSetType == char2.characterSetType
        assert char1.characterSet == char2.characterSet
        char2.modify(characterSet=[{'metachar': '0x1', 'isAllowed': True}])
        assert char1.characterSet != char2.characterSet
        char1.refresh()
        assert char1.characterSet == char2.characterSet

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.character_sets_s.character_sets.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        coll = policy.character_sets_s.get_collection()
        hashid = str(coll[0].id)
        char1 = policy.character_sets_s.character_sets.load(id=hashid)
        assert char1.kind == 'tm:asm:policies:character-sets:character-setstate'
        assert 'metachar' in char1.characterSet[1]
        assert char1.characterSet[1]['metachar'] == '0x1'
        assert 'isAllowed' in char1.characterSet[1]
        assert char1.characterSet[1]['isAllowed'] is False

        char1.modify(characterSet=[{'metachar': '0x1', 'isAllowed': True}])
        assert 'metachar' in char1.characterSet[1]
        assert char1.characterSet[1]['metachar'] == '0x1'
        assert 'isAllowed' in char1.characterSet[1]
        assert char1.characterSet[1]['isAllowed'] is True

        char2 = policy.character_sets_s.character_sets.load(id=char1.id)
        assert char1.selfLink == char2.selfLink
        assert char1.kind == char2.kind
        assert char1.characterSet == char2.characterSet

    def test_charactersets_subcollection(self, policy):
        coll = policy.character_sets_s.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        assert isinstance(coll[0], Character_Sets)
