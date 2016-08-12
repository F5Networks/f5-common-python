# Copyright 2015-2016 F5 Networks Inc.
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

from distutils.version import LooseVersion

from f5.bigip.resource import MissingRequiredCreationParameter
from f5.bigip.resource import MissingRequiredReadParameter
from f5.sdk_exception import UnsupportedMethod

import copy
from pprint import pprint as pp
import pytest

TESTDESCRIPTION = "TESTDESCRIPTION"

pytestmark = pytest.mark.skipif(
    LooseVersion(
        pytest.config.getoption('--release')
    ) < LooseVersion('11.6.0'),
    reason='An error occurs on 11.5.4 devices regarding sysdb'
)


def delete_resource(resources):
    for resource in resources.get_collection():
        resource.delete()


def setup_virtual_test(request, mgmt_root, partition, name):
    def teardown():
        delete_resource(vc1)
    request.addfinalizer(teardown)
    vc1 = mgmt_root.tm.ltm.virtuals
    pp('****')
    virtual1 = vc1.virtual.create(name=name, partition=partition)
    return virtual1, vc1


class TestVirtual(object):
    def test_virtual_create_refresh_update_delete_load(
            self, request, mgmt_root, setup_device_snapshot
    ):
        virtual1, vc1 = setup_virtual_test(
            request, mgmt_root, 'Common', 'vstest1'
        )
        assert virtual1.name == 'vstest1'
        virtual1.description = TESTDESCRIPTION
        virtual1.update()
        assert virtual1.description == TESTDESCRIPTION
        virtual1.description = ''
        virtual1.refresh()
        assert virtual1.description == TESTDESCRIPTION
        virtual2 = vc1.virtual.load(partition='Common', name='vstest1')
        assert virtual2.selfLink == virtual1.selfLink

    def test_virtual_modify(self, request, mgmt_root, setup_device_snapshot):
        virtual1, vc1 = setup_virtual_test(
            request, mgmt_root, 'Common', 'modtest1'
        )
        original_dict = copy.copy(virtual1.__dict__)
        desc = 'description'
        virtual1.modify(description='Cool mod test')
        for k, v in original_dict.items():
            if k != desc:
                original_dict[k] = virtual1.__dict__[k]
            elif k == desc:
                virtual1.__dict__[k] == 'Cool mod test'

    def test_stats(self, request, mgmt_root, setup_device_snapshot):
        virtual1, vc1 = setup_virtual_test(
            request, mgmt_root, 'Common', 'modtest1'
        )
        stats = virtual1.stats.load()
        pp(stats.raw)
        assert virtual1.cmpEnabled == u'yes'
        assert stats.entries['cmpEnabled']['description'] == u'enabled'
        virtual1.modify(cmpEnabled=u'no')
        stats.refresh()
        assert stats.entries['cmpEnabled']['description'] == u'disabled'
        with pytest.raises(UnsupportedMethod) as USMEIO:
            stats.modify(description='foo')
        assert USMEIO.value.message ==\
            "Stats does not support the modify method"


def test_profiles_CE(
        mgmt_root, opt_release, setup_device_snapshot
):
    v1 = mgmt_root.tm.ltm.virtuals.virtual.create(
        name="tv1", partition="Common"
    )
    p1 = v1.profiles_s.profiles.create(name="http", partition='Common')
    test_profiles_s = v1.profiles_s
    test_profiles_s.context = 'all'
    assert p1.selfLink ==\
        u"https://localhost/mgmt/tm/ltm/virtual/"\
        "~Common~tv1/profiles/~Common~http?ver="+opt_release

    p2 = v1.profiles_s.profiles
    assert p2.exists(name='http', partition='Common')

    v1.delete()


def test_profiles_CE_check_create_params(mgmt_root, setup_device_snapshot):
    v1 = mgmt_root.tm.ltm.virtuals.virtual.create(
        name="tv2", partition="Common"
    )
    with pytest.raises(MissingRequiredCreationParameter) as ex:
        v1.profiles_s.profiles.create(name="http")
    assert "Missing required params: ['partition']" in ex.value.message
    v1.delete()


def test_profiles_CE_check_load_params(mgmt_root, setup_device_snapshot):
    v1 = mgmt_root.tm.ltm.virtuals.virtual.create(
        name="tv3", partition="Common"
    )
    p1 = v1.profiles_s.profiles.create(name="http", partition="Common")

    with pytest.raises(MissingRequiredReadParameter) as ex:
        assert v1.profiles_s.profiles.load(name='http')
    assert "Missing required params: ['partition']" in ex.value.message

    v1.profiles_s.profiles.load(name="http", partition="Common")

    # Check for existence with partition given
    p1.exists(name='http', partition='Common')

    v1.delete()
