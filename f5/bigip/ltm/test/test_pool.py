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
#
import mock
import os
import pytest
from requests.exceptions import HTTPError

from f5.bigip import exceptions
from f5.bigip.test.big_ip_mock import BigIPMock
from f5.bigip.ltm import pool
from f5.bigip.ltm.pool import Pool

"""Usage example:

    py.test f5/bigip/test/test_pool.py

    with coverage:
    py.test --cov f5
"""

DATA_DIR = os.path.dirname(__file__)
JSON_FILE = os.path.join(DATA_DIR, 'pool.json')


def itest_get_description():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file(JSON_FILE))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    description = test_pool.get_description("my-Pool")
    assert description == "sdfds"


def itest_get_description_error():
    response = BigIPMock.create_mock_response(
        500, BigIPMock.read_json_file(JSON_FILE))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    # should raise a PoolQueryException
    with pytest.raises(exceptions.PoolQueryException):
        test_pool.get_description("my-Pool")


def itest_get_load_balancing():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file(JSON_FILE))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    mode = test_pool.get_lb_method("my-Pool")
    assert mode == "ROUND_ROBIN"


@pytest.fixture
def raise_custom_HTTPError():
    def customize_error(status_code, response_txt=''):
        def raise_error(*args, **kwargs):
            mock_response = mock.MagicMock()
            mock_response.status_code = status_code
            mock_response.text = response_txt
            HTTPErrorInstance = HTTPError(response=mock_response)
            raise HTTPErrorInstance
        return raise_error
    return customize_error


@pytest.fixture
def FakePool():
    fake_bigip = mock.MagicMock()
    fake_bigip.icr_url = 'https://0.0.0.0/mgmt/tm/'
    fake_pool = Pool(fake_bigip)
    fake_pool._del_arp_and_fdb = mock.MagicMock()
    fake_pool._get_items = mock.MagicMock()
    return fake_pool


def test_delete_with_no_name(FakePool):
    assert FakePool.delete() is False


def test_delete_no_name_but_folder(FakePool):
    assert FakePool.delete(folder='FolderName') is False


def test_delete_default_folder_and_name(FakePool):
    boolean_result = FakePool.delete(name='FakeName')
    assert FakePool._get_items.call_args ==\
        mock.call(folder='Common', suffix='/members', timeout=30,
                  name='FakeName')
    assert FakePool.bigip.icr_session.delete.call_args ==\
        mock.call('ltm/pool/', folder='Common',
                  suffix='/members', timeout=30, name='FakeName')
    assert boolean_result


def test_delete_empty_folder_and_name(FakePool):
    boolean_result = FakePool.delete(name='FakeName', folder='')
    assert FakePool._get_items.call_args ==\
        mock.call(folder='', name='FakeName', suffix='/members',
                  timeout=30)
    assert FakePool.bigip.icr_session.delete.call_args ==\
        mock.call('ltm/pool/', folder='',
                  suffix='/members', timeout=30, name='FakeName')
    assert boolean_result


def test_delete_404_HTTPError_in__get_items(FakePool, raise_custom_HTTPError):
    FakePool._get_items.side_effect = raise_custom_HTTPError(404)
    assert FakePool.delete(name='FakeName')


def test_delete_403_HTTPError_in__get_items(monkeypatch, FakePool,
                                            raise_custom_HTTPError):
    pool.Log = mock.MagicMock()
    response_txt = 'The mock is for a 403 status code.'
    FakePool._get_items.side_effect = raise_custom_HTTPError(403, response_txt)
    boolean_result = FakePool.delete(name='FakeName')
    assert pool.Log.error.call_args ==\
        mock.call('members', 'The mock is for a 403 status code.')
    assert not boolean_result


def test_delete_with_node_addresses(FakePool):
    FakePool._get_items.return_value = ['node_address_1', 'node_address_2']
    FakePool.delete(name='FakeName')
    assert FakePool._get_items.call_args ==\
        mock.call(folder='Common', suffix='/members', timeout=30,
                  name='FakeName')
    assert FakePool.bigip.icr_session.delete.call_args ==\
        mock.call('ltm/pool/', folder='Common',
                  suffix='/members', timeout=30, name='FakeName')
