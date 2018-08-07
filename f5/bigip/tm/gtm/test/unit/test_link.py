# Copyright 2018 F5 Networks Inc.
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
from f5.bigip.tm.gtm.link import Link
from f5.sdk_exception import MissingRequiredCreationParameter


@pytest.fixture
def FakeLink():
    fake_links = mock.MagicMock()
    fake_link = Link(fake_links)
    return fake_link


class TestCreate(object):
    def test_create_two(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        l1 = b.tm.gtm.links.link
        l2 = b.tm.gtm.links.link
        assert l1 is not l2

    def test_create_no_args(self, FakeLink):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLink.create()

    def test_create_datacenter(self, FakeLink):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLink.create(datacenter='Common')

    def test_create_name(self, FakeLink):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLink.create(name='myname')

    def test_create_routerAddresses(self, FakeLink):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeLink.create(routerAddress=[{'name': '10.10.10.10'}])
