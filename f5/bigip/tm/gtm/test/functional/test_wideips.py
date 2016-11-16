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
import pytest

from distutils.version import LooseVersion
from f5.bigip.tm.gtm.wideip import A
from f5.bigip.tm.gtm.wideip import Aaaa
from f5.bigip.tm.gtm.wideip import Cname
from f5.bigip.tm.gtm.wideip import Mx
from f5.bigip.tm.gtm.wideip import Naptr
from f5.bigip.tm.gtm.wideip import Srv
from f5.bigip.tm.gtm.wideip import Wideip
from requests.exceptions import HTTPError
from six import iteritems


TESTDESCRIPTION = "TESTDESCRIPTION"

# Start of V12.x Tests here


# Helper class to limit code repetition
class HelperTest(object):
    def __init__(self, collection_name):
        self.partition = 'Common'
        self.lowered = collection_name.lower()
        self.test_name = 'fake.' + self.urielementname() + '.lab.local'
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
            getattr(getattr(getattr(mgmt_root, 'gtm'), 'wideips'),
                    self.lowered)
        resource = getattr(resourcecollection, self.urielementname())
        self.delete_resource(resource)
        created = resource.create(name=self.test_name,
                                  partition=self.partition,
                                  **kwargs)
        request.addfinalizer(teardown)
        return created, resourcecollection

    def test_MCURDL(self, request, bigip, **kwargs):
        # Testing create
        wideip, rescollection = self.setup_test(request, bigip, **kwargs)
        assert wideip.name == self.test_name
        assert wideip.fullPath == '/Common/'+self.test_name
        assert wideip.generation and isinstance(wideip.generation, int)
        assert wideip.kind == self.kinds[self.urielementname()]

        # Testing update
        wideip.description = TESTDESCRIPTION
        wideip.update()
        if hasattr(wideip, 'description'):
            assert wideip.description == TESTDESCRIPTION

        # Testing refresh
        wideip.description = ''
        wideip.refresh()
        if hasattr(wideip, 'description'):
            assert wideip.description == TESTDESCRIPTION

        # Testing modify
        meta_data = wideip.__dict__.pop('_meta_data')
        start_dict = copy.deepcopy(wideip.__dict__)
        wideip.__dict__['_meta_data'] = meta_data
        wideip.modify(description='MODIFIED')
        desc = 'description'
        for k, v in iteritems(wideip.__dict__):
            if k != desc:
                start_dict[k] = wideip.__dict__[k]
                assert getattr(wideip, k) == start_dict[k]
            elif k == desc:
                assert getattr(wideip, desc) == 'MODIFIED'

        # Testing load
        p2 = getattr(rescollection, self.urielementname())
        wideip2 = p2.load(partition=self.partition, name=self.test_name)
        assert wideip.selfLink == wideip2.selfLink

    def test_collection(self, request, bigip, **kwargs):
        wideip, rescollection = self.setup_test(request, bigip, **kwargs)
        assert wideip.name == self.test_name
        assert wideip.fullPath == '/Common/'+self.test_name
        assert wideip.generation and isinstance(wideip.generation, int)
        assert wideip.kind == self.kinds[self.urielementname()]

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


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestWideipAtype(object):
    def test_MCURDL_and_collection(self, request, bigip):
        wideip = HelperTest('A_s')
        wideip.test_MCURDL(request, bigip)
        wideip.test_collection(request, bigip)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestWideipAaaaType(object):
    def test_MCURDL_and_collection(self, request, bigip):
        wideip = HelperTest('Aaaas')
        wideip.test_MCURDL(request, bigip)
        wideip.test_collection(request, bigip)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestWideipCnameType(object):
    def test_MCURDL_and_collection(self, request, bigip):
        wideip = HelperTest('Cnames')
        wideip.test_MCURDL(request, bigip)
        wideip.test_collection(request, bigip)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestWideipMxType(object):
    def test_MCURDL_and_collection(self, request, bigip):
        wideip = HelperTest('Mxs')
        wideip.test_MCURDL(request, bigip)
        wideip.test_collection(request, bigip)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestWideipNaptrType(object):
    def test_MCURDL_and_collection(self, request, bigip):
        wideip = HelperTest('Naptrs')
        wideip.test_MCURDL(request, bigip)
        wideip.test_collection(request, bigip)


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion(
        '12.0.0'),
    reason='This collection exists on 12.0.0 or greater.'
)
class TestWideipSrvType(object):
    def test_MCURDL_and_collection(self, request, bigip):
        wideip = HelperTest('Srvs')
        wideip.test_MCURDL(request, bigip)
        wideip.test_collection(request, bigip)

# End of v12.x Tests


