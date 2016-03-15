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
