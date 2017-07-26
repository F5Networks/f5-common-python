# Copyright 2017 F5 Networks Inc.
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

import json
import mock
import os
import pytest

from f5.bigip import ManagementRoot
from f5.bigip.tm.sys.software.hotfix import Hotfix
from f5.sdk_exception import UnsupportedOperation


fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures')
fixture_data = {}


def load_fixture(name):
    path = os.path.join(fixture_path, name)

    if path in fixture_data:
        return fixture_data[path]

    with open(path) as f:
        data = f.read()

    try:
        data = json.loads(data)
    except Exception:
        pass

    fixture_data[path] = data
    return data


@pytest.fixture
def FakeHotfix():
    fake_software = mock.MagicMock()
    return Hotfix(fake_software)


def test_create_raises(FakeHotfix):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeHotfix.create()
    assert EIO.value.message == "Hotfix does not support the create method."


def test_update_raises(FakeHotfix):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeHotfix.update()
    assert EIO.value.message == "Hotfix does not support the update method."


def test_modify_raises(FakeHotfix):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeHotfix.modify()
    assert EIO.value.message == "Hotfix does not support the modify method."


def test_load(responsivesessionfactory):
    responsivesessionfactory(200, **load_fixture('load_hotfix.json'))
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    res = mr.tm.sys.software.hotfix_s.hotfix.load(
        name='Hotfix-BIGIP-12.1.0.1.0.1447-HF1.iso'
    )
    assert res.kind == 'tm:sys:software:hotfix:hotfixstate'
    assert res.name == 'Hotfix-BIGIP-12.1.0.1.0.1447-HF1.iso'
    assert res.build == '1.0.1447'
    assert res.version == '12.1.0'


def test_delete(responsivesessionfactory):
    responsivesessionfactory(200, **load_fixture('load_hotfix.json'))
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    res = mr.tm.sys.software.hotfix_s.hotfix.load(
        name='Hotfix-BIGIP-12.1.0.1.0.1447-HF1.iso'
    )
    assert res.kind == 'tm:sys:software:hotfix:hotfixstate'
    assert res.name == 'Hotfix-BIGIP-12.1.0.1.0.1447-HF1.iso'
    assert res.build == '1.0.1447'
    assert res.version == '12.1.0'

    res.delete()
    assert res.deleted is True


def test_collection(responsivesessionfactory):
    responsivesessionfactory(200, **load_fixture('load_hotfixes.json'))
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    resc = mr.tm.sys.software.hotfix_s.get_collection()

    assert isinstance(resc, list)
    assert len(resc)
    assert isinstance(resc[0], Hotfix)