def delete_wideip_v11(mgmt_root, name):
    try:
        foo = mgmt_root.tm.gtm.wideips.wideip.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


def setup_create_test(request, mgmt_root, name):
    def teardown():
        delete_wideip_v11(mgmt_root, name)

    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, **kwargs):
    def teardown():
        delete_wideip_v11(mgmt_root, name)

    wideip1 = mgmt_root.tm.gtm.wideips.wideip.create(
        name=name, **kwargs)
    request.addfinalizer(teardown)
    return wideip1


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion(
        '12.0.0'),
    reason='This collection exists on 11.x'
)
class TestWideips_v11(object):
    def test_create_req_arg(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake.lab.local')
        wideip1 = mgmt_root.tm.gtm.wideips.wideip.create(
            name='fake.lab.local', partition='Common')
        assert wideip1.name == 'fake.lab.local'
        assert wideip1.generation and isinstance(wideip1.generation, int)
        assert wideip1.kind == 'tm:gtm:wideip:wideipstate'
        assert wideip1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/wideip/~Common~fake.lab.local')

    def test_create_optional_args(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake.lab.local')
        wideip1 = mgmt_root.tm.gtm.wideips.wideip.create(
            name='fake.lab.local', description=TESTDESCRIPTION)
        assert wideip1.description == TESTDESCRIPTION
        assert wideip1.ipv6NoErrorResponse == 'disabled'

    def test_create_duplicate(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'fake.lab.local')
        try:
            mgmt_root.tm.gtm.wideips.wideip.create(name='fake.lab.local')
        except HTTPError as err:
            assert err.response.status_code == 400

    def test_refresh(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake.lab.local')
        s1 = mgmt_root.tm.gtm.wideips.wideip.load(name='fake.lab.local')
        s2 = mgmt_root.tm.gtm.wideips.wideip.load(name='fake.lab.local')

        assert s1.ipv6NoErrorResponse == 'disabled'
        assert s2.ipv6NoErrorResponse == 'disabled'

        s2.update(ipv6NoErrorResponse='enabled')
        assert s1.ipv6NoErrorResponse == 'disabled'
        assert s2.ipv6NoErrorResponse == 'enabled'

        s1.refresh()
        assert s1.ipv6NoErrorResponse == 'enabled'

    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.wideips.wideip.load(name='fake.lab.local')
            assert err.response.status_code == 404

    def test_load(self, request, mgmt_root):
        setup_basic_test(request, mgmt_root, 'fake.lab.local')
        s1 = mgmt_root.tm.gtm.wideips.wideip.load(name='fake.lab.local')
        assert s1.ipv6NoErrorResponse == 'disabled'
        s1.ipv6NoErrorResponse = 'enabled'
        s1.update()
        s2 = mgmt_root.tm.gtm.wideips.wideip.load(name='fake.lab.local')
        assert s2.ipv6NoErrorResponse == 'enabled'

    def test_update(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake.lab.local')
        assert s1.ipv6NoErrorResponse == 'disabled'
        assert not hasattr(s1, 'description')
        s1.update(ipv6NoErrorResponse='enabled', description=TESTDESCRIPTION)
        assert s1.ipv6NoErrorResponse == 'enabled'
        assert hasattr(s1, 'description')
        assert s1.description == TESTDESCRIPTION

    def test_modify(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake.lab.local')
        original_dict = copy.copy(s1.__dict__)
        ipv6 = 'ipv6NoErrorResponse'
        s1.modify(ipv6NoErrorResponse='enabled')
        for k, v in iteritems(original_dict):
            if k != ipv6:
                original_dict[k] = s1.__dict__[k]
            elif k == ipv6:
                assert s1.__dict__[k] == 'enabled'

    def test_delete(self, request, mgmt_root):
        s1 = setup_basic_test(request, mgmt_root, 'fake.lab.local')
        s1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.gtm.wideips.wideip.load(name='fake.lab.local')
            assert err.response.status_code == 404

    def test_wideips_collection(self, request, mgmt_root):
        wideip1 = setup_basic_test(request, mgmt_root, 'fake.lab.local',
                                   partition='Common')

        assert wideip1.name == 'fake.lab.local'
        assert wideip1.fullPath == '/Common/fake.lab.local'
        assert wideip1.generation and isinstance(wideip1.generation, int)
        assert wideip1.kind == 'tm:gtm:wideip:wideipstate'
        assert wideip1.selfLink.startswith(
            'https://localhost/mgmt/tm/gtm/wideip/~Common~fake.lab.local')

        wideipc = mgmt_root.tm.gtm.wideips.get_collection()
        assert isinstance(wideipc, list)
        assert len(wideipc)
        assert isinstance(wideipc[0], Wideip)
