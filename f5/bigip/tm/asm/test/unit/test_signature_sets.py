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

from f5.bigip import ManagementRoot
from f5.bigip.tm.asm.signature_sets import Signature_Set
from f5.sdk_exception import MissingRequiredCreationParameter

import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakeSignatureSet():
    fake_asm = mock.MagicMock()
    fake_sigset = Signature_Set(fake_asm)
    fake_sigset._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_sigset


class TestCheckSignature(object):

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.tm.asm.signature_sets_s.signature_set
        t2 = b.tm.asm.signature_sets_s.signature_set
        assert t1 is t2

    def test_create_no_args(self, FakeSignatureSet):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeSignatureSet.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.tm.asm.signature_sets_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'tm:asm:signature-sets:signature-setstate'
        assert kind in list(iterkeys(test_meta))
        assert Signature_Set in test_meta2
        assert t._meta_data['object_has_stats'] is False
