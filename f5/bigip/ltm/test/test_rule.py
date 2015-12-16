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

import json
import os
import pytest
import responses

HOST_NAME = "host-abc"
RULE_NAME = "foo"
RULE_FOLDER = "Common"
RULE_BASE_URI = "https://" + HOST_NAME + "/mgmt/tm/ltm/rule/"
RULE_DATA = "rule.data"
RULE_JSON = "rule.json"


def get_data(file_name):
    """Reads data file, returning a string.

    :param string name: Name of file containing data.
    :rtype string: data string.
    """

    data_dir = os.path.dirname(__file__)
    file = open(os.path.join(data_dir, file_name))
    return file.read().strip()


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
def rule():
    """Return a Rule object"""
    big_ip = BigIP(HOST_NAME, "admin", "admin")
    return big_ip.ltm.rule


def test_create(rule):
    """Test creating a new rule"""

    # write a more complete test
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST,
                 RULE_BASE_URI,
                 status=200)

        assert rule.create(name=RULE_NAME, rule_definition=get_data(RULE_DATA))


def test_update(rule):
    """Test updating a rule"""

    # write a more complete test
    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT,
                 RULE_BASE_URI + '~' + RULE_FOLDER + '~' + RULE_NAME,
                 status=200)

        assert rule.update(name=RULE_NAME, rule_definition=get_data(RULE_DATA))


def test_get_rule(rule):
    """Test getting a rule"""

    # write a more complete test
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET,
                 RULE_BASE_URI + '~' + RULE_FOLDER + '~' + RULE_NAME,
                 status=200,
                 json=json_data(RULE_JSON))

        rule_definition = rule.get_rule(name=RULE_NAME)
        assert rule_definition == get_data(RULE_DATA)


def test_get_rules(rule):
    # TBD: write a test
    pass


def test_delete(rule):
    """Test deleting a rule"""

    # write a more complete test
    with responses.RequestsMock() as rsps:

        rsps.add(responses.DELETE,
                 RULE_BASE_URI + '~' + RULE_FOLDER + '~' + RULE_NAME,
                 status=200)

        assert rule.delete(name=RULE_NAME)


def test_delete_all(rule):
    # TBD: write a test
    pass


def test_delete_like(rule):
    # TBD: write a test
    pass
