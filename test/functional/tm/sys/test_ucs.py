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

import pytest
import time


@pytest.mark.skipif(pytest.config.getoption('--release') != '12.1.0',
                    reason='Needs v12.1 TMOS to pass')
class TestUcs(object):
    def test_ucs_LR(self, bigip):
        f = bigip.sys.ucs.load()
        ucs1 = len(f.items)
        assert ucs1 >= 0
        bigip.sys.ucs.exec_cmd('save', name='foobar.ucs')
        time.sleep(1)
        f.refresh()
        ucs2 = len(f.items)
        assert ucs2 > ucs1
