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

from f5.bigip.shared.authn import Root
from f5.bigip.shared.authn import Roots
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedMethod
from f5.sdk_exception import UnsupportedOperation

import mock
import pytest


@pytest.fixture
def FakeAuthnRoot():
    mo = mock.MagicMock()
    fake = Root(mo)
    return fake


@pytest.fixture
def FakeAuthnRoots():
    mo = mock.MagicMock()
    fake = Roots(mo)
    return fake


class TestAuthnRoot(object):
    def test_update_raises(self, FakeAuthnRoot):
        with pytest.raises(UnsupportedOperation):
            FakeAuthnRoot.update()

    def test_modify_raises(self, FakeAuthnRoot):
        with pytest.raises(UnsupportedOperation):
            FakeAuthnRoot.modify()

    def test_load_raises(self, FakeAuthnRoot):
        with pytest.raises(UnsupportedOperation):
            FakeAuthnRoot.load()

    def test_delete_raises(self, FakeAuthnRoot):
        with pytest.raises(UnsupportedOperation):
            FakeAuthnRoot.delete()

    def test_create_no_args(self, FakeAuthnRoot):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeAuthnRoot.create()


class TestAuthnRoots(object):
    def test_collection_raises(self, FakeAuthnRoots):
        with pytest.raises(UnsupportedMethod):
            FakeAuthnRoots.get_collection()
