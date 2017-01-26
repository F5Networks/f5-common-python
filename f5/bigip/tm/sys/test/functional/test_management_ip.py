# Copyright 2015-2106 F5 Networks Inc.
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
from f5.sdk_exception import UnsupportedMethod
from icontrol.exceptions import iControlUnexpectedHTTPError


def setup_management_ip_test(request, mgmt_root):
    def teardown():
        try:
            mgmt_root.tm.sys.management_ips.management_ip.load(
                name=mip[0].name)
        except iControlUnexpectedHTTPError:
            mgmt_root.tm.sys.management_ips.management_ip.create(
                name=mip[0].name)

    request.addfinalizer(teardown)

    mip = mgmt_root.tm.sys.management_ips.get_collection()
    return mip


def test_missing_required_params(mgmt_root):
    with pytest.raises(MissingRequiredCreationParameter) as err:
        mgmt_root.tm.sys.management_ips.management_ip.create()
    assert 'Missing required params: [\'name\']' in str(err)


def test_missing_mask(request, mgmt_root):
    name = '172.16.44.15'
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


def test_create_delete_addr(request, mgmt_root):
    mip = setup_management_ip_test(request, mgmt_root)
    assert mip[0].name == '172.16.44.15/24'

    mip1 = mgmt_root.tm.sys.management_ips.management_ip.load(
        name=mip[0].name)
    assert mip1.name == mip[0].name
    mip1.delete()

    with pytest.raises(iControlUnexpectedHTTPError) as err:
        mgmt_root.tm.sys.management_ips.management_ip.load(
            name=mip[0].name)
    assert ') was not found.' in str(err.value.message)

    mip2 = mgmt_root.tm.sys.management_ips.management_ip.create(
        name='172.16.44.16/24')
    assert mip2.name == '172.16.44.16/24'


def test_modify_addr(request, mgmt_root):
    mip = setup_management_ip_test(request, mgmt_root)
    mip1 = mgmt_root.tm.sys.management_ips.management_ip.load(
        name=mip[0].name)
    mip1.name = '172.16.44.20/24'
    with pytest.raises(UnsupportedMethod) as err:
        mip1.modify()
    assert 'Management_Ip does not support the modify method' in str(err)


def test_update_addr(request, mgmt_root):
    mip = setup_management_ip_test(request, mgmt_root)
    mip1 = mgmt_root.tm.sys.management_ips.management_ip.load(
        name=mip[0].name)
    mip1.name = '172.16.44.20/24'
    with pytest.raises(UnsupportedMethod) as err:
        mip1.update()
    assert 'Management_Ip does not support the update method' in str(err)
