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

import copy
from pprint import pprint as pp
from six import iteritems


def setup_sig_test(request, mgmt_root):
    def teardown():
        d.modify(updateInterval=interval)
    request.addfinalizer(teardown)
    d = mgmt_root.tm.asm.signature_update.load()
    interval = d.updateInterval
    return d, interval


class TestSignatureUpdate(object):
    def test_RL(self, request, mgmt_root):
        # Load
        inter = 'monthly'
        sig1, interval = setup_sig_test(request, mgmt_root)
        sig2 = mgmt_root.tm.asm.signature_update.load()
        assert sig1.updateInterval == sig2.updateInterval
        pp(sig1.raw)
        pp(sig2.raw)

        # Refresh
        sig1.modify(updateInterval=inter)
        sig1.refresh()
        assert sig1.updateInterval != sig2.updateInterval
        assert sig2.updateInterval == interval
        sig2.refresh()
        assert sig1.updateInterval == sig2.updateInterval

    def test_modify(self, request, mgmt_root):
        sig1, interval = setup_sig_test(request, mgmt_root)
        original_dict = copy.copy(sig1.__dict__)
        att = 'updateInterval'
        sig1.modify(updateInterval='monthly')
        for k, v in iteritems(original_dict):
            if k != att:
                original_dict[k] = sig1.__dict__[k]
            elif k == att:
                assert sig1.__dict__[k] == 'monthly'
