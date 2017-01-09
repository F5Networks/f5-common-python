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

from f5.bigip.tm.asm.attack_types import Attack_Type
import pytest
from requests.exceptions import HTTPError


def get_atckid(request, mgmt_root):
    atckcoll = mgmt_root.tm.asm.attack_types_s.get_collection()
    # We obtain the ID for the resource to test and return the hashed id
    hashid = str(atckcoll[0].id)
    return hashid


class TestAttackTypes(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.attack_types_s.attack_type.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        hashid = get_atckid(request, mgmt_root)
        atck = mgmt_root.tm.asm.attack_types_s.attack_type.load(id=hashid)
        kind = 'tm:asm:attack-types:attack-typestate'
        baseuri = 'https://localhost/mgmt/tm/asm/attack-types/'
        final_uri = baseuri+hashid
        assert atck.id == hashid
        assert atck.kind == kind
        assert atck.selfLink.startswith(final_uri)

    def test_refresh(self, request, mgmt_root):
        hashid = get_atckid(request, mgmt_root)
        atck1 = mgmt_root.tm.asm.attack_types_s.attack_type.load(id=hashid)
        atck2 = mgmt_root.tm.asm.attack_types_s.attack_type.load(id=hashid)
        kind = 'tm:asm:attack-types:attack-typestate'
        baseuri = 'https://localhost/mgmt/tm/asm/attack-types/'
        final_uri = baseuri+hashid
        assert atck1.id == hashid
        assert atck1.kind == kind
        assert atck1.selfLink.startswith(final_uri)
        atck2.refresh()
        assert atck1.id == atck2.id
        assert atck1.kind == atck2.kind
        assert atck1.selfLink == atck2.selfLink

    def test_collection(self, request, mgmt_root):
        sc = mgmt_root.tm.asm.attack_types_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Attack_Type)
