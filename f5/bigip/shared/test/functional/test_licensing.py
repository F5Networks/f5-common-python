# Copyright 2016 F5 Networks Inc.
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

from pprint import pprint as pp
import pytest

from f5.bigip.mixins import UnsupportedMethod


class TestActivation(object):
    def test_load(self, request, bigip):
        a = bigip.shared.licensing.activation.load()
        assert hasattr(a, 'generation')

    def test_update(self, request, bigip):
        with pytest.raises(UnsupportedMethod):
            bigip.shared.licensing.activation.update()


class TestRegistration(object):
    def test_load(self, request, bigip):
        reg = bigip.shared.licensing.registration.load()
        assert hasattr(reg, 'generation')

    def test_update(self, request, bigip):
        pp(bigip.shared.raw)
        with pytest.raises(UnsupportedMethod):
            bigip.shared.licensing.registration.update()
