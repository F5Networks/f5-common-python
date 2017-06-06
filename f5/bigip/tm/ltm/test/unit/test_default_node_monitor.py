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


from f5.bigip.tm.ltm.default_node_monitor import Default_Node_Monitor
from f5.sdk_exception import UnsupportedMethod


@pytest.fixture
def FakeDefaultNodeMonitor():
    fake_dnm = mock.MagicMock()
    return Default_Node_Monitor(fake_dnm)


def test_create_raises(FakeDefaultNodeMonitor):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeDefaultNodeMonitor.create()
    assert EIO.value.message == "Default_Node_Monitor does not support the " \
                                "create method"


def test_delete_raises(FakeDefaultNodeMonitor):
    with pytest.raises(UnsupportedMethod) as EIO:
        FakeDefaultNodeMonitor.delete()
    assert EIO.value.message == "Default_Node_Monitor does not support the " \
                                "delete method"
