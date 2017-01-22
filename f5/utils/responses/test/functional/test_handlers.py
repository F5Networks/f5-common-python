# coding=utf-8
#
# Copyright 2015-2016 F5 Networks Inc.
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

from distutils.version import LooseVersion
from f5.utils.responses.handlers import Stats
from requests.exceptions import HTTPError
import pytest


def delete_virtual_server(mgmt_root, name):
    try:
        foo = mgmt_root.tm.ltm.virtuals.virtual.load(
            name=name)
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    foo.delete()


@pytest.fixture
def virtual_setup(request, mgmt_root):
    def teardown():
        delete_virtual_server(mgmt_root, 'vs1')

    vs_kwargs = {'name': 'vs1', 'partition': 'Common'}
    vs = mgmt_root.tm.ltm.virtuals.virtual
    v1 = vs.create(profiles=['/Common/http'], **vs_kwargs)
    request.addfinalizer(teardown)
    return v1


class TestVirtualStatsHandling(object):
    def test_load(self, request, mgmt_root):
        vs = virtual_setup(request, mgmt_root)
        statistics = vs.stats.load()
