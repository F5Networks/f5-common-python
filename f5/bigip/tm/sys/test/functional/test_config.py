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

from f5.sdk_exception import UnsupportedMethod
from tempfile import NamedTemporaryFile

import os
import pytest


class TestConfig(object):
    def test_save(self, mgmt_root):
        c = mgmt_root.tm.sys.config
        config_save = c.exec_cmd('save')
        assert config_save.command == 'save'

    def test_load(self, mgmt_root):
        c = mgmt_root.tm.sys.config
        config_load = c.exec_cmd('load')
        assert config_load.command == 'load'

    def test_merge(self, mgmt_root):
        # Create a BIG-IP object to merge
        ntf = NamedTemporaryFile(delete=False)
        ntf_basename = os.path.basename(ntf.name)
        ntf.write('ltm pool mergepool { }')
        ntf.seek(0)
        # upload the file to BIG-IP
        mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)
        c = mgmt_root.tm.sys.config
        config_merge = c.exec_cmd('load',
                                  merge=True,
                                  file='/var/config/rest/downloads/{0}'.format(ntf_basename))
        assert config_merge.command == 'load'
        assert config_merge.options[0]['merge'] is True
        assert mgmt_root.tm.ltm.pools.pool.exists(name='mergepool') is True

        p1 = mgmt_root.tm.ltm.pools.pool.load(name='mergepool')
        p1.delete()

    def test_update(self, mgmt_root):
        with pytest.raises(UnsupportedMethod) as ex:
            mgmt_root.tm.sys.config.update(foo="bar")
        assert 'does not support the update method' in ex.value.message
