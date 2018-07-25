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

from f5.bigip import ManagementRoot
from f5.sdk_exception import InvalidCommand
from f5.sdk_exception import UnsupportedMethod


import pytest


class TestServiceTmm(object):
    def test_update_raises(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '13.0.0'
        with pytest.raises(UnsupportedMethod):
            b.tm.sys.service.tmm.update()

    def test_modify_raises(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '13.0.0'
        with pytest.raises(UnsupportedMethod):
            b.tm.sys.service.tmm.modify()

    def test_invalid_cmd(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b._meta_data['tmos_version'] = '13.0.0'
        with pytest.raises(InvalidCommand):
            b.tm.sys.service.tmm.exec_cmd('reset')
