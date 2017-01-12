# Copyright 2015-2106 F5 Networks Inc.
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

import copy
import pytest

from f5.bigip.tm.ltm.persistence import Cookie
from f5.bigip.tm.ltm.persistence import Dest_Addr
from f5.bigip.tm.ltm.persistence import Hash
from f5.bigip.tm.ltm.persistence import Msrdp
from f5.bigip.tm.ltm.persistence import Sip
from f5.bigip.tm.ltm.persistence import Source_Addr
from f5.bigip.tm.ltm.persistence import Ssl
from f5.bigip.tm.ltm.persistence import Universal

from requests.exceptions import HTTPError
from six import iteritems


# Helper class to limit code repetition
class HelperTest(object):
    def __init__(self, collection_name):
        self.timeout = '150'
        self.partition = 'Common'
        self.lowered = collection_name.lower()
        self.test_name = 'test.' + self.urielementname()
        self.kinds = {'cookie': 'tm:ltm:persistence:cookie:cookiestate',
                      'dest_addr': 'tm:ltm:persistence:'
                                   'dest-addr:dest-addrstate',
                      'hash': 'tm:ltm:persistence:hash:hashstate',
                      'msrdp': 'tm:ltm:persistence:msrdp:msrdpstate',
                      'sip': 'tm:ltm:persistence:sip:sipstate',
                      'source_addr': 'tm:ltm:persistence:'
                                     'source-addr:source-addrstate',
                      'ssl': 'tm:ltm:persistence:ssl:sslstate',
                      'universal': 'tm:ltm:persistence:'
                                   'universal:universalstate'}

    def urielementname(self):
        if self.lowered[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        return self.lowered[:-endind]

    def delete_resource(self, resource):
        try:
            foo = resource.load(name=self.test_name, partition=self.partition)
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            return
        foo.delete()

    def setup_test(self, request, mgmt_root, **kwargs):
        def teardown():
            self.delete_resource(resource)

        resourcecollection =\
            getattr(getattr(getattr(mgmt_root.tm, 'ltm'), 'persistence'),
                    self.lowered)
        resource = getattr(resourcecollection, self.urielementname())
        if resource.exists(name=self.test_name, partition=self.partition):
            resource.load(
                name=self.test_name, partition=self.partition).delete()
        created = resource.create(name=self.test_name,
                                  partition=self.partition,
                                  **kwargs)
        request.addfinalizer(teardown)
        return created, resourcecollection

    def load_resource(self, mgmt_root):
        resourcecollection =\
            getattr(getattr(getattr(mgmt_root.tm, 'ltm'), 'persistence'),
                    self.lowered)
        resource = getattr(resourcecollection, self.urielementname())

        r = resource.load(name=self.test_name)
        return r

    def test_create_req_arg(self, request, mgmt_root, **kwargs):
        r, _ = self.setup_test(request, mgmt_root, **kwargs)
        assert r.name == self.test_name
        assert r.kind == self.kinds[self.urielementname()]
        if self.urielementname() == 'msrdp' or self.urielementname() == 'ssl':
            assert r.timeout == '300'
        else:
            assert r.timeout == '180'

    def test_create_optional_args(self, request, mgmt_root):
        r, _ = self.setup_test(request, mgmt_root, timeout=self.timeout)
        assert r.name == self.test_name
        assert r.kind == self.kinds[self.urielementname()]
        assert r.timeout == self.timeout

    def test_refresh(self, request, mgmt_root):
        r, _ = self.setup_test(request, mgmt_root)

        assert r.name == self.test_name
        assert r.kind == self.kinds[self.urielementname()]
        if self.urielementname() == 'msrdp' or self.urielementname() == 'ssl':
            assert r.timeout == '300'
        else:
            assert r.timeout == '180'

        r2 = self.load_resource(mgmt_root)
        r2.update(timeout=self.timeout)
        assert r2.name == self.test_name
        assert r2.kind == self.kinds[self.urielementname()]
        assert r2.timeout == self.timeout
        r.refresh()
        assert r.timeout == r2.timeout

    def test_modify(self, request, mgmt_root):
        r, _ = self.setup_test(request, mgmt_root)
        original_dict = copy.copy(r.__dict__)
        itm = 'timeout'
        r.modify(timeout=self.timeout)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r.__dict__[k]
            elif k == itm:
                assert r.__dict__[k] == '150'

    def test_delete(self, request, mgmt_root):
        resourcecollection =\
            getattr(getattr(getattr(mgmt_root.tm, 'ltm'), 'persistence'),
                    self.lowered)
        resource = getattr(resourcecollection, self.urielementname())
        r, _ = self.setup_test(request, mgmt_root)
        r.delete()
        with pytest.raises(HTTPError) as err:
            resource.load(name=self.test_name)
        assert err.value.response.status_code == 404

    def test_load(self, request, mgmt_root):
        r, _ = self.setup_test(request, mgmt_root)
        assert r.name == self.test_name
        assert r.kind == self.kinds[self.urielementname()]
        if self.urielementname() == 'msrdp' or self.urielementname() == 'ssl':
            assert r.timeout == '300'
        else:
            assert r.timeout == '180'

        r.update(timeout=self.timeout)
        assert r.timeout == self.timeout
        r2 = self.load_resource(mgmt_root)
        assert r2.name == r.name
        assert r2.kind == r.kind
        assert r2.timeout == r.timeout

    def test_collection(self, mgmt_root):
        resourcecollection =\
            getattr(getattr(getattr(mgmt_root.tm, 'ltm'), 'persistence'),
                    self.lowered)
        rc = resourcecollection.get_collection()
        assert isinstance(rc, list)
        assert len(rc)
        if self.lowered == 'cookie':
            assert isinstance(rc[0], Cookie)
        elif self.lowered == 'dest_addr':
            assert isinstance(rc[0], Dest_Addr)
        elif self.lowered == 'hash':
            assert isinstance(rc[0], Hash)
        elif self.lowered == 'msrdp':
            assert isinstance(rc[0], Msrdp)
        elif self.lowered == 'sip':
            assert isinstance(rc[0], Sip)
        elif self.lowered == 'source_addr':
            assert isinstance(rc[0], Source_Addr)
        elif self.lowered == 'ssl':
            assert isinstance(rc[0], Ssl)
        elif self.lowered == 'universal':
            assert isinstance(rc[0], Universal)


class TestCookies(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('cookies')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('cookies')
        helper.test_collection(mgmt_root)


class TestDestAddr(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('dest_addrs')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('dest_addrs')
        helper.test_collection(mgmt_root)


class TestHash(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('hashs')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('hashs')
        helper.test_collection(mgmt_root)


class TestMsrdp(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('msrdps')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('msrdps')
        helper.test_collection(mgmt_root)


class TestSip(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('sips')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('sips')
        helper.test_collection(mgmt_root)


class TestSourceAddr(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('source_addrs')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('source_addrs')
        helper.test_collection(mgmt_root)


class TestSsl(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('ssls')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('ssls')
        helper.test_collection(mgmt_root)


class TestUniversal(object):
    def test_MCURDL(self, request, mgmt_root):
        helper = HelperTest('universals')
        helper.test_create_req_arg(request, mgmt_root)
        helper.test_create_optional_args(request, mgmt_root)
        helper.test_refresh(request, mgmt_root)
        helper.test_modify(request, mgmt_root)
        helper.test_load(request, mgmt_root)
        helper.test_delete(request, mgmt_root)

    def test_collection(self, mgmt_root):
        helper = HelperTest('universals')
        helper.test_collection(mgmt_root)
