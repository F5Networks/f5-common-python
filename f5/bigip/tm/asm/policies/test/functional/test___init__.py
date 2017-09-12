# Copyright 2015 F5 Networks Inc.
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
from f5.bigip.tm.asm.policies.parameters import ParametersResource
from f5.bigip.tm.asm.policies import Policy
from requests.exceptions import HTTPError


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('13.0.0'),
    reason='Needs TMOS version less than v13.0.0 to pass.'
)
class TestPolicy(object):
    def test_create_req_arg(self, policy):
        pol1 = policy
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri + endpoint
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.subPath == '/Common'
        assert pol1.kind == 'tm:asm:policies:policystate'

    def test_create_optional_args(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        codes = [400, 401, 403]
        pol1 = mgmt_root.tm.asm.policies_s.policy.create(
            name=name,
            allowedResponseCodes=codes
        )
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri+endpoint
        assert pol1.name == name
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.kind == 'tm:asm:policies:policystate'
        assert pol1.allowedResponseCodes == codes
        pol1.delete()

    def test_refresh(self, policy, mgmt_root):
        pol1 = policy
        pol2 = mgmt_root.tm.asm.policies_s.policy.load(id=pol1.id)
        assert pol1.name == pol2.name
        assert pol1.selfLink == pol2.selfLink
        assert pol1.kind == pol2.kind
        assert pol1.allowedResponseCodes == pol2.allowedResponseCodes
        pol1.modify(allowedResponseCodes=[400, 503])
        assert pol1.selfLink == pol2.selfLink
        assert pol1.allowedResponseCodes != pol2.allowedResponseCodes
        pol2.refresh()
        assert pol1.allowedResponseCodes == pol2.allowedResponseCodes

    def test_delete(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        pol1 = mgmt_root.tm.asm.policies_s.policy.create(name=name)
        idhash = str(pol1.id)
        pol1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.policies_s.policy.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.policies_s.policy.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, mgmt_root):
        pol1 = policy
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri+endpoint
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.subPath == '/Common'
        assert pol1.kind == 'tm:asm:policies:policystate'
        pol1.modify(allowedResponseCodes=[400, 503])
        assert pol1.allowedResponseCodes == [400, 503]
        pol2 = mgmt_root.tm.asm.policies_s.policy.load(id=pol1.id)
        assert pol1.name == pol2.name
        assert pol1.selfLink == pol2.selfLink
        assert pol1.kind == pol2.kind
        assert pol1.allowedResponseCodes == pol2.allowedResponseCodes

    def test_policy_collection(self, policy, mgmt_root):
        pc = mgmt_root.tm.asm.policies_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Policy)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('13.0.0'),
    reason='Needs TMOS version greater than or equal to v13.0.0 to pass.'
)
class TestPolicyV13(object):
    def test_create_req_arg(self, policy):
        pol1 = policy
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri + endpoint
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.subPath == '/Common'
        assert pol1.kind == 'tm:asm:policies:policystate'

    def test_create_optional_args(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        codes = [400, 401, 403]
        pol1 = mgmt_root.tm.asm.policies_s.policy.create(
            name=name,
            allowedResponseCodes=codes
        )
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri+endpoint
        assert pol1.name == name
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.kind == 'tm:asm:policies:policystate'

        # In v13, the allowedResponseCodes were moved to the General
        # UnnamedResource
        generals = pol1.general.load()
        assert generals.allowedResponseCodes == codes
        pol1.delete()

    def test_refresh(self, policy, mgmt_root):
        pol1 = policy
        pol2 = mgmt_root.tm.asm.policies_s.policy.load(id=pol1.id)
        gen1 = pol1.general.load()
        gen2 = pol2.general.load()
        assert pol1.name == pol2.name
        assert pol1.selfLink == pol2.selfLink
        assert pol1.kind == pol2.kind
        assert gen1.allowedResponseCodes == gen2.allowedResponseCodes
        gen1.modify(allowedResponseCodes=[400, 503])
        assert pol1.selfLink == pol2.selfLink
        assert gen1.allowedResponseCodes != gen2.allowedResponseCodes
        gen2.refresh()
        assert gen1.allowedResponseCodes == gen2.allowedResponseCodes

    def test_delete(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        pol1 = mgmt_root.tm.asm.policies_s.policy.create(name=name)
        idhash = str(pol1.id)
        pol1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.policies_s.policy.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.asm.policies_s.policy.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy, mgmt_root):
        pol1 = policy
        gen1 = pol1.general.load()
        endpoint = str(pol1.id)
        base_uri = 'https://localhost/mgmt/tm/asm/policies/'
        final_uri = base_uri + endpoint
        assert pol1.selfLink.startswith(final_uri)
        assert pol1.subPath == '/Common'
        assert pol1.kind == 'tm:asm:policies:policystate'
        gen1.modify(allowedResponseCodes=[400, 503])
        assert gen1.allowedResponseCodes == [400, 503]
        pol2 = mgmt_root.tm.asm.policies_s.policy.load(id=pol1.id)
        gen2 = pol2.general.load()
        assert pol1.name == pol2.name
        assert pol1.selfLink == pol2.selfLink
        assert pol1.kind == pol2.kind
        assert gen1.allowedResponseCodes == gen2.allowedResponseCodes

    def test_policy_collection(self, policy, mgmt_root):
        pc = mgmt_root.tm.asm.policies_s.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Policy)


class TestPolicyParameters(object):
    def test_create_req_arg(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        param1 = policy.parameters_s.parameter.create(name=name)
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == name
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is False
        param1.delete()

    def test_create_optional_args(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        param1 = policy.parameters_s.parameter.create(
            name=name,
            sensitiveParameter=True
        )
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == name
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is True
        param1.delete()

    def test_refresh(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        param1 = policy.parameters_s.parameter.create(name=name)
        param2 = policy.parameters_s.parameter.load(id=param1.id)
        assert param1.kind == param2.kind
        assert param1.name == param2.name
        assert param1.level == param2.level
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param2.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is False
        assert param2.sensitiveParameter is True
        param1.refresh()
        assert param1.sensitiveParameter is True
        param1.delete()

    def test_delete(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        param1 = policy.parameters_s.parameter.create(name=name)
        idhash = str(param1.id)
        param1.delete()
        with pytest.raises(HTTPError) as err:
            policy.parameters_s.parameter.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.parameters_s.parameter.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        param1 = policy.parameters_s.parameter.create(name=name)
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == name
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is False
        param1.modify(sensitiveParameter=True)
        assert param1.sensitiveParameter is True
        param2 = policy.parameters_s.parameter.load(id=param1.id)
        assert param1.name == param2.name
        assert param1.selfLink == param2.selfLink
        assert param1.kind == param2.kind
        assert param1.level == param2.level
        assert param1.sensitiveParameter == param2.sensitiveParameter
        param1.delete()

    def test_parameters_subcollection(self, policy):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        param1 = policy.parameters_s.parameter.create(name=name)
        assert param1.kind == 'tm:asm:policies:parameters:parameterstate'
        assert param1.name == name
        assert param1.type == 'explicit'
        assert param1.level == 'global'
        assert param1.sensitiveParameter is False

        cc = policy.parameters_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], ParametersResource)
        param1.delete()
