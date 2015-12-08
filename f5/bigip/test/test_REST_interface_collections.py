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

from f5.bigip.rest_collection import RESTInterfaceCollection
from f5.bigip.test.big_ip_mock import BigIPMock
from mock import Mock
from requests.exceptions import HTTPError

import os
import pytest

DATA_DIR = os.path.dirname(os.path.realpath(__file__))


class TestRESTInterfaceCollectionChild(RESTInterfaceCollection):
    def __init__(self, bigip, root_uri_path_element):
        self.bigip = bigip
        self.root_uri_path_element = root_uri_path_element


def test_exists():
    """exists() should return true for non-http error codes """
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    assert test_REST_iface_collection.exists()


def test_exists_404():
    """exists() should return false only for the 404 http error code """
    response = BigIPMock.create_mock_response(
        404,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.get = Mock()
    big_ip.icr_session.get.side_effect = HTTPError(response=response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    assert not test_REST_iface_collection.exists()


def test_exists_http_error():
    """exists() should raise for all other http errors """
    response = BigIPMock.create_mock_response(
        409,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.get = Mock()
    big_ip.icr_session.get.side_effect = HTTPError(response=response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    # Expect an exception because 409 is not an expected status code
    with pytest.raises(HTTPError):
        test_REST_iface_collection.exists()


def test_get_items():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    names = test_REST_iface_collection._get_items()

    assert isinstance(names, list)
    assert len(names) == 5
    for i in range(1, 6):
        assert 'nat%s' % i in names


def test_get_items_invalid_select():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    names = test_REST_iface_collection._get_items(select='bogus')

    assert isinstance(names, list)
    assert len(names) == 0


def test_get_items_404():
    response = BigIPMock.create_mock_response(
        404,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.get = Mock()
    big_ip.icr_session.get.side_effect = HTTPError(response=response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    # Should not raise because 404 is just not found so empty list
    names = test_REST_iface_collection._get_items()
    assert isinstance(names, list)
    assert len(names) == 0


def test_get_items_http_error():
    response = BigIPMock.create_mock_response(
        409,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.get = Mock()
    big_ip.icr_session.get.side_effect = HTTPError(response=response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    # Expect an exception because 409 is not an expected status code
    with pytest.raises(HTTPError):
        test_REST_iface_collection._get_items()


def test_get_items_uri_override():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    names = test_REST_iface_collection._get_items(uri="an/overriden/uri")

    assert len(names) == 5


def test_get_items_no_items():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))
    response.json = {'not_items': [{'a': 1}, {'b': 1}]}

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    names = test_REST_iface_collection._get_items()

    assert isinstance(names, list)
    assert len(names) == 0


def test_get_named_object():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    # Override the default jason here for single named object
    response.json = {'name': 'nat1'}

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    name = test_REST_iface_collection._get_named_object('nat1')

    assert name == 'nat1'


def test_get_named_object_http_error():
    response = BigIPMock.create_mock_response(
        404,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    # Override the default jason here for single named object
    response.json = {'name': 'nat1'}

    big_ip = BigIPMock(response)
    big_ip.icr_session.get = Mock(side_effect=HTTPError(response=response))
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    with pytest.raises(HTTPError):
        test_REST_iface_collection._get_named_object('nat1')


def test_delete():
    response = BigIPMock.create_mock_response(
        204,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    assert test_REST_iface_collection.delete(name='nat1')


def test_delete_no_name():
    response = BigIPMock.create_mock_response(
        204,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    assert not test_REST_iface_collection.delete()


def test_delete_404():
    response = BigIPMock.create_mock_response(
        404,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.delete = Mock(side_effect=HTTPError(response=response))
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    assert test_REST_iface_collection.delete(name='nat1')


def test_delete_http_error():
    response = BigIPMock.create_mock_response(
        503,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.delete = Mock(side_effect=HTTPError(response=response))
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    with pytest.raises(HTTPError):
        test_REST_iface_collection.delete(name='nat1')


def test_delete_all():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    assert test_REST_iface_collection.delete_all()


def test_delete_all_startswith():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    assert test_REST_iface_collection.delete_all(startswith="nat")


def test_delete_all_fail():
    response = BigIPMock.create_mock_response(
        200,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')
    test_REST_iface_collection.delete = Mock(return_value=False)

    assert not test_REST_iface_collection.delete_all()


def test_delete_all_http_error():
    response = BigIPMock.create_mock_response(
        503,
        BigIPMock.read_json_file(os.path.join(DATA_DIR, 'interfaces.json')))

    big_ip = BigIPMock(response)
    big_ip.icr_session.delete = Mock(side_effect=HTTPError(response=response))
    test_REST_iface_collection =\
        TestRESTInterfaceCollectionChild(big_ip, 'TEST')

    with pytest.raises(HTTPError):
        test_REST_iface_collection.delete_all()
