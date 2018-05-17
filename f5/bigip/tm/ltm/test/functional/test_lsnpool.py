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

from distutils.version import LooseVersion
from f5.sdk_exception import MissingRequiredCreationParameter
from f5.utils.responses.handlers import Stats
from icontrol.exceptions import iControlUnexpectedHTTPError
from requests.exceptions import HTTPError

TESTDESCRIPTION = 'TESTDESCRIPTION'
not_supported_prior_11_6_0 = pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release'))
    < LooseVersion('11.6.0'),
    reason='This collection exists on 11.6.0 or greater.')


@pytest.fixture
def virtual_setup(mgmt_root):
    vs_kwargs = {'name': 'vs', 'partition': 'Common'}
    vs = mgmt_root.tm.ltm.virtuals.virtual
    v1 = vs.create(profiles=['/Common/tcp'], **vs_kwargs)
    yield v1
    v1.delete()


def delete_pool(mgmt_root, name):
    try:
        p = mgmt_root.tm.ltm.lsn_pools.lsn_pool.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def delete_log_profile(mgmt_root, name):
    try:
        p = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_create_test(request, mgmt_root, name):
    def teardown():
        delete_pool(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_log_profile_create_test(request, mgmt_root, name):
    def teardown():
        delete_log_profile(mgmt_root, name)
    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_pool(mgmt_root, name)

    pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name=name,
                                                       partition=partition)
    request.addfinalizer(teardown)
    return pool1


def setup_log_profile_basic_test(request, mgmt_root, name, partition):
    def teardown():
        delete_log_profile(mgmt_root, name)

    profile = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.create(
        name=name, partition=partition)
    request.addfinalizer(teardown)
    return profile


