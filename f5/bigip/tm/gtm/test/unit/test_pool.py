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
from f5.bigip.resource import URICreationCollision
from f5.bigip.tm.gtm.pool import A
from f5.bigip.tm.gtm.pool import Aaaa
from f5.bigip.tm.gtm.pool import Cname
from f5.bigip.tm.gtm.pool import Member
from f5.bigip.tm.gtm.pool import Members_s
from f5.bigip.tm.gtm.pool import MembersCollection_v11
from f5.bigip.tm.gtm.pool import MembersCollectionA
from f5.bigip.tm.gtm.pool import MembersCollectionAAAA
from f5.bigip.tm.gtm.pool import MembersCollectionCname
from f5.bigip.tm.gtm.pool import MembersCollectionMx
from f5.bigip.tm.gtm.pool import MembersCollectionNaptr
from f5.bigip.tm.gtm.pool import MembersCollectionSrv
from f5.bigip.tm.gtm.pool import MembersResource_v11
from f5.bigip.tm.gtm.pool import MembersResourceA
from f5.bigip.tm.gtm.pool import MembersResourceAAAA
from f5.bigip.tm.gtm.pool import MembersResourceCname
from f5.bigip.tm.gtm.pool import MembersResourceMx
from f5.bigip.tm.gtm.pool import MembersResourceNaptr
from f5.bigip.tm.gtm.pool import MembersResourceSrv
from f5.bigip.tm.gtm.pool import Mx
from f5.bigip.tm.gtm.pool import Naptr
from f5.bigip.tm.gtm.pool import Pool
from f5.bigip.tm.gtm.pool import PoolCollection
from f5.bigip.tm.gtm.pool import Srv
from requests import HTTPError

from six import iterkeys


@pytest.fixture
def FakePoolv11():
    fake_gtm = mock.MagicMock()
    fake_pool = PoolCollection(fake_gtm)
    fake_pool._meta_data['bigip'].tmos_version = '11.6.0'
    return fake_pool


def Makepool(fakeicontrolsession):
    b = ManagementRoot('192.168.1.1', 'admin', 'admin')
    p = b.tm.gtm.pools.pool
    p._meta_data['uri'] = \
        'https://192.168.1.1:443/mgmt/tm/gtm/pool/~Common~testpool/'
    return p


class MockResponse(object):
    def __init__(self, attr_dict):
        self.__dict__ = attr_dict

    def json(self):
        return self.__dict__


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


class TestMembers(object):
    def test_members_s_subcoll_and_new_method_v11(self, fakeicontrolsession):
        memc = Members_s(Makepool(fakeicontrolsession))
        kind = 'tm:gtm:pool:members:membersstate'
        test_meta = memc._meta_data['attribute_registry']
        test_meta2 = memc._meta_data['allowed_lazy_attributes']
        assert isinstance(memc, MembersCollection_v11)
        assert hasattr(memc, 'member')
        assert memc.__class__.__name__ == 'Members_s'
        assert kind in list(iterkeys(test_meta))
        assert Member in test_meta2

    def test_members_new_method_v11(self, fakeicontrolsession):
        memc = Members_s(Makepool(fakeicontrolsession))
        memres = memc.member
        assert isinstance(memres, MembersResource_v11)
        assert memres.__class__.__name__ == 'Member'

    def test_member_create_v11(self, fakeicontrolsession):
        memc = Members_s(Makepool(fakeicontrolsession))
        memc2 = Members_s(Makepool(fakeicontrolsession))
        m1 = memc.member
        m2 = memc2.member
        assert m1 is not m2

    def test_member_create_no_args_v11(self, fakeicontrolsession):
        memc = Members_s(Makepool(fakeicontrolsession))
        with pytest.raises(MissingRequiredCreationParameter):
            memc.member.create()


class TestPoolCreatev11(object):
    def test_create_two_v11(self, fakeicontrolsession):
        b = ManagementRoot('192.168.1.1', 'admin', 'admin')
        p1 = b.tm.gtm.pools.pool
        p2 = b.tm.gtm.pools.pool
        assert p1 is not p2

    def test_create_no_args_v11(self, FakePoolv11):
        with pytest.raises(MissingRequiredCreationParameter):
            FakePoolv11.pool.create()


