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

from f5.bigip.shared.authz import Token
from f5.bigip.shared.authz import User
from f5.sdk_exception import ConstraintError
from f5.sdk_exception import MissingRequiredCreationParameter

import mock
import pytest


@pytest.fixture
def FakeToken():
    mo = mock.MagicMock()
    resource = Token(mo)
    return resource


@pytest.fixture
def FakeUser():
    mo = mock.MagicMock()
    resource = User(mo)
    return resource


class TestToken(object):
    def test_invalid_timeout_non_number_value(self, FakeToken):
        with pytest.raises(ConstraintError):
            FakeToken.update(timeout="abc")

    def test_invalid_timeout_number_value(self, FakeToken):
        with pytest.raises(ConstraintError):
            FakeToken.update(timeout=360000)

    def test_create_no_args(self, FakeToken):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeToken.create()


class TestUser(object):
    def test_create_user_no_args(self, FakeUser):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeUser.create()
