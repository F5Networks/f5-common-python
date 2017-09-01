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

import mock
import pytest

from f5.bigip.tm.sys.daemon_log_settings import Clusterd
from f5.bigip.tm.sys.daemon_log_settings import Csyncd
from f5.bigip.tm.sys.daemon_log_settings import Icrd
from f5.bigip.tm.sys.daemon_log_settings import Lind
from f5.bigip.tm.sys.daemon_log_settings import Mcpd
from f5.bigip.tm.sys.daemon_log_settings import Tmm
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeClusterd():
    fake_sys = mock.MagicMock()
    return Clusterd(fake_sys)


@pytest.fixture
def FakeCsyncd():
    fake_sys = mock.MagicMock()
    return Csyncd(fake_sys)


@pytest.fixture
def FakeIcrd():
    fake_sys = mock.MagicMock()
    return Icrd(fake_sys)


@pytest.fixture
def FakeLind():
    fake_sys = mock.MagicMock()
    return Lind(fake_sys)


@pytest.fixture
def FakeMcpd():
    fake_sys = mock.MagicMock()
    return Mcpd(fake_sys)


@pytest.fixture
def FakeTmm():
    fake_sys = mock.MagicMock()
    return Tmm(fake_sys)


class TestCreate(object):
    def test_clusterd(self, FakeClusterd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeClusterd.create()
        assert str(err.value) == 'Clusterd does not support the create method'

    def test_csyncd(self, FakeCsyncd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeCsyncd.create()
        assert str(err.value) == 'Csyncd does not support the create method'

    def test_icrd(self, FakeIcrd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeIcrd.create()
        assert str(err.value) == 'Icrd does not support the create method'

    def test_lind(self, FakeLind):
        with pytest.raises(UnsupportedMethod) as err:
            FakeLind.create()
        assert str(err.value) == 'Lind does not support the create method'

    def test_mcpd(self, FakeMcpd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeMcpd.create()
        assert str(err.value) == 'Mcpd does not support the create method'

    def test_tmm(self, FakeTmm):
        with pytest.raises(UnsupportedMethod) as err:
            FakeTmm.create()
        assert str(err.value) == 'Tmm does not support the create method'


class TestDelete(object):
    def test_clusterd(self, FakeClusterd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeClusterd.delete()
        assert str(err.value) == 'Clusterd does not support the delete method'

    def test_csyncd(self, FakeCsyncd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeCsyncd.delete()
        assert str(err.value) == 'Csyncd does not support the delete method'

    def test_icrd(self, FakeIcrd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeIcrd.delete()
        assert str(err.value) == 'Icrd does not support the delete method'

    def test_lind(self, FakeLind):
        with pytest.raises(UnsupportedMethod) as err:
            FakeLind.delete()
        assert str(err.value) == 'Lind does not support the delete method'

    def test_mcpd(self, FakeMcpd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeMcpd.delete()
        assert str(err.value) == 'Mcpd does not support the delete method'

    def test_tmm(self, FakeTmm):
        with pytest.raises(UnsupportedMethod) as err:
            FakeTmm.delete()
        assert str(err.value) == 'Tmm does not support the delete method'
