# Copyright 2017 F5 Networks Inc.
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


def setup_source_test(request, mgmt_root):
    def teardown():
        # remove tacacs source
        sa.type = auth_source
        sa.update()
        # remove tacacs object
        auth_tacobj.delete()
    request.addfinalizer(teardown)

    sa = mgmt_root.tm.auth.source.load()
    auth_source = sa.type

    auth_tacobj = mgmt_root.tm.auth.tacacs_s.tacacs.create(name='system-auth',
                                                           protocol='ip',
                                                           service='ppp',
                                                           servers=[
                                                               '172.16.44.20'],
                                                           secret='letmein00')
    return sa


class TestSource(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        source1 = setup_source_test(request, mgmt_root)
        source2 = mgmt_root.tm.auth.source.load()
        assert len(source1.type) == len(source2.type)

        # Update
        source1.type = 'tacacs'
        source1.update()
        assert 'tacacs' in source1.type
        assert 'tacacs' not in source2.type

        # Refresh
        source2.refresh()
        assert 'tacacs' in source2.type
