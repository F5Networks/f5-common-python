# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import pytest


@pytest.fixture(scope='function')
def setup_sig_test(mgmt_root):
    d = mgmt_root.tm.asm.signature_update.load()
    interval = d.updateInterval
    yield d
    d.modify(updateInterval=interval)


class TestSignatureUpdate(object):
    def test_RL(self, mgmt_root, setup_sig_test):
        # Load
        inter = 'monthly'
        sig1 = setup_sig_test
        sig2 = mgmt_root.tm.asm.signature_update.load()
        assert sig1.updateInterval == sig2.updateInterval

        # Refresh
        sig1.modify(updateInterval=inter)
        sig1.refresh()
        assert sig1.updateInterval != sig2.updateInterval
        sig2.refresh()
        assert sig1.updateInterval == sig2.updateInterval
