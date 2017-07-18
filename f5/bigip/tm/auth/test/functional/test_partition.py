# Copyright 2017 F5 Networks Inc.
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

from f5.bigip.tm.auth.partition import Partition
from f5.sdk_exception import MissingRequiredCreationParameter
from requests.exceptions import HTTPError

PARTITION_NAME1 = 'part1'
PARTITION_NAME2 = 'part2'
PARTITION_NAME3 = 'part3'


@pytest.fixture(scope='function')
def partition(mgmt_root):
    partitions = mgmt_root.tm.auth.partitions.partition
    local = partitions.create(name=PARTITION_NAME1)
    yield local
    local.delete()


@pytest.fixture(scope='function')
def partition_desc(mgmt_root):
    partitions = mgmt_root.tm.auth.partitions.partition
    local = partitions.create(name=PARTITION_NAME2, description='foo')
    yield local
    local.delete()


@pytest.fixture(scope='function')
def partition_delete(mgmt_root):
    partitions = mgmt_root.tm.auth.partitions.partition
    local = partitions.create(name=PARTITION_NAME3)
    yield local


def delete_partition(mgmt_root, name):
    partition = mgmt_root.tm.auth.partitions.partition
    try:
        part1 = partition.load(name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    part1.delete()


def setup_create_test(request, mgmt_root):
    def teardown():
        delete_partition(mgmt_root, 'part1')
    request.addfinalizer(teardown)


def setup_create_two(request, mgmt_root):
    def teardown():
        for name in ['part1', 'part2']:
            delete_partition(mgmt_root, name)
    request.addfinalizer(teardown)


class TestCreate(object):
    def test_create_two(self, request, mgmt_root):
        setup_create_two(request, mgmt_root)

        n1 = mgmt_root.tm.auth.partitions.partition.create(name='part1')
        n2 = mgmt_root.tm.auth.partitions.partition.create(name='part2')

        assert n1 is not n2
        assert n2.name != n1.name

    def test_create_no_args(self, mgmt_root):
        '''Test that partition.create() with no options throws a ValueError '''
        part1 = mgmt_root.tm.auth.partitions.partition
        with pytest.raises(MissingRequiredCreationParameter):
            part1.create()

    def test_create_description(self, partition_desc):
        assert partition_desc.description == 'foo'


class TestLoad(object):
    def test_load_no_object(self, mgmt_root):
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.auth.partitions.partition.load(name='user10')
            assert err.response.status == 404

    def test_load(self, partition_desc):
        assert partition_desc.name == 'part2'
        assert partition_desc.description == 'foo'
        assert isinstance(partition_desc, Partition)


class TestRefresh(object):
    def test_refresh(self, mgmt_root, partition_desc):
        n1 = mgmt_root.tm.auth.partitions.partition.load(name='part2')
        n2 = mgmt_root.tm.auth.partitions.partition.load(name='part2')
        assert n1.description == 'foo'
        assert n2.description == 'foo'

        n2.update(description='foobaz')
        assert n2.description == 'foobaz'
        assert n1.description == 'foo'

        n1.refresh()
        assert n1.description == 'foobaz'


class TestDelete(object):
    def test_delete(self, mgmt_root, partition_delete):
        partition_delete.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.auth.partitions.partition.load(name='part3')
        assert err.value.response.status_code == 404


class TestUpdate(object):
    def test_update_with_args(self, partition_desc):
        assert partition_desc.description == 'foo'
        partition_desc.update(description='foobar')
        assert partition_desc.description == 'foobar'

    def test_update_parameters(self, partition_desc):
        assert partition_desc.description == 'foo'
        partition_desc.description = 'foobar'
        partition_desc.update()
        assert partition_desc.description == 'foobar'
