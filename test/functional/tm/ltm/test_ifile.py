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

from f5.bigip.resource import MissingRequiredCreationParameter
import pytest
from requests.exceptions import HTTPError


def delete_ifile(mgmt_root, name, partition, IFILE):
    try:
        ifile = mgmt_root.tm.ltm.ifiles.ifile.load(name=name,
                                                   partition=partition)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    ifile.delete()

    # not testing this function here; but need to clean it up
    try:
        IFILE.delete()
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return


def setup_create_test(request, mgmt_root, name, partition, IFILE):
    def teardown():
        delete_ifile(mgmt_root, name, partition, IFILE)

    request.addfinalizer(teardown)


def setup_basic_test(request, mgmt_root, name, partition, IFILE):
    def teardown():
        delete_ifile(mgmt_root, name, partition, IFILE)

    ifile1 = mgmt_root.tm.ltm.ifiles.ifile.create(
        name='ifile1', partition='Common', fileName=IFILE.name)

    request.addfinalizer(teardown)
    return ifile1


def test_create_no_args(mgmt_root):
    with pytest.raises(MissingRequiredCreationParameter):
        mgmt_root.tm.ltm.ifiles.ifile.create()


def test_create_no_filename(mgmt_root):
    with pytest.raises(MissingRequiredCreationParameter):
        mgmt_root.tm.ltm.ifiles.ifile.create(name='ifile1', partition='Common')


def test_create(request, mgmt_root, IFILE):
    setup_create_test(request, mgmt_root, 'ifile1', 'Common', IFILE)
    ifile1 = mgmt_root.tm.ltm.ifiles.ifile.create(
        name='ifile1', partition='Common', fileName=IFILE.name)

    assert ifile1.name == 'ifile1'
    assert ifile1.partition == 'Common'


def test_delete(request, mgmt_root, IFILE):
    ifile1 = setup_basic_test(request, mgmt_root, 'ifile1', 'Common', IFILE)
    ifile1.delete()
    with pytest.raises(HTTPError) as err:
        mgmt_root.tm.ltm.ifiles.ifile.load(
            name='ifile1', partition='Common')
        assert err.response.status_code == 404

    # not testing this function here; but need to clean it up
    try:
        IFILE.delete()
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
