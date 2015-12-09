# Copyright 2015 F5 Networks Inc.
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

import mock
import os
import pytest
from requests.exceptions import HTTPError

from f5.bigip import exceptions
from f5.bigip.ltm import pool
from f5.bigip.ltm.pool import Pool
from f5.bigip.test.big_ip_mock import BigIPMock

"""Usage example:

    py.test f5/bigip/test/test_pool.py

    with coverage:
    py.test --cov f5
"""

DATA_DIR = os.path.dirname(__file__)
JSON_FILE = os.path.join(DATA_DIR, 'pool.json')


def test_get_description():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file(JSON_FILE))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    description = test_pool.get_description("my-Pool")
    assert description == "sdfds"


def test_get_description_error():
    response = BigIPMock.create_mock_response(
        500, BigIPMock.read_json_file(JSON_FILE))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    # should raise a PoolQueryException
    with pytest.raises(exceptions.PoolQueryException):
        test_pool.get_description("my-Pool")


def test_get_load_balancing():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file(JSON_FILE))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    mode = test_pool.get_lb_method("my-Pool")
    assert mode == "ROUND_ROBIN"


@pytest.fixture
def FakePool():
    fake_bigip = mock.MagicMock()
    fake_bigip.icr_uri = 'https://0.0.0.0/mgmt/tm/'
    fake_pool = Pool(fake_bigip)
    fake_pool._del_arp_and_fdb = mock.MagicMock()
    fake_pool._get_items = mock.MagicMock()
    return fake_pool


@pytest.fixture
def FakePoolForCreate(FakePool):
    mock_exists = mock.MagicMock()
    mock_exists.return_value = False
    FakePool.exists = mock_exists
    return FakePool


class TestCreate(object):
    def test_create_with_no_args(self, FakePoolForCreate):
        FakePoolForCreate.create()


class TestDelete(object):
    def test_delete_with_no_args(self, FakePool):
        assert FakePool.delete() is False

    def test_delete_with_folder_arg(self, FakePool):
        assert FakePool.delete(folder='FolderName') is False

    def test_delete_with_name_arg(self, FakePool):
        boolean_result = FakePool.delete(name='FakeName')
        assert FakePool._get_items.call_args ==\
            mock.call(folder='Common', suffix='/members', timeout=30,
                      name='FakeName')
        assert FakePool.bigip.icr_session.delete.call_args ==\
            mock.call('https://0.0.0.0/mgmt/tm/ltm/pool/', folder='Common',
                      suffix='/members', timeout=30, name='FakeName')
        assert boolean_result

    def test_delete_empty_folder_and_name(self, FakePool):
        boolean_result = FakePool.delete(name='FakeName', folder='')
        assert FakePool._get_items.call_args ==\
            mock.call(folder='', name='FakeName', suffix='/members',
                      timeout=30)
        assert FakePool.bigip.icr_session.delete.call_args ==\
            mock.call('https://0.0.0.0/mgmt/tm/ltm/pool/', folder='',
                      suffix='/members', timeout=30, name='FakeName')
        assert boolean_result

    def test_delete_404_HTTPError_in__get_items(self, FakePool,
                                                raise_custom_HTTPError):
        FakePool._get_items.side_effect = raise_custom_HTTPError(404)
        assert FakePool.delete(name='FakeName')

    def test_delete_403_HTTPError_in__get_items(self, FakePool,
                                                raise_custom_HTTPError):
        pool.Log = mock.MagicMock()  # Needs to ensure cleanup.
        response_txt = 'The mock is for a 403 status code.'
        FakePool._get_items.side_effect = raise_custom_HTTPError(403,
                                                                 response_txt)
        boolean_result = FakePool.delete(name='FakeName')
        assert pool.Log.error.call_args ==\
            mock.call('members', 'The mock is for a 403 status code.')
        assert not boolean_result

    def test_delete_with_node_addresses(self, FakePool):
        FakePool._get_items.return_value = ['node_address_1', 'node_address_2']
        FakePool.delete(name='FakeName')
        assert FakePool._get_items.call_args ==\
            mock.call(folder='Common', suffix='/members', timeout=30,
                      name='FakeName')
        assert FakePool.bigip.icr_session.delete.call_args ==\
            mock.call('https://0.0.0.0/mgmt/tm/ltm/pool/', folder='Common',
                      suffix='/members', timeout=30, name='FakeName')

    def test_icr_delete_raises_404(self, FakePool, raise_custom_HTTPError):
        pool.Log = mock.MagicMock()
        response_txt = 'This is fake 404 text.'
        FakePool.bigip.icr_session.delete.side_effect =\
            raise_custom_HTTPError(404, response_txt)
        with pytest.raises(HTTPError):
            FakePool.delete(name='FakeName')
        assert FakePool._get_items.call_args ==\
            mock.call(folder='Common', suffix='/members', timeout=30,
                      name='FakeName')
        assert FakePool.bigip.icr_session.delete.call_args ==\
            mock.call('https://0.0.0.0/mgmt/tm/ltm/pool/', folder='Common',
                      suffix='/members', timeout=30, name='FakeName')
        assert pool.Log.error.call_args ==\
            mock.call('members', response_txt)

    def test__delete_no_exception(self, FakePool):
        FakePool._delete('FakeFolder', 'FakeName', 30)

    def test__delete_400_exception(self, FakePool, raise_custom_HTTPError):
        response_txt = 'This is fake 400 text. is referenced'
        FakePool.bigip.icr_session.delete.side_effect =\
            raise_custom_HTTPError(400, response_txt)
        FakePool._delete('FakeFolder', 'FakeName', 30)

    def test__delete_500_exception(self, FakePool, raise_custom_HTTPError):
        response_txt = 'This is fake 500 text.'
        FakePool.bigip.icr_session.delete.side_effect =\
            raise_custom_HTTPError(500, response_txt)
        with pytest.raises(exceptions.PoolDeleteException):
            FakePool._delete('FakeFolder', 'FakeName', 30)
