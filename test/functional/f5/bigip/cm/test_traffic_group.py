# Copyright 2016 F5 Networks Inc.
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

from requests import HTTPError

TEST_DESCR = "TEST DESCRIPTION"


def setup_traffic_group_test(request, bigip, name, partition, **kwargs):
    def teardown():
        try:
            tg.delete()
        except HTTPError as err:
            if err.response.status_code is not 404:
                raise
    request.addfinalizer(teardown)
    tg = bigip.cm.traffic_groups.traffic_group.create(
        name=name, partition=partition, **kwargs)
    return tg


class TestTrafficGroups(object):
    def test_device_list(self, bigip):
        groups = bigip.cm.traffic_groups.get_collection()
        assert len(groups)
        assert groups[0].generation > 0
        assert hasattr(groups[0], 'mac')


class TestDevice(object):
    def test_device_CURDL(self, request, bigip):
        # Create and Delete are done by setup/teardown
        tg1 = setup_traffic_group_test(
            request, bigip, 'test-tg', 'Common')
        assert tg1.generation > 0

        # Load
        tg2 = bigip.cm.traffic_groups.traffic_group.load(
            name=tg1.name, partition=tg1.partition)
        assert tg1.generation == tg2.generation

        # Update
        tg1.description = TEST_DESCR
        tg1.update()
        assert tg1.description == TEST_DESCR
        assert not hasattr(tg2, 'description')
        assert tg1.generation > tg2.generation

        # Refresh
        tg2.refresh()
        assert tg2.description == TEST_DESCR
        assert tg1.generation == tg2.generation
