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


class TestHttpd(object):
    def test_load(self, bigip):
        httpd = bigip.sys.httpd.load()
        assert httpd.maxClients == 10
        httpd.refresh()
        assert httpd.maxClients == 10

    def test_update(self, bigip):
        httpd = bigip.sys.httpd.load()
        httpd.update(maxClients=10)
        assert httpd.maxClients == 10
        httpd.update(maxClients=20)
        assert httpd.maxClients == 20
