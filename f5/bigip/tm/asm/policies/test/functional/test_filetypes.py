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

from f5.bigip.tm.asm.policies.filetypes import Filetype
from requests.exceptions import HTTPError


class TestFiletypes(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        ft1 = policy.filetypes_s.filetype.create(name=name)
        assert ft1.kind == 'tm:asm:policies:filetypes:filetypestate'
        assert ft1.name == name
        assert ft1.responseCheck is False
        ft1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        ft1 = policy.filetypes_s.filetype.create(
            name=name,
            responseCheck=True
        )
        assert ft1.kind == 'tm:asm:policies:filetypes:filetypestate'
        assert ft1.name == name
        assert ft1.responseCheck is True
        ft1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        ft1 = policy.filetypes_s.filetype.create(name=name)
        ft2 = policy.filetypes_s.filetype.load(id=ft1.id)
        assert ft1.kind == ft2.kind
        assert ft1.name == ft2.name
        assert ft1.responseCheck == ft2.responseCheck
        ft2.modify(responseCheck=True)
        assert ft1.responseCheck is False
        assert ft2.responseCheck is True
        ft1.refresh()
        assert ft1.responseCheck is True
        ft1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        ft1 = policy.filetypes_s.filetype.create(name=name)
        idhash = str(ft1.id)
        ft1.delete()
        with pytest.raises(HTTPError) as err:
            policy.filetypes_s.filetype.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.filetypes_s.filetype.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        ft1 = policy.filetypes_s.filetype.create(name=name)
        assert ft1.kind == 'tm:asm:policies:filetypes:filetypestate'
        assert ft1.name == name
        assert ft1.responseCheck is False
        ft1.modify(responseCheck=True)
        assert ft1.responseCheck is True
        ft2 = policy.filetypes_s.filetype.load(id=ft1.id)
        assert ft1.name == ft2.name
        assert ft1.selfLink == ft2.selfLink
        assert ft1.kind == ft2.kind
        assert ft1.responseCheck == ft2.responseCheck
        ft1.delete()

    def test_filetypes_subcollection(self, policy):
        ftc = policy.filetypes_s.get_collection()
        assert isinstance(ftc, list)
        assert len(ftc)
        assert isinstance(ftc[0], Filetype)
