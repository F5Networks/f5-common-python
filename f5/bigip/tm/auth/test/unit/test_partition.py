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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.auth.partition import Partition
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakePartition():
    fake_part_s = mock.MagicMock()
    fake_part = Partition(fake_part_s)
    return fake_part


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('localhost', 'admin', 'admin')
        n1 = b.tm.auth.partitions.partition
        n2 = b.tm.auth.partitions.partition
        assert n1 is not n2

    def test_create_no_args(self, FakePartition):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePartition.create()

    def test_create_description(self, FakePartition):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePartition.create(description='description')
