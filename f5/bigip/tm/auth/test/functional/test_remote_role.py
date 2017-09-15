# Copyright 2017 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from distutils.version import LooseVersion
from f5.sdk_exception import UnsupportedOperation
import pytest


def setup_remote_role_test(request, mgmt_root):
    def teardown():
        # remove remote role info added during test
        rri1.delete()
    request.addfinalizer(teardown)

    rr = mgmt_root.tm.auth.remote_role.load()

    rri1 = rr.role_infos.role_info.create(name='adm',
                                          attribute='%F5-LTM-User-Info-1=adm',
                                          lineOrder=1)
    return rri1


class TestRemoteRole(object):
    @pytest.mark.skipif(
        LooseVersion(
            pytest.config.getoption('--release')
        ) < LooseVersion('12.0.0'),
        reason='Remote role isn\'t fully implemented until 12.')
    def test_RML_Remote_Role(self, request, mgmt_root):
        # Load a role
        role1 = setup_remote_role_test(request, mgmt_root)
        role2 = mgmt_root.tm.auth.remote_role.role_infos.role_info.load(name='adm')
        assert role1.deny == role2.deny

        # Modify the deny attribute on a role
        role1.modify(deny='enabled')
        assert 'enabled' in role1.deny
        assert 'enabled' not in role2.deny

        # Refresh
        role2.refresh()
        assert 'enabled' in role2.deny

        # Test update method not supported
        with pytest.raises(UnsupportedOperation) as ex:
            role1.deny = 'disabled'
            role1.update()
        assert 'does not support update, ' \
               'use modify instead' in ex.value.message
