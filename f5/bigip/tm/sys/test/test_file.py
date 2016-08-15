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
from f5.bigip.tm.sys.file import Ifile


@pytest.fixture
def FakeSysIfile():
    fake_ifile_s = mock.MagicMock()
    fake_ifile = Ifile(fake_ifile_s)
    return fake_ifile


def test_create_no_args(FakeSysIfile):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeSysIfile.create()


def test_create_missing_arg(FakeSysIfile):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeSysIfile.create(name='test_ifile')
        assert 'sourcePath' in ex.value.message
