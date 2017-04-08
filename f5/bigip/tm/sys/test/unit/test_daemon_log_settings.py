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
        assert err.value.message == 'Clusterd does not support the create ' \
                                    'method'

    def test_csyncd(self, FakeCsyncd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeCsyncd.create()
        assert err.value.message == 'Csyncd does not support the create method'

    def test_icrd(self, FakeIcrd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeIcrd.create()
        assert err.value.message == 'Icrd does not support the create method'

    def test_lind(self, FakeLind):
        with pytest.raises(UnsupportedMethod) as err:
            FakeLind.create()
        assert err.value.message == 'Lind does not support the create method'

    def test_mcpd(self, FakeMcpd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeMcpd.create()
        assert err.value.message == 'Mcpd does not support the create method'

    def test_tmm(self, FakeTmm):
        with pytest.raises(UnsupportedMethod) as err:
            FakeTmm.create()
        assert err.value.message == 'Tmm does not support the create method'


class TestDelete(object):
    def test_clusterd(self, FakeClusterd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeClusterd.delete()
        assert err.value.message == 'Clusterd does not support the delete ' \
                                    'method'

    def test_csyncd(self, FakeCsyncd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeCsyncd.delete()
        assert err.value.message == 'Csyncd does not support the delete method'

    def test_icrd(self, FakeIcrd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeIcrd.delete()
        assert err.value.message == 'Icrd does not support the delete method'

    def test_lind(self, FakeLind):
        with pytest.raises(UnsupportedMethod) as err:
            FakeLind.delete()
        assert err.value.message == 'Lind does not support the delete method'

    def test_mcpd(self, FakeMcpd):
        with pytest.raises(UnsupportedMethod) as err:
            FakeMcpd.delete()
        assert err.value.message == 'Mcpd does not support the delete method'

    def test_tmm(self, FakeTmm):
        with pytest.raises(UnsupportedMethod) as err:
            FakeTmm.delete()
        assert err.value.message == 'Tmm does not support the delete method'
