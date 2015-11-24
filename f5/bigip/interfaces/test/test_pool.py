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
from f5.bigip import exceptions
from f5.bigip.interfaces.pool import Pool
from f5.bigip.interfaces.test.big_ip_mock import BigIPMock

import pytest

"""Note: Because of file names pased to read_json_file(), tests assume
they are being called from f5-common-python directory. Change file paths
if you want to call from a different directory.

Usage example:

    cd <path>/f5-common-python
    py.test f5/bigip/interfaces/test/test_pool.py

    with coverage:
    py.test --cov f5
"""


def test_get_description():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file("f5/bigip/interfaces/test/pool.json"))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    description = test_pool.get_description("my-Pool")
    assert description == "sdfds"


def test_get_description_error():
    response = BigIPMock.create_mock_response(
        500, BigIPMock.read_json_file("f5/bigip/interfaces/test/pool.json"))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    # should raise a PoolQueryException
    with pytest.raises(exceptions.PoolQueryException):
        test_pool.get_description("my-Pool")


def test_get_load_balancing():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file("f5/bigip/interfaces/test/pool.json"))

    big_ip = BigIPMock(response)
    test_pool = Pool(big_ip)

    mode = test_pool.get_lb_method("my-Pool")
    assert mode == "ROUND_ROBIN"
