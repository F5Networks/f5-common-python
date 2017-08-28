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

from f5.bigip.tm.ltm.profile import Ocsp_Stapling_Params
from f5.sdk_exception import MissingUpdateParameter


@pytest.fixture
def FakeProfile():
    fake_profiles = mock.MagicMock()
    fake_profile = Ocsp_Stapling_Params(fake_profiles)
    return fake_profile


class Test_OCSP_update(object):

    def test_without_proxyserverpool(self):
        profile = FakeProfile()
        profile.useProxyServer = 'enabled'
        with pytest.raises(MissingUpdateParameter) as err:
            profile.update()
        assert 'Missing proxyServerPool parameter value' in str(err.value)
