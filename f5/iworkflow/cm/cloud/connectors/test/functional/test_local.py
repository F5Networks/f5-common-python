# Copyright 2015-2016 F5 Networks Inc.
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


@pytest.fixture(scope='module')
def connector(mgmt_root):
    locals = mgmt_root.cm.cloud.connectors.locals
    local = locals.local.create(name='local1')
    yield local
    local.delete()


class TestLocal(object):
    def test_local_curdl(self, connector):
        assert connector.name == 'local1'
        assert connector.kind == 'cm:cloud:connectors:cloudconnectorstate'
        assert connector.selfLink.startswith(
            'https://localhost/mgmt/cm/cloud/connectors/local/'
        )
