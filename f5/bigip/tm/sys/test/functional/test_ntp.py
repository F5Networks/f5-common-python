# Copyright 2016 F5 Networks Inc.
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

import pytest

from distutils.version import LooseVersion
from requests.exceptions import HTTPError


def setup_ntp_test(request, mgmt_root):
    def teardown():
        n.servers = []
        n.update()
    request.addfinalizer(teardown)
    n = mgmt_root.tm.sys.ntp.load()
    return n


def delete_resource(mgmt_root, name, partition):
    try:
        s = mgmt_root.tm.sys.ntp.restricts.restrict.load(
            name=name, partition=partition
        )
    except HTTPError as err:
        if err.response.status_code != 404:
            raise
        return
    s.delete()


def setup_restrict_test(request, mgmt_root, name, partition, **kwargs):
    def teardown():
        delete_resource(mgmt_root, name, partition)
    request.addfinalizer(teardown)
    return mgmt_root.tm.sys.ntp.restricts


class TestGlobal_Setting(object):
    def test_RUL(self, request, mgmt_root):
        # Load
        ip = '192.168.1.1'
        ntp1 = setup_ntp_test(request, mgmt_root)
        ntp2 = mgmt_root.tm.sys.ntp.load()

        # Update
        ntp1.servers = [ip]
        ntp1.update()

        assert ip in ntp1.servers
        assert not hasattr(ntp2, 'servers')

        # Refresh
        ntp2.refresh()
        assert ip in ntp2.servers


class TestNtpRestrictions(object):
    def test_create_base(self, request, mgmt_root):
        ntp = setup_restrict_test(request, mgmt_root,
                                  name="r1", partition="Common")

        ntp1 = ntp.restrict.create(name='r1', partition='Common')

        if pytest.config.getoption('--release') < LooseVersion('11.6.1'):
            assert ntp1.name == 'r1'
            assert ntp1.partition == 'Common'
        elif pytest.config.getoption('--release') >= LooseVersion('12.1.0'):
            assert ntp1.name == 'r1'
            assert not hasattr(ntp1, 'partition')
        else:
            assert ntp1.name == '/Common/r1'
            # The 'partition' attribute was removed in 11.6.1?
            assert not hasattr(ntp1, 'partition')

        if pytest.config.getoption('--release') >= LooseVersion('12.1.0'):
            link = 'https://localhost/mgmt/tm/sys/ntp/restrict/r1'
        else:
            link = 'https://localhost/mgmt/tm/sys/ntp/restrict/~Common~r1'

        assert ntp1.defaultEntry == "disabled"
        assert ntp1.ignore == "disabled"
        assert ntp1.kod == "disabled"
        assert ntp1.limited == "disabled"
        assert ntp1.lowPriorityTrap == "disabled"
        assert ntp1.noModify == "disabled"
        assert ntp1.noPeer == "disabled"
        assert ntp1.noQuery == "disabled"
        assert ntp1.noServePackets == "disabled"
        assert ntp1.noTrap == "disabled"
        assert ntp1.noTrust == "disabled"
        assert ntp1.nonNtpPort == "disabled"
        assert ntp1.ntpPort == "disabled"
        assert ntp1.version == "disabled"
        assert ntp1.kind == 'tm:sys:ntp:restrict:restrictstate'
        assert ntp1.selfLink.startswith(link)

    def test_create_full(self, request, mgmt_root):
        ntp = setup_restrict_test(request, mgmt_root,
                                  name="r2", partition="Common")

        params = dict(
            address="192.168.1.0",
            defaultEntry="enabled",
            ignore="enabled",
            kod="enabled",
            limited="enabled",
            lowPriorityTrap="enabled",
            mask="255.255.255.0",
            noModify="enabled",
            noPeer="enabled",
            noQuery="enabled",
            noServePackets="enabled",
            noTrap="disabled",
            noTrust="enabled",
            nonNtpPort="enabled",
            ntpPort="enabled",
            version="enabled"
        )
        ntp1 = ntp.restrict.create(name='r2', partition='Common', **params)

        # In 11.6.1 and later they started prepending the partition name
        # to the name attribute here. So we handle this case for our tests.
        #
        # According to Narendra, they should always have behaved this way
        # so this must have been a bugfix
        if pytest.config.getoption('--release') < LooseVersion('11.6.1'):
            assert ntp1.name == 'r2'
            assert ntp1.partition == 'Common'
        elif pytest.config.getoption('--release') >= LooseVersion('12.1.0'):
            assert ntp1.name == 'r2'
            assert not hasattr(ntp1, 'partition')
        else:
            assert ntp1.name == '/Common/r2'
            assert not hasattr(ntp1, 'partition')
            # The 'partition' attribute was removed in 11.6.1?

        if pytest.config.getoption('--release') >= LooseVersion('12.1.0'):
            link = 'https://localhost/mgmt/tm/sys/ntp/restrict/r2'
        else:
            link = 'https://localhost/mgmt/tm/sys/ntp/restrict/~Common~r2'

        assert ntp1.address == "192.168.1.0"
        assert ntp1.defaultEntry == "enabled"
        assert ntp1.ignore == "enabled"
        assert ntp1.kod == "enabled"
        assert ntp1.limited == "enabled"
        assert ntp1.lowPriorityTrap == "enabled"
        assert ntp1.mask == "255.255.255.0"
        assert ntp1.noModify == "enabled"
        assert ntp1.noPeer == "enabled"
        assert ntp1.noQuery == "enabled"
        assert ntp1.noServePackets == "enabled"
        assert ntp1.noTrap == "disabled"
        assert ntp1.noTrust == "enabled"
        assert ntp1.nonNtpPort == "enabled"
        assert ntp1.ntpPort == "enabled"
        assert ntp1.version == "enabled"
        assert ntp1.kind == 'tm:sys:ntp:restrict:restrictstate'
        assert ntp1.selfLink.startswith(link)
