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

from distutils.version import LooseVersion
from f5.bigip.tm.asm.policies.sensitive_parameters import Sensitive_Parameter
from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('11.6.0'),
    reason='This collection is fully implemented on 11.6.0 or greater.'
)
class TestSensitiveParameters(object):
    def test_modify_raises(self, policy):
        with pytest.raises(UnsupportedOperation):
            policy.sensitive_parameters_s.sensitive_parameter.modify()

    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.sensitive_parameters_s.sensitive_parameter.create(
            name=name
        )
        assert r1.kind == 'tm:asm:policies:sensitive-parameters:sensitive-parameterstate'
        assert r1.name == name
        r1.delete()

    def test_refresh(self, set_s_par, policy):
        r1 = set_s_par
        r2 = policy.sensitive_parameters_s.sensitive_parameter.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.name == r2.name
        assert r1.id == r2.id
        r1.refresh()
        assert r1.kind == r2.kind
        assert r1.name == r2.name
        assert r1.id == r2.id

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        r1 = policy.sensitive_parameters_s.sensitive_parameter.create(
            name=name
        )
        idhash = r1.id
        r1.delete()
        with pytest.raises(HTTPError) as err:
            policy.sensitive_parameters_s.sensitive_parameter.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.sensitive_parameters_s.sensitive_parameter.load(
                id='Lx3553-321'
            )
        assert err.value.response.status_code == 404

    def test_load(self, set_s_par, policy):
        r1 = set_s_par
        assert r1.kind == 'tm:asm:policies:sensitive-parameters:sensitive-parameterstate'
        r2 = policy.sensitive_parameters_s.sensitive_parameter.load(id=r1.id)
        assert r1.kind == r2.kind
        assert r1.name == r2.name

    def test_sensitive_parameters_subcollection(self, policy):
        cc = policy.sensitive_parameters_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Sensitive_Parameter)
