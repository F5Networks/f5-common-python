import mock
import pytest

from requests.exceptions import HTTPError


@pytest.fixture
def raise_custom_HTTPError():
    '''return a function that raises a customized HTTPError when called'''
    def customize_error(status_code, response_txt=''):
        def raise_error(*args, **kwargs):
            mock_response = mock.MagicMock()
            mock_response.status_code = status_code
            mock_response.text = response_txt
            HTTPErrorInstance = HTTPError(response=mock_response)
            raise HTTPErrorInstance
        return raise_error
    return customize_error
