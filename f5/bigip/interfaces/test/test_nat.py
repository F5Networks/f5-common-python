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

from f5.bigip.interfaces.nat import NAT
from f5.bigip.interfaces.test.big_ip_mock import BigIPMock
from mock import Mock
from requests.exceptions import HTTPError

import os
import pytest

DATA_DIR = os.path.dirname(os.path.realpath(__file__))


def test_get_nats():
    response = BigIPMock.create_mock_response(
        200, BigIPMock.read_json_file(os.path.join(DATA_DIR, 'nat.json')))

    big_ip = BigIPMock(response)
    test_nat = NAT(big_ip)
    nats = test_nat.get_nats(folder='Common')

    assert isinstance(nats, list)
    assert len(nats) == 5
    assert 'nat1' in nats
    assert 'nat2' in nats
    assert 'nat3' in nats
    assert 'nat4' in nats
    assert 'nat5' in nats


def test_get_nats_error():
    response = BigIPMock.create_mock_response(
        400, BigIPMock.read_json_file(os.path.join(DATA_DIR, 'nat.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.get = Mock(side_effect=HTTPError(response=response))
    test_nat = NAT(big_ip)

    with pytest.raises(HTTPError):
        test_nat.get_nats(folder="Common")
