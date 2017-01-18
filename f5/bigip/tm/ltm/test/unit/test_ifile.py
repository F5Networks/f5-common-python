# Copyright 2015 F5 Networks Inc.
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

from f5.bigip.tm.ltm.ifile import Ifile
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeLtmIfile():
    fake_ifile_s = mock.MagicMock()
    fake_ifile = Ifile(fake_ifile_s)
    return fake_ifile


def test_create_no_args(FakeLtmIfile):
    with pytest.raises(MissingRequiredCreationParameter):
        FakeLtmIfile.create()


def test_create_missing_arg(FakeLtmIfile):
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        FakeLtmIfile.create(name='test_ifile')
        assert 'fileName' in ex.value.message