class TestPoolCollectionv11(object):
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
        self.memkinds = {'a': 'tm:gtm:pool:a:members:membersstate',
                         'aaaa': 'tm:gtm:pool:aaaa:members:membersstate',
                         'cname': 'tm:gtm:pool:cname:members:membersstate',
                         'mx': 'tm:gtm:pool:mx:members:membersstate',
                         'naptr': 'tm:gtm:pool:naptr:members:membersstate',
                         'srv': 'tm:gtm:pool:srv:members:membersstate'}

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

    def set_subcoll_pool(self, fakeicontrolsession_v12):
        r1, r2, = self.set_resources(fakeicontrolsession_v12)
        r1._meta_data['uri'] = \
            'https://192.168.1.1:443/mgmt/tm/gtm/pool/'+self.urielementname()\
            + '~Common~testpool/'
        r2._meta_data['uri'] = \
            'https://192.168.1.1:443/mgmt/tm/gtm/pool/'+self.urielementname()\
            + '~Common~testpool/'
        return r1, r2

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
        with pytest.raises(MissingRequiredCreationParameter):
            r1.create()

    def test_members_s_subcoll_and_new_method_v12(
            self, fakeicontrolsession_v12, klass):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        test_meta = memc._meta_data['attribute_registry']
        test_meta2 = memc._meta_data['allowed_lazy_attributes']
        kind = self.memkinds[self.urielementname()]
        assert isinstance(memc, klass)
        assert hasattr(memc, 'member')
        assert memc.__class__.__name__ == 'Members_s'
        assert kind in list(iterkeys(test_meta))
        assert Member in test_meta2

    def test_members_new_method_v12(self, fakeicontrolsession_v12, klass):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memres = memc.member
        assert isinstance(memres, klass)
        assert memres.__class__.__name__ == 'Member'

    def test_member_create_v12(self, fakeicontrolsession_v12):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memc2 = Members_s(r2)
        m1 = memc.member
        m2 = memc2.member
        assert m1 is not m2

    def test_member_create_no_args_v12(self, fakeicontrolsession_v12):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memres = memc.member
        with pytest.raises(MissingRequiredCreationParameter):
            memres.create()

    def test_URI_creation_collision(self, fakeicontrolsession_v12):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memres = memc.member
        memres._meta_data['bigip']._meta_data['tmos_version'] = '12.1.0'
        memres._meta_data['uri'] = 'URI'
        with pytest.raises(URICreationCollision) as UCCEIO:
            memres.create(uri='URI')
        assert str(UCCEIO.value) == \
            "There was an attempt to assign a new uri to this resource," \
            " the _meta_data['uri'] is URI and it should not be changed."

    def test_non_404_response__v12_1(self, fakeicontrolsession_v12):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memc._meta_data['uri'] = 'mock://URI'
        memres = memc.member
        memres._meta_data['bigip']._meta_data['tmos_version'] = '12.1.0'
        mock_response = mock.MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        error = HTTPError(response=mock_response)
        session = mock.MagicMock(name='mock_session')
        session.post.side_effect = error
        memres._meta_data['bigip']._meta_data['icr_session'] = session
        with pytest.raises(HTTPError) as err:
                memres.create(name='fake', partition='fakepart')
        assert err.value.response.status_code == 500

    def test_404_response_v12_1(self, fakeicontrolsession_v12):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memres = memc.member
        memres._meta_data['bigip']._meta_data['tmos_version'] = '12.1.0'
        mock_response = mock.MagicMock()
        mock_response.status_code = 404
        error = HTTPError(response=mock_response)
        MRO = MockResponse({u"kind": self.memkinds[self.urielementname()],
                            u"selfLink":
                                u".../~Common~testpool/members/~Common~fake"})
        session = mock.MagicMock(name='mock_session')
        session.post.side_effect = error
        session.get.return_value = MRO
        memres._meta_data['bigip']._meta_data['icr_session'] = session
        a = memres.create(name='fake', partition='Common')
        assert a.selfLink == '.../~Common~testpool/members/~Common~fake'
        assert a.kind == self.memkinds[self.urielementname()]

    def test_200_response_v12_1(self, fakeicontrolsession_v12):
        r1, r2, = self.set_subcoll_pool(fakeicontrolsession_v12)
        memc = Members_s(r1)
        memres = memc.member
        memres._meta_data['bigip']._meta_data['tmos_version'] = '12.1.0'
        MRO = MockResponse({u"kind": self.memkinds[self.urielementname()],
                            u"selfLink":
                                u".../~Common~testpool/members/~Common~fake"})
        session = mock.MagicMock(name='mock_session')
        session.post.return_value = MRO
        memres._meta_data['bigip']._meta_data['icr_session'] = session
        a = memres.create(name='fake', partition='Common')
        assert a.selfLink == '.../~Common~testpool/members/~Common~fake'
        assert a.kind == self.memkinds[self.urielementname()]


