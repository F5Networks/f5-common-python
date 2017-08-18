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

from f5.bigip.tm.asm.signature_systems import Signature_System


class TestSignatureSystems(object):
    def test_collection(self, mgmt_root):
        coll = mgmt_root.tm.asm.signature_systems_s.get_collection()
        assert coll
        assert coll[0] is not coll[1]
        assert isinstance(coll[0], Signature_System)
        assert isinstance(coll[1], Signature_System)
        assert coll[0].kind == coll[1].kind
        assert coll[0].id != coll[1].id
        assert coll[0].name != coll[1].name

    def test_load(self, mgmt_root):
        coll = mgmt_root.tm.asm.signature_systems_s.get_collection()
        idhash1 = str(coll[0].id)
        sig1 = mgmt_root.tm.asm.signature_systems_s.signature_system.load(id=idhash1)
        idhash2 = str(coll[1].id)
        sig2 = mgmt_root.tm.asm.signature_systems_s.signature_system.load(id=idhash2)
        assert sig1.kind == 'tm:asm:signature-systems:signature-systemstate'
        assert sig2.kind == sig1.kind
        assert sig1.name != sig2.name
        assert sig1.id == coll[0].id
        assert sig2.id == coll[1].id

    def test_refresh(self, mgmt_root):
        coll = mgmt_root.tm.asm.signature_systems_s.get_collection()
        idhash1 = str(coll[0].id)
        sig1 = mgmt_root.tm.asm.signature_systems_s.signature_system.load(id=idhash1)
        sig2 = mgmt_root.tm.asm.signature_systems_s.signature_system.load(id=idhash1)

        assert sig1.kind == 'tm:asm:signature-systems:signature-systemstate'
        sig2.refresh()
        assert sig2.kind == sig1.kind
        assert sig1.name == sig2.name
        assert sig1.id == coll[0].id
        assert sig2.id == coll[0].id
