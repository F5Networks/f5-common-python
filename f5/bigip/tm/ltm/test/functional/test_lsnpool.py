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

import pytest
import time

from f5.sdk_exception import MissingRequiredCreationParameter
from f5.utils.responses.handlers import Stats
from icontrol.exceptions import iControlUnexpectedHTTPError
from requests.exceptions import HTTPError

TESTDESCRIPTION = 'TESTDESCRIPTION'


@pytest.fixture
def virtual_setup(mgmt_root):
    vs_kwargs = {'name': 'vs', 'partition': 'Common'}
    vs = mgmt_root.tm.ltm.virtuals.virtual
    v1 = vs.create(profiles=['/Common/tcp'], **vs_kwargs)
    yield v1
    v1.delete()


def delete_pool(bigip, name):
    try:
        p = bigip.ltm.lsnpools.lsnpool.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_create_test(request, bigip, name):
    def teardown():
        delete_pool(bigip, name)
    request.addfinalizer(teardown)


def setup_basic_test(request, bigip, name, partition):
    def teardown():
        delete_pool(bigip, name)

    pool1 = bigip.ltm.lsnpools.lsnpool.create(name=name,
                                              partition=partition)
    request.addfinalizer(teardown)
    return pool1


class TestLSNPool(object):
    def test_create_no_args(self, bigip):
        pool1 = bigip.ltm.lsnpools.lsnpool
        with pytest.raises(MissingRequiredCreationParameter):
            pool1.create()

    def test_create(self, request, bigip):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'napt'

    def test_refresh(self, request, bigip):
        pool1 = setup_basic_test(request, bigip, 'lsnpool1', 'Common')
        assert pool1.mode == "napt"
        pool1.mode = "pba"
        pool1.refresh()
        assert pool1.mode == "napt"

    def test_update(self, request, bigip):
        pool1 = setup_basic_test(request, bigip, 'lsnpool1', 'Common')
        pool1.mode = "pba"
        pool1.update()
        assert pool1.mode == "pba"
        pool1.mode = "napt"
        pool1.refresh()
        assert pool1.mode == "pba"

    def test_exists(self, request, bigip):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1')
        pos_test = bigip.ltm.lsnpools.lsnpool.exists(name='lsnpool1')
        assert pos_test
        neg_test = bigip.ltm.lsnpools.lsnpool.exists(name='lsnpool2')
        assert not neg_test

    def test_stats(self, request, bigip):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1',
                                                  mode='deterministic')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'deterministic'

        nops = 0
        time.sleep(0.1)
        while True:
            try:
                stats = Stats(pool1.stats.load())
                assert stats.stat['common_endPoints']['value'] == 0
                pool_nm = '/Common/lsnpool1'
                assert stats.stat['tmName']['description'] == pool_nm
                assert stats.stat['common_activeTranslations']['value'] == 0
                break
            except iControlUnexpectedHTTPError as e:
                # This can be caused by restjavad restarting.
                if nops == 3:
                    raise e
                else:
                    nops += 1
            time.sleep(1)

    def test_create_with_nondefault_mode(self, request, bigip):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1',
                                                  mode='deterministic')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'deterministic'
        setup_create_test(request, bigip, 'lsnpool2')
        pool2 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool2', mode='pba')
        assert pool2.name == 'lsnpool2'
        assert pool2.mode == 'pba'

    def test_create_with_invalid_mode(self, request, bigip):
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            def create_request():
                setup_create_test(request, bigip, 'lsnpool1')
                pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1',
                                                          mode='invalid_mode')
            create_request()
        expected_msg = ('invalid property value \\\\"mode\\\\":\\\\"'
                        'invalid_mode\\\\')
        assert expected_msg in str(excinfo.value)

    def test_create_with_member(self, request, bigip):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1',
                                                  members=["4.4.0.0/16",
                                                           "5.5.0.0/32"])
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == "napt"
        assert pool1.members == ["4.4.0.0/16", "5.5.0.0/32"]

    def test_virtual_with_pool(self, request, bigip, virtual_setup):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1',
                                                  members=["4.4.0.0/16",
                                                           "5.5.0.0/32"])
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == "napt"
        assert pool1.members == ["4.4.0.0/16", "5.5.0.0/32"]

        virtual_setup.modify(sourceAddressTranslation={"pool": pool1.name,
                                                       "type": "lsn"})
        assert virtual_setup.sourceAddressTranslation["type"] == "lsn"
        pool_nm = "/Common/lsnpool1"
        assert virtual_setup.sourceAddressTranslation["pool"] == pool_nm
        virtual_setup.modify(sourceAddressTranslation={"type": None})

    def test_collection(self, request, bigip):
        setup_create_test(request, bigip, 'lsnpool1')
        pool1 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool1',
                                                  mode='deterministic')
        setup_create_test(request, bigip, 'lsnpool2')
        pool2 = bigip.ltm.lsnpools.lsnpool.create(name='lsnpool2', mode='pba')
        pool_list = bigip.ltm.lsnpools.get_collection()
        assert len(pool_list) == 2
        assert pool_list[0].name == 'lsnpool1'
        assert pool_list[1].name == 'lsnpool2'
