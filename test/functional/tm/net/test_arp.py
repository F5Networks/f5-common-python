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

import pytest

from f5.bigip.resource import MissingRequiredCreationParameter
from requests.exceptions import HTTPError


TEST_IP = '192.168.98.100'
TEST_MAC = '02:00:00:00:00:01'


def delete_resource(resources):
    for resource in resources.get_collection():
        try:
            resource.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise


def setup_arp_test(request, bigip, partition, name, ip, mac):
    def teardown():
        delete_resource(ac1)
    request.addfinalizer(teardown)

    ac1 = bigip.net.arps
    a1 = ac1.arp.create(
        partition=partition, name=name, ipAddress=ip, macAddress=mac)
    return a1, ac1


class TestArp(object):
    def test_create_missing_args(self, request, bigip):
        with pytest.raises(MissingRequiredCreationParameter):
            bigip.net.arps.arp.create(name='s1', partition='Common')

    def test_CURDL(self, request, bigip):
        # We assume that setup and teardown will create/delete
        name = 'arp_test'
        partition = 'Common'
        a1, ac1 = setup_arp_test(
            request, bigip, partition, name, TEST_IP, TEST_MAC)
        a2 = bigip.net.arps.arp.load(name=name, partition=partition)
        assert a1.name == name
        assert a1.ipAddress == TEST_IP
        assert a1.macAddress == TEST_MAC
        assert a1.name == a2.name
        assert a1.generation == a2.generation

        a1.macAddress = '02:00:00:00:00:02'
        a1.update()
        assert a1.macAddress != a2.macAddress

        a2.refresh()
        assert a1.macAddress == a2.macAddress
        assert a1.generation == a2.generation
