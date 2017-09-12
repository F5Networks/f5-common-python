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
import random

from f5.bigip.tm.asm.policies.whitelist_ips import Whitelist_Ip
from f5.sdk_exception import AttemptedMutationOfReadOnly
from requests.exceptions import HTTPError


class TestWhitelistIps(object):
    def test_create_req_arg(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(4))
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name
        )
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == name
        assert ip1.ipMask == '255.255.255.255'
        ip1.delete()

    def test_create_optional_args(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(3)) + '.0'
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name,
            ipMask='255.255.255.0'
        )
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == name
        assert ip1.ipMask == '255.255.255.0'
        ip1.delete()

    def test_refresh(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(4))
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name
        )
        ip2 = policy.whitelist_ips_s.whitelist_ip.load(id=ip1.id)
        assert ip1.kind == ip2.kind
        assert ip1.ipAddress == ip2.ipAddress
        assert ip1.description == ip2.description
        ip2.modify(description='TESTFAKE')
        assert ip1.description == ''
        assert ip2.description == 'TESTFAKE'
        ip1.refresh()
        assert ip1.description == 'TESTFAKE'
        ip1.delete()

    def test_modify_read_only_raises(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(3)) + '.0'
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name,
            ipMask='255.255.255.0'
        )
        with pytest.raises(AttemptedMutationOfReadOnly):
            ip1.modify(ipMask='255.255.0.0')

    def test_delete(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(4))
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name
        )
        idhash = str(ip1.id)
        ip1.delete()
        with pytest.raises(HTTPError) as err:
            policy.whitelist_ips_s.whitelist_ip.load(id=idhash)
        assert err.value.response.status_code == 404

    def test_load_no_object(self, policy):
        with pytest.raises(HTTPError) as err:
            policy.whitelist_ips_s.whitelist_ip.load(id='Lx3553-321')
        assert err.value.response.status_code == 404

    def test_load(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(4))
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name
        )
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == name
        assert ip1.ipMask == '255.255.255.255'
        assert ip1.description == ''
        ip1.modify(description='TESTFAKE')
        assert ip1.description == 'TESTFAKE'
        ip2 = policy.whitelist_ips_s.whitelist_ip.load(id=ip1.id)
        assert ip1.kind == ip2.kind
        assert ip1.ipAddress == ip2.ipAddress
        assert ip1.selfLink == ip2.selfLink
        assert ip1.description == ip2.description
        ip1.delete()

    def test_whitelistips_subcollection(self, policy):
        name = '.'.join(str(random.randint(1, 254)) for i in range(4))
        ip1 = policy.whitelist_ips_s.whitelist_ip.create(
            ipAddress=name
        )
        assert ip1.kind == 'tm:asm:policies:whitelist-ips:whitelist-ipstate'
        assert ip1.ipAddress == name
        assert ip1.ipMask == '255.255.255.255'
        cc = policy.whitelist_ips_s.get_collection()
        assert isinstance(cc, list)
        assert len(cc)
        assert isinstance(cc[0], Whitelist_Ip)
        ip1.delete()
