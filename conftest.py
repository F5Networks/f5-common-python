# Copyright 2015-2016 F5 Networks Inc.
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
from f5.bigip import ManagementRoot
from f5.utils.testutils.registrytools import register_device
from icontrol.session import iControlRESTSession
import logging
import mock
import os
import pytest
import requests
from tempfile import NamedTemporaryFile


logger = logging.getLogger()
logger.setLevel(logging.WARNING)

requests.packages.urllib3.disable_warnings()


def pytest_addoption(parser):
    parser.addoption("--bigip", action="store",
                     help="BIG-IP hostname or IP address")
    parser.addoption("--username", action="store", help="BIG-IP REST username",
                     default="admin")
    parser.addoption("--password", action="store", help="BIG-IP REST password",
                     default="admin")
    parser.addoption("--port", action="store", help="BIG-IP port",
                     default=443)
    parser.addoption("--peer", action="store",
                     help="Peer BIG-IP hostname or IP address", default='none')
    parser.addoption("--release", action="store",
                     help="TMOS version, in dotted format, eg. 12.0.0",
                     default='11.6.0')


@pytest.fixture
def fakeicontrolsession(monkeypatch):
    class Response(object):

        def json(self):
            return {'selfLink': 'https://localhost/mgmt/tm/sys?ver=11.6.0'}

    fakesessionclass = mock.create_autospec(iControlRESTSession, spec_set=True)
    fakesessioninstance = mock.create_autospec(iControlRESTSession('A', 'B'),
                                               spec_set=True)
    fakesessioninstance.get =\
        mock.MagicMock(return_value=Response())
    fakesessionclass.return_value = fakesessioninstance
    monkeypatch.setattr('f5.bigip.iControlRESTSession', fakesessionclass)


@pytest.fixture
def fakeicontrolsessionfactory(monkeypatch):
    class Response(object):
        def __init__(self, **json_keys):
            if 'selfLink' not in json_keys:
                json_keys['selfLink'] =\
                    'https://localhost/mgmt/tm/sys?ver=11.6.0'
            self.params = json_keys

        def json(self):
            return self.params

    def _session_factory(**json_keys):
        fakesessionclass = mock.create_autospec(iControlRESTSession,
                                                spec_set=True)
        fakesessioninstance =\
            mock.create_autospec(iControlRESTSession('A', 'B'), spec_set=True)
        fakesessioninstance.get =\
            mock.MagicMock(return_value=Response(**json_keys))
        fakesessionclass.return_value = fakesessioninstance
        monkeypatch.setattr('f5.bigip.iControlRESTSession', fakesessionclass)

    return _session_factory


@pytest.fixture
def fakeicontrolsession_v12(monkeypatch):
    class Response(object):
        def json(self):
            return {'selfLink': 'https://localhost/mgmt/tm/sys?ver=12.1.0'}
    fakesessionclass = mock.create_autospec(iControlRESTSession, spec_set=True)
    fakesessioninstance =\
        mock.create_autospec(iControlRESTSession('A', 'B'), spec_set=True)
    fakesessioninstance.get = mock.MagicMock(return_value=Response())
    fakesessionclass.return_value = fakesessioninstance
    monkeypatch.setattr('f5.bigip.iControlRESTSession', fakesessionclass)


@pytest.fixture(scope='session')
def opt_bigip(request):
    return request.config.getoption("--bigip")


@pytest.fixture(scope='session')
def opt_username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope='session')
def opt_password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope='session')
def opt_port(request):
    return request.config.getoption("--port")


@pytest.fixture(scope='session')
def bigip(opt_bigip, opt_username, opt_password, opt_port, scope="module"):
    '''bigip fixture'''
    b = BigIP(opt_bigip, opt_username, opt_password, port=opt_port)
    return b


@pytest.fixture(scope='module')
def mgmt_root(opt_bigip, opt_username, opt_password, opt_port, scope="module"):
    '''bigip fixture'''
    m = ManagementRoot(opt_bigip, opt_username, opt_password, port=opt_port)
    return m


@pytest.fixture(scope='session')
def opt_release(request):
    return request.config.getoption("--release")


@pytest.fixture
def opt_peer(request):
    return request.config.getoption("--peer")


@pytest.fixture
def peer(opt_peer, opt_username, opt_password, scope="module"):
    '''peer bigip fixture'''
    p = BigIP(opt_peer, opt_username, opt_password)
    return p


@pytest.fixture
def NAT(bigip):
    n = bigip.ltm.nats.nat
    return n


@pytest.fixture
def USER(bigip):
    n = bigip.auth.users.user
    return n


def _delete_pools_members(bigip, pool_records):
    for pr in pool_records:
        if bigip.ltm.pools.pool.exists(partition=pr.partition, name=pr.name):
            pool_inst = bigip.ltm.pools.pool.load(partition=pr.partition,
                                                  name=pr.name)
            members_list = pool_inst.members_s.get_collection()
            pool_inst.delete()
            for mem_inst in members_list:
                mem_inst.delete()


@pytest.fixture
def pool_factory():
    def _setup_boilerplate(bigip, request, pool_records):
        _delete_pools_members(bigip, pool_records)
        pool_registry = {}
        members_registry = {}
        for pr in pool_records:
            pool_registry[pr.name] =\
                bigip.ltm.pools.pool.create(partition=pr.partition,
                                            name=pr.name)
            if pr.memberconfigs != (tuple(),):
                members_collection = pool_registry[pr.name].members_s
                for memconf in pr.memberconfigs:
                    members_registry[memconf.memname] =\
                        members_collection.members\
                        .create(partition=memconf.mempartition,
                                name=memconf.memname)

        def deleter():
            for member_instance in members_registry.values():
                member_instance.delete()
            for pool_instance in pool_registry.values():
                pool_instance.delete()
        request.addfinalizer(deleter)
        return pool_registry, members_registry
    return _setup_boilerplate


@pytest.fixture(scope='module')
def setup_device_snapshot(request, mgmt_root):
    '''Snapshot the device to manage objects created by tests.

    Snapshot the device before a test runs and after, then remove objects
    that persist after suite runs.
    '''

    before_snapshot = register_device(mgmt_root)

    def teardown():
        after_snapshot = register_device(mgmt_root)
        diff = set(after_snapshot) - set(before_snapshot)
        for item in diff:
            after_snapshot[item].delete()
    request.addfinalizer(teardown)
    return before_snapshot


@pytest.fixture
def IFILE(mgmt_root):
    ntf = NamedTemporaryFile()
    ntf_basename = os.path.basename(ntf.name)
    ntf.write('this is a test file')
    ntf.seek(0)
    mgmt_root.shared.file_transfer.uploads.upload_file(ntf.name)
    tpath_name = 'file:/var/config/rest/downloads/{0}'.format(ntf_basename)
    i = mgmt_root.tm.sys.file.ifiles.ifile.create(name=ntf_basename,
                                                  sourcePath=tpath_name)
    return i
