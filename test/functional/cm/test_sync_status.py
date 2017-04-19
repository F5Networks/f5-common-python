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


class TestSyncStatus(object):
    def test_get_status(self, request, bigip):
        sync_status = bigip.cm.sync_status
        pp(sync_status.raw)
        assert sync_status._meta_data['uri'].endswith(
            "/mgmt/tm/cm/sync-status/")
        sync_status.refresh()
        des =\
            (sync_status.entries['https://localhost/mgmt/tm/cm/sync-status/0']
             ['nestedStats']
             ['entries']
             ['status']
             ['description'])
        assert des == u"Standalone"
