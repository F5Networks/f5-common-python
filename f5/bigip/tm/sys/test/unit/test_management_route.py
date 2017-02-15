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


from f5.bigip.tm.sys.management_route import Management_Route
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeMgmtRoute():
    fake_sys = mock.MagicMock()
    return Management_Route(fake_sys)


def test_create_no_args(FakeMgmtRoute):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeMgmtRoute.create()
    assert "Missing required params:" in EIO.value.message


def test_create_missing_name(FakeMgmtRoute):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeMgmtRoute.create(gateway='192.168.1.1', network='172.16.15.0/24')
    assert EIO.value.message == "Missing required params: ['name']"


def test_create_missing_network(FakeMgmtRoute):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeMgmtRoute.create(name='testnet', gateway='192.168.1.1')
    assert EIO.value.message == "Missing required params: ['network']"


def test_create_missing_gateway(FakeMgmtRoute):
    with pytest.raises(MissingRequiredCreationParameter) as EIO:
        FakeMgmtRoute.create(name='testnet', network='172.16.15.0/24')
    assert EIO.value.message == "Missing required params: ['gateway']"
