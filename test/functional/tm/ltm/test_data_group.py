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

import copy
from f5.bigip.resource import MissingRequiredCreationParameter
import pytest

from requests.exceptions import HTTPError
from six import iteritems


def delete_external_datagroup(mgmt_root, name, partition, DATAGROUP):
    try:
        dg = mgmt_root.tm.ltm.data_group.externals.external.load(
            name=name, partition=partition)

    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    dg.delete()

    try:
        DATAGROUP.delete()
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return


def delete_internal_datagroup(mgmt_root, name, partition):
    try:
        dg = mgmt_root.tm.ltm.data_group.internals.internal.load(
            name=name, partition=partition)

    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    dg.delete()


def setup_create_test_edg(request, mgmt_root, name, partition, DATAGROUP):
    def teardown():
        delete_external_datagroup(mgmt_root, name, partition, DATAGROUP)

    request.addfinalizer(teardown)


def setup_basic_test_edg(request, mgmt_root, name, partition, DATAGROUP,
                         **kwargs):
    def teardown():
        delete_external_datagroup(mgmt_root, name, partition, DATAGROUP)

    dg1 = mgmt_root.tm.ltm.data_group.externals.external.create(
        name='dg1', partition='Common',
        externalFileName=DATAGROUP.name, **kwargs)

    request.addfinalizer(teardown)
    return dg1


def setup_create_test_idg(request, mgmt_root, name, partition):
    def teardown():
        delete_internal_datagroup(mgmt_root, name, partition)

    request.addfinalizer(teardown)


def setup_basic_test_idg(request, mgmt_root, name, partition, **kwargs):
    def teardown():
        delete_internal_datagroup(mgmt_root, name, partition)

    dg1 = mgmt_root.tm.ltm.data_group.internals.internal.create(
        name='dg1', partition='Common', type='string',
        records=[{'name': 'a', 'data': '1'}], **kwargs)

    request.addfinalizer(teardown)
    return dg1


class TestExternalDatagroup(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.data_group.externals.external.create()

    def test_create_no_filename(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.data_group.externals.external.create(
                name='dg1', type='string', partition='Common')

    def test_create_no_type(self, mgmt_root, DATAGROUP):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.data_group.externals.external.create(
                name='dg1', partition='Common', fileName=DATAGROUP.name)

    def test_create(self, request, mgmt_root, DATAGROUP):
        setup_create_test_edg(request, mgmt_root, 'dg1', 'Common', DATAGROUP)
        dg1 = mgmt_root.tm.ltm.data_group.externals.external.create(
            name='dg1', partition='Common',
            externalFileName=DATAGROUP.name)

        assert dg1.name == 'dg1'
        assert dg1.partition == 'Common'
        assert dg1.type == 'string'

    def test_delete(self, request, mgmt_root, DATAGROUP):
        dg1 = setup_basic_test_edg(request, mgmt_root, 'dg1', 'Common',
                                   DATAGROUP)
        dg1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.ltm.data_group.externals.external.load(
                name='dg1', partition='Common')
            assert err.response.status_code == 404

        try:
            DATAGROUP.delete()
        except HTTPError as err:
            if err.response.status_code != 404:
                raise
            return

    def test_modify(self, request, mgmt_root, DATAGROUP):
        dg1 = setup_basic_test_edg(request, mgmt_root, 'dg1', 'Common',
                                   DATAGROUP, description='first_fake')
        assert dg1.description == 'first_fake'
        original_dict = copy.copy(dg1.__dict__)
        desc = 'description'
        dg1.modify(description='CustomFake')
        for k, v in iteritems(original_dict):
            if k != desc:
                original_dict[k] = dg1.__dict__[k]
            elif k == desc:
                assert dg1.__dict__[k] == 'CustomFake'

    def test_update(self, request, mgmt_root, DATAGROUP):
        dg1 = setup_basic_test_edg(request, mgmt_root, 'dg1', 'Common',
                                   DATAGROUP, description='first_fake')
        assert dg1.description == 'first_fake'
        dg1.description = 'CustomFake'
        dg1.update()
        assert dg1.description == 'CustomFake'


class TestInternalDatagroup(object):
    def test_create_no_args(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.data_group.internals.internal.create()

    def test_create_no_records(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.data_group.internals.internal.create(
                name='dg1', type='string', partition='Common')

    def test_create_no_type(self, mgmt_root):
        with pytest.raises(MissingRequiredCreationParameter):
            mgmt_root.tm.ltm.data_group.internals.internal.create(
                name='dg1', partition='Common',
                records=[{'name': 'a', 'data': '1'}])

    def test_create(self, request, mgmt_root):
        setup_create_test_idg(request, mgmt_root, 'dg1', 'Common')
        dg1 = mgmt_root.tm.ltm.data_group.internals.internal.create(
            name='dg1', partition='Common', type='string',
            records=[{'name': 'a', 'data': '1'}])

        assert dg1.name == 'dg1'
        assert dg1.partition == 'Common'
        assert dg1.type == 'string'

    def test_delete(self, request, mgmt_root):
        dg1 = setup_basic_test_idg(request, mgmt_root, 'dg1', 'Common')
        dg1.delete()
        with pytest.raises(HTTPError) as err:
            mgmt_root.tm.ltm.data_group.internals.internal.load(
                name='dg1', partition='Common')
            assert err.response.status_code == 404

    def test_modify(self, request, mgmt_root):
        dg1 = setup_basic_test_idg(request, mgmt_root, 'dg1', 'Common',
                                   description='first_fake')
        assert dg1.description == 'first_fake'
        original_dict = copy.copy(dg1.__dict__)
        desc = 'description'
        dg1.modify(description='CustomFake')
        for k, v in iteritems(original_dict):
            if k != desc:
                original_dict[k] = dg1.__dict__[k]
            elif k == desc:
                assert dg1.__dict__[k] == 'CustomFake'

    def test_update(self, request, mgmt_root):
        dg1 = setup_basic_test_idg(request, mgmt_root, 'dg1', 'Common',
                                   description='first_fake')
        assert dg1.description == 'first_fake'
        dg1.description = 'CustomFake'
        dg1.update()
        assert dg1.description == 'CustomFake'
