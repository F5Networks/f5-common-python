# Copyright 2014-2017 F5 Networks Inc.
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

from f5.bigip.tm.gtm.global_settings import General
from f5.bigip.tm.gtm.global_settings import Load_Balancing
from f5.bigip.tm.gtm.global_settings import Metrics
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeMet():
    fake_global = mock.MagicMock()
    return Metrics(fake_global)


@pytest.fixture
def FakeLb():
    fake_global = mock.MagicMock()
    return Load_Balancing(fake_global)


@pytest.fixture
def FakeGeneral():
    fake_global = mock.MagicMock()
    return General(fake_global)


class TestGeneral(object):
    def test_create_raises(self, FakeGeneral):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeGeneral.create()
        assert EIO.value.message == \
            "General does not support the create method"

    def test_delete_raises(self, FakeGeneral):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeGeneral.delete()
        assert EIO.value.message == \
            "General does not support the delete method"


class TestLoadBalancing(object):
    def test_create_raises(self, FakeLb):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeLb.create()
        assert EIO.value.message == \
            "Load_Balancing does not support the create method"

    def test_delete_raises(self, FakeLb):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeLb.delete()
        assert EIO.value.message == \
            "Load_Balancing does not support the delete method"


class TestMetrics(object):
    def test_create_raises(self, FakeMet):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeMet.create()
        assert EIO.value.message == \
            "Metrics does not support the create method"

    def test_delete_raises(self, FakeMet):
        with pytest.raises(UnsupportedMethod) as EIO:
            FakeMet.delete()
        assert EIO.value.message == \
            "Metrics does not support the delete method"
