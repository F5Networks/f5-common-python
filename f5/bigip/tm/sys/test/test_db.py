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

from f5.bigip.resource import UnsupportedOperation
from f5.bigip.tm.sys import Dbs
import mock
import pytest


@pytest.fixture
def fake_dbs():
    fake_sys = mock.MagicMock()
    dbs = Dbs(fake_sys)
    dbs._meta_data['bigip'].tmos_version = '11.6.0'
    return dbs


class TestDb(object):
    def test_create_raises(self):
        dbs = fake_dbs()
        print(dbs.raw)
        db = dbs.db
        with pytest.raises(UnsupportedOperation):
            db.create()

    def test_delete_raises(self):
        dbs = fake_dbs()
        db = dbs.db
        with pytest.raises(UnsupportedOperation):
            db.delete()
