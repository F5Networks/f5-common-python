# Copyright 2106 F5 Networks Inc.
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


def setup(request, bigip, name, partition, ipaddr):
    def teardown():
        if st.exists(name=name, partition=partition):
            st.delete()
    request.addfinalizer(teardown)

    stc = bigip.ltm.snat_translations
    st = stc.snat_translation.create(
        name=name, partition=partition, address=ipaddr)
    return stc, st


class TestSnatTranslations(object):
    def test_get_collection(self, request, bigip):
        stc, st = setup(
            request, bigip, 'test-snatxlate', 'Common', '192.168.50.51')
        sts = stc.get_collection()
        assert len(sts) >= 1
        assert [s for s in sts if s.name == 'test-snatxlate']


class TestSnatTranslation(object):
    def test_CURDLE(self, request, bigip):
        # Assume create and delete are tested by setup/teardown
        stc, st1 = setup(
            request, bigip, 'test-snatxlate', 'Common', '192.168.101.1')

        # Exists
        assert stc.snat_translation.exists(
            name='test-snatxlate', partition='Common')

        # Load
        st2 = stc.snat_translation.load(
            name='test-snatxlate', partition='Common')
        assert st1.generation == st2.generation
        assert st1.name == st2.name

        #  Update
        st1.disabled = True
        st1.update()
        assert st1.disabled is True
        assert st1.generation != st2.generation

        # Refresh
        st2.refresh()
        assert st2.disabled is True
        assert st1.generation == st2.generation
