# Copyright 2014-2017 F5 Networks Inc.
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
import pytest

from six import iteritems


@pytest.fixture(scope='function')
def general(mgmt_root):
    s = mgmt_root.tm.gtm.global_settings.general.load()
    yield s
    s.modify(autoDiscovery='yes')


@pytest.fixture(scope='function')
def lb(mgmt_root):
    s = mgmt_root.tm.gtm.global_settings.load_balancing.load()
    yield s
    s.modify(ignorePathTtl='no')


@pytest.fixture(scope='function')
def metric(mgmt_root):
    s = mgmt_root.tm.gtm.global_settings.metrics.load()
    yield s
    s.modify(defaultProbeLimit=12)


class TestMetrics(object):
    def test_refresh_update(self, mgmt_root, metric):
        r1 = metric
        r2 = mgmt_root.tm.gtm.global_settings.metrics.load()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.defaultProbeLimit == r2.defaultProbeLimit
        r1.defaultProbeLimit = 24
        r1.update()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.defaultProbeLimit != r2.defaultProbeLimit

        r2.refresh()
        assert r1.defaultProbeLimit == r2.defaultProbeLimit
        assert r2.defaultProbeLimit == 24

    def test_modify(self, metric):
        r1 = metric
        original_dict = copy.copy(r1.__dict__)
        itm = 'defaultProbeLimit'
        r1.modify(defaultProbeLimit=24)
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 24

    def test_load(self, mgmt_root, metric):
        r1 = metric
        uri = 'https://localhost/mgmt/tm/gtm/global-settings/metrics'
        assert r1.kind == \
            'tm:gtm:global-settings:metrics:metricsstate'
        assert r1.selfLink.startswith(uri)
        assert r1.defaultProbeLimit == 12
        r1.modify(defaultProbeLimit=24)
        assert r1.defaultProbeLimit == 24

        r2 = mgmt_root.tm.gtm.global_settings.metrics.load()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.defaultProbeLimit == r2.defaultProbeLimit


class TestLoadBalancing(object):
    def test_refresh_update(self, mgmt_root, lb):
        r1 = lb
        r2 = mgmt_root.tm.gtm.global_settings.load_balancing.load()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.ignorePathTtl == r2.ignorePathTtl
        r1.ignorePathTtl = 'yes'
        r1.update()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.ignorePathTtl != r2.ignorePathTtl

        r2.refresh()
        assert r1.ignorePathTtl == r2.ignorePathTtl
        assert r2.ignorePathTtl == 'yes'

    def test_modify(self, lb):
        r1 = lb
        original_dict = copy.copy(r1.__dict__)
        itm = 'autoDiscovery'
        r1.modify(ignorePathTtl='yes')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 'yes'

    def test_load(self, mgmt_root, lb):
        r1 = lb
        uri = 'https://localhost/mgmt/tm/gtm/global-settings/load-balancing'
        assert r1.kind == \
            'tm:gtm:global-settings:load-balancing:load-balancingstate'
        assert r1.selfLink.startswith(uri)
        assert r1.ignorePathTtl == 'no'
        r1.modify(ignorePathTtl='yes')
        assert r1.ignorePathTtl == 'yes'

        r2 = mgmt_root.tm.gtm.global_settings.load_balancing.load()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.ignorePathTtl == r2.ignorePathTtl


class TestGeneral(object):
    def test_refresh_update(self, mgmt_root, general):
        r1 = general
        r2 = mgmt_root.tm.gtm.global_settings.general.load()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.autoDiscovery == r2.autoDiscovery
        r1.autoDiscovery = 'no'
        r1.update()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.autoDiscovery != r2.autoDiscovery

        r2.refresh()
        assert r1.autoDiscovery == r2.autoDiscovery
        assert r2.autoDiscovery == 'no'

    def test_modify(self, general):
        r1 = general
        original_dict = copy.copy(r1.__dict__)
        itm = 'autoDiscovery'
        r1.modify(autoDiscovery='no')
        for k, v in iteritems(original_dict):
            if k != itm:
                original_dict[k] = r1.__dict__[k]
            elif k == itm:
                assert r1.__dict__[k] == 'no'

    def test_load(self, mgmt_root, general):
        r1 = general
        uri = 'https://localhost/mgmt/tm/gtm/global-settings/general'
        assert r1.kind == 'tm:gtm:global-settings:general:generalstate'
        assert r1.selfLink.startswith(uri)
        assert r1.autoDiscovery == 'yes'
        r1.modify(autoDiscovery='no')
        assert r1.autoDiscovery == 'no'

        r2 = mgmt_root.tm.gtm.global_settings.general.load()
        assert r1.kind == r2.kind
        assert r1.selfLink == r2.selfLink
        assert r1.autoDiscovery == r2.autoDiscovery
