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

import pytest

from f5.bigip.tm.asm.policy_templates import Policy_Template
from f5.sdk_exception import UnsupportedOperation
from requests.exceptions import HTTPError


@pytest.fixture(scope='class')
def return_template(mgmt_root):
    rc = mgmt_root.tm.asm.policy_templates_s.get_collection()
    return rc[0], rc[0].id


class TestPolicyTemplates(object):
    def test_create_raises(self, mgmt_root):
        rc = mgmt_root.tm.asm.policy_templates_s
        with pytest.raises(UnsupportedOperation):
            rc.policy_template.create()

    def test_delete_raises(self, mgmt_root):
        rc = mgmt_root.tm.asm.policy_templates_s
        with pytest.raises(UnsupportedOperation):
            rc.policy_template.delete()

    def test_modify_raises(self, mgmt_root):
        rc = mgmt_root.tm.asm.policy_templates_s
        with pytest.raises(UnsupportedOperation):
            rc.policy_template.modify()

    def test_refresh(self, mgmt_root):
        res1, hashid = return_template(mgmt_root)
        rc = mgmt_root.tm.asm.policy_templates_s
        res2 = rc.policy_template.load(id=hashid)
        assert res1.selfLink == res2.selfLink
        assert res1.title == res2.title
        assert res1.id == res2.id
        assert res1.userDefined == res2.userDefined
        res1.refresh()
        assert res1.selfLink == res2.selfLink
        assert res1.title == res2.title
        assert res1.id == res2.id
        assert res1.userDefined == res2.userDefined

    def test_load_no_object(self, mgmt_root):
        rc = mgmt_root.tm.asm.policy_templates_s
        with pytest.raises(HTTPError) as err:
            rc.policy_template.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, mgmt_root):
        _, hashid = return_template(mgmt_root)
        rc = mgmt_root.tm.asm.policy_templates_s
        res = rc.policy_template.load(id=hashid)
        link = 'https://localhost/mgmt/tm/asm/policy-templates/'
        assert res.selfLink.startswith(link + hashid)
        assert res.id == hashid
        assert res.userDefined is False

    def test_collection(self, mgmt_root):
        sc = mgmt_root.tm.asm.policy_templates_s.get_collection()
        assert isinstance(sc, list)
        assert len(sc)
        assert isinstance(sc[0], Policy_Template)
