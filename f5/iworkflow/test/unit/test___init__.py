# Copyright 2014 F5 Networks Inc.
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

import mock
import pytest
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

from f5.iworkflow import ManagementRoot

from f5.iworkflow.cm import Cm
from f5.iworkflow.shared import Shared
from f5.iworkflow.tm import Tm


@pytest.fixture
def FakeIWorkflow(fakeiwficontrolsession):
    mo = ManagementRoot('FakeHostName', 'admin', 'admin')
    mo.icontrol = mock.MagicMock()
    return mo


@pytest.fixture
def FakeIWorkflowWithPort(fakeiwficontrolsession):
    mo = ManagementRoot('FakeHostName', 'admin', 'admin', port='10443')
    mo.icontrol = mock.MagicMock()
    return mo


def test___get__attr(FakeIWorkflow):
    bigip_dot_cm = FakeIWorkflow.cm
    assert isinstance(bigip_dot_cm, Cm)
    bigip_dot_shared = FakeIWorkflow.shared
    assert isinstance(bigip_dot_shared, Shared)
    bigip_dot_sys = FakeIWorkflow.tm
    assert isinstance(bigip_dot_sys, Tm)
    with pytest.raises(AttributeError):
        FakeIWorkflow.tm.this_is_not_a_real_attribute
    assert FakeIWorkflow.hostname == 'FakeHostName'


def test_invalid_args():
    with pytest.raises(TypeError) as err:
        ManagementRoot('FakeHostName', 'admin', 'admin', badArgs='foobar')
    assert 'Unexpected **kwargs' in str(err.value)


def test_icontrol_version(FakeIWorkflowWithPort):
    assert hasattr(FakeIWorkflowWithPort, 'icontrol_version')


def test_non_default_port_number(FakeIWorkflowWithPort):
    uri = urlparse.urlsplit(FakeIWorkflowWithPort._meta_data['uri'])
    assert uri.port == 10443
