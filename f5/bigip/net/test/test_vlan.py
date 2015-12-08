# Copyright 2015 F5 Networks Inc.
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

from f5.bigip import BigIP
from requests.exceptions import HTTPError

import json
import os
import pytest
import responses

HOST_NAME = "host-abc"
VLAN_NAME = "external"
VLAN_FOLDER = "Common"
VLAN_BASE_URI = "https://" + HOST_NAME + "/mgmt/tm/net/vlan/"
VLAN_ALL_JSON = "vlan.json"
VLAN_EXTERNAL_JSON = "vlan_ext.json"


def json_data(file_name):
    """Reads JSON file, returning a JSON object.

    The file must contain a valid JSON object, for example:
    {"key": "value"...} or
    {"key": {"key": "value"}...}

    :param string name: Name of file containing JSON object.
    :rtype string: JSON object as a string.
    """

    data_dir = os.path.dirname(__file__)
    file = open(os.path.join(data_dir, file_name))
    return json.load(file)


@pytest.fixture
def vlan():
    """Return a Vlan object"""
    big_ip = BigIP(HOST_NAME, "admin", "admin")
    return big_ip.net.vlan


def test_get_description(vlan):
    """Test getting a valid description"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER + "~" + VLAN_NAME,
                 status=200,
                 json=json_data(VLAN_EXTERNAL_JSON))

        description = vlan.get_description(VLAN_NAME)
        assert description == "External VLAN"


def test_get_description_http_error(vlan):
    """Test that an HTTPException is raised"""

    with responses.RequestsMock() as rsps:
        exception = HTTPError('Some kind of HTTP error.')
        rsps.add(responses.GET,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER + "~" + VLAN_NAME,
                 status=200,
                 body=exception)

        # should raise an HTTP exception
        with pytest.raises(HTTPError):
            vlan.get_description(VLAN_NAME)


def test_get_vlan_name_by_description(vlan):
    """Test finding a VLAN given a description"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER,
                 status=200,
                 json=json_data(VLAN_ALL_JSON))

        v = vlan.get_vlan_name_by_description(description="External VLAN")
        assert v["name"] == "external"


def test_get_vlan_name_by_bad_description(vlan):
    """Test cannot find VLAN given the wrong description"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER,
                 status=200,
                 json=json_data(VLAN_ALL_JSON))

        v = vlan.get_vlan_name_by_description(description="asdfjkl")
        assert not v


def test_create(vlan):
    """Test creating a new VLAN"""

    # write a more complete test
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST,
                 VLAN_BASE_URI,
                 status=200)

        assert vlan.create(name="internal")


def test_get_vlans(vlan):
    """Test getting a list of all vlans"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 VLAN_BASE_URI + "~Common",
                 status=200,
                 json=json_data(VLAN_ALL_JSON))

        vlans = vlan.get_vlans()
        assert vlans.__len__() > 0


def test_get_id(vlan):
    """Test getting a valid ID"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER + "~" + VLAN_NAME,
                 status=200,
                 json=json_data(VLAN_EXTERNAL_JSON))

        id = vlan.get_id(VLAN_NAME)
        assert id == 4093
    pass


def test_set_id(vlan):
    """Test setting a vlan ID"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER + "~" + VLAN_NAME,
                 status=200)

        assert vlan.set_id(VLAN_NAME, vlanid=4095)


def test_get_interface(vlan):
    # TODO(write test)
    pass


def test_set_interface(vlan):
    """Test setting an interface"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER + "~" + VLAN_NAME,
                 status=200)

        assert vlan.set_interface(VLAN_NAME, interface="1.1")
    pass


def test_set_description(vlan):
    """Test setting a description"""

    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT,
                 VLAN_BASE_URI + "~" + VLAN_FOLDER + "~" + VLAN_NAME,
                 status=200)

        assert vlan.set_description(VLAN_NAME, description="My test VLAN")
    pass
