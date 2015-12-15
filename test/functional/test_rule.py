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

import os
import pytest
from requests.exceptions import HTTPError


def get_data(file_name):
    """Reads data file, returning a string.

    :param string name: Name of file containing data.
    :rtype string: data string.
    """

    data_dir = os.path.dirname(__file__)
    file = open(os.path.join(data_dir, file_name))
    return file.read().strip()


RULE_DATA = "rule.ldap.data"

rule1 = {
    'name': 'test_foo',
    'definition':  get_data(RULE_DATA)
}

rule2 = {
    'name': 'test_bar',
    'definition':  get_data(RULE_DATA)
}

# TBD: set to True once we figure out how to create a new partition
multi_partition = False

rule_default_folder = 'Common'
rule_other_folder = 'Uncommon' if multi_partition else rule_default_folder


def setup_standard_test(request, bigip):
    def teardown():
        bigip.ltm.rule.delete(rule1['name'])
        assert not bigip.ltm.rule.exists(rule1['name'])
        bigip.ltm.rule.delete(rule2['name'])
        assert not bigip.ltm.rule.exists(rule2['name'])
    request.addfinalizer(teardown)

    assert bigip.ltm.rule.create(rule1['name'], rule1['definition'])
    assert bigip.ltm.rule.exists(rule1['name'])


def setup_multi_rule_test(request, bigip):
    setup_standard_test(request, bigip)

    # create with all paramters
    assert bigip.ltm.rule.create(rule2['name'],
                                 rule2['definition'],
                                 rule_default_folder)
    assert bigip.ltm.rule.exists(rule2['name'])


def test_create_and_delete_one(request, bigip):
    assert bigip.ltm.rule.create(rule1['name'], rule1['definition'])
    assert bigip.ltm.rule.exists(rule1['name'])

    assert bigip.ltm.rule.delete(rule1['name'])
    assert not bigip.ltm.rule.exists(rule1['name'])


def test_create_and_delete_two(request, bigip):
    setup_multi_rule_test(request, bigip)

    assert bigip.ltm.rule.delete_like('test_')
    assert not bigip.ltm.rule.exists(rule1['name'])
    assert not bigip.ltm.rule.exists(rule2['name'])


def test_get_rule(request, bigip):
    setup_standard_test(request, bigip)

    rule_definition = bigip.ltm.rule.get_rule(rule1['name'])
    assert rule_definition == rule1['definition']


def test_create_duplicate_name(request, bigip):
    setup_standard_test(request, bigip)

    # create duplicate by name
    with pytest.raises(HTTPError):
        bigip.ltm.rule.create(rule1['name'], rule2['definition'])
    assert bigip.ltm.rule.exists(rule1['name'])
