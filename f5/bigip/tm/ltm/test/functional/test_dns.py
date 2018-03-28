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

from distutils.version import LooseVersion
from requests.exceptions import HTTPError


@pytest.fixture(scope='function')
def nameserver(mgmt_root):
    resource = mgmt_root.tm.ltm.dns.nameservers.nameserver.create(
        name='ns1',
        address='1.1.1.1',
        port=53
    )
    yield resource
    resource.delete()


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.0.0'),
    reason='This collection is fully implemented on 12.0.0 or greater.'
)
class TestAuditLogs(object):
    def test_update_refresh(self, nameserver):
        assert nameserver.kind == 'tm:ltm:dns:nameserver:nameserverstate'
        assert nameserver.port == 53
        nameserver.update(port=1234)
        nameserver.refresh()
        assert nameserver.port == 1234

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.ltm.dns.nameservers.nameserver.load(name='not-found')
        assert err.value.response.status_code == 404

    def test_load(self, nameserver, mgmt_root):
        r1 = mgmt_root.tm.ltm.dns.nameservers.nameserver.load(name='ns1')
        assert r1.kind == 'tm:ltm:dns:nameserver:nameserverstate'
        r2 = mgmt_root.tm.ltm.dns.nameservers.nameserver.load(name='ns1')
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink

    def test_collection(self, nameserver, mgmt_root):
        collection = mgmt_root.tm.ltm.dns.nameservers.get_collection()
        assert len(collection) == 1
