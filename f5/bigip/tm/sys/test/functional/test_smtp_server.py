# Copyright 2018 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import os
import pytest
import tempfile


@pytest.fixture()
def smtp_server(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    n = mgmt_root.tm.sys.smtp_servers.smtp_server.create(name=name)
    yield n
    n.delete()


class TestSmtp_Server(object):
    def test_read(self, smtp_server):
        assert smtp_server.smtpServerPort == 25

    def test_update(self, smtp_server):
        smtp_server.update(fromAddress='foo@bar.com')
        assert smtp_server.fromAddress == 'foo@bar.com'
        smtp_server.refresh()
        assert smtp_server.fromAddress == 'foo@bar.com'

    def test_modify(self, smtp_server):
        smtp_server.modify(fromAddress='foo@bar.com')
        assert smtp_server.fromAddress == 'foo@bar.com'
        smtp_server.refresh()
        assert smtp_server.fromAddress == 'foo@bar.com'

    def test_delete(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        n = mgmt_root.tm.sys.smtp_servers.smtp_server.create(name=name)
        assert n.name == name
        n.delete()
        exists = mgmt_root.tm.sys.smtp_servers.smtp_server.exists(name=name)
        assert exists is False

    def test_pairs(self, smtp_server):
        assert smtp_server.authenticationDisabled is True
        assert smtp_server.authenticationEnabled is False
        smtp_server.update(authenticationDisabled=False)
        smtp_server.refresh()
        assert smtp_server.authenticationDisabled is False
        assert smtp_server.authenticationEnabled is True
