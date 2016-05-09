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

from f5.bigip import BigIP

import mock
import pytest


@pytest.fixture
def FakeiControl():
    bigip = BigIP('host', 'fake_admin', 'fake_admin')
    bigip._meta_data['icr_session'] = mock.MagicMock()
    return bigip


class TestCMSync(object):
    def test_sync_to_group(self, FakeiControl):
        cm = FakeiControl.cm
        cm.sync_to_group('test')
        session = cm._meta_data['bigip']._meta_data['icr_session']
        session.post.assert_called_with(
            'https://host/mgmt/tm/cm/',
            json={'utilCmdArgs': 'config-sync to-group test', 'command': 'run'}
        )

    def test_sync_from_group(self, FakeiControl):
        cm = FakeiControl.cm
        cm.sync_from_group('test')
        session = cm._meta_data['bigip']._meta_data['icr_session']
        session.post.assert_called_with(
            'https://host/mgmt/tm/cm/',
            json={
                'utilCmdArgs': 'config-sync from-group test', 'command': 'run'
            }
        )
