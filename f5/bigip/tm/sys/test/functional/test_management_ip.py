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

import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from icontrol.exceptions import iControlUnexpectedHTTPError


def test_missing_required_params(mgmt_root):
    with pytest.raises(MissingRequiredCreationParameter) as err:
        mgmt_root.tm.sys.management_ips.management_ip.create()
    assert 'Missing required params: [\'name\']' in str(err)


def test_missing_mask(request, mgmt_root):
    name = '10.0.2.15'
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.sys.management_ips.management_ip.create(
            name=name)
    assert 'a netmask must be specified' in str(err.value.message)


def test_invalid_addr(request, mgmt_root):
    name = '/24'
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.sys.management_ips.management_ip.create(
            name=name)
    assert 'invalid address' in str(err.value.message)


def test_create_existing_addr(request, mgmt_root):
    name = '10.0.2.15/24'
    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.sys.management_ips.management_ip.create(
            name=name)
    assert 'The requested management IP (10.0.2.15) already exists.' in\
           str(err.value.message)


def test_modify_addr(request, mgmt_root):
    name = '10.0.2.15/24'
    mip1 = mgmt_root.tm.sys.management_ips.management_ip.load(
        name=name)
    assert hasattr(mip1, 'description') is False
    # Add a description and update
    mip1.modify(description='adding a description')
    # Assert description is now present
    assert mip1.description == 'adding a description'
    # Remove description
    mip1.modify(description='')
    assert hasattr(mip1, 'description') is False


def test_update_addr(request, mgmt_root):
    name = '10.0.2.15/24'
    mip3 = mgmt_root.tm.sys.management_ips.management_ip.load(
        name=name)
    mip3.name = '10.0.2.16/24'
    mip3.update()
    # Prove name doesn't actually update
    assert mip3.name == '10.0.2.15/24'
    # Shouldn't be a description currently
    assert hasattr(mip3, 'description') is False
    # Add a description and update
    mip3.description = 'adding a description'
    mip3.update()
    # Assert description is now present
    assert mip3.description == 'adding a description'
    # Remove description
    delattr(mip3, 'description')
    mip3.update()
