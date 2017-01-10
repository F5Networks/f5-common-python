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

import pytest
import time

from f5.sdk_exception import F5SDKError
from pytest import symbols
from requests.exceptions import HTTPError


def wait_for_state(obj, state):
    for x in range(60):
        obj.refresh()
        if obj.status == state:
            return
        elif obj.status == 'FAILED':
            raise F5SDKError(
                str(obj.errorMessage)
            )
        time.sleep(1)


@pytest.fixture(scope='function')
def decl_mgmt_authority(mgmt_root):
    authorities = mgmt_root.cm.asm.tasks.declare_mgmt_authority_s
    authority = authorities.declare_mgmt_authority.create(
        deviceIp=symbols.biq_bigip_unmanaged_device,
        deviceUsername="admin",
        devicePassword="admin",
        rootUser="root",
        rootPassword="default",
        createChildTasks="true",
        name="Import-device_{0}".format(symbols.biq_bigip_unmanaged_device)
    )
    try:
        wait_for_state(authority, 'FINISHED')
        yield authority
    except Exception:
        pass
    finally:
        authority.delete()


@pytest.fixture(scope='module')
def authorities(mgmt_root):
    authorities = mgmt_root.cm.asm.tasks.declare_mgmt_authority_s
    yield authorities


class TestDeclareManagementAuthority(object):
    def curdl(self, decl_mgmt_authority):
        assert decl_mgmt_authority.rootUser == 'NEW'
        assert decl_mgmt_authority.deviceIp == \
            symbols.biq_bigip_unmanaged_device
        assert decl_mgmt_authority.deviceUsername == 'admin'
        assert decl_mgmt_authority.kind == \
            'cm:asm:tasks:declare-mgmt-authority:dmataskitemstate'

    def test_load_no_object(self, authorities):
        with pytest.raises(HTTPError) as err:
            authorities.declare_mgmt_authority.load(
                id='9a8d42f7-543e'
            )
            assert err.response.status_code == 404

    def test_load(self, decl_mgmt_authority, authorities):
        hashid = str(decl_mgmt_authority.id)
        authority = authorities.declare_mgmt_authority.load(id=hashid)
        assert authority.id == decl_mgmt_authority.id
        assert authority.selfLink == decl_mgmt_authority.selfLink

    def test_exists(self, decl_mgmt_authority, authorities):
        hashid = str(decl_mgmt_authority.id)
        assert authorities.declare_mgmt_authority.exists(id=hashid)

    def test_refresh(self, decl_mgmt_authority):
        hashid = str(decl_mgmt_authority.id)
        link = decl_mgmt_authority.selfLink
        decl_mgmt_authority.refresh()
        assert decl_mgmt_authority.id == hashid
        assert decl_mgmt_authority.selfLink == link
