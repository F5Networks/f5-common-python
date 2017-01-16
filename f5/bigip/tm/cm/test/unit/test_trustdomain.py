# Copyright 2016 F5 Networks Inc.
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

import mock
import pytest

from f5.bigip.tm.cm.trust_domain import Trust_Domain
from f5.sdk_exception import UnsupportedOperation


@pytest.fixture
def FakeTrustDomain():
    fake_trust_domain_s = mock.MagicMock()
    return Trust_Domain(fake_trust_domain_s)


class TestTrustDomain(object):
    def test_create_raises(self):
        with pytest.raises(UnsupportedOperation) as err:
            i = FakeTrustDomain()
            i.create(name='test_trust')
            msg = 'BIG-IP trust domains cannot be created by users'
            assert err.value.message == msg

    def test_delete_raises(self):
        with pytest.raises(UnsupportedOperation) as err:
            i = FakeTrustDomain()
            i.delete()
            msg = 'BIG-IP trust domains cannot be deleted by users'
            assert err.value.message == msg
