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

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.tm.sys.file import Ifiles
from f5.bigip.tm.sys.file import Ssl_Certs
from f5.bigip.tm.sys.file import Ssl_Crls
from f5.bigip.tm.sys.file import Ssl_Csrs
from f5.bigip.tm.sys.file import Ssl_Keys


@pytest.fixture
def FakeIfiles():
    fake_sys = mock.MagicMock()
    ifiles = Ifiles(fake_sys)
    ifiles._meta_data['bigip'].tmos_version = '11.6.0'
    return ifiles


class TestIfile(object):
    def test_missing_create_args(self):
        ifiles = FakeIfiles()
        ifile = ifiles.ifile
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            ifile.create(name='test_ifile')
            assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSsl_Certs():
    fake_sys = mock.MagicMock()
    certs = Ssl_Certs(fake_sys)
    certs._meta_data['bigip'].tmos_version = '11.6.0'
    return certs


class TestSsl_Certs(object):
    def test_missing_create_args(self):
        certs = FakeSsl_Certs()
        cert = certs.ssl_cert
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            cert.create(name='test_cert')
            assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSsl_Crls():
    fake_sys = mock.MagicMock()
    crls = Ssl_Crls(fake_sys)
    crls._meta_data['bigip'].tmos_version = '11.6.0'
    return crls


class TestSsl_Crls(object):
    def test_missing_create_args(self):
        crls = FakeSsl_Crls()
        crl = crls.ssl_crl
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            crl.create(name='test_cert')
            assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSsl_Csrs():
    fake_sys = mock.MagicMock()
    csrs = Ssl_Csrs(fake_sys)
    csrs._meta_data['bigip'].tmos_version = '11.6.0'
    return csrs


class TestSsl_Csrs(object):
    def test_missing_create_args(self):
        csrs = FakeSsl_Csrs()
        csr = csrs.ssl_csr
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            csr.create(name='test_cert')
            assert 'sourcePath' in ex.value.message


@pytest.fixture
def FakeSsl_Keys():
    fake_sys = mock.MagicMock()
    keys = Ssl_Keys(fake_sys)
    keys._meta_data['bigip'].tmos_version = '11.6.0'
    return keys


class TestSsl_Keys(object):
    def test_missing_create_args(self):
        keys = FakeSsl_Keys()
        key = keys.ssl_key
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            key.create(name='test_key')
            assert 'sourcePath' in ex.value.message

