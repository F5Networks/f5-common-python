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

import mock
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.resource import Collection
from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.gtm.pool import A
from f5.bigip.tm.gtm.pool import Aaaa
from f5.bigip.tm.gtm.pool import Cname
from f5.bigip.tm.gtm.pool import Mx
from f5.bigip.tm.gtm.pool import Naptr
from f5.bigip.tm.gtm.pool import Pool
from f5.bigip.tm.gtm.pool import PoolCollection
from f5.bigip.tm.gtm.pool import Srv

from six import iterkeys


@pytest.fixture
def FakePoolv11():
    fake_gtm = mock.MagicMock()
    fake_pool = PoolCollection(fake_gtm)
    fake_pool._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_pool


class TestPools(object):
    def test_new_method_v11(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.gtm.pools
        assert isinstance(p1, Collection)
        assert hasattr(p1, 'pool')
        assert not hasattr(p1, 'a_s')
        assert not hasattr(p1, 'aaaas')
        assert not hasattr(p1, 'cnames')
        assert not hasattr(p1, 'mxs')
        assert not hasattr(p1, 'naptrs')
        assert not hasattr(p1, 'srvs')

    def test_new_method_v12(self, fakeicontrolsession_v12):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.gtm.pools
        assert isinstance(p1, OrganizingCollection)
        assert not hasattr(p1, 'pool')
        assert hasattr(p1, 'a_s')
        assert hasattr(p1, 'aaaas')
        assert hasattr(p1, 'cnames')
        assert hasattr(p1, 'mxs')
        assert hasattr(p1, 'naptrs')
        assert hasattr(p1, 'srvs')


class TestCreatev11(object):
    def test_create_two_v11(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.gtm.pools.pool
        p2 = b.tm.gtm.pools.pool
        assert p1 is not p2

    def test_create_no_args_v11(self, FakePoolv11):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePoolv11.pool.create()


class TestCollectionv11(object):
    def test_pool_attr_exists(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p = b.tm.gtm.pools
        test_meta = p._meta_data['attribute_registry']
        test_meta2 = p._meta_data['allowed_lazy_attributes']
        kind = 'tm:gtm:pool:poolstate'
        assert kind in list(iterkeys(test_meta))
        assert Pool in test_meta2


# Start v12.x Tests
# Helper class to limit code repetition
class HelperTest(object):
    def __init__(self, collection_name):
        self.partition = 'Common'
        self.lowered = collection_name.lower()
        self.test_name = 'fakepool_' + self.urielementname()
        self.poolkinds = {'a': 'tm:gtm:pool:a:astate',
                          'aaaa': 'tm:gtm:pool:aaaa:aaaastate',
                          'cname': 'tm:gtm:pool:cname:cnamestate',
                          'mx': 'tm:gtm:pool:mx:mxstate',
                          'naptr': 'tm:gtm:pool:naptr:naptrstate',
                          'srv': 'tm:gtm:pool:srv:srvstate'}

    def urielementname(self):
        if self.lowered[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        return self.lowered[:-endind]

    def set_resources(self, fakeicontrolsession_v12):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        resourcecollection =\
            getattr(getattr(getattr(mr.tm, 'gtm'), 'pools'),
                    self.lowered)
        resource1 = getattr(resourcecollection, self.urielementname())
        resource2 = getattr(resourcecollection, self.urielementname())
        return resource1, resource2

    def set_collections(self, fakeicontrolsession_v12):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        resourcecollection =\
            getattr(getattr(getattr(mr.tm, 'gtm'), 'pools'),
                    self.lowered)
        return resourcecollection

    def test_collections(self, fakeicontrolsession_v12, klass):
        rc = self.set_collections(fakeicontrolsession_v12)
        test_meta = rc._meta_data['attribute_registry']
        test_meta2 = rc._meta_data['allowed_lazy_attributes']
        kind = self.poolkinds[self.urielementname()]
        assert kind in list(iterkeys(test_meta))
        assert klass in test_meta2

    def test_create_two_v12(self, fakeicontrolsession_v12):
        r1, r2, = self.set_resources(fakeicontrolsession_v12)
        assert r1 is not r2

    def test_create_no_args_v12(self, fakeicontrolsession_v12):
        r1, r2, = self.set_resources(fakeicontrolsession_v12)
        del r2
        with pytest.raises(MissingRequiredCreationParameter):
            r1.create()


class Testv12(object):
    def test_wideip_type_a(self, fakeicontrolsession_v12):
        p = HelperTest('a_s')
        p.test_collections(fakeicontrolsession_v12, A)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_aaaa(self, fakeicontrolsession_v12):
        p = HelperTest('aaaas')
        p.test_collections(fakeicontrolsession_v12, Aaaa)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_cname(self, fakeicontrolsession_v12):
        p = HelperTest('cnames')
        p.test_collections(fakeicontrolsession_v12, Cname)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_mx(self, fakeicontrolsession_v12):
        p = HelperTest('Mxs')
        p.test_collections(fakeicontrolsession_v12, Mx)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_naptr(self, fakeicontrolsession_v12):
        p = HelperTest('Naptrs')
        p.test_collections(fakeicontrolsession_v12, Naptr)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_srv(self, fakeicontrolsession_v12):
        p = HelperTest('Srvs')
        p.test_collections(fakeicontrolsession_v12, Srv)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)
