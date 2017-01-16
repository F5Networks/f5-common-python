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

from f5.bigip.tm.vcmp.guest import DisallowedCreationParameter
from f5.bigip.tm.vcmp.guest import DisallowedReadParameter
from f5.bigip.tm.vcmp.guest import Guest
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeGuest():
    fake_guests = mock.MagicMock()
    return Guest(fake_guests)


def test_create_no_args(FakeGuest):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeGuest.create()
    assert "Missing required params: ['name']" in ex.value.message


def test_create_with_parition(FakeGuest):
    with pytest.raises(DisallowedCreationParameter) as ex:
        FakeGuest.create(name='test', partition='Common')
    assert "'partition' is not allowed as a create parameter" in \
        ex.value.message


def test_load_with_partition(FakeGuest):
    with pytest.raises(DisallowedReadParameter) as ex:
        FakeGuest.load(name='test', partition='Common')
    assert "'partition' is not allowed as a load parameter" in \
        ex.value.message
