# Copyright 2018 F5 Networks Inc.
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

from f5.bigip.tm.sys.cluster import Cluster
from f5.bigip.tm.sys.cluster import Default
from f5.sdk_exception import InvalidResource
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeCluster():
    fake_sys = mock.MagicMock()
    return Cluster(fake_sys)


@pytest.fixture
def FakeClusterDefault():
    fake_sys = mock.MagicMock()
    return Default(fake_sys)


def test_create_raises(FakeCluster):
    with pytest.raises(InvalidResource) as EIO:
        FakeCluster.create()
    assert str(EIO.value) == "Only Resources support 'create'."


def test_delete_raises(FakeCluster):
    with pytest.raises(InvalidResource) as EIO:
        FakeCluster.delete()
    assert str(EIO.value) == "Only Resources support 'delete'."


def test_default_create_raises(FakeClusterDefault):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeClusterDefault.create()
    assert str(EIO.value) == "Default does not support the create method"


def test_default_delete_raises(FakeClusterDefault):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeClusterDefault.delete()
    assert str(EIO.value) == "Default does not support the delete method"
