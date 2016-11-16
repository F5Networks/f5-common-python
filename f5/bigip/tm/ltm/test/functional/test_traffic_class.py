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

import copy
from six import iteritems


TESTDESCRIPTION = "TESTDESCRIPTION"


def delete_resource(resources):
    for resource in resources.get_collection():
        resource.delete()


def setup_traffic_test(request, mgmt_root, name, classification):
    def teardown():
        delete_resource(tc1)
    request.addfinalizer(teardown)
    tc1 = mgmt_root.tm.ltm.traffic_class_s
    traffic1 = tc1.traffic_class.create(name=name,
                                        classification=classification)
    return traffic1, tc1


class TestTrafficClass(object):
    def test_trafficclass_create_refresh_update_delete_load(
            self, request, mgmt_root):
        traffic1, tc1 = setup_traffic_test(
            request, mgmt_root, 'fake_traffic1', 'fakeclasstag')
        assert traffic1.name == 'fake_traffic1'
        traffic1.description = TESTDESCRIPTION
        traffic1.update()
        assert traffic1.description == TESTDESCRIPTION
        traffic1.description = ''
        traffic1.refresh()
        assert traffic1.description == TESTDESCRIPTION
        traffic2 = tc1.traffic_class.load(name='fake_traffic1')
        assert traffic1.description == traffic2.description

    def test_trafficclass_modify(self, request, mgmt_root):
        traffic1, tc1 = setup_traffic_test(
            request, mgmt_root, 'fake_traffic1', 'fakeclasstag')
        original_dict = copy.copy(traffic1.__dict__)
        desc = 'description'
        traffic1.modify(description='Cool mod test')
        for k, v in iteritems(traffic1.__dict__):
            if k != desc:
                original_dict[k] = traffic1.__dict__[k]
            elif k == desc:
                assert traffic1.__dict__[k] == 'Cool mod test'
