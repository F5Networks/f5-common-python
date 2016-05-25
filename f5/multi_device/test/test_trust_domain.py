# Copyright 2015-2016 F5 Networks Inc.
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

from f5.multi_device.cluster import TrustDomain
from f5.multi_device.exceptions import DeviceNotTrusted

import mock
import pytest


class MockDeviceInfo(object):
    def __init__(self, name):
        self.name = name
        self.selfDevice = 'true'
        self.managementIp = '1.1.1.1'


@pytest.fixture
def BigIPs():
    mock_bigips = []
    for bigip in range(4):
        mock_bigip = mock.MagicMock()
        mock_bigip.__name = 'me'
        mock_bigip.tm.cm.devices.get_collection.return_value = \
            [MockDeviceInfo('test')]
        mock_bigip.tm.cm.devices.get_collection.__name__ = 'test'
        mock_bigips.append(mock_bigip)
    return mock_bigips


@pytest.fixture
def TrustDomainCreateNew(BigIPs):
    mock_bigips = BigIPs
    td = TrustDomain()
    return td, mock_bigips


def test_validate_device_not_trusted(TrustDomainCreateNew):
    td, mock_bigips = TrustDomainCreateNew
    with pytest.raises(DeviceNotTrusted) as ex:
        td.devices = mock_bigips
        td.validate()
    assert "'test' is not trusted by 'test', which trusts: []" in \
        ex.value.message
