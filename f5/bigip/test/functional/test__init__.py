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

import pytest

from f5.bigip import ManagementRoot
from f5.sdk_exception import TimeoutError


def test_invalid_args(opt_bigip, opt_username, opt_password, opt_port):
    with pytest.raises(TypeError) as err:
        ManagementRoot(opt_bigip, opt_username, opt_password, port=opt_port,
                       badArgs='foobar')
    assert 'Unexpected **kwargs' in err.value.message


def test_icontrol_version(opt_bigip, opt_username, opt_password, opt_port):
    m = ManagementRoot(opt_bigip, opt_username, opt_password, port=opt_port)
    assert hasattr(m, 'icontrol_version')


def test_tmos_version(mgmt_root):
    assert mgmt_root.tmos_version == \
        mgmt_root._meta_data['bigip']._meta_data['tmos_version']
    assert mgmt_root.tmos_version is not None
    assert mgmt_root._meta_data['bigip']._meta_data['tmos_version'] != ''


def test_hard_timeout():
    # The IP and port here are set to these values deliberately. They should never resolve.
    with pytest.raises(TimeoutError) as ex:
        ManagementRoot('10.255.255.1', 'foo', 'bar', port=81, timeout=1)
    assert str(ex.value) == 'Timed out waiting for response'
