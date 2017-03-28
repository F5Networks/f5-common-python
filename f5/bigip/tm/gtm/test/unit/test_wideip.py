# Copyright 2014-2017 F5 Networks Inc.
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
from f5.bigip.resource import OrganizingCollection
from f5.bigip.tm.gtm.wideip import A
from f5.bigip.tm.gtm.wideip import Aaaa
from f5.bigip.tm.gtm.wideip import Cname
from f5.bigip.tm.gtm.wideip import Mx
from f5.bigip.tm.gtm.wideip import Naptr
from f5.bigip.tm.gtm.wideip import Srv
from f5.bigip.tm.gtm.wideip import Wideip
from f5.bigip.tm.gtm.wideip import WideipCollection
from f5.sdk_exception import MissingRequiredCreationParameter

from six import iterkeys


@pytest.fixture
def FakeWideipv11():
    fake_gtm = mock.MagicMock()
    fake_wideip = WideipCollection(fake_gtm)
    fake_wideip._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_wideip


class TestWideips(object):
    def test_new_method_v11(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        w1 = b.tm.gtm.wideips
        assert isinstance(w1, Collection)
        assert hasattr(w1, 'wideip')
        assert not hasattr(w1, 'a_s')
        assert not hasattr(w1, 'aaaas')
        assert not hasattr(w1, 'cnames')
        assert not hasattr(w1, 'mxs')
        assert not hasattr(w1, 'naptrs')
        assert not hasattr(w1, 'srvs')

    def test_new_method_v12(self, fakeicontrolsession_v12):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        w1 = b.tm.gtm.wideips
        assert isinstance(w1, OrganizingCollection)
        assert hasattr(w1, 'a_s')
        assert hasattr(w1, 'aaaas')
        assert hasattr(w1, 'cnames')
        assert hasattr(w1, 'mxs')
        assert hasattr(w1, 'naptrs')
        assert hasattr(w1, 'srvs')
        assert not hasattr(w1, 'wideip')


class TestCreatev11(object):
    def test_create_two_v11(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        w1 = b.tm.gtm.wideips.wideip
        w2 = b.tm.gtm.wideips.wideip
        assert w1 is not w2

    def test_create_no_args_v11(self, FakeWideipv11):
        with pytest.raises(MissingRequiredCreationParameter):
            FakeWideipv11.wideip.create()


class TestCollectionv11(object):
    def test_wideip_attr_exists(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        w = b.tm.gtm.wideips
        test_meta = w._meta_data['attribute_registry']
        test_meta2 = w._meta_data['allowed_lazy_attributes']
        kind = 'tm:gtm:wideip:wideipstate'
        assert kind in list(iterkeys(test_meta))
        assert Wideip in test_meta2


# Start v12.x Tests
# Helper class to limit code repetition
class HelperTest(object):
    def __init__(self, collection_name):
        self.lowered = collection_name.lower()
        self.kinds = {'a': 'tm:gtm:wideip:a:astate',
                      'aaaa': 'tm:gtm:wideip:aaaa:aaaastate',
                      'cname': 'tm:gtm:wideip:cname:cnamestate',
                      'mx': 'tm:gtm:wideip:mx:mxstate',
                      'naptr': 'tm:gtm:wideip:naptr:naptrstate',
                      'srv': 'tm:gtm:wideip:srv:srvstate'}

    def urielementname(self):
        if self.lowered[-2:] == '_s':
            endind = 2
        else:
            endind = 1
        return self.lowered[:-endind]

    def set_resources(self, fakeicontrolsession_v12):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b = mr.tm
        resourcecollection =\
            getattr(getattr(getattr(b, 'gtm'), 'wideips'),
                    self.lowered)
        resource1 = getattr(resourcecollection, self.urielementname())
        resource2 = getattr(resourcecollection, self.urielementname())
        return resource1, resource2

    def set_collections(self, fakeicontrolsession_v12):
        mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
        b = mr.tm
        resourcecollection =\
            getattr(getattr(getattr(b, 'gtm'), 'wideips'),
                    self.lowered)
        return resourcecollection

    def test_collections(self, fakeicontrolsession_v12, klass):
        rc = self.set_collections(fakeicontrolsession_v12)
        test_meta = rc._meta_data['attribute_registry']
        test_meta2 = rc._meta_data['allowed_lazy_attributes']
        kind = self.kinds[self.urielementname()]
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
        w = HelperTest('a_s')
        w.test_collections(fakeicontrolsession_v12, A)
        w.test_create_two_v12(fakeicontrolsession_v12)
        w.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_aaaa(self, fakeicontrolsession_v12):
        w = HelperTest('aaaas')
        w.test_collections(fakeicontrolsession_v12, Aaaa)
        w.test_create_two_v12(fakeicontrolsession_v12)
        w.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_cname(self, fakeicontrolsession_v12):
        w = HelperTest('cnames')
        w.test_collections(fakeicontrolsession_v12, Cname)
        w.test_create_two_v12(fakeicontrolsession_v12)
        w.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_mx(self, fakeicontrolsession_v12):
        w = HelperTest('Mxs')
        w.test_collections(fakeicontrolsession_v12, Mx)
        w.test_create_two_v12(fakeicontrolsession_v12)
        w.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_naptr(self, fakeicontrolsession_v12):
        w = HelperTest('Naptrs')
        w.test_collections(fakeicontrolsession_v12, Naptr)
        w.test_create_two_v12(fakeicontrolsession_v12)
        w.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_wideip_type_srv(self, fakeicontrolsession_v12):
        w = HelperTest('Srvs')
        w.test_collections(fakeicontrolsession_v12, Srv)
        w.test_create_two_v12(fakeicontrolsession_v12)
        w.test_create_no_args_v12(fakeicontrolsession_v12)
