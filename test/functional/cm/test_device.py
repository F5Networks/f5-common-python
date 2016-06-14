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


def setup_device_test(request, bigip, name, partition, **kwargs):
    d = bigip.cm.devices.device.create(
        name=name, partition=partition, **kwargs)

    def teardown():
        try:
            d.delete()
        except HTTPError as err:
            if err.response.status_code is not 404:
                raise
    request.addfinalizer(teardown)
    return d


class TestDevices(object):
    def test_device_list(self, bigip):
        devices = bigip.cm.devices.get_collection()
        assert len(devices)
        assert devices[0].generation > 0
        assert hasattr(devices[0], 'hostname')


class TestDevice(object):
    def test_device_CURDL(self, request, bigip):
        # Create and Delete are done by setup/teardown
        d1 = setup_device_test(
            request, bigip, 'test-device', 'Common', hostname='test')
        assert d1.generation > 0

        # Load
        d2 = bigip.cm.devices.device.load(
            name=d1.name, partition=d1.partition)
        assert d1.hostname == d2.hostname
        assert d1.generation == d2.generation

        # Update
        d1.description = TEST_DESCR
        d1.update()
        assert d1.description == TEST_DESCR
        assert not hasattr(d2, 'description')
        assert d1.generation != d2.generation

        # Refresh
        d2.refresh()
        assert d2.description == TEST_DESCR
        assert d1.generation == d2.generation
