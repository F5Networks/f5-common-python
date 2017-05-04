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
from f5.bigip.tm.sys.software.volume import Volume
from f5.sdk_exception import UnsupportedOperation
import pytest


class TestVolume(object):
    def test_create_raises(self, mgmt_root):
        with pytest.raises(UnsupportedOperation):
            mgmt_root.tm.sys.software.volumes.volume.create()

    def test_modify_raises(self, mgmt_root):
        with pytest.raises(UnsupportedOperation):
            mgmt_root.tm.sys.software.volumes.volume.modify()

    def test_update_raises(self, mgmt_root):
        with pytest.raises(UnsupportedOperation):
            mgmt_root.tm.sys.software.volumes.volume.update()

    def test_delete(self, mgmt_root):
        # Until we are able to install ISOs in Jenkins (which will allow us to
        # create volumes) we cannot test delete
        pass

    def test_load(self, mgmt_root, opt_release):
        r1 = mgmt_root.tm.sys.software.volumes.volume.load(name='HD1.1')
        link = 'https://localhost/mgmt/tm/sys/software/volume/HD1.1'
        assert r1.selfLink.startswith(link)
        assert r1.status == 'complete'
        assert r1.product == 'BIG-IP'
        rc = mgmt_root.tm.sys.software.volumes.get_collection()
        if len(rc) == 1:
            assert rc[0].active is True
            assert rc[0].name == 'HD1.1'
            assert LooseVersion(rc[0].version) == LooseVersion(opt_release)

    def test_collection(self, mgmt_root):
        rc = mgmt_root.tm.sys.software.volumes.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        assert isinstance(rc[0], Volume)
