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

from distutils.version import LooseVersion
import mock
import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.sys.file import Ifile
from f5.bigip.tm.sys.file import Ssl_Cert
from f5.bigip.tm.sys.file import Ssl_Crl
from f5.bigip.tm.sys.file import Ssl_Csr
from f5.bigip.tm.sys.file import Ssl_Key


@pytest.fixture
def FakeSysIfile():
    fake_ifile_s = mock.MagicMock()
    fake_ifile = Ifile(fake_ifile_s)
    return fake_ifile


def test_ifile_create_no_args(FakeSysIfile):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeSysIfile.create()


def test_ifile_create_missing_arg(FakeSysIfile):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeSysIfile.create(name='test_ifile')
        assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSysCert():
    fake_cert_s = mock.MagicMock()
    fake_cert = Ssl_Cert(fake_cert_s)
    return fake_cert


def test_cert_create_no_args(FakeSysCert):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeSysCert.create()


def test_cert_create_missing_arg(FakeSysCert):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeSysCert.create(name='test_cert')
        assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSysCrl():
    fake_crl_s = mock.MagicMock()
    fake_crl = Ssl_Crl(fake_crl_s)
    return fake_crl


def test_crl_create_no_args(FakeSysCrl):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeSysCrl.create()


def test_crl_create_missing_arg(FakeSysCrl):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeSysCrl.create(name='test_crl')
        assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSysCsr():
    fake_csr_s = mock.MagicMock()
    fake_csr = Ssl_Csr(fake_csr_s)
    return fake_csr


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.0.0'),
    reason='csr management is only supported in 12.0.0 or greater.'
)
def test_csr_create_no_args(FakeSysCsr):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeSysCsr.create()


@pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('12.0.0'),
    reason='csr management is only supported in 12.0.0 or greater.'
)
def test_csr_create_missing_arg(FakeSysCsr):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeSysCsr.create(name='test_csr')
        assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSysKey():
    fake_key_s = mock.MagicMock()
    fake_key = Ssl_Key(fake_key_s)
    return fake_key


def test_key_create_no_args(FakeSysKey):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeSysKey.create()


def test_key_create_missing_arg(FakeSysKey):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeSysKey.create(name='test_key')
        assert 'sourcePath' in ex.value.message
