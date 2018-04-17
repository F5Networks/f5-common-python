# Copyright 2017 F5 Networks Inc.
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

from f5.bigip.cm.system import Tmos
from f5.sdk_exception import UnsupportedMethod

import mock
import pytest


@pytest.fixture
def FakeTmos():
    mo = mock.MagicMock()
    r = {'tmos_version': '11.6.0'}
    m = mock.MagicMock()
    m.__getitem__.side_effect = r.__getitem__
    m.__iter__.side_effect = r.__iter__
    mo._meta_data['bigip']._meta_data = m
    resource = Tmos(mo)

    return resource


class TestTmos(object):
    def test_create(self, FakeTmos):
        with pytest.raises(UnsupportedMethod):
            FakeTmos.create()

    def test_modify(self, FakeTmos):
        with pytest.raises(UnsupportedMethod):
            FakeTmos.modify()

    def test_update(self, FakeTmos):
        with pytest.raises(UnsupportedMethod):
            FakeTmos.update()

    def test_delete(self, FakeTmos):
        with pytest.raises(UnsupportedMethod):
            FakeTmos.delete()
