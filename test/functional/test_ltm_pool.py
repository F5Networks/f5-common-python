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

from requests.exceptions import HTTPError

from f5.bigip.resource import MissingRequiredCreationParameter


def delete_pool(bigip, name, partition):
    p = bigip.ltm.poolcollection.pool
    try:
        p.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    p.delete()


def setup_create_test(request, bigip, name, partition):
    def teardown():
        delete_pool(bigip, name, partition)
    request.addfinalizer(teardown)


def setup_basic_test(request, bigip, name, partition):
    def teardown():
        delete_pool(bigip, name, partition)

    pool1 = bigip.ltm.poolcollection.pool
    pool1.create(name=name, partition=partition)
    request.addfinalizer(teardown)
    return pool1


class TestCreate(object):
    def test_create_no_args(self, bigip):
        pool1 = bigip.ltm.poolcollection.pool
        with pytest.raises(MissingRequiredCreationParameter):
            pool1.create()

    def test_create(self, request, bigip):
        setup_create_test(request, bigip, 'pool1', 'Common')
        pool1 = bigip.ltm.poolcollection.pool
        pool1.create(name='pool1', partition='Common')
        assert pool1.name == 'pool1'
        assert pool1.partition == 'Common'
        assert pool1.generation and isinstance(pool1.generation, int)
        assert pool1.fullPath == '/Common/pool1'
        assert pool1.kind == 'tm:ltm:pool:poolstate'
        assert pool1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/pool/~Common~pool1')

    def test_refresh(self, request, bigip):
        pool1 = setup_basic_test(request, bigip, 'pool1', 'Common')
        assert pool1.allowNat == "yes"
        pool1.allowNat = "no"
        pool1.refresh()
        assert pool1.allowNat == "yes"

    def test_update(self, request, bigip):
        pool1 = setup_basic_test(request, bigip, 'pool1', 'Common')
        pool1.allowNat = "no"
        pool1.update()
        assert pool1.allowNat == "no"
        pool1.allowNat = "yes"
        pool1.refresh()
        assert pool1.allowNat == "no"
