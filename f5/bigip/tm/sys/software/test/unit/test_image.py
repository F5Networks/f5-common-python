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
from f5.bigip.tm.sys.software.image import Image
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
def FakeImage():
    fake_software = mock.MagicMock()
    return Image(fake_software)


def test_create_raises(FakeImage):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeImage.create()
    assert str(EIO.value) == "Image does not support the create method."


def test_update_raises(FakeImage):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeImage.update()
    assert str(EIO.value) == "Image does not support the update method."


def test_modify_raises(FakeImage):
    with pytest.raises(UnsupportedOperation) as EIO:
        FakeImage.modify()
    assert str(EIO.value) == "Image does not support the modify method."


def test_load(responsivesessionfactory):
    responsivesessionfactory(200, **load_fixture('load_image.json'))
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    res = mr.tm.sys.software.images.image.load(
        name='BIGIP-12.1.0.0.0.1434.iso'
    )
    assert res.kind == 'tm:sys:software:image:imagestate'
    assert res.name == 'BIGIP-12.1.0.0.0.1434.iso'
    assert res.build == '0.0.1434'
    assert res.version == '12.1.0'


def test_delete(responsivesessionfactory):
    responsivesessionfactory(200, **load_fixture('load_image.json'))
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    res = mr.tm.sys.software.images.image.load(
        name='BIGIP-12.1.0.0.0.1434.iso'
    )
    assert res.kind == 'tm:sys:software:image:imagestate'
    assert res.name == 'BIGIP-12.1.0.0.0.1434.iso'
    assert res.build == '0.0.1434'
    assert res.version == '12.1.0'

    res.delete()
    assert res.deleted is True


def test_collection(responsivesessionfactory):
    responsivesessionfactory(200, **load_fixture('load_images.json'))
    mr = ManagementRoot('192.168.1.1', 'admin', 'admin')
    resc = mr.tm.sys.software.images.get_collection()

    assert isinstance(resc, list)
    assert len(resc)
    assert isinstance(resc[0], Image)
