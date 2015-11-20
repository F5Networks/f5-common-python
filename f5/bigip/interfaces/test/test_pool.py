from f5.bigip import exceptions
from f5.bigip.interfaces.pool import Pool
from f5.bigip.interfaces.test.big_ip_mock import BigIPMock

import mock
import pytest


# @pytest.mark.usefixtures("return_mock_imports")
class TestPool(object):
    # import_names_to_mock = ['f5.bigip']

    def _create_mock_response(self, status_code, json):
        response = mock.Mock()
        response.status_code = status_code
        response.text = json


        return response

    def test_get_description(self):

        response = self._create_mock_response(200,
                                              '{"description": "A mock pool"}')
        big_ip = BigIPMock(response)
        test_pool = Pool(big_ip)

        description = test_pool.get_description("pool_name")

        assert description == "A mock pool"

    def test_get_description_error(self):

        response = self._create_mock_response(500, "")
        big_ip = BigIPMock(response)
        test_pool = Pool(big_ip)

        with pytest.raises(exceptions.PoolQueryException):
            test_pool.get_description("pool_name")

    def test_get_description_without_name(self):

        response = self._create_mock_response(500, "")
        big_ip = BigIPMock(response)
        test_pool = Pool(big_ip)

        description = test_pool.get_description()

        assert description is None
