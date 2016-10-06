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
import copy
from distutils.version import LooseVersion
from f5.bigip.tm.gtm.pool import A
from f5.bigip.tm.gtm.pool import Aaaa
from f5.bigip.tm.gtm.pool import Cname
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
from f5.bigip.tm.gtm.pool import Srv
from pprint import pprint as pp
import pytest

from requests.exceptions import HTTPError
from six import iteritems

pp(__file__)


GTM_SERVER = 'fake_serv1'
GTM_VS = 'fakeVS'
RES_NAME = GTM_SERVER + ':' + GTM_VS
WIDEIPNAME = 'fake.wide.net'
TESTDESCRIPTION = "TESTDESCRIPTION"

# Dependencies setup to be shared between v11 and v12 tests


def delete_gtm_server(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.servers.server.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def delete_dc(mgmt_root, name, partition):
    try:
        delete_gtm_server(mgmt_root, GTM_SERVER)
        foo = mgmt_root.tm.gtm.datacenters.datacenter.load(
            name=name, partition=partition
        )
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def create_dc(request, mgmt_root, name, partition):
    def teardown():
        delete_dc(mgmt_root, name, partition)

    dc = mgmt_root.tm.gtm.datacenters.datacenter.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return dc


def setup_gtm_server(request, mgmt_root, name, partition, **kwargs):
    def teardown():
        delete_gtm_server(mgmt_root, name)

    dc = create_dc(request, mgmt_root, 'dc1', partition)
    serv1 = mgmt_root.tm.gtm.servers.server.create(
        name=name, datacenter=dc.name,
        **kwargs)
    request.addfinalizer(teardown)
    return serv1


def delete_gtm_vs(mgmt_root, name):
    s1 = mgmt_root.tm.gtm.servers.server.load(name=GTM_SERVER)
    try:
        foo = s1.virtual_servers_s.virtual_server.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_gtm_vs(request, mgmt_root, name, destination, **kwargs):
    def teardown():
        delete_gtm_vs(mgmt_root, name)

    s1 = setup_gtm_server(request, mgmt_root, GTM_SERVER, 'Common', **kwargs)
    vs = s1.virtual_servers_s.virtual_server.create(
        name=name, destination=destination)
    request.addfinalizer(teardown)
    return vs


def delete_wideip_v12(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.wideips.a_s.a.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_wideip_v12(request, mgmt_root, name, **kwargs):
    def teardown():
        delete_wideip_v12(mgmt_root, name)

    wideip1 = mgmt_root.tm.gtm.wideips.a_s.a.create(
        name=name, **kwargs)
    request.addfinalizer(teardown)
    return wideip1


# Start of V12.x Tests here


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
            getattr(getattr(getattr(mgmt_root.tm, 'gtm'), 'pools'),
                    self.lowered)
        resource = getattr(resourcecollection, self.urielementname())
        self.delete_resource(resource)
        created = resource.create(name=self.test_name,
                                  partition=self.partition,
                                  **kwargs)
        request.addfinalizer(teardown)
        return created, resourcecollection

    def test_MCURDL(self, request, mgmt_root, **kwargs):
        # Testing create
        pool, rescollection = self.setup_test(request, mgmt_root, **kwargs)
        assert pool.name == self.test_name
        assert pool.fullPath == '/Common/'+self.test_name
        assert pool.generation and isinstance(pool.generation, int)
        assert pool.kind == self.poolkinds[self.urielementname()]

        # Testing update
        pool.description = TESTDESCRIPTION
        pp(pool.raw)
        pool.update()
        if hasattr(pool, 'description'):
            assert pool.description == TESTDESCRIPTION

        # Testing refresh
        pool.description = ''
        pool.refresh()
        if hasattr(pool, 'description'):
            assert pool.description == TESTDESCRIPTION

        # Testing modify
        meta_data = pool.__dict__.pop('_meta_data')
        start_dict = copy.deepcopy(pool.__dict__)
        pool.__dict__['_meta_data'] = meta_data
        pool.modify(description='MODIFIED')
        desc = 'description'
        for k, v in iteritems(pool.__dict__):
            if k != desc:
                start_dict[k] = pool.__dict__[k]
                assert getattr(pool, k) == start_dict[k]
            elif k == desc:
                assert getattr(pool, desc) == 'MODIFIED'

        # Testing load
        p2 = getattr(rescollection, self.urielementname())
        pool2 = p2.load(partition=self.partition, name=self.test_name)
        assert pool.selfLink == pool2.selfLink

    def test_collection(self, request, mgmt_root, **kwargs):
        pool, rescollection = self.setup_test(request, mgmt_root, **kwargs)
        assert pool.name == self.test_name
        assert pool.fullPath == '/Common/'+self.test_name
        assert pool.generation and isinstance(pool.generation, int)
        assert pool.kind == self.poolkinds[self.urielementname()]

        coll = rescollection.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        if self.lowered == 'a_s':
            assert isinstance(coll[0], A)
        elif self.lowered == 'aaaas':
            assert isinstance(coll[0], Aaaa)
        elif self.lowered == 'cnames':
            assert isinstance(coll[0], Cname)
        elif self.lowered == 'mxs':
            assert isinstance(coll[0], Mx)
        elif self.lowered == 'naptrs':
            assert isinstance(coll[0], Naptr)
        elif self.lowered == 'srvs':
            assert isinstance(coll[0], Srv)

    def setup_members_test(self, request, mgmt_root, **kwargs):
        pool, rescollection = self.setup_test(request, mgmt_root, **kwargs)
        mem_coll = pool.members_s
        if isinstance(pool, A):
            setup_gtm_vs(request, mgmt_root, GTM_VS, '20.20.20.20:80',
                         addresses=[{'name': '1.1.1.1'}])
            member = mem_coll.member.create(name=RES_NAME,
                                            partition=self.partition)
        elif isinstance(pool, Aaaa):
            setup_gtm_vs(request, mgmt_root, GTM_VS,
                         'fd00:7967:71a5::.80',
                         addresses=[{'name': 'fda8:e5d6:5ef6::'}])
            member = mem_coll.member.create(name=RES_NAME,
                                            partition=self.partition)
        elif isinstance(pool, Cname) or isinstance(pool, Mx):
            setup_wideip_v12(request, mgmt_root, WIDEIPNAME,
                             partition=self.partition)
            member = mem_coll.member.create(name=WIDEIPNAME)
        elif isinstance(pool, Naptr):
            setup_wideip_v12(request, mgmt_root, WIDEIPNAME,
                             partition=self.partition)
            member = mem_coll.member.create(name=WIDEIPNAME,
                                            flags='a', service='http')
        elif isinstance(pool, Srv):
            setup_wideip_v12(request, mgmt_root, WIDEIPNAME,
                             partition=self.partition)
            member = mem_coll.member.create(name=WIDEIPNAME, port=80)

        return member, mem_coll, member.name

    def test_members_MCURDL(self, request, mgmt_root, **kwargs):
        # Testing create
        member, rescollection, name = self.setup_members_test(
            request, mgmt_root, **kwargs)
        assert member.name == name
        assert member.generation and isinstance(member.generation, int)
        assert member.kind == self.memkinds[self.urielementname()]

        # Testing update
        member.description = TESTDESCRIPTION
        pp(member.raw)
        member.update()
        if hasattr(member, 'description'):
            assert member.description == TESTDESCRIPTION

        # Testing refresh
        member.description = ''
        member.refresh()
        if hasattr(member, 'description'):
            assert member.description == TESTDESCRIPTION

        # Testing modify
        meta_data = member.__dict__.pop('_meta_data')
        start_dict = copy.deepcopy(member.__dict__)
        member.__dict__['_meta_data'] = meta_data
        member.modify(description='MODIFIED')
        desc = 'description'
        for k, v in iteritems(member.__dict__):
            if k != desc:
                start_dict[k] = member.__dict__[k]
                assert getattr(member, k) == start_dict[k]
            elif k == desc:
                assert getattr(member, desc) == 'MODIFIED'

    def test_members_sucollection(self, request, mgmt_root, **kwargs):
        member, rescollection, name = self.setup_members_test(
            request, mgmt_root, **kwargs)
        assert member.name == name
        assert member.generation and isinstance(member.generation, int)
        assert member.kind == self.memkinds[self.urielementname()]

        coll = rescollection.get_collection()
        assert isinstance(coll, list)
        assert len(coll)
        if self.lowered == 'a_s':
            assert isinstance(coll[0], MembersResourceA)
            assert rescollection.kind == \
                'tm:gtm:pool:a:members:memberscollectionstate'
        elif self.lowered == 'aaaas':
            assert isinstance(coll[0], MembersResourceAAAA)
            assert rescollection.kind == \
                'tm:gtm:pool:aaaa:members:memberscollectionstate'
        elif self.lowered == 'cnames':
            assert isinstance(coll[0], MembersResourceCname)
            assert rescollection.kind == \
                'tm:gtm:pool:cname:members:memberscollectionstate'
        elif self.lowered == 'mxs':
            assert isinstance(coll[0], MembersResourceMx)
            assert rescollection.kind == \
                'tm:gtm:pool:mx:members:memberscollectionstate'
        elif self.lowered == 'naptrs':
            assert isinstance(coll[0], MembersResourceNaptr)
            assert rescollection.kind == \
                'tm:gtm:pool:naptr:members:memberscollectionstate'
        elif self.lowered == 'srvs':
            assert isinstance(coll[0], MembersResourceSrv)
            assert rescollection.kind == \
                'tm:gtm:pool:srv:members:memberscollectionstate'


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolAtype(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('A_s')
        pool.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('A_s')
        pool.test_collection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolATypeSubcollMembers(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('A_s')
        pool.test_members_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('A_s')
        pool.test_members_sucollection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolAAAAtype(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Aaaas')
        pool.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Aaaas')
        pool.test_collection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolAAAATypeSubcollMembers(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Aaaas')
        pool.test_members_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Aaaas')
        pool.test_members_sucollection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolCnametype(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Cnames')
        pool.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Cnames')
        pool.test_collection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolCnameTypeSubcollMembers(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Cnames')
        pool.test_members_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Cnames')
        pool.test_members_sucollection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolMxstype(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Mxs')
        pool.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Mxs')
        pool.test_collection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolMxsTypeSubcollMembers(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Mxs')
        pool.test_members_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Mxs')
        pool.test_members_sucollection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolNaptrtype(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Naptrs')
        pool.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Naptrs')
        pool.test_collection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolNaptrTypeSubcollMembers(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Naptrs')
        pool.test_members_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Naptrs')
        pool.test_members_sucollection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPooSrvAtype(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Srvs')
        pool.test_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Srvs')
        pool.test_collection(request, mgmt_root)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestPoolSrvTypeSubcollMembers(object):
    def test_MCURDL(self, request, mgmt_root):
        pool = HelperTest('Srvs')
        pool.test_members_MCURDL(request, mgmt_root)

    def test_collection(self, request, mgmt_root):
        pool = HelperTest('Srvs')
        pool.test_members_sucollection(request, mgmt_root)

# End of v12.x Tests
# Start of v11.x Tests


def delete_pool(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.pools.pool.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_pool_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_pool(mgmt_root, name)

    poolc = mgmt_root.tm.gtm.pools
    pool = poolc.pool.create(name=name, partition=partition)
    request.addfinalizer(teardown)
    return pool, poolc


def setup_create_pool_test(request, mgmt_root, name):
    def teardown():
        delete_pool(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_create_member_test(request, mgmt_root, name):
    def teardown():
        delete_pool(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_member_basic_test(request, mgmt_root, name, partition, poolname):
    def teardown():
        delete_pool(mgmt_root, poolname)

    setup_gtm_vs(request, mgmt_root, GTM_VS, '20.20.20.20:80',
                 addresses=[{'name': '1.1.1.1'}])
    pool, poolcoll = setup_pool_basic_test(request, mgmt_root, poolname,
                                           partition)
    memberc = pool.members_s
    member = memberc.member.create(name=name, partition=partition)
    request.addfinalizer(teardown)
    return member, memberc


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion(
        '12.0.0'),
    reason='This collection exists on 11.x'
)
class TestPools_v11(object):
    def test_create_req_arg(self, request, mgmt_root):
        setup_create_pool_test(request, mgmt_root, 'fake_pool')
        pool1 = mgmt_root.tm.gtm.pools.pool.create(
            name='fake_pool', partition='Common')
        assert pool1.name == 'fake_pool'
        assert pool1.generation and isinstance(pool1.generation, int)
        assert pool1.kind == 'tm:gtm:pool:poolstate'
        assert pool1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/pool/~Common~fake_pool')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_pool_test(request, mgmt_root, 'fake_pool')
        pool1 = mgmt_root.tm.gtm.pools.pool.create(
            name='fake_pool', partition='Common', description=TESTDESCRIPTION)
        assert pool1.description == TESTDESCRIPTION
        assert pool1.limitMaxBpsStatus == 'disabled'

    def test_create_duplicate(self, request, mgmt_root):
        setup_create_pool_test(request, mgmt_root, 'fake_pool')
        try:
            mgmt_root.tm.gtm.pools.pool.create(name='fake_pool',
                                               partition='Common')
        except HTTPError as err:
            assert err.response.status_code == 400

    def test_refresh(self, request, mgmt_root):
        setup_pool_basic_test(request, mgmt_root, 'fake_pool', 'Common')
        p1 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
        p2 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')

        assert p1.limitMaxBpsStatus == 'disabled'
        assert p2.limitMaxBpsStatus == 'disabled'

        p2.update(limitMaxBpsStatus='enabled')
        assert p1.limitMaxBpsStatus == 'disabled'
        assert p2.limitMaxBpsStatus == 'enabled'

        p1.refresh()
        assert p1.limitMaxBpsStatus == 'enabled'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_pool_basic_test(request, mgmt_root, 'fake_pool', 'Common')
        p1 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
        assert p1.limitMaxBpsStatus == 'disabled'
        p1.limitMaxBpsStatus = 'enabled'
        p1.update()
        p2 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
        assert p2.limitMaxBpsStatus == 'enabled'

    def test_update(self, request, mgmt_root):
        p1, sc = setup_pool_basic_test(request, mgmt_root, 'fake_pool',
                                       'Common')
        assert p1.limitMaxBpsStatus == 'disabled'
        assert not hasattr(p1, 'description')
        p1.update(limitMaxBpsStatus='enabled', description=TESTDESCRIPTION)
        assert p1.limitMaxBpsStatus == 'enabled'
        assert hasattr(p1, 'description')
        assert p1.description == TESTDESCRIPTION

    def test_modify(self, request, mgmt_root):
        p1, sc = setup_pool_basic_test(request, mgmt_root, 'fake_pool',
                                       'Common')
        original_dict = copy.copy(p1.__dict__)
        limit = 'limitMaxBpsStatus'
        p1.modify(limitMaxBpsStatus='enabled')
        for k, v in iteritems(original_dict):
            if k != limit:
                original_dict[k] = p1.__dict__[k]
            elif k == limit:
                assert p1.__dict__[k] == 'enabled'

    def test_delete(self, request, mgmt_root):
        p1, sc = setup_pool_basic_test(request, mgmt_root, 'fake_pool',
                                       'Common')
        p1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.wideips.wideip.load(name='fake_pool')
            assert err.response.status_code == 404

    def test_pool_collection(self, request, mgmt_root):
        pool1, pcoll = setup_pool_basic_test(request, mgmt_root,
                                             'fake_pool', 'Common')

        assert pool1.fullPath == '/Common/fake_pool'
        assert pool1.name == 'fake_pool'
        assert pool1.generation and isinstance(pool1.generation, int)
        assert pool1.kind == 'tm:gtm:pool:poolstate'
        assert pool1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/pool/~Common~fake_pool')

        pc = pcoll.get_collection()
        assert isinstance(pc, list)
        assert len(pc)
        assert isinstance(pc[0], Pool)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion(
        '12.0.0'),
    reason='This collection exists on 11.x'
)
class TestMembersSubCollection_v11(object):
    def test_create_req_arg(self, request, mgmt_root):
        setup_create_member_test(request, mgmt_root, 'fake_pool')
        setup_gtm_vs(request, mgmt_root, GTM_VS, '20.20.20.20:80',
                     addresses=[{'name': '1.1.1.1'}])
        p1, pc = setup_pool_basic_test(request, mgmt_root, 'fake_pool',
                                       'Common')
        m1 = p1.members_s.member.create(name=RES_NAME, partition='Common')
        uri = 'https://localhost/mgmt/tm/gtm/pool/~Common~fake_pool/' \
              'members/~Common~fake_serv1:fakeVS'
        assert m1.name == RES_NAME
        assert m1.generation and isinstance(m1.generation, int)
        assert m1.kind == 'tm:gtm:pool:members:membersstate'
        assert m1.selfLink.startswith(uri)

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_member_test(request, mgmt_root, 'fake_pool')
        setup_gtm_vs(request, mgmt_root, GTM_VS, '20.20.20.20:80',
                     addresses=[{'name': '1.1.1.1'}])
        p1, pc = setup_pool_basic_test(request, mgmt_root, 'fake_pool',
                                       'Common')
        m1 = p1.members_s.member.create(name=RES_NAME, partition='Common',
                                        description='FancyFakeMember',
                                        limitMaxBpsStatus='enabled',
                                        limitMaxBps=1337)
        assert m1.name == RES_NAME
        assert m1.description == 'FancyFakeMember'
        assert m1.limitMaxBpsStatus == 'enabled'
        assert m1.limitMaxBps == 1337

    def test_create_duplicate(self, request, mgmt_root):
        setup_member_basic_test(request, mgmt_root, RES_NAME, 'Common',
                                'fake_pool')
        p1 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
        try:
            p1.members_s.member.create(name=RES_NAME, partition='Common')
        except HTTPError as err:
            assert err.response.status_code == 409

    def test_refresh(self, request, mgmt_root):
        setup_member_basic_test(request, mgmt_root, RES_NAME, 'Common',
                                'fake_pool')
        p1 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
        m1 = p1.members_s.member.load(name=RES_NAME, partition='Common')
        m2 = p1.members_s.member.load(name=RES_NAME, partition='Common')

        assert m1.limitMaxBpsStatus == 'disabled'
        assert m1.limitMaxBpsStatus == 'disabled'

        m2.update(limitMaxBpsStatus='enabled')
        assert m1.limitMaxBpsStatus == 'disabled'
        assert m2.limitMaxBpsStatus == 'enabled'

        m1.refresh()
        assert m2.limitMaxBpsStatus == 'enabled'

    def test_load_no_object(self, request, mgmt_root):
        p1, pc = setup_pool_basic_test(request, mgmt_root, 'fake_pool',
                                       'Common')
        try:
            p1.members_s.member.load(name=RES_NAME)
        except HTTPError as err:
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        m1, mc = setup_member_basic_test(request, mgmt_root, RES_NAME,
                                         'Common', 'fake_pool')
        assert m1.name == RES_NAME
        assert m1.limitMaxBpsStatus == 'disabled'

        m1.limitMaxBpsStatus = 'enabled'
        m1.update()
        m2 = mc.member.load(name=RES_NAME, partition='Common')
        assert m2.name == RES_NAME
        assert m2.limitMaxBpsStatus == 'enabled'

    def test_update(self, request, mgmt_root):
        m1, mc = setup_member_basic_test(request, mgmt_root, RES_NAME,
                                         'Common', 'fake_pool')
        assert m1.limitMaxBpsStatus == 'disabled'
        m1.update(limitMaxBpsStatus='enabled')
        assert m1.limitMaxBpsStatus == 'enabled'

    def test_modify(self, request, mgmt_root):
        m1, mc = setup_member_basic_test(request, mgmt_root, RES_NAME,
                                         'Common', 'fake_pool')
        original_dict = copy.copy(m1.__dict__)
        limit = 'limitMaxBpsStatus'
        m1.modify(limitMaxBpsStatus='enabled')
        for k, v in iteritems(original_dict):
            if k != limit:
                original_dict[k] = m1.__dict__[k]
            elif k == limit:
                assert m1.__dict__[k] == 'enabled'

    @pytest.mark.skipif(pytest.config.getoption('--release') == '11.6.0',
                        reason='Due to a bug in 11.6.0 Final this test '
                               'fails')
    def test_delete(self, request, mgmt_root):
        m1, mc = setup_member_basic_test(request, mgmt_root, RES_NAME,
                                         'Common', 'fake_pool')
        m1.delete()
        p1 = mgmt_root.tm.gtm.pools.pool.load(name='fake_pool')
        try:
            p1.members_s.member.load(name=RES_NAME)
        except HTTPError as err:
            assert err.response.status_code == 404

    def test_member_collection(self, request, mgmt_root):
        m1, mc = setup_member_basic_test(request, mgmt_root, RES_NAME,
                                         'Common', 'fake_pool')
        uri = 'https://localhost/mgmt/tm/gtm/pool/~Common~fake_pool/' \
              'members/~Common~fake_serv1:fakeVS'
        assert m1.name == RES_NAME
        assert m1.generation and isinstance(m1.generation, int)
        assert m1.kind == 'tm:gtm:pool:members:membersstate'
        assert m1.selfLink.startswith(uri)

        msc = mc.get_collection()
        assert isinstance(msc, list)
        assert len(msc)
        assert isinstance(msc[0], MembersResource_v11)