class TestV12Members(object):
    def test_members_type_a(self, fakeicontrolsession_v12):
        p = HelperTest('A_s')
        p.test_members_s_subcoll_and_new_method_v12(fakeicontrolsession_v12,
                                                    MembersCollectionA)
        p.test_members_new_method_v12(fakeicontrolsession_v12,
                                      MembersResourceA)
        p.test_member_create_v12(fakeicontrolsession_v12)
        p.test_member_create_no_args_v12(fakeicontrolsession_v12)
        p.test_URI_creation_collision(fakeicontrolsession_v12)
        p.test_non_404_response__v12_1(fakeicontrolsession_v12)
        p.test_404_response_v12_1(fakeicontrolsession_v12)
        p.test_200_response_v12_1(fakeicontrolsession_v12)

    def test_members_type_aaaa(self, fakeicontrolsession_v12):
        p = HelperTest('Aaaas')
        p.test_members_s_subcoll_and_new_method_v12(fakeicontrolsession_v12,
                                                    MembersCollectionAAAA)
        p.test_members_new_method_v12(fakeicontrolsession_v12,
                                      MembersResourceAAAA)
        p.test_member_create_v12(fakeicontrolsession_v12)
        p.test_member_create_no_args_v12(fakeicontrolsession_v12)
        p.test_non_404_response__v12_1(fakeicontrolsession_v12)
        p.test_404_response_v12_1(fakeicontrolsession_v12)
        p.test_200_response_v12_1(fakeicontrolsession_v12)

    def test_members_type_cname(self, fakeicontrolsession_v12):
        p = HelperTest('Cnames')
        p.test_members_s_subcoll_and_new_method_v12(fakeicontrolsession_v12,
                                                    MembersCollectionCname)
        p.test_members_new_method_v12(fakeicontrolsession_v12,
                                      MembersResourceCname)
        p.test_member_create_v12(fakeicontrolsession_v12)
        p.test_member_create_no_args_v12(fakeicontrolsession_v12)

    def test_members_type_mx(self, fakeicontrolsession_v12):
        p = HelperTest('Mxs')
        p.test_members_s_subcoll_and_new_method_v12(fakeicontrolsession_v12,
                                                    MembersCollectionMx)
        p.test_members_new_method_v12(fakeicontrolsession_v12,
                                      MembersResourceMx)
        p.test_member_create_v12(fakeicontrolsession_v12)
        p.test_member_create_no_args_v12(fakeicontrolsession_v12)

    def test_members_type_naptr(self, fakeicontrolsession_v12):
        p = HelperTest('Naptrs')
        p.test_members_s_subcoll_and_new_method_v12(fakeicontrolsession_v12,
                                                    MembersCollectionNaptr)
        p.test_members_new_method_v12(fakeicontrolsession_v12,
                                      MembersResourceNaptr)
        p.test_member_create_v12(fakeicontrolsession_v12)
        p.test_member_create_no_args_v12(fakeicontrolsession_v12)

    def test_members_type_srv(self, fakeicontrolsession_v12):
        p = HelperTest('Srvs')
        p.test_members_s_subcoll_and_new_method_v12(fakeicontrolsession_v12,
                                                    MembersCollectionSrv)
        p.test_members_new_method_v12(fakeicontrolsession_v12,
                                      MembersResourceSrv)
        p.test_member_create_v12(fakeicontrolsession_v12)
        p.test_member_create_no_args_v12(fakeicontrolsession_v12)


class TestV12Pools(object):
    def test_pool_type_a(self, fakeicontrolsession_v12):
        p = HelperTest('A_s')
        p.test_collections(fakeicontrolsession_v12, A)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_pool_type_aaaa(self, fakeicontrolsession_v12):
        p = HelperTest('Aaaas')
        p.test_collections(fakeicontrolsession_v12, Aaaa)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_pool_type_cname(self, fakeicontrolsession_v12):
        p = HelperTest('Cnames')
        p.test_collections(fakeicontrolsession_v12, Cname)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_pool_type_mx(self, fakeicontrolsession_v12):
        p = HelperTest('Mxs')
        p.test_collections(fakeicontrolsession_v12, Mx)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_pool_type_naptr(self, fakeicontrolsession_v12):
        p = HelperTest('Naptrs')
        p.test_collections(fakeicontrolsession_v12, Naptr)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)

    def test_pool_type_srv(self, fakeicontrolsession_v12):
        p = HelperTest('Srvs')
        p.test_collections(fakeicontrolsession_v12, Srv)
        p.test_create_two_v12(fakeicontrolsession_v12)
        p.test_create_no_args_v12(fakeicontrolsession_v12)
