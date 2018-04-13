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

from f5.sdk_exception import MissingRequiredCreationParameter
from pytest import symbols

import os
import pytest
import tempfile


pytestmark = pytest.mark.skipif(
    not symbols
    or symbols and not hasattr(symbols, 'run_hardware_tests')
    or symbols and hasattr(symbols, 'run_hardware_tests')
    and symbols.modules['run_hardware_tests'] is False,
    reason='This series of tests requires a hardware BIG-IP be specified.'
)


@pytest.fixture
def trunk(mgmt_root):
    file = tempfile.NamedTemporaryFile()
    name = os.path.basename(file.name)
    resource = mgmt_root.tm.net.trunks.trunk.create(
        name=name
    )
    yield resource
    resource.delete()


@pytest.fixture
def trunks(mgmt_root):
    collection = mgmt_root.tm.net.trunks
    return collection


class TestResource(object):
    def test_get_collection(self, trunk, trunks):
        assert len(list(trunks.get_collection())) > 1

    def test_create(self, mgmt_root):
        file = tempfile.NamedTemporaryFile()
        name = os.path.basename(file.name)
        resource = mgmt_root.tm.net.trunks.trunk.create(
            name=name
        )
        assert resource.name == name
        resource.delete()

    def test_update(self, trunk):
        """Test resource updates

        Defaults asserted are taken from 13.1.0

        :param trunk:
        :return:
        """
        assert trunk.stp == 'enabled'
        assert trunk.lacp == 'disabled'
        trunk.lacp = 'enabled'
        trunk.stp = 'disabled'
        trunk.update()
        assert trunk.stp == 'disabled'
        assert trunk.lacp == 'enabled'

    def test_refresh(self, trunk):
        """Test resource refreshing

        Defaults asserted are taken from 13.1.0

        :param trunk:
        :return:
        """
        assert trunk.stp == 'enabled'
        trunk.stp = 'disabled'

        # A refresh without an update should show no change
        trunk.refresh()
        assert trunk.stp == 'enabled'

    def test_guest_no_creation_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter) as ex:
            mgmt_root.tm.net.trunks.trunk.create()
        assert 'name' in str(ex.value)
