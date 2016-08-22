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

import pytest


class TestConfig(object):
    def test_save(self, bigip):
        c = bigip.sys.config
        c.exec_cmd('save')

    def test_update(selfself, mgmt_root):
        with pytest.raises(UnsupportedMethod) as ex:
            mgmt_root.tm.sys.config.update(foo="bar")
        assert 'does not support the update method' in ex.value.message
