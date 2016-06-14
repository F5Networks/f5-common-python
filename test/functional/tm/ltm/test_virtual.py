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

from pprint import pprint as pp

TESTDESCRIPTION = "TESTDESCRIPTION"


def delete_resource(resources):
    for resource in resources.get_collection():
        resource.delete()


def setup_virtual_test(request, bigip, partition, name):
    def teardown():
        delete_resource(vc1)
    request.addfinalizer(teardown)
    vc1 = bigip.ltm.virtuals
    pp('****')
    virtual1 = vc1.virtual.create(name=name, partition=partition)
    return virtual1, vc1


class TestVirtual(object):
    def test_virtual_create_refresh_update_delete_load(self, request, bigip):
        virtual1, vc1 = setup_virtual_test(request, bigip, 'Common', 'vstest1')
        assert virtual1.name == 'vstest1'
        virtual1.description = TESTDESCRIPTION
        virtual1.update()
        assert virtual1.description == TESTDESCRIPTION
        virtual1.description = ''
        virtual1.refresh()
        assert virtual1.description == TESTDESCRIPTION
        virtual2 = vc1.virtual.load(partition='Common', name='vstest1')
        assert virtual2.selfLink == virtual1.selfLink


def test_profiles_CE(bigip, opt_release):
    v1 = bigip.ltm.virtuals.virtual.create(name="tv1", partition="Common")
    p1 = v1.profiles_s.profiles.create(name="http")
    pp(p1.raw)
    test_profiles_s = v1.profiles_s
    pp(test_profiles_s.raw)
    test_profiles_s.context = 'all'
    pp(test_profiles_s.raw)
    assert p1.selfLink ==\
        u"https://localhost/mgmt/tm/ltm/virtual/"\
        "~Common~tv1/profiles/http?ver="+opt_release

    p2 = v1.profiles_s.profiles
    assert p2.exists(name='http')

    v1.delete()
