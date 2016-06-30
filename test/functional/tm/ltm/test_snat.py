# Copyright 2015-2106 F5 Networks Inc.
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

import pytest

from icontrol.session import iControlUnexpectedHTTPError
from requests.exceptions import HTTPError

from f5.bigip.tm.ltm.snat import RequireOneOf

TESTDESCRIPTION = 'TESTDESCRIPTION'

EXPECTED_ORIGINS_DELETION_MESSAGE = 'one of the following must be ',\
    'specified:\\\\nadd, delete, modify, replace-all-with","errorStack":[]}\''


def delete_snat(bigip, name, partition):
    try:
        s = bigip.ltm.snats.snat.load(name=name, partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    s.delete()


def setup_create_test(request, bigip, name, partition):
    def teardown():
        delete_snat(bigip, name, partition)
    request.addfinalizer(teardown)
    snat1 = bigip.ltm.snats.snat
    return snat1


def setup_basic_test(request, bigip, name, partition, orig='1.1.1.1'):
    def teardown():
        delete_snat(bigip, name, partition)

    snat_s1 = bigip.ltm.snats
    snat1 = bigip.ltm.snats.snat.create(
        name=name, partition=partition, origins=orig, automap=True)
    request.addfinalizer(teardown)
    return snat1, snat_s1


class TestSNAT(object):
    def test_create_no_args(self, request, bigip):
        snat1 = setup_create_test(request, bigip, 'TESTNAME', 'Common')
        with pytest.raises(RequireOneOf):
            snat1.create()

    def test_create(self, request, bigip):
        snat = setup_create_test(request, bigip, 'snat1', 'Common')
        snat1 = snat.create(
            name='snat1', partition='Common', origins='1.1.1.1', automap=True)
        assert snat1.name == 'snat1'
        assert snat1.partition == 'Common'
        assert snat1.generation and isinstance(snat1.generation, int)
        assert snat1.kind == 'tm:ltm:snat:snatstate'
        assert snat1.selfLink.startswith(
            'https://localhost/mgmt/tm/ltm/snat/~Common~snat1')

    def test_update_and_refresh(self, request, bigip):
        snat1, sc1 = setup_basic_test(request, bigip, 'snat1', 'Common')
        snat1.description = TESTDESCRIPTION
        snat1.update()
        assert snat1.description == TESTDESCRIPTION
        snat1.description = "NEWDESCRIPTION"
        snat1.refresh()
        assert snat1.description == TESTDESCRIPTION
        snat1.description = "NEWDESCRIPTION"
        snat1.update()
        assert snat1.description == "NEWDESCRIPTION"

    def test_load_and_delete(self, request, bigip):
        snat1, sc1 = setup_basic_test(request, bigip, 'snat1', 'Common')
        snat1.delete()
        assert snat1.__dict__ == {'deleted': True}

    def test_add_one_origin(self, request, bigip):
        snat1, sc1 = setup_basic_test(request, bigip, 'snat1', 'Common')
        assert snat1.origins == [{u'name': u'1.1.1.1/32'}]
        origin2 = {u'name': u'2.2.2.2/32'}
        snat1.origins.append(origin2)
        snat1.update()
        assert snat1.origins == [{u'name': u'1.1.1.1/32'},
                                 {u'name': u'2.2.2.2/32'}]
        snat1.origins[0]['name'] = u'3.3.3.3/32'
        snat1.update()
        assert snat1.origins == [{u'name': u'2.2.2.2/32'},
                                 {u'name': u'3.3.3.3/32'}]
        snat1.origins = []
        with pytest.raises(iControlUnexpectedHTTPError) as UHEIO:
            snat1.update()
        assert UHEIO.value.message.endswith(EXPECTED_ORIGINS_DELETION_MESSAGE)
