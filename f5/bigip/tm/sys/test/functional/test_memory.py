# Copyright 2018 F5 Networks Inc.
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

from f5.bigip.tm.sys.memory import Memory


class TestMemory(object):
    def test_load_refresh(self, mgmt_root):
        h1 = mgmt_root.tm.sys.memory.load()
        assert isinstance(h1, Memory)
        assert hasattr(h1, 'entries')
        assert h1.kind == 'tm:sys:memory:memorystats'
        assert 'https://localhost/mgmt/tm/sys/memory/memory-host' in h1.entries.keys()

        h2 = mgmt_root.tm.sys.memory.load()

        assert isinstance(h2, Memory)
        assert hasattr(h2, 'entries')
        assert h2.kind == 'tm:sys:memory:memorystats'
        assert 'https://localhost/mgmt/tm/sys/memory/memory-host' in h2.entries.keys()

        h1.refresh()

        assert h1.kind == h2.kind
        assert h1.entries.keys() == h2.entries.keys()
