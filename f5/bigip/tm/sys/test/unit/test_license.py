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

from f5.bigip.tm.sys import License
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeLicense():
    fake_sys = mock.MagicMock()
    return License(fake_sys)


def test_create_raises(FakeLicense):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeLicense.create()
    assert str(EIO.value) == "License does not support the create method"


def test_delete_raises(FakeLicense):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeLicense.delete()
    assert str(EIO.value) == "License does not support the delete method"


def test_exec_install(FakeLicense):
    assert "install" in FakeLicense._meta_data['allowed_commands']
    FakeLicense._meta_data['bigip']._meta_data.__getitem__.return_value = "14.0.0"
    FakeLicense._exec_cmd = mock.MagicMock()
    version_dict = {"13.1.0": 13, "14.0.0": 14}

    def get_version(version):
        return version_dict[version]

    License.LooseVersion = mock.MagicMock(side_effect=get_version)
    FakeLicense.exec_cmd("install", registrationKey='1234-56789-0')
    FakeLicense._exec_cmd.assert_called_with("install", registrationKey='1234-56789-0')
