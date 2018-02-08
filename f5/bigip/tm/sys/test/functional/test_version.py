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


def setup_version_test(request, mgmt_root):
    def teardown():
        v.selfLink = selflink
    request.addfinalizer(teardown)
    v = mgmt_root.tm.sys.version.load()
    selflink = v.selfLink
    return v, selflink


class TestVersion(object):
    def test_entry(self, request, mgmt_root):
        # Load
        ver1, orig_link = setup_version_test(request, mgmt_root)
        ver2 = mgmt_root.tm.sys.version.load()
        assert len(ver1.selfLink) == len(ver2.selfLink)
