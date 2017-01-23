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


import pytest


@pytest.fixture(scope='function')
def easy_setup(mgmt_root):
    easy_setup = mgmt_root.shared.system.easy_setup.load()
    yield easy_setup
    easy_setup.update(
        ntpServerAddresses=[
            "pool.ntp.org"
        ],
        dnsServerAddresses=[
            "10.0.2.3"
        ],
        dnsSearchDomains=[
            "olympus.f5net.com"
        ]
    )


class TestEasySetup(object):
    def test_load(self, easy_setup):
        assert easy_setup.ntpServerAddresses == ['pool.ntp.org']
        assert easy_setup.dnsServerAddresses == ['10.0.2.3']
        assert easy_setup.dnsSearchDomains == ['olympus.f5net.com']

    def test_update(self, easy_setup):
        easy_setup.update(
            ntpServerAddresses=['pool1.ntp.org']
        )
        assert easy_setup.ntpServerAddresses == ['pool1.ntp.org']
        easy_setup.refresh()
        assert easy_setup.ntpServerAddresses == ['pool1.ntp.org']
