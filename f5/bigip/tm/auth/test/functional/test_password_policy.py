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
#

from pprint import pprint as pp

import copy


class TestPasswordPolicy(object):
    def test_load(self, bigip):
        password_policy = bigip.auth.password_policy.load()
        pp(password_policy._meta_data['uri'])
        pp(password_policy.raw)
        assert password_policy.maxLoginFailures == 0
        password_policy.refresh()
        assert password_policy.maxLoginFailures == 0

    def test_update(self, bigip):
        password_policy = bigip.auth.password_policy.load()
        password_policy.update(maxLoginFailures=10)
        assert password_policy.maxLoginFailures == 10
        password_policy.update(maxLoginFailures=0)
        assert password_policy.maxLoginFailures == 0

    def test_modify(self, mgmt_root):
        password_policy = mgmt_root.tm.auth.password_policy.load()
        original_dict = copy.copy(password_policy.__dict__)
        max_fails = 'maxLoginFailures'
        password_policy.modify(maxLoginFailures=25)
        for k, v in original_dict.items():
            if k != max_fails:
                original_dict[k] = password_policy.__dict__[k]
            elif k == max_fails:
                password_policy.__dict__[k] == 'Cool mod test'
        password_policy.modify(maxLoginFailures=0)
        assert password_policy.maxLoginFailures == 0
