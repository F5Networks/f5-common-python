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

import pytest

from icontrol.exceptions import iControlUnexpectedHTTPError


def test_create_example_resource(request, mgmt_root):
    with pytest.raises(iControlUnexpectedHTTPError) as error:
        mgmt_root.tm.ltm.pools.pool.create(name='example')
    assert 'is a reserved keyword and must not be used as resource name' in str(error.value.message)


def test_load_example_resource(request, mgmt_root):
    x = mgmt_root.tm.ltm.pools.pool.load(name='example')
    assert x.kind == 'tm:ltm:pool:poolcollectionstate'
    assert x.kind != 'tm:ltm:pool:poolstate'
    assert x.items[0].get('name') is None
