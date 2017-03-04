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

from f5.bigip import ManagementRoot
from f5.bigip.shared.iapp import Package_Management_Task
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.sdk_exception import UnsupportedOperation

import mock
import pytest
from six import iterkeys


@pytest.fixture
def FakeIapp():
    mo = mock.MagicMock()
    fake_iapp = Package_Management_Task(mo)
    return fake_iapp


class TestIapp(object):
    def test_update_raises(self, FakeIapp):
        with pytest.raises(UnsupportedOperation):
            FakeIapp.update()

    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t1 = b.shared.iapp.package_management_tasks_s.package_management_task
        t2 = b.shared.iapp.package_management_tasks_s.package_management_task
        assert t1 is t2

    def test_create_no_args(self, FakeIapp):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeIapp.create()

    def test_collection(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        t = b.shared.iapp.package_management_tasks_s
        test_meta = t._meta_data['attribute_registry']
        test_meta2 = t._meta_data['allowed_lazy_attributes']
        kind = 'shared:iapp:package-management-tasks:iapppackagemanagementtaskstate'  # NOQA
        assert kind in list(iterkeys(test_meta))
        assert Package_Management_Task in test_meta2
        assert t._meta_data['object_has_stats'] is False
