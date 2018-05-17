# Copyright 2018 F5 Networks Inc.
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

from f5.bigip.tm.sys.disk import Logical_Disk

import pytest
from requests import HTTPError


class TestLogicalDisk(object):
    def test_load_refresh(self, mgmt_root):
        d1 = mgmt_root.tm.sys.disk.logical_disks.logical_disk.load(name='HD1')
        assert d1.name == 'HD1'
        assert d1.kind == 'tm:sys:disk:logical-disk:logical-diskstate'
        assert d1.mode == 'mixed'

        d2 = mgmt_root.tm.sys.disk.logical_disks.logical_disk.load(name='HD1')
        assert d2.name == d1.name
        assert d2.kind == d1.kind
        assert d2.mode == d1.mode

        d1.refresh()
        assert d1.name == d2.name
        assert d1.kind == d2.kind
        assert d1.mode == d2.mode

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.sys.disk.logical_disks
        with pytest.raises(HTTPError) as err:
            rc.logical_disk.load(name='not_exists')
        assert err.value.response.status_code == 404

    def test_logical_disks_collection(self, mgmt_root):
        rc = mgmt_root.tm.sys.disk.logical_disks.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Logical_Disk)
