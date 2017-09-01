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
from f5.multi_device.exceptions import DeviceAlreadyInTrustDomain
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
    assert "'test' is not trusted by 'test', which trusts: []" in str(ex.value)


@mock.patch('f5.multi_device.trust_domain.TrustDomain._set_attributes')
@mock.patch('f5.multi_device.trust_domain.TrustDomain.validate')
def test___init__(mock_set_attr, mock_validate, BigIPs):
    mock_bigips = BigIPs
    td = TrustDomain(devices=mock_bigips)
    assert td._set_attributes.call_args == mock.call(devices=mock_bigips)


def test__set_attributes(BigIPs):
    mock_bigips = BigIPs
    td = TrustDomain()
    td._set_attributes(devices=mock_bigips, partition='test')
    assert td.devices == mock_bigips
    assert td.partition == 'test'
    assert td.device_group_name == 'device_trust_group'
    assert td.device_group_type == 'sync-only'


@mock.patch('f5.multi_device.trust_domain.TrustDomain._add_trustee')
@mock.patch('f5.multi_device.trust_domain.pollster')
def test_create(mock_add_trustee, mock_pollster, TrustDomainCreateNew):
    td, mock_bigips = TrustDomainCreateNew
    td.create(devices=mock_bigips, partition='test')
    assert td.devices == mock_bigips
    assert td.partition == 'test'
    assert td._add_trustee.call_args_list == \
        [
            mock.call(mock_bigips[1]),
            mock.call(mock_bigips[2]),
            mock.call(mock_bigips[3])
        ]


@mock.patch('f5.multi_device.trust_domain.TrustDomain._add_trustee')
@mock.patch('f5.multi_device.trust_domain.pollster')
@mock.patch('f5.multi_device.trust_domain.TrustDomain._remove_trustee')
def test_teardown(
        mock_add_trustee, mock_pollster, mock_rem_trustee, TrustDomainCreateNew
):
    td, mock_bigips = TrustDomainCreateNew
    td.create(devices=mock_bigips, partition='test')
    td.teardown()
    assert td.domain == {}
    assert td._remove_trustee.call_args_list == \
        [
            mock.call(mock_bigips[0]),
            mock.call(mock_bigips[1]),
            mock.call(mock_bigips[2]),
            mock.call(mock_bigips[3])
        ]


@mock.patch('f5.multi_device.trust_domain.get_device_info')
@mock.patch('f5.multi_device.trust_domain.TrustDomain._modify_trust')
def test__add_trustee(mock_dev_info, mock_mod_trust, TrustDomainCreateNew):
    td, mock_bigips = TrustDomainCreateNew
    td._set_attributes(devices=mock_bigips, partition='test')
    td._add_trustee(mock_bigips[1])
    assert td._modify_trust.call_args == \
        mock.call(mock_bigips[0], td._get_add_trustee_cmd, mock_bigips[1])


@mock.patch('f5.multi_device.trust_domain.TrustDomain._modify_trust')
def test__add_trustee_already_in_domain(
        mock_mod_trust, TrustDomainCreateNew
):
    td, mock_bigips = TrustDomainCreateNew
    td._set_attributes(devices=mock_bigips, partition='test')
    td.domain = {'test': 'device'}
    with pytest.raises(DeviceAlreadyInTrustDomain) as ex:
        td._add_trustee(mock_bigips[1])
    assert "Device: 'test' is already in this trust domain" in str(ex.value)
