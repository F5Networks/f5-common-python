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

import os
import pytest
import tempfile

from requests.exceptions import HTTPError
from f5.bigip.tm.asm.policies.host_names import Host_Name


class TestHostNames(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).replace('_', '')
        host1 = policy.host_names_s.host_name.create(
            name=name + '.com'
        )
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == name + '.com'
        assert host1.includeSubdomains is False
        host1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).replace('_', '')
        host1 = policy.host_names_s.host_name.create(
            name=name + '.com',
            includeSubdomains=True
        )
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == name + '.com'
        assert host1.includeSubdomains is True
        host1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).replace('_', '')
        host1 = policy.host_names_s.host_name.create(
            name=name + '.com'
        )
        host2 = policy.host_names_s.host_name.load(id=host1.id)
        assert host1.kind == host2.kind
        assert host1.name == host2.name
        assert host1.includeSubdomains == host2.includeSubdomains
        host2.modify(includeSubdomains=True)
        assert host1.includeSubdomains is False
        assert host2.includeSubdomains is True
        host1.refresh()
        assert host1.includeSubdomains is True
        host1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).replace('_', '')
        host1 = policy.host_names_s.host_name.create(
            name=name + '.com'
        )
        idhash = str(host1.id)
        host1.delete()
        with pytest.raises(HTTPError) as err:
            policy.host_names_s.host_name.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.host_names_s.host_name.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).replace('_', '')
        host1 = policy.host_names_s.host_name.create(
            name=name + '.com'
        )
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == name + '.com'
        assert host1.includeSubdomains is False
        host1.modify(includeSubdomains=True)
        assert host1.includeSubdomains is True
        host2 = policy.host_names_s.host_name.load(id=host1.id)
        assert host1.name == host2.name
        assert host1.selfLink == host2.selfLink
        assert host1.kind == host2.kind
        assert host1.includeSubdomains == host2.includeSubdomains
        host1.delete()

    def test_hostnames_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name).replace('_', '')
        host1 = policy.host_names_s.host_name.create(
            name=name + '.com'
        )
        assert host1.kind == 'tm:asm:policies:host-names:host-namestate'
        assert host1.name == name + '.com'
        cc = policy.host_names_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Host_Name)
        host1.delete()