class TestLSNPool(object):
    def test_create_no_args(self, mgmt_root):
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool
        with pytest.raises(MissingRequiredCreationParameter):
            pool1.create()

    def test_create(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'napt'

    @not_supported_prior_11_6_0
    def test_create_with_logProfile_without_logPub(self, request, mgmt_root):
        setup_log_profile_create_test(request, mgmt_root, 'lsnlogpool1')
        logprofile1 = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.create(
            name='lsnlogpool1')

        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            setup_create_test(request, mgmt_root, 'lsnpool1')
            mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(
                name='lsnpool1',
                logProfile=logprofile1.name)
            expected_msg = ('Configuration of LSN Pool (/Common/lsnpool1) '
                            'is incomplete, you cannot use a log profile '
                            'without a log publisher.')
            assert expected_msg in str(excinfo.value)

    @not_supported_prior_11_6_0
    def test_create_with_logProfile(self, request, mgmt_root):
        setup_log_profile_create_test(request, mgmt_root, 'lsnlogpool1')
        logprofile1 = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.create(
            name='lsnlogpool1')

        setup_create_test(request, mgmt_root, 'lsnpool1')

        default_pub = '/Common/local-db-publisher'
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                           logProfile=logprofile1.name,
                                                           logPublisher=default_pub)

        assert pool1.name == 'lsnpool1'
        assert pool1.logProfile == '/Common/lsnlogpool1'
        assert pool1.logPublisher == default_pub

    def test_refresh(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'lsnpool1', 'Common')
        assert pool1.mode == "napt"
        pool1.mode = "deterministic"
        pool1.refresh()
        assert pool1.mode == "napt"

    def test_update(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'lsnpool1', 'Common')
        pool1.mode = "deterministic"
        pool1.update()
        assert pool1.mode == "deterministic"
        pool1.mode = "napt"
        pool1.refresh()
        assert pool1.mode == "deterministic"

    @not_supported_prior_11_6_0
    def test_update_pba(self, request, mgmt_root):
        pool1 = setup_basic_test(request, mgmt_root, 'lsnpool1', 'Common')
        pool1.mode = "pba"
        pool1.update()
        assert pool1.mode == "pba"
        pool1.mode = "napt"
        pool1.refresh()
        assert pool1.mode == "pba"

    def test_exists(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1')
        pos_test = mgmt_root.tm.ltm.lsn_pools.lsn_pool.exists(name='lsnpool1')
        assert pos_test
        neg_test = mgmt_root.tm.ltm.lsn_pools.lsn_pool.exists(name='lsnpool2')
        assert not neg_test

    def test_stats(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                           mode='deterministic')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'deterministic'

        nops = 0
        time.sleep(0.1)
        while True:
            try:
                stats = Stats(pool1.stats.load())
                bkp_pool = 'common_backupPoolTranslations'
                assert stats.stat[bkp_pool]['value'] == 0
                pool_nm = '/Common/lsnpool1'
                assert stats.stat['tmName']['description'] == pool_nm
                assert stats.stat['common_activeTranslations']['value'] == 0
                break
            except Exception as e:
                # This can be caused by restjavad restarting.
                if nops == 3:
                    raise e
                else:
                    nops += 1
            time.sleep(1)

    def test_create_with_nondefault_mode(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                           mode='deterministic')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'deterministic'

    @not_supported_prior_11_6_0
    def test_create_with_nondefault_mode_11_6_0(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                           mode='deterministic')
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == 'deterministic'
        setup_create_test(request, mgmt_root, 'lsnpool2')
        pool2 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool2', mode='pba')
        assert pool2.name == 'lsnpool2'
        assert pool2.mode == 'pba'

    def test_create_with_invalid_mode(self, request, mgmt_root):
        with pytest.raises(iControlUnexpectedHTTPError) as excinfo:
            def create_request():
                setup_create_test(request, mgmt_root, 'lsnpool1')
                mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                           mode='invalid_mode')
            create_request()
        expected_msg = ('invalid property value \\\\"mode\\\\":\\\\"'
                        'invalid_mode\\\\')
        assert expected_msg in str(excinfo.value)

    def test_create_with_member(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                           members=["4.4.0.0/16",
                                                                    "5.5.0.0/32"])
        assert pool1.name == 'lsnpool1'
        assert pool1.mode == "napt"
        assert pool1.members == ["4.4.0.0/16", "5.5.0.0/32"]

    def test_virtual_with_pool(self, request, mgmt_root, virtual_setup):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        pool1 = mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
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

    def test_collection(self, request, mgmt_root):
        setup_create_test(request, mgmt_root, 'lsnpool1')
        mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool1',
                                                   mode='deterministic')
        setup_create_test(request, mgmt_root, 'lsnpool2')
        mgmt_root.tm.ltm.lsn_pools.lsn_pool.create(name='lsnpool2',
                                                   mode='napt')
        pool_list = mgmt_root.tm.ltm.lsn_pools.get_collection()
        assert len(pool_list) == 2
        assert pool_list[0].name == 'lsnpool1'
        assert pool_list[1].name == 'lsnpool2'


@not_supported_prior_11_6_0
class TestLSNPoolLogProfile(object):
    def test_create_no_args(self, mgmt_root):
        logprofile = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile
        with pytest.raises(MissingRequiredCreationParameter):
            logprofile.create()

    def test_create(self, request, mgmt_root):
        setup_log_profile_create_test(request, mgmt_root, 'lsnlogpool1')
        logprofile1 = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.create(
            name='lsnlogpool1')
        assert logprofile1.name == 'lsnlogpool1'
        assert logprofile1.endInboundSession['action'] == 'enabled'
        assert logprofile1.startInboundSession['action'] == 'disabled'

    def test_update(self, request, mgmt_root):
        profile1 = setup_log_profile_basic_test(request,
                                                mgmt_root,
                                                'lsnlogprofile1', 'Common')
        profile1.startOutboundSession = {"action": "enabled",
                                         "elements": ["destination"]}
        profile1.update()
        assert profile1.startOutboundSession["action"] == "enabled"
        assert profile1.startOutboundSession["elements"] == ["destination"]
        profile1.startOutboundSession["action"] = "disabled"
        profile1.refresh()
        assert profile1.startOutboundSession["action"] == "enabled"

    def test_exists(self, request, mgmt_root):
        setup_log_profile_create_test(request, mgmt_root, 'logprofile1')
        mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.create(name='logprofile1')
        pos_test = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.exists(
            name='logprofile1')
        assert pos_test
        neg_test = mgmt_root.tm.ltm.lsn_log_profiles.lsn_log_profile.exists(
            name='logprofile2')
        assert not neg_test
