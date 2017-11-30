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

from distutils.version import LooseVersion

pytestmark = pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release'))
    < LooseVersion('12.0.0'),
    reason='Needs v12 TMOS or greater to pass.'
)


@pytest.fixture(scope='function')
def root_credentials(mgmt_root):
    result = mgmt_root.shared.authn.roots.root.create(
        oldPassword='default',
        newPassword='ChangeMyPassword1234'
    )
    yield result
    mgmt_root.shared.authn.roots.root.create(
        oldPassword='ChangeMyPassword1234',
        newPassword='default'
    )


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) >= LooseVersion('12.1.0'),
    reason='This fixture requires < 12.1.0.'
)
class TestAuthnV12(object):
    def test_create(self, root_credentials):
        assert root_credentials.newPassword == 'ChangeMyPassword1234'


@pytest.mark.skipif(
    LooseVersion(pytest.config.getoption('--release')) < LooseVersion('12.1.0'),
    reason='This fixture requires >= 12.1.0.'
)
class TestAuthnPostV12(object):
    def test_create(self, root_credentials):
        assert root_credentials.generation == 0
